import unittest
import os
import pwd

from pyswing.utils.FileHelper import *
from pyswing.utils.Logger import Logger

import pyswing.database


class TestDatabase(unittest.TestCase):

    @classmethod
    def setUpClass(self):

        Logger.pushLogData("unitTesting", __name__)

        forceWorkingDirectory()

        pyswing.database.pySwingDatabase = None
        pyswing.database.pySwingDatabaseInitialised = False
        pyswing.database.pySwingDatabaseOverridden = False

    def tearDown(self):
        pass


    def test_initialiseDatabase(self):

        self.assertIsNone(pyswing.database.pySwingDatabase, "Check Default Database (%s)" % pyswing.database.pySwingDatabase)

        pyswing.database.initialiseDatabase("test_initialiseDatabase")

        homeDirectory = pwd.getpwuid(os.getuid()).pw_dir

        self.assertTrue(homeDirectory in pyswing.database.pySwingDatabase)
        self.assertTrue("pyswing_test_initialiseDatabase.db" in pyswing.database.pySwingDatabase)

        pyswing.database.initialiseDatabase("test_somethingElse")

        self.assertTrue(homeDirectory in pyswing.database.pySwingDatabase)
        self.assertFalse("pyswing_test_initialiseDatabase.db" in pyswing.database.pySwingDatabase)
        self.assertTrue("pyswing_test_somethingElse.db" in pyswing.database.pySwingDatabase)

        # Restore the default values (doesn't work in tearDown())...
        pyswing.database.pySwingDatabase = None
        pyswing.database.pySwingDatabaseInitialised = False
        pyswing.database.pySwingDatabaseOverridden = False


    def test_overrideDatabase(self):

        self.assertIsNone(pyswing.database.pySwingDatabase, "Check Default Database (%s)" % pyswing.database.pySwingDatabase)

        pyswing.database.overrideDatabase("test_overrideDatabase")

        self.assertEqual("test_overrideDatabase", pyswing.database.pySwingDatabase)

        pyswing.database.initialiseDatabase("test_somethingElse")

        self.assertEqual("test_overrideDatabase", pyswing.database.pySwingDatabase)

        # Restore the default values (doesn't work in tearDown())...
        pyswing.database.pySwingDatabase = None
        pyswing.database.pySwingDatabaseInitialised = False
        pyswing.database.pySwingDatabaseOverridden = False


if __name__ == "__main__":
    unittest.main()
