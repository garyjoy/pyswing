import datetime
import unittest
import sqlite3

from pyswing.utils.FileHelper import forceWorkingDirectory, deleteFile, copyFile
from pyswing.utils.Logger import Logger
import pyswing.constants
import pyswing.database
import pyswing.globals
from pyswing.EvaluateTwoRuleStrategies import evaluateTwoRuleStrategies
from pyswing.EvaluateThreeRuleStrategies import evaluateThreeRuleStrategies


class TestEvaluateThreeRuleStrategies(unittest.TestCase):

    @classmethod
    def setUpClass(self):
        Logger.pushLogData("unitTesting", __name__)
        forceWorkingDirectory()

        pyswing.globals.potentialRuleMatches = None
        pyswing.globals.equityCount = None

        pyswing.database.overrideDatabase("output/TestEvaluateThreeRuleStrategies.db")
        pyswing.constants.pySwingStartDate = datetime.datetime(2015, 1, 1)

        deleteFile(pyswing.database.pySwingDatabase)

        copyFile(pyswing.database.pySwingTestDatabase, pyswing.database.pySwingDatabase)

    @classmethod
    def tearDownClass(self):
        deleteFile(pyswing.database.pySwingDatabase)


    def test_EvaluateThreeRuleStrategies(self):

        args = "-n unitTest -m 0.1 -s test_EvaluateTwoRuleStrategies".split()
        evaluateTwoRuleStrategies(args)

        rowCount = self._countRows("TwoRuleStrategy")

        self.assertEqual(rowCount, 19488)

        args = "-n unitTest -N 1 -s v4.0 -t 5".split()
        evaluateThreeRuleStrategies(args)

        rowCount = self._countRows("ThreeRuleStrategy")

        self.assertEqual(rowCount, 53)


    def _countRows(self, tableName):
        connection = sqlite3.connect(pyswing.database.pySwingDatabase)
        query = "select count(1) from '%s'" % (tableName)
        cursor = connection.cursor()
        cursor.execute(query)
        rowCount = cursor.fetchone()[0]
        connection.close()
        return rowCount


if __name__ == '__main__':
    unittest.main()


