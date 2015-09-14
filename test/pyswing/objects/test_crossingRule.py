import datetime
import logging
import unittest
import sqlite3
from unittest.mock import patch

from utils.FileHelper import forceWorkingDirectory, deleteFile
from utils.Logger import Logger
from pyswing.objects.equity import Equity
from pyswing.objects.crossingRule import CrossingRule
from pyswing.objects.indicatorSMA import IndicatorSMA
import pyswing.constants


class TestCrossingRule(unittest.TestCase):

    @classmethod
    def setUpClass(self):

        Logger.pushLogData("unitTesting", __name__)
        forceWorkingDirectory()

        pyswing.constants.pySwingDatabase = "output/TestCrossingRule.db"
        pyswing.constants.pySwingStartDate = datetime.datetime(2015, 1, 1)

        deleteFile(pyswing.constants.pySwingDatabase)

        # TODO:  Move this into another class / function (with UNit Test etc.)
        Logger.log(logging.INFO, "Creating Test Database", {"scope":__name__, "database":pyswing.constants.pySwingDatabase})
        query = open('resources/pyswing.sql', 'r').read()
        connection = sqlite3.connect(pyswing.constants.pySwingDatabase)
        c = connection.cursor()
        c.executescript(query)
        connection.commit()
        c.close()
        connection.close()

        pretendDate = datetime.datetime(2015, 9, 1)
        with patch.object(Equity, '_getTodaysDate', return_value=pretendDate) as mock_method:

            self._equityCBA = Equity("WOR.AX")
            self._equityCBA.importData()

        indicatorSMA = IndicatorSMA(self._equityCBA.dataFrame(), "WOR.AX")
        indicatorSMA.updateIndicator()


    @classmethod
    def tearDownClass(self):
        deleteFile(pyswing.constants.pySwingDatabase)
        pass


    def test_CrossingRule(self):

        rule = CrossingRule("Indicator_SMA","SMA_5","Indicator_SMA","SMA_10")
        rule.evaluateRule("WOR.AX")

        dataPointMatch = rule._ruleData.ix['2015-08-28 00:00:00']
        self.assertEqual(dataPointMatch['Match'], 1)

        dataPointMatch = rule._ruleData.ix['2015-08-31 00:00:00']
        self.assertEqual(dataPointMatch['Match'], 0)


if __name__ == '__main__':
    unittest.main()