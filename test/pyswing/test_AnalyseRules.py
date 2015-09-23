import datetime
import unittest
import sqlite3
from unittest.mock import patch

from utils.FileHelper import forceWorkingDirectory, deleteFile
from utils.Logger import Logger
import pyswing.constants
import pyswing.globals
from pyswing.ImportData import importData
from pyswing.UpdateIndicators import updateIndicators
from pyswing.EvaluateRules import evaluateRules
from pyswing.AnalyseRules import analyseRules
from pyswing.objects.equity import Equity
from pyswing.CreateDatabase import createDatabase


class TestAnalyseRules(unittest.TestCase):

    @classmethod
    def setUpClass(self):
        Logger.pushLogData("unitTesting", __name__)
        forceWorkingDirectory()

        pyswing.globals.potentialRuleMatches = None
        pyswing.globals.equityCount = None

        pyswing.constants.pySwingDatabase = "output/TestAnalyseRules.db"
        pyswing.constants.pySwingStartDate = datetime.datetime(2015, 1, 1)

        deleteFile(pyswing.constants.pySwingDatabase)

        args = "-D %s -s %s" % (pyswing.constants.pySwingDatabase, pyswing.constants.pySwingDatabaseScript)
        createDatabase(args.split())

    @classmethod
    def tearDownClass(self):
        deleteFile(pyswing.constants.pySwingDatabase)


    def test_AnalyseRules(self):

        pretendDate = datetime.datetime(2015, 7, 1)
        with patch.object(Equity, '_getTodaysDate', return_value=pretendDate) as mock_method:
            args = "-n unitTest".split()
            importData(args)

        args = "-n unitTest".split()
        updateIndicators(args)

        args = "-n unitTest".split()
        evaluateRules(args)

        args = "-n unitTest".split()
        analyseRules(args)

        rowCount = self._countRows("Rules")

        self.assertEqual(rowCount, 84)


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


