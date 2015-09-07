import unittest

from utils.FileHelper import forceWorkingDirectory
from utils.Logger import Logger


class TestUpdateIndicators(unittest.TestCase):

    @classmethod
    def setUpClass(self):

        Logger.pushLogData("unitTesting", __name__)
        forceWorkingDirectory()

        # pyswing.constants.pySwingDatabase = "output/UpdateIndicators.db"
        # pyswing.constants.pySwingStartDate = datetime.datetime(2015, 1, 1)
        #
        # deleteFile(pyswing.constants.pySwingDatabase)
        #
        # Logger.log(logging.INFO, "Creating Test Database", {"scope":__name__, "database":pyswing.constants.pySwingDatabase})
        # query = open('resources/pyswing.sql', 'r').read()
        # connection = sqlite3.connect(pyswing.constants.pySwingDatabase)
        # c = connection.cursor()
        # c.executescript(query)
        # connection.commit()
        # c.close()
        # connection.close()

    @classmethod
    def tearDownClass(self):
        # deleteFile(pyswing.constants.pySwingDatabase)
        pass


    def test_UpdateIndicators(self):

        # args = "-n unitTest".split()
        # updateIndicators(args)

        # TODO:  Implement Unit Tests

        pass


if __name__ == '__main__':
    unittest.main()


