import datetime
import unittest
from unittest.mock import patch

from pyswing.utils.FileHelper import forceWorkingDirectory, deleteFile
from pyswing.utils.Logger import Logger
from pyswing.objects.exitValuesTrailingStop import ExitValuesTrailingStop
from pyswing.objects.equity import Equity
from pyswing.objects.exitValues import getExitStrategies
import pyswing.constants
import pyswing.database
from pyswing.CreateDatabase import createDatabase


class TestExitValuesTrailingStop(unittest.TestCase):

    @classmethod
    def setUpClass(self):

        Logger.pushLogData("unitTesting", __name__)
        forceWorkingDirectory()

        pyswing.database.overrideDatabase("output/TestExitValuesTrailingStop.db")
        pyswing.constants.pySwingStartDate = datetime.datetime(2013, 1, 1)

        deleteFile(pyswing.database.pySwingDatabase)

        args = "-n %s" % ("unitTesting")
        createDatabase(args.split())

        pretendDate = datetime.datetime(2015, 9, 1)
        with patch.object(Equity, '_getTodaysDate', return_value=pretendDate) as mock_method:

            self._equityWOR = Equity("WOR.AX")
            self._equityWOR.importData()


    @classmethod
    def tearDownClass(self):
        deleteFile(pyswing.database.pySwingDatabase)


    def test_ExitValues(self):

        exitValues = ExitValuesTrailingStop("WOR.AX", 0.03, 2)
        exitValues.calculateExitValues()

        dataPointBuyWin = exitValues._buyExitValueDataFrame.ix['2015-07-02 00:00:00']
        self.assertAlmostEqual(dataPointBuyWin['ExitValue'], 1.581, 3)

        dataPointBuyLose = exitValues._buyExitValueDataFrame.ix['2015-07-13 00:00:00']
        self.assertAlmostEqual(dataPointBuyLose['ExitValue'], -1.741, 3)

        dataPointSellWin = exitValues._sellExitValueDataFrame.ix['2015-07-03 00:00:00']
        self.assertAlmostEqual(dataPointSellWin['ExitValue'], 6.000, 3)

        dataPointSellLose = exitValues._sellExitValueDataFrame.ix['2015-07-14 00:00:00']
        self.assertAlmostEqual(dataPointSellLose['ExitValue'], -4.832, 3)

        strategies = getExitStrategies()
        self.assertTrue(len(strategies) == 1)


if __name__ == '__main__':
    unittest.main()
