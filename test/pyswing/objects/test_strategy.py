import datetime
import unittest
import sqlite3

# from pyswing.AnalyseRules import analyseRules
# from pyswing.CalculateExitValues import calculateExitValues
# from pyswing.CreateDatabase import createDatabase
# from pyswing.EvaluateRules import evaluateRules
# from pyswing.ImportData import importData
# from pyswing.UpdateIndicators import updateIndicators
# from pyswing.objects.equity import Equity
# from unittest.mock import patch

from utils.FileHelper import forceWorkingDirectory, deleteFile, copyFile
from utils.Logger import Logger
import pyswing.constants
import pyswing.globals
from pyswing.objects.strategy import Strategy, getStrategies


class TestStrategy(unittest.TestCase):

    @classmethod
    def setUpClass(self):
        Logger.pushLogData("unitTesting", __name__)
        forceWorkingDirectory()

        pyswing.globals.potentialRuleMatches = None
        pyswing.globals.equityCount = None

        pyswing.constants.pySwingDatabase = "output/TestStrategy.db"
        pyswing.constants.pySwingStartDate = datetime.datetime(2015, 1, 1)

        deleteFile(pyswing.constants.pySwingDatabase)

        copyFile("resources/TestDatabase.db", pyswing.constants.pySwingDatabase)

        # TestDatabase.db *should* be equivalent to running the following...

        # args = "-D %s -s %s" % (pyswing.constants.pySwingDatabase, pyswing.constants.pySwingDatabaseScript)
        # createDatabase(args.split())
        #
        # pretendDate = datetime.datetime(2015, 7, 1)
        # with patch.object(Equity, '_getTodaysDate', return_value=pretendDate) as mock_method:
        #     args = "-n unitTest".split()
        #     importData(args)
        #
        # args = "-n unitTest".split()
        # updateIndicators(args)
        #
        # args = "-n unitTest".split()
        # evaluateRules(args)
        #
        # args = "-n unitTest".split()
        # analyseRules(args)
        #
        # args = "-n unitTest".split()
        # calculateExitValues(args)


    @classmethod
    def tearDownClass(self):
        deleteFile(pyswing.constants.pySwingDatabase)


    def test_getStrategies(self):

        strategies = getStrategies()
        self.assertEqual(len(strategies), 124)

    def test_evaluateStrategy(self):

        strategy = Strategy("Rule Equities Indicator_BB20 abs(t1.Close - t2.upperband) < abs(t1.Close - t2.middleband)", "Rule Equities abs(Close - High) * 2 < abs(Close - Low)", "Exit TrailingStop3.0 RiskRatio2", "Buy")
        strategy.evaluateStrategy()
        numberOfTrades = self._numberOfTrades('Buy')
        self.assertEqual(numberOfTrades, 70)


    def _numberOfTrades(self, type):
        connection = sqlite3.connect(pyswing.constants.pySwingDatabase)
        query = "select numberOfTrades from 'TwoRuleStrategy' where type = '%s'" % type
        cursor = connection.cursor()
        cursor.execute(query)
        numberOfTrades = cursor.fetchone()[0]
        connection.close()
        return numberOfTrades


if __name__ == '__main__':
    unittest.main()


