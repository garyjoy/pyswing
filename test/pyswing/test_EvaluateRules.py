import datetime
import logging
import unittest
import sqlite3

from utils.FileHelper import forceWorkingDirectory, deleteFile
from utils.Logger import Logger
import pyswing.constants
from pyswing.ImportData import importData
from pyswing.UpdateIndicators import updateIndicators
from pyswing.EvaluateRules import evaluateRules
from unittest.mock import patch
from pyswing.objects.equity import Equity


class TestEvaluateRules(unittest.TestCase):

    @classmethod
    def setUpClass(self):
        Logger.pushLogData("unitTesting", __name__)
        forceWorkingDirectory()

        pyswing.constants.pySwingDatabase = "output/TestEvaluateRules.db"
        pyswing.constants.pySwingStartDate = datetime.datetime(2015, 1, 1)

        deleteFile(pyswing.constants.pySwingDatabase)

        Logger.log(logging.INFO, "Creating Test Database", {"scope":__name__, "database":pyswing.constants.pySwingDatabase})
        query = open('resources/pyswing.sql', 'r').read()
        connection = sqlite3.connect(pyswing.constants.pySwingDatabase)
        c = connection.cursor()
        c.executescript(query)
        connection.commit()
        c.close()
        connection.close()

    @classmethod
    def tearDownClass(self):
        deleteFile(pyswing.constants.pySwingDatabase)
        pass


    def test_UpdateIndicators(self):

        pretendDate = datetime.datetime(2015, 7, 1)
        with patch.object(Equity, '_getTodaysDate', return_value=pretendDate) as mock_method:
            args = "-n unitTest".split()
            importData(args)

        args = "-n unitTest".split()
        updateIndicators(args)

        args = "-n unitTest".split()
        evaluateRules(args)

        # TODO: Check that these numbers (i.e. 321) are correct...

        rowCount = self._countRows("Rule Indicator_ROC ROC_5 > 20")
        self.assertEqual(rowCount, 387)


    def _countRows(self, tableName):
        connection = sqlite3.connect(pyswing.constants.pySwingDatabase)
        query = "select count(1) from '%s'" % (tableName)
        cursor = connection.cursor()
        cursor.execute(query)
        rowCount = cursor.fetchone()[0]
        connection.close()
        return rowCount


if __name__ == '__main__':
    unittest.main()


