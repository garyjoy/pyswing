import unittest
import io

from pyswing.HelloWorld import helloWorld
from utils.FileHelper import forceWorkingDirectory, deleteFile


class TestHelloWorld(unittest.TestCase):

    def test_HelloWorld(self):

        forceWorkingDirectory()
        args = "-n F".split()
        helloWorld(args)

        deleteFile("output/helloWorld.db")


if __name__ == '__main__':
    unittest.main()


