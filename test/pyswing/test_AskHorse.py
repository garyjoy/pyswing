import datetime
import unittest
import sqlite3
from unittest.mock import patch

from pyswing.utils.FileHelper import forceWorkingDirectory, deleteFile, copyFile
from pyswing.utils.Logger import Logger
import pyswing.constants
import pyswing.database
import pyswing.globals
from pyswing.AskHorse import askHorse


class TestAskHorse(unittest.TestCase):

    @classmethod
    def setUpClass(self):
        Logger.pushLogData("unitTesting", __name__)
        forceWorkingDirectory()

        pyswing.globals.potentialRuleMatches = None
        pyswing.globals.equityCount = None

        pyswing.database.overrideDatabase("output/TestAskHorse.db")
        pyswing.constants.pySwingStartDate = datetime.datetime(2015, 1, 1)

        deleteFile(pyswing.database.pySwingDatabase)

        copyFile(pyswing.database.pySwingTestDatabase, pyswing.database.pySwingDatabase)

    @classmethod
    def tearDownClass(self):
        deleteFile(pyswing.database.pySwingDatabase)


    @patch("pyswing.AskHorse.sendEmail")
    def test_AskHorse(self, sendEmail):

        self._createStrategy()

        args = "-n unitTest".split()
        askHorse(args)

        self.assertTrue(sendEmail.called)
        self.assertEqual(len(sendEmail.call_args[0][0]), 3)


    def _countRows(self, tableName):
        connection = sqlite3.connect(pyswing.database.pySwingDatabase)
        query = "select count(1) from '%s'" % (tableName)
        cursor = connection.cursor()
        cursor.execute(query)
        rowCount = cursor.fetchone()[0]
        connection.close()
        return rowCount


    def _createStrategy(self):

        connection = sqlite3.connect(pyswing.database.pySwingDatabase)
        query = "insert into ActiveStrategy (strategy,rule1,rule2,rule3,exit,type,meanResultPerTrade,medianResultPerTrade,totalProfit,numberOfTrades,sharpeRatio,maximumDrawdown,active) values ('v4.0', 'Rule Indicator_RSI RSI > 20', 'Rule Indicator_RSI RSI > 20', 'Rule Indicator_RSI RSI > 20', 'Exit TrailingStop3.0 RiskRatio2', 'Buy', 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1)"
        cursor = connection.cursor()
        cursor.execute(query)
        connection.commit()
        connection.close()


if __name__ == '__main__':
    unittest.main()


