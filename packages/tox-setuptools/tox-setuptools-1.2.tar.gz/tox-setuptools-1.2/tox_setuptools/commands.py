from setuptools.command.test import test
import sys


class ToxTest(test):
    user_options = [('tox-args=', 'a', 'Arguments to pass to tox')]

    def __init__(self, dist, **kw):
        self.test_suite = True
        self.test_args = []
        self.tox_args = None
        super().__init__(dist, **kw)

    def initialize_options(self):
        test.initialize_options(self)

    def finalize_options(self):
        test.finalize_options(self)

    def run_tests(self):
        # import here, cause outside the eggs aren't loaded
        import tox
        import shlex
        args = self.tox_args
        if args:
            args = shlex.split(self.tox_args)
        else:
            args = []
        errno = tox.cmdline(args=args)
        sys.exit(errno)
