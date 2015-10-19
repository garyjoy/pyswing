import datetime
import unittest
from unittest.mock import patch

from utils.FileHelper import forceWorkingDirectory, deleteFile
from utils.Logger import Logger
from pyswing.objects.indicators.indicatorAROON import IndicatorAROON
from pyswing.objects.equity import Equity
import pyswing.constants
from pyswing.CreateDatabase import createDatabase


class TestIndicatorADX(unittest.TestCase):

    @classmethod
    def setUpClass(self):

        Logger.pushLogData("unitTesting", __name__)
        forceWorkingDirectory()

        pyswing.constants.pySwingDatabase = "output/TestIndicatorAROON.db"
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


    def test_IndicatorADX(self):

        cbaIndicatorAROON = IndicatorAROON(self._equityCBA.dataFrame(), "CBA.AX")
        cbaIndicatorAROON.updateIndicator()

        dataPoint = cbaIndicatorAROON._indicatorDataFrame.ix['2015-08-31 00:00:00']

        self.assertEqual(dataPoint['Code'], "CBA.AX")
        self.assertAlmostEqual(dataPoint['aroondown'], 71.43, 2)
        self.assertAlmostEqual(dataPoint['aroonup'], 35.71, 2)


if __name__ == '__main__':
    unittest.main()
