# -*- coding: utf-8 -*-
# usage: python web2py.py -S <myapp>/<mycontroller> -M -R <path_to_this_file>.py

import unittest #, os
# from datetime import datetime
# from gluon import *
# from gluon.globals import current
# from contrib.populate import populate_generator

# import pdb
# from IPython.core.debugger import Pdb

class TestExample(unittest.TestCase):

    #def setUp(self):
        #""""""

    #def tearDown(self):
        #""""""

    def test_example(self):
        """ Just let the logger to say Hello to the world """
        logger.debug("Hello world!")
        self.assertTrue(True)

test_cases = (
    # Append here test libs you want to run...
    # TestExample,
)
def load_tests(loader):
    # https://docs.python.org/2/library/unittest.html#load-tests-protocol
    suite = unittest.TestSuite()
    for test_class in test_cases:
        tests = loader.loadTestsFromTestCase(test_class)
        suite.addTests(tests)
    return suite

suite = load_tests(unittest.TestLoader())
unittest.TextTestRunner(verbosity=4).run(suite)
