import unittest
import os

import pyswing.constants
from utils.FileHelper import forceWorkingDirectory, deleteFile
from utils.Logger import Logger
from pyswing.CreateDatabase import createDatabase


class TestCreateDatabase(unittest.TestCase):

    @classmethod
    def setUpClass(self):
        Logger.pushLogData("unitTesting", __name__)
        forceWorkingDirectory()
        pyswing.constants.pySwingDatabase = "output/TestCreateDatabase.db"
        deleteFile(pyswing.constants.pySwingDatabase)

    @classmethod
    def tearDownClass(self):
        deleteFile(pyswing.constants.pySwingDatabase)


    def test_CreateDatabase(self):

        args = "-D %s -s %s" % (pyswing.constants.pySwingDatabase, pyswing.constants.pySwingDatabaseScript)
        createDatabase(args.split())

        self.assertTrue(os.path.isfile(pyswing.constants.pySwingDatabase))


if __name__ == '__main__':
    unittest.main()


