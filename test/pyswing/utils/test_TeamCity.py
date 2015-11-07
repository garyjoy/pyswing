import unittest
from unittest import mock

from pyswing.utils.Logger import Logger
from pyswing.utils.TeamCity import TeamCity
from pyswing.utils.FileHelper import forceWorkingDirectory


class testTeamCity(unittest.TestCase):
    """
    Unit Tests for the TeamCity (static) Class.
    """

    @classmethod
    def setUpClass(self):
        Logger.pushLogData("unitTesting", __name__)
        forceWorkingDirectory()


    @mock.patch('builtins.print')
    def test_setBuildResultTextWithFalse(self, mockPrint):

        TeamCity.setBuildResultText("Hello!", False)
        mockPrint.assert_called_with("##teamcity[buildStatus text='Hello!']")

    @mock.patch('builtins.print')
    def test_setBuildResultTextWithTrue(self, mockPrint):

        TeamCity.setBuildResultText("Hello!", True)
        mockPrint.assert_called_with("##teamcity[buildStatus text='Hello! ({build.status.text})']")

    @mock.patch('builtins.print')
    def test_setBuildResultTextWithDefault(self, mockPrint):

        TeamCity.setBuildResultText("Hello!")
        mockPrint.assert_called_with("##teamcity[buildStatus text='Hello! ({build.status.text})']")


if __name__ == "__main__":
    unittest.main()