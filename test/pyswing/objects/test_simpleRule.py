import datetime
import unittest
from unittest.mock import patch

from utils.FileHelper import forceWorkingDirectory, deleteFile
from utils.Logger import Logger
from pyswing.objects.simpleRule import SimpleRule
from pyswing.objects.equity import Equity
from pyswing.objects.indicatorROC import IndicatorROC
import pyswing.constants
import pyswing.globals
from pyswing.CreateDatabase import createDatabase


class TestSimpleRule(unittest.TestCase):

    @classmethod
    def setUpClass(self):

        Logger.pushLogData("unitTesting", __name__)
        forceWorkingDirectory()

        pyswing.globals.potentialRuleMatches = None
        pyswing.globals.equityCount = None

        pyswing.constants.pySwingDatabase = "output/TestSimpleRule.db"
        pyswing.constants.pySwingStartDate = datetime.datetime(2014, 1, 1)

        deleteFile(pyswing.constants.pySwingDatabase)

        args = "-D %s -s %s" % (pyswing.constants.pySwingDatabase, pyswing.constants.pySwingDatabaseScript)
        createDatabase(args.split())

        pretendDate = datetime.datetime(2015, 9, 1)
        with patch.object(Equity, '_getTodaysDate', return_value=pretendDate) as mock_method:

            self._equityCBA = Equity("WOR.AX")
            self._equityCBA.importData()

        indicatorROC = IndicatorROC(self._equityCBA.dataFrame(), "WOR.AX")
        indicatorROC.updateIndicator()

        self.rule = SimpleRule("Indicator_ROC", "ROC_5 > 10")
        self.rule.evaluateRule("WOR.AX")


    @classmethod
    def tearDownClass(self):
        deleteFile(pyswing.constants.pySwingDatabase)


    def test_IndicatorSMA(self):

        dataPointMatch = self.rule._ruleData.ix['2015-04-27 00:00:00']
        self.assertEqual(dataPointMatch['Match'], 1)

        dataPointNoMatch = self.rule._ruleData.ix['2015-04-28 00:00:00']
        self.assertEqual(dataPointNoMatch['Match'], 0)

    def test_getEquityCount(self):

        equityCount = self.rule._getEquityCount()
        self.assertEqual(equityCount, 1)

        potentialRuleMatches = self.rule._getPotentialRuleMatches()
        self.assertEqual(potentialRuleMatches, 434)

    def test_analyseRule(self):

        self.rule.analyseRule()

        self.assertAlmostEqual(self.rule._matchesPerDay, 0.032, 3)


if __name__ == '__main__':
    unittest.main()
