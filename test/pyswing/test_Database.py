import datetime
import unittest
from unittest.mock import patch

from pyswing.AnalyseRules import analyseRules
from pyswing.CalculateExitValues import calculateExitValues
from pyswing.CreateDatabase import createDatabase
from pyswing.EvaluateRules import evaluateRules
from pyswing.ImportData import importData
from pyswing.UpdateIndicators import updateIndicators
from pyswing.objects.equity import Equity
from utils.FileHelper import forceWorkingDirectory, deleteFile, copyFile
from utils.Logger import Logger
import pyswing.constants
import pyswing.globals
import os


class TestDatabase(unittest.TestCase):
    """
    This isn't really a Unit Test.

    Instead it creates a test database (resources/TestDatabase.db) that other Unit Tests leverage.

    The only real point of this is to limit the amount of traffic sent to Yahoo Finance...
    """

    @classmethod
    def setUpClass(self):
        Logger.pushLogData("unitTesting", __name__)
        forceWorkingDirectory()

        pyswing.globals.potentialRuleMatches = None
        pyswing.globals.equityCount = None

        pyswing.constants.pySwingDatabase = "output/TestDatabase.db"
        pyswing.constants.pySwingStartDate = datetime.datetime(2015, 1, 1)

        deleteFile(pyswing.constants.pySwingDatabase)
        deleteFile(pyswing.constants.pySwingTestDatabase)

        args = "-D %s -s %s" % (pyswing.constants.pySwingDatabase, pyswing.constants.pySwingDatabaseScript)
        createDatabase(args.split())

        pretendDate = datetime.datetime(2015, 7, 1)
        with patch.object(Equity, '_getTodaysDate', return_value=pretendDate) as mock_method:
            args = "-n unitTest".split()
            importData(args)

        args = "-n unitTest".split()
        updateIndicators(args)

        args = "-n unitTest".split()
        evaluateRules(args)

        args = "-n unitTest".split()
        analyseRules(args)

        args = "-n unitTest".split()
        calculateExitValues(args)


    @classmethod
    def tearDownClass(self):
        deleteFile(pyswing.constants.pySwingDatabase)


    def test_TestDatabase(self):

        self.assertTrue(os.path.exists(pyswing.constants.pySwingDatabase))
        self.assertFalse(os.path.exists(pyswing.constants.pySwingTestDatabase))

        copyFile(pyswing.constants.pySwingDatabase, pyswing.constants.pySwingTestDatabase)

        self.assertTrue(os.path.exists(pyswing.constants.pySwingTestDatabase))


if __name__ == '__main__':
    unittest.main()


