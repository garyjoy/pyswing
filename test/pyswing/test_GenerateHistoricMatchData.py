import datetime
import unittest
import sqlite3

from pyswing.utils.FileHelper import forceWorkingDirectory, deleteFile, copyFile
from pyswing.utils.Logger import Logger
import pyswing.constants
import pyswing.globals
from pyswing.GenerateHistoricMatchData import generateHistoricMatchData


class TestGenerateHistoricMatchData(unittest.TestCase):

    @classmethod
    def setUpClass(self):
        Logger.pushLogData("unitTesting", __name__)
        forceWorkingDirectory()

        pyswing.globals.potentialRuleMatches = None
        pyswing.globals.equityCount = None

        # pyswing.constants.pySwingDatabase = "output/TestGenerateHistoricMatchData.db"
        # pyswing.constants.pySwingStartDate = datetime.datetime(2015, 1, 1)
        #
        # deleteFile(pyswing.constants.pySwingDatabase)
        #
        # copyFile(pyswing.constants.pySwingTestDatabase, pyswing.constants.pySwingDatabase)

    @classmethod
    def tearDownClass(self):
        # deleteFile(pyswing.constants.pySwingDatabase)
        pass


    def test_GenerateHistoricMatchData(self):

        # TODO:  Make this into a Unit Test...

        # args = "-n unitTest".split()
        # args = "-n asx".split()
        # generateHistoricMatchData(args)

        pass




if __name__ == '__main__':
    unittest.main()


