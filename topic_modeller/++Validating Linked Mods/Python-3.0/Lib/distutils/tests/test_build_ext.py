import sys
import os
import tempfile
import shutil
from io import StringIO

from distutils.core import Extension, Distribution
from distutils.command.build_ext import build_ext
from distutils import sysconfig

import unittest
from test import support

# http://bugs.python.org/issue4373
# Don't load the xx module more than once.
ALREADY_TESTED = False

class BuildExtTestCase(unittest.TestCase):
    def setUp(self):
        # Create a simple test environment
        # Note that we're making changes to sys.path
        self.tmp_dir = tempfile.mkdtemp(prefix="pythontest_")
        self.sys_path = sys.path[:]
        sys.path.append(self.tmp_dir)

        xx_c = os.path.join(sysconfig.project_base, 'Modules', 'xxmodule.c')
        shutil.copy(xx_c, self.tmp_dir)

    def test_build_ext(self):
        global ALREADY_TESTED
        xx_c = os.path.join(self.tmp_dir, 'xxmodule.c')
        xx_ext = Extension('xx', [xx_c])
        dist = Distribution({'name': 'xx', 'ext_modules': [xx_ext]})
        dist.package_dir = self.tmp_dir
        cmd = build_ext(dist)
        if os.name == "nt":
            # On Windows, we must build a debug version iff running
            # a debug build of Python
            cmd.debug = sys.executable.endswith("_d.exe")
        cmd.build_lib = self.tmp_dir
        cmd.build_temp = self.tmp_dir

        old_stdout = sys.stdout
        if not support.verbose:
            # silence compiler output
            sys.stdout = StringIO()
        try:
            cmd.ensure_finalized()
            cmd.run()
        finally:
            sys.stdout = old_stdout

        if ALREADY_TESTED:
            return
        else:
            ALREADY_TESTED = True

        import xx

        for attr in ('error', 'foo', 'new', 'roj'):
            self.assertTrue(hasattr(xx, attr))

        self.assertEqual(xx.foo(2, 5), 7)
        self.assertEqual(xx.foo(13,15), 28)
        self.assertEqual(xx.new().demo(), None)
        doc = 'This is a template module just for instruction.'
        self.assertEqual(xx.__doc__, doc)
        self.assertTrue(isinstance(xx.Null(), xx.Null))
        self.assertTrue(isinstance(xx.Str(), xx.Str))

    def tearDown(self):
        # Get everything back to normal
        support.unload('xx')
        sys.path = self.sys_path
        # XXX on Windows the test leaves a directory with xx module in TEMP
        shutil.rmtree(self.tmp_dir, os.name == 'nt' or sys.platform == 'cygwin')

def test_suite():
    if not sysconfig.python_build:
        if support.verbose:
            print('test_build_ext: The test must be run in a python build dir')
        return unittest.TestSuite()
    else: return unittest.makeSuite(BuildExtTestCase)

if __name__ == '__main__':
    support.run_unittest(test_suite())
