import unittest
import inspect
from dataactcore.models.baseInterface import BaseInterface
from dataactbroker.handlers.interfaceHolder import InterfaceHolder
from testUtils import TestUtils
from loginTests import LoginTests
from fileTests import FileTests
import sys
import os
import xmlrunner

def runTests():

    BaseInterface.IS_FLASK = False # Unit tests using interfaces are not enclosed in a Flask route
    interfaces = InterfaceHolder()
    utils = TestUtils()
    open(FileTests.TABLES_CLEARED_FILE,"w").write(str(False)) # Mark file tests as not having cleared tables
    # Pass routeTests into other test sets to save time, they can also run without the arguments
    # Create test suite
    suite = unittest.TestSuite()
    # Get lists of method names
    loginMethods = LoginTests.__dict__.keys()
    fileMethods = FileTests.__dict__.keys()
    #loginMethods = []
    #fileMethods = [["test_file_submission"]]
    for method in loginMethods:
        # If test method, add to suite
        if(method[0:4] == "test"):
            test =LoginTests(methodName=method)
            test.addUtils(utils)
            suite.addTest(test)

    for method in fileMethods:
        # If test method, add to suite
        if(method[0:4] == "test"):
            test =FileTests(methodName=method,interfaces=interfaces)
            test.addUtils(utils)
            suite.addTest(test)

    print(str(suite.countTestCases()) + " tests in suite")

    # Run tests and store results
    if TestUtils.TEST_OUTPUT == "junitxml":
        runner = xmlrunner.XMLTestRunner(output='test-reports')
    else:
        runner = unittest.TextTestRunner(verbosity=2)
    runner.run(suite)

if __name__ == '__main__':
    if(len(sys.argv) == 2) :
        TestUtils.BASE_URL = sys.argv[1] + ":8080"
    url = os.getenv('BROKER_NAME', "NOT SET")
    if(url != "NOT SET") :
        TestUtils.BASE_URL = "http://broker"
        TestUtils.TEST_OUTPUT = "junitxml"
    runTests()