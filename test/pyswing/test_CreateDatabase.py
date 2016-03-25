import unittest
import os

import pyswing.constants
import pyswing.database
from pyswing.utils.FileHelper import forceWorkingDirectory, deleteFile
from pyswing.utils.Logger import Logger
from pyswing.CreateDatabase import createDatabase


class TestCreateDatabase(unittest.TestCase):

    @classmethod
    def setUpClass(self):
        Logger.pushLogData("unitTesting", __name__)
        forceWorkingDirectory()


    def test_CreateTestDatabase(self):

        pyswing.database.overrideDatabase("output/TestCreateDatabase.db")
        deleteFile(pyswing.database.pySwingDatabase)

        args = "-n %s" % ("unitTesting")
        createDatabase(args.split())

        self.assertTrue(os.path.isfile(pyswing.database.pySwingDatabase))

        deleteFile(pyswing.database.pySwingDatabase)


    def test_CreateDatabase(self):

        pyswing.database.overrideDatabase(pyswing.database.pySwingTestDatabase)

        originalSize = os.path.getsize(pyswing.database.pySwingDatabase)

        args = "-n %s" % ("unitTesting")
        createDatabase(args.split())

        subsequentSize = os.path.getsize(pyswing.database.pySwingDatabase)

        self.assertEqual(originalSize, subsequentSize)



if __name__ == '__main__':
    unittest.main()


