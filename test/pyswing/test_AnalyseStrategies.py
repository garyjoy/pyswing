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
from pyswing.AnalyseStrategies import analyseStrategies


class TestAnalyseStrategies(unittest.TestCase):

    @classmethod
    def setUpClass(self):
        Logger.pushLogData("unitTesting", __name__)
        forceWorkingDirectory()

        pyswing.globals.potentialRuleMatches = None
        pyswing.globals.equityCount = None

        pyswing.database.overrideDatabase("output/TestAnalyseStrategies.db")
        pyswing.constants.pySwingStartDate = datetime.datetime(2015, 1, 1)

        deleteFile(pyswing.database.pySwingDatabase)

        copyFile(pyswing.database.pySwingTestDatabase, pyswing.database.pySwingDatabase)

    @classmethod
    def tearDownClass(self):
        deleteFile(pyswing.database.pySwingDatabase)


    def test_AnalyseStrategies(self):

        args = "-n unitTest -m 1.0 -s test_EvaluateTwoRuleStrategies".split()
        evaluateTwoRuleStrategies(args)

        rowCount = self._countRows("TwoRuleStrategy")

        self.assertEqual(rowCount, 1974)

        args = "-n unitTest -N 1 -s v4.0 -t 5".split()
        evaluateThreeRuleStrategies(args)

        rowCount = self._countRows("ThreeRuleStrategy")

        self.assertEqual(rowCount, 71)

        args = "-n unitTest -r 4.0 -s v4.0 -t 3".split()
        analyseStrategies(args)

        rowCount = self._countRows("Strategy")

        self.assertEqual(rowCount, 1)


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


