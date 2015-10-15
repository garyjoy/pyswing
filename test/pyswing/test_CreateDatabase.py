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

        # TODO:  Hard-coding the User is not good...
        # "/Users/garyjoy/pyswing.db" will not work on my Macbook Air (it's just "Gary")

        pyswing.constants.pySwingDatabase = "/Users/garyjoy/pyswing.db"

        if not os.path.exists(pyswing.constants.pySwingDatabase):
            pyswing.constants.pySwingDatabase = "/Users/gary/pyswing.db"

        if not os.path.exists(pyswing.constants.pySwingDatabase):
            self.assertTrue(os.path.exists(pyswing.constants.pySwingDatabase))

        with self.assertRaises(SystemExit) as myThing:
            createDatabase([])

        self.assertEqual(myThing.exception.code, 1)


if __name__ == '__main__':
    unittest.main()


