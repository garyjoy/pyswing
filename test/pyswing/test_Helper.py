import datetime
import unittest
from unittest.mock import patch
import os

from pyswing.AnalyseRules import analyseRules
from pyswing.CalculateExitValues import calculateExitValues
from pyswing.CreateDatabase import createDatabase
from pyswing.EvaluateRules import evaluateRules
from pyswing.ImportData import importData
from pyswing.UpdateIndicators import updateIndicators
from pyswing.objects.equity import Equity
from pyswing.utils.FileHelper import forceWorkingDirectory, deleteFile, copyFile
from pyswing.utils.Logger import Logger
import pyswing.constants
import pyswing.database
import pyswing.globals


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

        pyswing.database.overrideDatabase("output/TestDatabase.db")
        pyswing.constants.pySwingStartDate = datetime.datetime(2015, 1, 1)

        deleteFile(pyswing.database.pySwingDatabase)
        deleteFile(pyswing.database.pySwingTestDatabase)

        args = "-n %s" % ("unitTesting")
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
        deleteFile(pyswing.database.pySwingDatabase)


    def test_TestDatabase(self):

        self.assertTrue(os.path.exists(pyswing.database.pySwingDatabase))
        self.assertFalse(os.path.exists(pyswing.database.pySwingTestDatabase))

        copyFile(pyswing.database.pySwingDatabase, pyswing.database.pySwingTestDatabase)

        self.assertTrue(os.path.exists(pyswing.database.pySwingTestDatabase))


if __name__ == '__main__':
    unittest.main()


