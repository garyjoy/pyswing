import datetime
import unittest
from unittest.mock import patch

from utils.FileHelper import forceWorkingDirectory, deleteFile
from utils.Logger import Logger
from pyswing.objects.indicatorMACD import IndicatorMACD
from pyswing.objects.equity import Equity
import pyswing.constants
from pyswing.CreateDatabase import createDatabase


class TestIndicatorMACD(unittest.TestCase):

    @classmethod
    def setUpClass(self):

        Logger.pushLogData("unitTesting", __name__)
        forceWorkingDirectory()

        pyswing.constants.pySwingDatabase = "output/TestIndicatorMACD.db"
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


    def test_IndicatorMACD(self):

        cbaIndicatorMACD = IndicatorMACD(self._equityCBA.dataFrame(), "CBA.AX")
        cbaIndicatorMACD.updateIndicator()

        dataPoint = cbaIndicatorMACD._indicatorDataFrame.ix['2015-08-31 00:00:00']

        self.assertAlmostEqual(dataPoint['macd'], -1.66, 2)
        self.assertAlmostEqual(dataPoint['macdsignal'], -1.56, 2)
        self.assertAlmostEqual(dataPoint['macdhist'], -0.09, 2)


if __name__ == '__main__':
    unittest.main()
