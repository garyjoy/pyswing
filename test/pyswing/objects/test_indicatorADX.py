import datetime
import unittest
from unittest.mock import patch

from utils.FileHelper import forceWorkingDirectory, deleteFile
from utils.Logger import Logger
from pyswing.objects.indicatorADX import IndicatorADX
from pyswing.objects.equity import Equity
import pyswing.constants
from pyswing.CreateDatabase import createDatabase


class TestIndicatorADX(unittest.TestCase):

    @classmethod
    def setUpClass(self):

        Logger.pushLogData("unitTesting", __name__)
        forceWorkingDirectory()

        pyswing.constants.pySwingDatabase = "output/TestIndicatorADX.db"
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

        cbaIndicatorADX = IndicatorADX(self._equityCBA.dataFrame(), "CBA.AX")
        cbaIndicatorADX.updateIndicator()

        dataPoint = cbaIndicatorADX._indicatorDataFrame.ix['2015-08-31 00:00:00']

        self.assertEqual(dataPoint['Code'], "CBA.AX")
        self.assertAlmostEqual(dataPoint['ADX'], 34.09, 2)
        self.assertAlmostEqual(dataPoint['ADX_ROC'], 17.02, 2)


if __name__ == '__main__':
    unittest.main()
