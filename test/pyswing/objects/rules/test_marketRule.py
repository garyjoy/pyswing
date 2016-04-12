import datetime
import unittest
from unittest.mock import patch

from pyswing.utils.FileHelper import forceWorkingDirectory, deleteFile
from pyswing.utils.Logger import Logger
from pyswing.objects.rules.marketRule import MarketRule
from pyswing.objects.rules.relativeRule import Comparison
from pyswing.objects.equity import Equity
from pyswing.objects.indicators.indicatorADI import IndicatorADI
import pyswing.constants
import pyswing.database
import pyswing.globals
from pyswing.CreateDatabase import createDatabase


class TestMarketRule(unittest.TestCase):

    @classmethod
    def setUpClass(self):

        Logger.pushLogData("unitTesting", __name__)
        forceWorkingDirectory()

        pyswing.globals.potentialRuleMatches = None
        pyswing.globals.equityCount = None

        pyswing.database.overrideDatabase("output/TestMarketRule.db")
        pyswing.constants.pySwingStartDate = datetime.datetime(2014, 1, 1)

        deleteFile(pyswing.database.pySwingDatabase)

        args = "-n %s" % ("unitTesting")
        createDatabase(args.split())

        pretendDate = datetime.datetime(2015, 9, 1)
        with patch.object(Equity, '_getTodaysDate', return_value=pretendDate) as mock_method:

            self._equity = Equity("WOR.AX")
            self._equity.importData()

        indicatorADI = IndicatorADI()
        indicatorADI.updateIndicator()

        self.rule = MarketRule("Indicator_ADI", "ADI > 0")
        self.rule.evaluateRule()


    @classmethod
    def tearDownClass(self):
        deleteFile(pyswing.database.pySwingDatabase)


    def test_IndicatorADI(self):

        dataPointMatch = self.rule._ruleData.ix['2015-08-28 00:00:00']
        self.assertEqual(dataPointMatch['Match'], 1)

        dataPointNoMatch = self.rule._ruleData.ix['2015-08-31 00:00:00']
        self.assertEqual(dataPointNoMatch['Match'], 0)

    def test_getEquityCount(self):

        potentialRuleMatches = self.rule._getPotentialRuleMatches()
        self.assertEqual(potentialRuleMatches, 434)

    def test_analyseRule(self):

        self.rule.analyseRule()
        self.assertAlmostEqual(self.rule._matchesPerDay, 0.438, 3)


if __name__ == '__main__':
    unittest.main()
