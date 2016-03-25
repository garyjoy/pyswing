import datetime
import unittest
from unittest.mock import patch

from pyswing.utils.FileHelper import forceWorkingDirectory, deleteFile
from pyswing.utils.Logger import Logger
from pyswing.objects.exitValuesYesterday import ExitValuesYesterday
from pyswing.objects.equity import Equity
import pyswing.constants
import pyswing.database
from pyswing.CreateDatabase import createDatabase


class TestExitValuesYesterday(unittest.TestCase):

    @classmethod
    def setUpClass(self):

        Logger.pushLogData("unitTesting", __name__)
        forceWorkingDirectory()

        pyswing.database.overrideDatabase("output/TestExitValuesYesterday.db")
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

        exitValues = ExitValuesYesterday("WOR.AX", 0.02, 3)
        exitValues.calculateExitValues()

        # Gapped Above Limit (10.308780) on Day 2 (Open=9 and Close=10.358178)
        dataPointBuyWin = exitValues._buyExitValueDataFrame.ix['2015-06-30 00:00:00']
        self.assertAlmostEqual(dataPointBuyWin['ExitValue'], 6.508, 3)

        # Gapped Below Stop (9.453822) on Day 3 (Open=9.580096 and Close=9.453336)
        dataPointBuyLose = exitValues._buyExitValueDataFrame.ix['2015-07-17 00:00:00']
        self.assertAlmostEqual(dataPointBuyLose['ExitValue'], -1.323, 3)

        # Passed Stop (9.803891) on Day 3 (Open=10.212030 and Close=9.803891)
        dataPointSellWin = exitValues._sellExitValueDataFrame.ix['2015-06-26 00:00:00']
        self.assertAlmostEqual(dataPointSellWin['ExitValue'], 3.997, 3)

        # Gapped Above Stop (9.628255) on Day 2 (Open=9.443470 and Close=9.745466)
        dataPointSellLose = exitValues._sellExitValueDataFrame.ix['2015-07-09 00:00:00']
        self.assertAlmostEqual(dataPointSellLose['ExitValue'], -3.198, 3)


if __name__ == '__main__':
    unittest.main()
