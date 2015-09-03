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

    def test_deleteFile(self):

        relativeFilePath = "output/test_deleteFile.txt"

        try:
            file = open(relativeFilePath, 'w')
            file.write("Hello!")
            file.close()
        except OSError as osError:
            Logger.log(logging.ERROR, "Cannot Create File", {"scope":__name__, "directory":relativeFilePath})
            Logger.log(logging.DEBUG, "Caught Exception", {"scope":__name__, "exception":str(osError)})

        self.assertTrue(os.path.exists(relativeFilePath))

        deleteFile(relativeFilePath)

        self.assertFalse(os.path.exists(relativeFilePath))

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
