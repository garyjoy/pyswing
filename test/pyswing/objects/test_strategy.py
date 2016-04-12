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

from pyswing.utils.FileHelper import forceWorkingDirectory, deleteFile, copyFile
from pyswing.utils.Logger import Logger
import pyswing.constants
import pyswing.database
import pyswing.globals
from pyswing.objects.strategy import Strategy, getTwoRuleStrategies, getBestUnprocessedTwoRuleStrategy, \
    getRules, markTwoRuleStrategyAsProcessed, getStrategies, getLatestDate, emptyHistoricTradesTable


class TestStrategy(unittest.TestCase):

    @classmethod
    def setUpClass(self):
        Logger.pushLogData("unitTesting", __name__)
        forceWorkingDirectory()

        pyswing.globals.potentialRuleMatches = None
        pyswing.globals.equityCount = None

        pyswing.database.overrideDatabase("output/TestStrategy.db")
        pyswing.constants.pySwingStartDate = datetime.datetime(2015, 1, 1)

        deleteFile(pyswing.database.pySwingDatabase)

        copyFile(pyswing.database.pySwingTestDatabase, pyswing.database.pySwingDatabase)

        twoRuleStrategy = Strategy("Rule Equities Indicator_BB20 abs(t1.Close - t2.upperband) < abs(t1.Close - t2.middleband)", "Rule Equities abs(Close - High) * 2 < abs(Close - Low)", "Exit TrailingStop3.0 RiskRatio2", "Buy")
        twoRuleStrategy.evaluateTwoRuleStrategy()

        threeRuleStrategy = Strategy("Rule Equities Indicator_BB20 abs(t1.Close - t2.upperband) < abs(t1.Close - t2.middleband)", "Rule Equities abs(Close - High) * 2 < abs(Close - Low)", "Exit TrailingStop3.0 RiskRatio2", "Buy", "Rule Indicator_RSI RSI > 20")
        threeRuleStrategy.evaluateThreeRuleStrategy()

        historicTrades = Strategy("Rule Equities Indicator_BB20 abs(t1.Close - t2.upperband) < abs(t1.Close - t2.middleband)", "Rule Equities abs(Close - High) * 2 < abs(Close - Low)", "Exit TrailingStop3.0 RiskRatio2", "Buy", "Rule Indicator_RSI RSI > 20")
        historicTrades.generateHistoricTrades()


    @classmethod
    def tearDownClass(self):
        deleteFile(pyswing.database.pySwingDatabase)


    def test_getTwoRuleStrategies(self):

        strategies = getTwoRuleStrategies(1)
        self.assertEqual(len(strategies), 1974)

    def test_getStrategies(self):

        strategies = getStrategies(34, -10)
        self.assertEqual(len(strategies), 1)

    def test_getLatestDate(self):

        latestDate = getLatestDate()
        self.assertEqual(latestDate, "2015-07-01 00:00:00")

    def test_analyseStrategy(self):

        strategies = getStrategies(34, -10)
        strategies[0].analyse()

    def test_analyseStrategy(self):

        strategy = Strategy('Rule Indicator_RSI RSI > 20', 'Rule Indicator_RSI RSI > 20', 'Exit TrailingStop3.0 RiskRatio2', 'Buy', 'Rule Indicator_RSI RSI > 20')
        strategy.meanResultPerTrade = 1.0
        strategy.medianResultPerTrade = 1.0
        strategy.totalProfit = 1.0
        strategy.numberOfTrades = 1.0
        strategy.sharpeRatio = 1.0
        strategy.maximumDrawdown = 1.0
        data = strategy.askHorse('2015-05-25 00:00:00')
        self.assertTrue(data)
        self.assertEqual(len(strategy.tradeDetails), 3)

        strategy = Strategy('Rule Equities abs(Close - High) * 10 < abs(Close - Low)', 'Rule Equities abs(Close - High) * 10 < abs(Close - Low)', 'Exit TrailingStop3.0 RiskRatio2', 'Buy', 'Rule Equities abs(Close - High) * 10 < abs(Close - Low)')
        strategy.meanResultPerTrade = 1.0
        strategy.medianResultPerTrade = 1.0
        strategy.totalProfit = 1.0
        strategy.numberOfTrades = 1.0
        strategy.sharpeRatio = 1.0
        strategy.maximumDrawdown = 1.0
        moreData = strategy.askHorse('2015-05-26 00:00:00')
        self.assertFalse(moreData)
        self.assertEqual(len(strategy.tradeDetails), 0)

    def test_getRules(self):

        rules = getRules()
        self.assertEqual(len(rules), 182)

    def test_evaluateStrategy(self):

        rule1, rule2, exit, type = getBestUnprocessedTwoRuleStrategy(10)

        numberOfTrades = self._numberOfTwoRuleTrades('Buy')
        self.assertEqual(numberOfTrades, 70)

        self.assertEqual(rule1, "Rule Equities Indicator_BB20 abs(t1.Close - t2.upperband) < abs(t1.Close - t2.middleband)")
        self.assertEqual(rule2, "Rule Equities abs(Close - High) * 2 < abs(Close - Low)")

        numberOfTrades = self._numberOfThreeRuleTrades('Buy')
        self.assertEqual(numberOfTrades, 70)

        numberOfTrades = self._numberOfSearchedTwoRuleTrades()
        self.assertEqual(numberOfTrades, 0)
        markTwoRuleStrategyAsProcessed(rule1, rule2, type)
        numberOfTrades = self._numberOfSearchedTwoRuleTrades()
        self.assertEqual(numberOfTrades, 1)

    def test_generateHistoricTrades(self):
        self.assertEqual(self._numberOfHistoricTrades(), 70)
        emptyHistoricTradesTable()
        self.assertEqual(self._numberOfHistoricTrades(), 0)


    def _numberOfSearchedTwoRuleTrades(self):
        connection = sqlite3.connect(pyswing.database.pySwingDatabase)
        query = "select count(1) from 'TwoRuleStrategy' where Searched = 1"
        cursor = connection.cursor()
        cursor.execute(query)
        numberOfTrades = cursor.fetchone()[0]
        connection.close()
        return numberOfTrades

    def _numberOfTwoRuleTrades(self, type):
        connection = sqlite3.connect(pyswing.database.pySwingDatabase)
        query = "select numberOfTrades from 'TwoRuleStrategy' where type = '%s'" % type
        cursor = connection.cursor()
        cursor.execute(query)
        numberOfTrades = cursor.fetchone()[0]
        connection.close()
        return numberOfTrades

    def _numberOfThreeRuleTrades(self, type):
        connection = sqlite3.connect(pyswing.database.pySwingDatabase)
        query = "select numberOfTrades from 'ThreeRuleStrategy' where type = '%s'" % type
        cursor = connection.cursor()
        cursor.execute(query)
        numberOfTrades = cursor.fetchone()[0]
        connection.close()
        return numberOfTrades

    def _numberOfHistoricTrades(self):
        connection = sqlite3.connect(pyswing.database.pySwingDatabase)
        query = "select count(1) from 'HistoricTrades'"
        cursor = connection.cursor()
        cursor.execute(query)
        numberOfTrades = cursor.fetchone()[0]
        connection.close()
        return numberOfTrades


if __name__ == '__main__':
    unittest.main()


