import unittest

from utils.FileHelper import forceWorkingDirectory
from utils.Logger import Logger
from pyswing.objects.indicator import Indicator


class TestIndicator(unittest.TestCase):

    @classmethod
    def setUpClass(self):
        Logger.pushLogData("unitTesting", __name__)
        forceWorkingDirectory()

        # self._indicator = Indicator()

    @classmethod
    def tearDown(self):
        pass


    def test_something(self):

        # self.assertEqual(len(self._market.tickers.index), 72)

        pass


if __name__ == '__main__':
    unittest.main()
