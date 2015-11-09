import datetime
import unittest
import sqlite3

from pyswing.utils.FileHelper import forceWorkingDirectory, deleteFile, copyFile
from pyswing.utils.Logger import Logger
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

        copyFile(pyswing.constants.pySwingTestDatabase, pyswing.constants.pySwingDatabase)

    @classmethod
    def tearDownClass(self):
        deleteFile(pyswing.constants.pySwingDatabase)


    def test_EvaluateTwoRuleStrategies(self):

        # TODO:  This takes a few minutes to run. Can I speed it up somehow..?
        args = "-n unitTest -m 0.1 -s test_EvaluateTwoRuleStrategies".split()
        evaluateTwoRuleStrategies(args)

        rowCount = self._countRows("TwoRuleStrategy")

        self.assertEqual(rowCount, 9744)


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


