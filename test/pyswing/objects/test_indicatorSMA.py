import datetime
import unittest
from unittest.mock import patch

from utils.FileHelper import forceWorkingDirectory, deleteFile
from utils.Logger import Logger
from pyswing.objects.indicatorSMA import IndicatorSMA
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

        self.assertAlmostEqual(dataPoint['SMA_5'], 75.82, 2)
        self.assertAlmostEqual(dataPoint['SMA_10'], 75.85, 2)
        self.assertAlmostEqual(dataPoint['SMA_15'], 76.70, 2)
        self.assertAlmostEqual(dataPoint['SMA_20'], 77.76, 2)
        self.assertAlmostEqual(dataPoint['SMA_50'], 80.80, 2)
        self.assertAlmostEqual(dataPoint['SMA_200'], 82.10, 2)


if __name__ == '__main__':
    unittest.main()
