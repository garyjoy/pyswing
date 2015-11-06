import datetime
import unittest
from unittest.mock import patch

from pyswing.utils.FileHelper import forceWorkingDirectory, deleteFile
from pyswing.utils.Logger import Logger
from pyswing.objects.rules.multipleIndicatorRule import MultipleIndicatorRule
from pyswing.objects.equity import Equity
from pyswing.objects.indicators.indicatorSMA import IndicatorSMA
import pyswing.constants
from pyswing.CreateDatabase import createDatabase


class TestMultipleIndicatorRule(unittest.TestCase):

    @classmethod
    def setUpClass(self):

        Logger.pushLogData("unitTesting", __name__)
        forceWorkingDirectory()

        pyswing.constants.pySwingDatabase = "output/TestMultipleIndicatorRule.db"
        pyswing.constants.pySwingStartDate = datetime.datetime(2013, 1, 1)

        deleteFile(pyswing.constants.pySwingDatabase)

        args = "-D %s -s %s" % (pyswing.constants.pySwingDatabase, pyswing.constants.pySwingDatabaseScript)
        createDatabase(args.split())

        pretendDate = datetime.datetime(2015, 9, 1)
        with patch.object(Equity, '_getTodaysDate', return_value=pretendDate) as mock_method:

            self._equityCBA = Equity("WOR.AX")
            self._equityCBA.importData()

        indicatorSMA = IndicatorSMA(self._equityCBA.dataFrame(), "WOR.AX")
        indicatorSMA.updateIndicator()


    @classmethod
    def tearDownClass(self):
        deleteFile(pyswing.constants.pySwingDatabase)


    def test_IndicatorSMA(self):

        rule = MultipleIndicatorRule("Equities", "Indicator_SMA", "t1.Close > t2.SMA_200")

        rule.evaluateRule("WOR.AX")

        dataPointMatch = rule._ruleData.ix['2015-07-03 00:00:00']
        self.assertEqual(dataPointMatch['Match'], 1)

        dataPointNoMatch = rule._ruleData.ix['2015-07-06 00:00:00']
        self.assertEqual(dataPointNoMatch['Match'], 0)


if __name__ == '__main__':
    unittest.main()
