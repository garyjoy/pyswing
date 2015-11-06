import datetime
import unittest
from unittest.mock import patch

import pyswing.constants
from pyswing.utils.FileHelper import forceWorkingDirectory, deleteFile
from pyswing.utils.Logger import Logger
from pyswing.objects.equity import Equity
from pyswing.objects.rules.crossingRule import CrossingRule
from pyswing.objects.indicators.indicatorSMA import IndicatorSMA
from pyswing.objects.indicators.indicatorEMA import IndicatorEMA
from pyswing.CreateDatabase import createDatabase


class TestCrossingRule(unittest.TestCase):

    @classmethod
    def setUpClass(self):

        Logger.pushLogData("unitTesting", __name__)
        forceWorkingDirectory()

        pyswing.constants.pySwingDatabase = "output/TestCrossingRule.db"
        pyswing.constants.pySwingStartDate = datetime.datetime(2015, 1, 1)

        deleteFile(pyswing.constants.pySwingDatabase)

        args = "-D %s -s %s" % (pyswing.constants.pySwingDatabase, pyswing.constants.pySwingDatabaseScript)
        createDatabase(args.split())

        pretendDate = datetime.datetime(2015, 9, 1)
        with patch.object(Equity, '_getTodaysDate', return_value=pretendDate) as mock_method:

            self._equityCBA = Equity("WOR.AX")
            self._equityCBA.importData()

        indicatorSMA = IndicatorSMA(self._equityCBA.dataFrame(), "WOR.AX")
        indicatorSMA.updateIndicator()

        indicatorEMA = IndicatorEMA(self._equityCBA.dataFrame(), "WOR.AX")
        indicatorEMA.updateIndicator()


    @classmethod
    def tearDownClass(self):
        deleteFile(pyswing.constants.pySwingDatabase)


    def test_CrossingRule(self):

        rule = CrossingRule("Indicator_SMA","SMA_5","Indicator_SMA","SMA_10")
        rule.evaluateRule("WOR.AX")

        dataPointMatch = rule._ruleData.ix['2015-08-28 00:00:00']
        self.assertEqual(dataPointMatch['Match'], 1)

        dataPointMatch = rule._ruleData.ix['2015-08-31 00:00:00']
        self.assertEqual(dataPointMatch['Match'], 0)

        anotherRule = CrossingRule("Indicator_SMA","SMA_5","Indicator_EMA","EMA_50")
        anotherRule.evaluateRule("WOR.AX")

        dataPointMatch = anotherRule._ruleData.ix['2015-07-03 00:00:00']
        self.assertEqual(dataPointMatch['Match'], 1)

        dataPointMatch = anotherRule._ruleData.ix['2015-07-06 00:00:00']
        self.assertEqual(dataPointMatch['Match'], 0)


if __name__ == '__main__':
    unittest.main()
