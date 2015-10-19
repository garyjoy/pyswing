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


    def test_CreateTestDatabase(self):

        pyswing.constants.pySwingDatabase = "output/TestCreateDatabase.db"
        deleteFile(pyswing.constants.pySwingDatabase)

        args = "-D %s -s %s" % (pyswing.constants.pySwingDatabase, pyswing.constants.pySwingDatabaseScript)
        createDatabase(args.split())

        self.assertTrue(os.path.isfile(pyswing.constants.pySwingDatabase))

        deleteFile(pyswing.constants.pySwingDatabase)


    def test_CreateDatabase(self):

        pyswing.constants.pySwingDatabase = pyswing.constants.pySwingTestDatabase

        originalSize = os.path.getsize(pyswing.constants.pySwingDatabase)

        createDatabase([])

        subsequentSize = os.path.getsize(pyswing.constants.pySwingDatabase)

        self.assertEqual(originalSize, subsequentSize)



if __name__ == '__main__':
    unittest.main()


