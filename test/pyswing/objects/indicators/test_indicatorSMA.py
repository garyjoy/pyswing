import datetime
import unittest
from unittest.mock import patch

from pyswing.utils.FileHelper import forceWorkingDirectory, deleteFile
from pyswing.utils.Logger import Logger
from pyswing.objects.indicators.indicatorSMA import IndicatorSMA
from pyswing.objects.equity import Equity
import pyswing.constants
from pyswing.CreateDatabase import createDatabase


class TestIndicatorSMA(unittest.TestCase):

    @classmethod
    def setUpClass(self):

        Logger.pushLogData("unitTesting", __name__)
        forceWorkingDirectory()

        pyswing.constants.pySwingDatabase = "output/TestIndicatorSMA.db"
        pyswing.constants.pySwingStartDate = datetime.datetime(2014, 1, 1)

        deleteFile(pyswing.constants.pySwingDatabase)

        args = "-D %s -s %s" % (pyswing.constants.pySwingDatabase, pyswing.constants.pySwingDatabaseScript)
        createDatabase(args.split())

        pretendDate = datetime.datetime(2015, 9, 1)
        with patch.object(Equity, '_getTodaysDate', return_value=pretendDate) as mock_method:

            self._equityCBA = Equity("CBA.AX")
            self._equityCBA.importData()

    @classmethod
    def tearDownClass(self):
        deleteFile(pyswing.constants.pySwingDatabase)


    def test_IndicatorSMA(self):

        cbaIndicatorSMA = IndicatorSMA(self._equityCBA.dataFrame(), "CBA.AX")

        dataPoint = cbaIndicatorSMA._indicatorDataFrame.ix['2015-08-31 00:00:00']

        # These tests will fail if the Adjusted Close values change...
        self.assertAlmostEqual(dataPoint['SMA_5'], 72.93, 2)
        self.assertAlmostEqual(dataPoint['SMA_10'], 72.96, 2)
        self.assertAlmostEqual(dataPoint['SMA_15'], 73.78, 2)
        self.assertAlmostEqual(dataPoint['SMA_20'], 74.80, 2)
        self.assertAlmostEqual(dataPoint['SMA_50'], 77.72, 2)
        self.assertAlmostEqual(dataPoint['SMA_200'], 78.98, 2)


if __name__ == '__main__':
    unittest.main()
