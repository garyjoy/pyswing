import unittest

from pyswing.utils.FileHelper import forceWorkingDirectory
from pyswing.utils.Logger import Logger
import pyswing.constants
import pyswing.database
import pyswing.globals


class TestGenerateHistoricMatchData(unittest.TestCase):

    @classmethod
    def setUpClass(self):
        Logger.pushLogData("unitTesting", __name__)
        forceWorkingDirectory()

        pyswing.globals.potentialRuleMatches = None
        pyswing.globals.equityCount = None

        # pyswing.database.overrideDatabase("output/TestGenerateHistoricMatchData.db")
        # pyswing.constants.pySwingStartDate = datetime.datetime(2015, 1, 1)
        #
        # deleteFile(pyswing.database.pySwingDatabase)
        #
        # copyFile(pyswing.database.pySwingTestDatabase, pyswing.database.pySwingDatabase)

    @classmethod
    def tearDownClass(self):
        # deleteFile(pyswing.database.pySwingDatabase)
        pass


    def test_GenerateHistoricMatchData(self):

        # TODO:  Make this into a Unit Test...

        # args = "-n unitTest".split()
        # args = "-n asx".split()
        # generateHistoricMatchData(args)

        pass




if __name__ == '__main__':
    unittest.main()


