import datetime
import unittest
from unittest.mock import patch

from pyswing.utils.FileHelper import forceWorkingDirectory, deleteFile
from pyswing.utils.Logger import Logger
from pyswing.objects.indicators.indicatorADI import IndicatorADI
from pyswing.objects.equity import Equity
import pyswing.constants
import pyswing.database
from pyswing.CreateDatabase import createDatabase


class TestIndicatorADI(unittest.TestCase):

    @classmethod
    def setUpClass(self):

        Logger.pushLogData("unitTesting", __name__)
        forceWorkingDirectory()

        pyswing.database.overrideDatabase("output/TestIndicatorADI.db")
        pyswing.constants.pySwingStartDate = datetime.datetime(2014, 1, 1)

        deleteFile(pyswing.database.pySwingDatabase)

        args = "-n %s" % ("unitTesting")
        createDatabase(args.split())

        pretendDate = datetime.datetime(2015, 9, 1)
        with patch.object(Equity, '_getTodaysDate', return_value=pretendDate) as mock_method:

            self._equityCBA = Equity("CBA.AX")
            self._equityCBA.importData()

            self._equityTLS = Equity("TLS.AX")
            self._equityTLS.importData()

    @classmethod
    def tearDownClass(self):
        deleteFile(pyswing.database.pySwingDatabase)


    def test_IndicatorSMA(self):

        indicatorADI = IndicatorADI()

        dataPoint = indicatorADI._indicatorDataFrame.ix['2015-08-31 00:00:00']

        # These tests will fail if the Adjusted Close values change...
        self.assertAlmostEqual(dataPoint['ADI'], -2.00, 2)
        self.assertAlmostEqual(dataPoint['ADI_ROC'], 12.5, 2)
        self.assertAlmostEqual(dataPoint['ADI_EMA'], -1.16, 2)
        self.assertAlmostEqual(dataPoint['ADI_SUM'], -18.0, 2)


if __name__ == '__main__':
    unittest.main()
