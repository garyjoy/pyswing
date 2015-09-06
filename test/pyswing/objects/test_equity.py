import datetime
import logging
import unittest
import sqlite3

from unittest.mock import patch
from utils.FileHelper import forceWorkingDirectory, deleteFile
from utils.Logger import Logger
from pyswing.objects.equity import Equity
import pyswing.constants


class TestEquity(unittest.TestCase):

    @classmethod
    def setUpClass(self):
        Logger.pushLogData("unitTesting", __name__)
        forceWorkingDirectory()

        deleteFile("output/TestEquity.db")

        pyswing.constants.pySwingDatabase = "output/TestEquity.db"
        pyswing.constants.pySwingStartDate = datetime.datetime(2015, 1, 1)

        Logger.log(logging.INFO, "Creating Test Database", {"scope":__name__, "database":pyswing.constants.pySwingDatabase})
        query = open('resources/pyswing.sql', 'r').read()
        connection = sqlite3.connect(pyswing.constants.pySwingDatabase)
        c = connection.cursor()
        c.executescript(query)
        connection.commit()
        c.close()
        connection.close()

        pretendDate = datetime.datetime(2015, 4, 1)
        with patch.object(Equity, '_getTodaysDate', return_value=pretendDate) as mock_method:

            self._equityCBA = Equity("CBA.AX")
            self._equityCBA.importData()

            self._equityTLS = Equity("TLS.AX")
            self._equityTLS.importData()

    @classmethod
    def tearDownClass(self):
        deleteFile("output/TestEquity.db")
        pass


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
        # 2 Mar 2015	91.40	92.61	91.14	92.05	2,130,100	88.46

        dayData = cbaData.ix['2015-03-02 00:00:00']

        open = dayData.Open
        close = dayData.Close
        high = dayData.High
        low = dayData.Low
        volume = dayData.Volume

        self.assertAlmostEqual(open, 87.84, 2) # 91.40 * (88.46 / 92.05)
        self.assertAlmostEqual(close, 88.46, 2)

        self.assertEqual(int.from_bytes(volume, byteorder='little'), 2130100)


if __name__ == '__main__':
    unittest.main()
