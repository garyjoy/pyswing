import datetime
import unittest
import sqlite3
from unittest.mock import patch

from pyswing.utils.FileHelper import forceWorkingDirectory, deleteFile
from pyswing.utils.Logger import Logger
import pyswing.constants
from pyswing.ImportData import importData
from pyswing.UpdateIndicators import updateIndicators
from pyswing.EvaluateRules import evaluateRules
from pyswing.objects.equity import Equity
from pyswing.CreateDatabase import createDatabase


class TestEvaluateRules(unittest.TestCase):

    @classmethod
    def setUpClass(self):
        Logger.pushLogData("unitTesting", __name__)
        forceWorkingDirectory()

        pyswing.constants.pySwingDatabase = "output/TestEvaluateRules.db"

        pyswing.constants.pySwingStartDate = datetime.datetime(2015, 1, 1)

        deleteFile(pyswing.constants.pySwingDatabase)

        args = "-D %s -s %s" % (pyswing.constants.pySwingDatabase, pyswing.constants.pySwingDatabaseScript)
        createDatabase(args.split())

    @classmethod
    def tearDownClass(self):
        deleteFile(pyswing.constants.pySwingDatabase)

    def test_EvaluateRules(self):

        pretendDate = datetime.datetime(2015, 7, 1)
        with patch.object(Equity, '_getTodaysDate', return_value=pretendDate) as mock_method:
            args = "-n unitTest".split()
            importData(args)

        args = "-n unitTest".split()
        updateIndicators(args)

        args = "-n unitTest".split()
        evaluateRules(args)

        rowCount = self._countRows("Rule Indicator_ROC ROC_5 > 20")
        anotherRowCount = self._countRows("Rule Indicator_SMA SMA_10 Cross Indicator_SMA SMA_200")

        self.assertEqual(rowCount, 387)
        self.assertEqual(rowCount, anotherRowCount)


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


