import datetime
import unittest
from unittest.mock import patch

from pyswing.utils.FileHelper import forceWorkingDirectory, deleteFile
from pyswing.utils.Logger import Logger
from pyswing.objects.indicators.indicatorSTOCH import IndicatorSTOCH
from pyswing.objects.equity import Equity
import pyswing.constants
from pyswing.CreateDatabase import createDatabase


class TestIndicatorSTOCH(unittest.TestCase):

    @classmethod
    def setUpClass(self):

        Logger.pushLogData("unitTesting", __name__)
        forceWorkingDirectory()

        pyswing.constants.pySwingDatabase = "output/TestIndicatorSTOCH.db"
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


    def test_IndicatorSTOCH(self):

        cbaIndicatorSTOCH = IndicatorSTOCH(self._equityCBA.dataFrame(), "CBA.AX")
        cbaIndicatorSTOCH.updateIndicator()

        dataPoint = cbaIndicatorSTOCH._indicatorDataFrame.ix['2015-08-31 00:00:00']

        self.assertAlmostEqual(dataPoint['slowk'], 74.86, 2)
        self.assertAlmostEqual(dataPoint['slowd'], 73.89, 2)
        self.assertAlmostEqual(dataPoint['STOCH_K_ROC'], 507.42, 2)
        self.assertAlmostEqual(dataPoint['STOCH_D_ROC'], 253.54, 2)


if __name__ == '__main__':
    unittest.main()
