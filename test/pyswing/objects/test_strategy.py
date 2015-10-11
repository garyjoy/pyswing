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
from pyswing.objects.strategy import Strategy, getTwoRuleStrategies, getBestUnprocessedTwoRuleStrategy, getRules, markTwoRuleStrategyAsProcessed


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

        copyFile(pyswing.constants.pySwingTestDatabase, pyswing.constants.pySwingDatabase)

    @classmethod
    def tearDownClass(self):
        deleteFile(pyswing.constants.pySwingDatabase)


    def test_getStrategies(self):

        strategies = getTwoRuleStrategies(0.1)
        self.assertEqual(len(strategies), 124)


    def test_getRules(self):

        rules = getRules()
        self.assertEqual(len(rules), 84)


    def test_evaluateStrategy(self):

        twoRuleStrategy = Strategy("Rule Equities Indicator_BB20 abs(t1.Close - t2.upperband) < abs(t1.Close - t2.middleband)", "Rule Equities abs(Close - High) * 2 < abs(Close - Low)", "Exit TrailingStop3.0 RiskRatio2", "Buy")
        twoRuleStrategy.evaluateTwoRuleStrategy()
        numberOfTrades = self._numberOfTwoRuleTrades('Buy')
        self.assertEqual(numberOfTrades, 70)

        bestStrategy = getBestUnprocessedTwoRuleStrategy(10)

        self.assertEqual(bestStrategy[0], "Rule Equities Indicator_BB20 abs(t1.Close - t2.upperband) < abs(t1.Close - t2.middleband)")
        self.assertEqual(bestStrategy[1], "Rule Equities abs(Close - High) * 2 < abs(Close - Low)")

        threeRuleStrategy = Strategy("Rule Equities Indicator_BB20 abs(t1.Close - t2.upperband) < abs(t1.Close - t2.middleband)", "Rule Equities abs(Close - High) * 2 < abs(Close - Low)", "Exit TrailingStop3.0 RiskRatio2", "Buy", "Rule Equities Close -1 Comparison.GreaterThan 1.01")
        threeRuleStrategy.evaluateThreeRuleStrategy()
        numberOfTrades = self._numberOfThreeRuleTrades('Buy')
        self.assertEqual(numberOfTrades, 36)

        numberOfTrades = self._numberOfSearchedTwoRuleTrades()
        self.assertEqual(numberOfTrades, 0)
        markTwoRuleStrategyAsProcessed(bestStrategy[0], bestStrategy[1])
        numberOfTrades = self._numberOfSearchedTwoRuleTrades()
        self.assertEqual(numberOfTrades, 1)


    def _numberOfSearchedTwoRuleTrades(self):
        connection = sqlite3.connect(pyswing.constants.pySwingDatabase)
        query = "select count(1) from 'TwoRuleStrategy' where Searched = 1"
        cursor = connection.cursor()
        cursor.execute(query)
        numberOfTrades = cursor.fetchone()[0]
        connection.close()
        return numberOfTrades

    def _numberOfTwoRuleTrades(self, type):
        connection = sqlite3.connect(pyswing.constants.pySwingDatabase)
        query = "select numberOfTrades from 'TwoRuleStrategy' where type = '%s'" % type
        cursor = connection.cursor()
        cursor.execute(query)
        numberOfTrades = cursor.fetchone()[0]
        connection.close()
        return numberOfTrades

    def _numberOfThreeRuleTrades(self, type):
        connection = sqlite3.connect(pyswing.constants.pySwingDatabase)
        query = "select numberOfTrades from 'ThreeRuleStrategy' where type = '%s'" % type
        cursor = connection.cursor()
        cursor.execute(query)
        numberOfTrades = cursor.fetchone()[0]
        connection.close()
        return numberOfTrades


if __name__ == '__main__':
    unittest.main()


