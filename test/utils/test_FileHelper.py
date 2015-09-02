import unittest

from utils.Logger import Logger
from utils.FileHelper import *


class TestFileHelper(unittest.TestCase):

    @classmethod
    def setUpClass(self):

        Logger.pushLogData("unitTesting", __name__)

        forceWorkingDirectory()


    def test_ensureDirectoryExists_and_deleteDirectory(self):

        relativeDirectoryPath = "output/TestFileHelper"

        ensureDirectoryExists(relativeDirectoryPath)

        self.assertTrue(os.path.exists(relativeDirectoryPath))

        deleteDirectory(relativeDirectoryPath)

        self.assertFalse(os.path.exists(relativeDirectoryPath))

    def test_forceWorkingDirectory(self):

        forceWorkingDirectory()
        newWorkingDirectory = "test/resources/"
        os.chdir(newWorkingDirectory)
        forceWorkingDirectory()
        self.assertTrue(os.path.exists("test"), "test directory exist")

        newWorkingDirectory = "test/resources/one"
        os.chdir(newWorkingDirectory)
        forceWorkingDirectory()
        self.assertTrue(os.path.exists("test"), "test directory exist")

        newWorkingDirectory = "test/resources/one/two"
        os.chdir(newWorkingDirectory)
        forceWorkingDirectory()
        self.assertTrue(os.path.exists("test"), "test directory exist")

        newWorkingDirectory = "test/resources/one/two/three"
        os.chdir(newWorkingDirectory)
        forceWorkingDirectory()
        self.assertTrue(os.path.exists("test"), "test directory exist")

        newWorkingDirectory = "test/resources/one/two/three/four"
        os.chdir(newWorkingDirectory)
        forceWorkingDirectory()
        self.assertTrue(os.path.exists("test"), "test directory exist")

        newWorkingDirectory = "../"
        os.chdir(newWorkingDirectory)
        forceWorkingDirectory()
        self.assertFalse(os.path.exists("test"), "test directory should NOT exist")


if __name__ == "__main__":
    unittest.main()
