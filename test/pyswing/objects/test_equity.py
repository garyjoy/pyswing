import datetime
import unittest
from unittest.mock import patch

from pyswing.utils.FileHelper import forceWorkingDirectory, deleteFile
from pyswing.utils.Logger import Logger
from pyswing.objects.equity import Equity
import pyswing.constants
import pyswing.database
from pyswing.CreateDatabase import createDatabase


class TestEquity(unittest.TestCase):

    @classmethod
    def setUpClass(self):
        Logger.pushLogData("unitTesting", __name__)
        forceWorkingDirectory()

        pyswing.database.overrideDatabase("output/TestEquity.db")
        pyswing.constants.pySwingStartDate = datetime.datetime(2015, 1, 1)

        deleteFile(pyswing.database.pySwingDatabase)

        args = "-n %s" % ("unitTesting")
        createDatabase(args.split())

        pretendDate = datetime.datetime(2015, 4, 1)
        with patch.object(Equity, '_getTodaysDate', return_value=pretendDate) as mock_method:

            self._equityCBA = Equity("CBA.AX")
            self._equityCBA.importData()

            self._equityTLS = Equity("TLS.AX")
            self._equityTLS.importData()

    @classmethod
    def tearDownClass(self):
        deleteFile(pyswing.database.pySwingDatabase)


    def test_importData(self):

        latestDate = self._equityCBA._getLatestDate()
        expectedLatestDate = datetime.datetime(2015, 4, 1)

        self.assertEquals(latestDate, expectedLatestDate)

        pretendDate = datetime.datetime(2015, 5, 1)
        with patch.object(Equity, '_getTodaysDate', return_value=pretendDate) as mock_method:

            self._equityCBA = Equity("CBA.AX")
            self._equityCBA.importData()

            self._equityTLS = Equity("TLS.AX")
            self._equityTLS.importData()

        latestDate = self._equityCBA._getLatestDate()
        expectedLatestDate = datetime.datetime(2015, 5, 1)

        self.assertEquals(latestDate, expectedLatestDate)


    def test_dataFrame(self):

        cbaData = self._equityCBA.dataFrame()

        # https://au.finance.yahoo.com/q/hp?s=CBA.AX&a=00&b=1&c=2015&d=02&e=6&f=2015&g=d
        # Date	        Open	High	Low	    Close	Volume	    Adj Close*
        # 2 Mar 2015	91.40	92.61	91.14	92.05	2,130,100	85.09

        dayData = cbaData.ix['2015-03-02 00:00:00']

        open = dayData.Open
        close = dayData.Close
        high = dayData.High
        low = dayData.Low
        volume = dayData.Volume

        # These tests will fail if the Adjusted Close values change...
        self.assertAlmostEqual(open, 84.49, 2) # 91.40 * (85.09 / 92.05)
        self.assertAlmostEqual(close, 85.09, 2)

        self.assertEqual(volume, 2130100)


if __name__ == '__main__':
    unittest.main()
