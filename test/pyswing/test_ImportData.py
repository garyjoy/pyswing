import datetime
import unittest
import sqlite3
from unittest.mock import patch

from pyswing.utils.FileHelper import forceWorkingDirectory, deleteFile
from pyswing.utils.Logger import Logger
import pyswing.constants
import pyswing.database
from pyswing.ImportData import importData
from pyswing.objects.equity import Equity
from pyswing.CreateDatabase import createDatabase


class TestImportData(unittest.TestCase):

    @classmethod
    def setUpClass(self):
        Logger.pushLogData("unitTesting", __name__)
        forceWorkingDirectory()

        pyswing.database.overrideDatabase("output/TestImportData.db")
        pyswing.constants.pySwingStartDate = datetime.datetime(2015, 1, 1)

        deleteFile(pyswing.database.pySwingDatabase)

        args = "-n %s" % ("unitTesting")
        createDatabase(args.split())

    @classmethod
    def tearDownClass(self):
        deleteFile(pyswing.database.pySwingDatabase)


    def test_ImportData(self):

        pretendDate = datetime.datetime(2015, 5, 1)
        with patch.object(Equity, '_getTodaysDate', return_value=pretendDate) as mock_method:
            args = "-n unitTest".split()
            importData(args)

        rowCount = self._countEquityRows()
        self.assertEqual(rowCount, 261) # 87 * 3

        pretendDate = datetime.datetime(2015, 6, 1)
        with patch.object(Equity, '_getTodaysDate', return_value=pretendDate) as mock_method:
            args = "-n unitTest".split()
            importData(args)

        rowCount = self._countEquityRows()
        self.assertEqual(rowCount, 324) # 108 * 3


    def _countEquityRows(self):
        connection = sqlite3.connect(pyswing.database.pySwingDatabase)
        query = "select count(1) from Equities"
        cursor = connection.cursor()
        cursor.execute(query)
        rowCount = cursor.fetchone()[0]
        connection.close()
        return rowCount


if __name__ == '__main__':
    unittest.main()


