#!/usr/bin/env python

from scripttest import TestFileEnvironment
import os
import unittest
import shutil
import sys
import pmagpy.check_updates as check_updates

env = TestFileEnvironment('./new-test-output')
WD = check_updates.get_pmag_dir()
programs_WD = os.path.join(WD, 'programs')

class TestProgramsHelp(unittest.TestCase):

    def setUp(self):
        if not os.path.exists('./new-test-output'):
            os.mkdir('./new-test-output')

    def tearDown(self):
        if os.path.exists('./new-test-output'):
            shutil.rmtree('./new-test-output')
        

    @unittest.skipIf(sys.platform not in ['darwin', 'win32', 'win62'], "Doesn't work without PmagPy in PYTHONPATH")
    def test_all(self):
        programs = os.listdir(programs_WD)
        not_checked = []
        for prog in programs:
            print "Testing help message for:", prog
            if prog in ['__init__.py', 'program_envs.py']:
                continue
            if not prog.endswith('.py') or '#' in prog:
                not_checked.append(prog)
                continue
            if prog.lower() != prog:
                continue
            res = env.run(prog, '-h')
            #except AssertionError as ex:
            #    not_checked.append(prog)
            #    print 'ex', type(ex)
            #    print res
        print 'not_checked', not_checked


