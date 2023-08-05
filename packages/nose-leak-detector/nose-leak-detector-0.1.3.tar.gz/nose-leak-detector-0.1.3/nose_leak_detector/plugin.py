""" Nose Plugin for finding leaked memory """

__author__ = "Andrew S. Brown (asbrown@nextdoor.com)"

from builtins import *
import collections
import functools
import gc
import operator
import re

try:
    from unittest import mock
    from unittest.mock import Base
except ImportError:
    import mock
    try:
        from mock.mock import Base
    except ImportError:
        from mock import Base

import resource
import sys
import traceback
import weakref

from nose.plugins import Plugin
from pympler import muppy
from pympler import summary
import termcolor

ReportDetail = collections.namedtuple('ReportDetail', ['title', 'color'])

LEVEL_DIR = 1
LEVEL_MODULE = 2
LEVEL_CLASS = 3
LEVEL_TEST = 4


class LeakDetected(Exception):
    pass


class LeakDetectorTestCase(object):
    def __init__(self, test, detector):
        self.test = test
        self.detector = detector

    def __call__(self, result):
        return self.detector.run_test(self.test, result)


class LeakDetectorPlugin(Plugin):
    name = 'leak-detector'
    detect_leaked_mocks = True
    fail_fast = True

    REPORT_DETAILS = {
        LEVEL_DIR: ReportDetail(title='Directory', color='magenta'),
        LEVEL_MODULE: ReportDetail(title='Module', color='green'),
        LEVEL_CLASS: ReportDetail(title='Class', color='blue'),
        LEVEL_TEST: ReportDetail(title='Test', color='red'),
    }
    CLASS_NAME = 'LeakDetector'

    def __init__(self):
        super(LeakDetectorPlugin, self).__init__()
        self.reporting_level = 0
        self.check_for_leaks_before_next_test = True
        self.report_delta = False
        self.add_traceback_to_mocks = False
        self.ignore_patterns = []

        self.patch_mock = False
        self.failed_test_with_leak = False
        self.last_test_name = None
        self.last_test_type = None
        self.last_test_class_name = None
        self.level_name = {}
        self.previous_summaries = {}
        self.current_summary = None
        self.skip_next_check = False

        self.mock_patch = None
        self._final_exc_info = None
        self.mock_refs = []
        self.previous_mock_refs = []

    def options(self, parser, env):
        """
        Add options to command line.
        """
        super(LeakDetectorPlugin, self).options(parser, env)
        parser.add_option("--leak-detector-level", action="store",
                          default=env.get('NOSE_LEAK_DETECTOR_LEVEL'),
                          dest="leak_detector_level",
                          help="Level at which to detect leaks and report memory deltas "
                               "(0=None, 1=Dir, 2=Module, 3=TestCaseClass, 4=Test)")

        parser.add_option("--leak-detector-report-delta", action="store_true",
                          default=env.get('NOSE_LEAK_DETECTOR_REPORT_DELTA'),
                          dest="leak_detector_report_delta",
                          help="")

        parser.add_option("--leak-detector-patch-mock", action="store_true",
                          default=env.get('NOSE_LEAK_DETECTOR_PATCH_MOCK', True),
                          dest="leak_detector_patch_mock",
                          help="")

        parser.add_option("--leak-detector-add-traceback", action="store_true",
                          default=env.get('NOSE_LEAK_DETECTOR_ADD_TRACEBACK', False),
                          dest="leak_detector_add_traceback",
                          help="")

        parser.add_option("--leak-detector-ignore-pattern", action="append",
                          default=(list(filter(operator.truth,
                                               env.get('NOSE_LEAK_DETECTOR_IGNORE_PATTERNS',
                                                       '').split(','))) or
                                   ['NOSE_LEAK_DETECTOR_IGNORE']),
                          dest="leak_detector_ignore_patterns",
                          help="")

    def configure(self, options, conf):
        """
        Configure plugin.
        """
        super(LeakDetectorPlugin, self).configure(options, conf)
        if options.leak_detector_level:
            self.reporting_level = int(options.leak_detector_level)
        self.report_delta = options.leak_detector_report_delta
        self.patch_mock = options.leak_detector_patch_mock
        self.ignore_patterns = options.leak_detector_ignore_patterns
        self.add_traceback_to_mocks = options.leak_detector_add_traceback

    def begin(self):
        self.create_initial_summary()

        if self.detect_leaked_mocks:

            # Record pre-existing mocks
            gc.collect()
            self.mock_refs = list(weakref.ref(m) for m in muppy.get_objects()
                                  if isinstance(m, mock.Mock))

            if self.patch_mock:
                detector = self

                def decorator(f):
                    @functools.wraps(f)
                    def wrapper(mock, *args, **kwargs):
                        f(mock, *args, **kwargs)
                        detector.register_mock(mock)
                    return wrapper

                Base.__init__ = decorator(Base.__init__)

    def prepareTestCase(self, test):
        return LeakDetectorTestCase(test, detector=self)

    def create_initial_summary(self):
        # forget the current summary now that we are starting a new test
        self.current_summary = None

        if self.report_delta:
            initial_summary = self.get_summary()

        # Before any tests are run record a memory summary
        if not self.previous_summaries and self.reporting_level and self.report_delta:
            for i in range(1, LEVEL_TEST + 1):
                self.previous_summaries[i] = initial_summary

    def beforeTest(self, test):
        if self.last_test_name and self.last_test_type is not type(test.test):
            self.finished_level(LEVEL_CLASS, self.last_test_class_name)

        if not self.last_test_name or self.last_test_type is type(test.test):
            self.started_level(LEVEL_CLASS, self.last_test_class_name)

        self.started_level(LEVEL_TEST, str(test))

    def afterTest(self, test):
        self.last_test_name = str(test.test)
        self.last_test_class_name = test.test.__class__.__name__

        self.finished_level(LEVEL_TEST, str(test))

    def run_test(self, test, result):
        self.current_summary = None

        def do_check(before):
            try:
                self.check_for_leaks()
            except LeakDetected as e:
                exception_class, value, _ = sys.exc_info()
                message = str(value) + ' at %s' % self.get_level_path()
                if self.last_test_name:
                    message += " for prior test '%s'" % self.last_test_name
                    result.addError(test, (exception_class, message, None))
                else:
                    if before:
                        message += ' before test'
                    else:
                        message += ' before any tests were run'
                    result.addError(test, (exception_class, message, None))
                self.failed_test_with_leak = True
                if not self.fail_fast:
                    result.stop()

        if self.check_for_leaks_before_next_test:
            do_check(before=True)

        self.level_name[LEVEL_MODULE] = test.test.__class__.__module__

        test.test(result)

        if self.reporting_level >= LEVEL_TEST:
            do_check(before=False)

    def get_level_path(self):
        name = u''
        for i in range(1, self.reporting_level + 1):
            default_name = '<unknown %s>' % self.REPORT_DETAILS[i].title.lower()
            name += '/' + (self.level_name.get(i, default_name) or default_name)
        return name

    # TODO(asbrown): nose plugins report changes in mdule and directory at load time so we'll
    # have to save this information with each test to detect changes in module and directory
    # def beforeContext(self):
    #     self.started_level(LEVEL_MODULE)
    #
    # def afterContext(self):
    #     self.finished_level(LEVEL_MODULE,
    #                         self.last_test.test.__module__ if self.last_test else None)

    # def beforeDirectory(self, path):
    #     self.started_level(LEVEL_DIR, path)
    #
    # def afterDirectory(self, path):
    #     self.finished_level(LEVEL_DIR, path)

    def started_level(self, level, name=None):
        self.level_name[level] = name

    def finished_level(self, level, name):
        if level <= int(self.reporting_level):
            self.check_for_leaks_before_next_test = True

        if level > int(self.reporting_level):
            return

        if self.report_delta:
            color = self.REPORT_DETAILS[level].color
            report = u'Memory Delta Report for %s: %s\n' % (
                self.REPORT_DETAILS[level].title.upper(), name)
            memory_usage = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss

            print('Peak memory usage for %s: %s' % (name, memory_usage))

            old_summary = self.previous_summaries[level]

            if not self.current_summary:
                self.current_summary = self.get_summary()

            diff = self._fast_get_summary_diff(old_summary, self.current_summary)
            filtered_diff = [row for row in diff if row[1] or row[2]]
            if filtered_diff:
                print(termcolor.colored(report, color))
                print(summary.print_(filtered_diff))
            else:
                report += 'No changes\n'
                report += 'Peak memory usage: %s' % memory_usage
                print(termcolor.colored(report, color))

            self.previous_summaries[level] = self.current_summary

    def final_check(self):
        if self.detect_leaked_mocks and not self._final_exc_info:
            self.current_summary = None
            self.previous_summaries.clear()

            try:
                self.check_for_leaks()
            except LeakDetected:
                self._final_exc_info = sys.exc_info()[:2]

    def report(self, stream):
        self.final_check()

        msg = u'Leak Detector Report: '
        if self._final_exc_info:
            msg += 'FAILED: '
            color = 'red'
            msg += str(self._final_exc_info[1])
        else:
            color = 'green'
            msg += 'PASSED: All mocks have been reset or garbage collected.'
        msg += '\n'
        stream.write(termcolor.colored(msg, color))

    def finalize(self, result):
        self.final_check()

        if self.patch_mock and hasattr(Base.__init__, '__wrapped__'):
            Base.__init__ = Base.__init__.__wrapped__

        # Guarantee a test failure if we saw an exception during the report phase
        if self._final_exc_info and self.last_test_name:
            exception_class, value = self._final_exc_info
            del self._final_exc_info  # ensure that we remove the reference to the failed mock
            raise value

    def register_mock(self, mock):
        # Save the traceback on the patch so we can see where it was created
        if not mock.__dict__.get('_mock_traceback', None):
            frames = [f for f in traceback.format_stack(limit=10)[:-1] if 'mock.py' not in f]
            # Reversing these makes them easier to see
            mock.__dict__['_mock_traceback'] = list(reversed(frames))

        # Save the mock to our list of mocks
        self.mock_refs.append(weakref.ref(mock))

    def check_for_leaks(self):
        gc.collect()

        mocks = list(filter(lambda m: m is not None, [r() for r in self.mock_refs]))

        # Exclude some mocks from consideration
        # Use list so that we don't keep around a generate that isn't gc'd
        filtered_mocks = list(
            filter(lambda m: not any(re.search(pattern, repr(m))
                                     for pattern in self.ignore_patterns), mocks))

        # Use list so that we don't keep around a generate that isn't gc'd
        new_mocks = list(m for m in filtered_mocks
                         if id(m) not in set(id(r()) for r in self.previous_mock_refs))

        self.previous_mock_refs = list(map(weakref.ref, mocks))

        if new_mocks:
            def error_message(mock):
                data = vars(mock)
                msg = ' --> '.join(data.pop(
                    '_mock_traceback',
                    ["No traceback available.  Consider setting '--leak-detector-add-traceback' to "
                     "see where this mock was created."]))
                return msg + ' : ' + str(data)
            errs = list(map(error_message, new_mocks))
            msg = ('Found %d new mock(s) that have not been garbage collected:\n%s' %
                   (len(new_mocks), errs))

            # Ensure hard references to the mocks are no longer on the stack
            del mocks[:], new_mocks[:]
            raise LeakDetected(msg)

    def get_summary(self):
        gc.collect()
        # exclude everything in this object itself
        excluded = set(id(o) for o in muppy.get_referents(self))
        return summary.summarize(o for o in muppy.get_objects() if not id(o) in excluded)

    @staticmethod
    def is_called_mock(obj):
        return isinstance(obj, mock.Mock) and obj.called

    # from https://github.com/pympler/pympler/pull/6
    @staticmethod
    def _fast_get_summary_diff(left, right):

        objects_key = lambda object_footprint: object_footprint[0]
        val_neg = lambda lval: [lval[0], -lval[1], -lval[2]]

        def next_safe(it):
            try:
                val = it.next()
                return val, False
            except StopIteration:
                return None, True

        lsorted = sorted(left, key=objects_key)
        rsorted = sorted(right, key=objects_key)

        lit = iter(lsorted)
        rit = iter(rsorted)
        lval = None
        rval = None
        lend = False
        rend = False
        ret = []
        while not lend or not rend:
            if lval is None:
                if lend:
                    if rval:
                        ret.extend([rval] + [x for x in rit])
                    break
                else:
                    lval, lend = next_safe(lit)

            if rval is None:
                if rend:
                    if lval:
                        ret.extend([val_neg(lval)] + [val_neg(x) for x in lit])
                    break
                else:
                    rval, rend = next_safe(rit)

            if lval is None or rval is None:
                continue

            if objects_key(lval) == objects_key(rval):
                ret.append([rval[0], rval[1] - lval[1], rval[2] - lval[2]])
                lval, lend = next_safe(lit)
                rval, rend = next_safe(rit)
            elif objects_key(lval) < objects_key(rval):
                ret.append(val_neg(lval))
                lval, lend = next_safe(lit)
            else:
                ret.append(rval)
                rval, rend = next_safe(rit)

        return ret


# Register this plugin with multiprocess plugin if applicable.
try:
    from nose.plugins import multiprocess
    multiprocess._instantiate_plugins = multiprocess._instantiate_plugins or []
    multiprocess._instantiate_plugins.append(LeakDetectorPlugin)
except ImportError:
    pass
