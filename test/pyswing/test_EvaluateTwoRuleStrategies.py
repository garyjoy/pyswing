import datetime
import unittest
import sqlite3
from unittest.mock import patch

from utils.FileHelper import forceWorkingDirectory, deleteFile, copyFile
from utils.Logger import Logger
import pyswing.constants
import pyswing.globals
from pyswing.EvaluateTwoRuleStrategies import evaluateTwoRuleStrategies


class TestEvaluateTwoRuleStrategies(unittest.TestCase):

    @classmethod
    def setUpClass(self):
        Logger.pushLogData("unitTesting", __name__)
        forceWorkingDirectory()

        pyswing.globals.potentialRuleMatches = None
        pyswing.globals.equityCount = None

        pyswing.constants.pySwingDatabase = "output/TestEvaluateTwoRuleStrategies.db"
        pyswing.constants.pySwingStartDate = datetime.datetime(2015, 1, 1)

        deleteFile(pyswing.constants.pySwingDatabase)

        copyFile("resources/TestDatabase.db", pyswing.constants.pySwingDatabase)

        # TestDatabase.db *should* be equivalent to running the following...

        # args = "-D %s -s %s" % (pyswing.constants.pySwingDatabase, pyswing.constants.pySwingDatabaseScript)
        # createDatabase(args.split())
        #
        # pretendDate = datetime.datetime(2015, 7, 1)
        # with patch.object(Equity, '_getTodaysDate', return_value=pretendDate) as mock_method:
        #     args = "-n unitTest".split()
        #     importData(args)
        #
        # args = "-n unitTest".split()
        # updateIndicators(args)
        #
        # args = "-n unitTest".split()
        # evaluateRules(args)
        #
        # args = "-n unitTest".split()
        # analyseRules(args)
        #
        # args = "-n unitTest".split()
        # calculateExitValues(args)


    @classmethod
    def tearDownClass(self):
        deleteFile(pyswing.constants.pySwingDatabase)


    def test_EvaluateTwoRuleStrategies(self):

        args = "-n unitTest".split()
        evaluateTwoRuleStrategies(args)

        rowCount = self._countRows("TwoRuleStrategy")

        self.assertEqual(rowCount, 124)


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


