import datetime
import unittest
from unittest.mock import patch

from utils.FileHelper import forceWorkingDirectory, deleteFile
from utils.Logger import Logger
from pyswing.objects.equity import Equity
from pyswing.objects.relativeRule import RelativeRule, Comparison
import pyswing.constants
from pyswing.CreateDatabase import createDatabase


class TestRelativeRule(unittest.TestCase):

    @classmethod
    def setUpClass(self):

        Logger.pushLogData("unitTesting", __name__)
        forceWorkingDirectory()

        pyswing.constants.pySwingDatabase = "output/TestRelativeRule.db"
        pyswing.constants.pySwingStartDate = datetime.datetime(2015, 1, 1)

        deleteFile(pyswing.constants.pySwingDatabase)

        args = "-D %s -s %s" % (pyswing.constants.pySwingDatabase, pyswing.constants.pySwingDatabaseScript)
        createDatabase(args.split())

        pretendDate = datetime.datetime(2015, 9, 1)
        with patch.object(Equity, '_getTodaysDate', return_value=pretendDate) as mock_method:

            self._equityCBA = Equity("WOR.AX")
            self._equityCBA.importData()


    @classmethod
    def tearDownClass(self):
        deleteFile(pyswing.constants.pySwingDatabase)


    def test_RelativeRule(self):

        rule = RelativeRule("Equities", "Close", -1, Comparison.GreaterThan, 1.01)
        rule.evaluateRule("WOR.AX")

        dataPointMatch = rule._ruleData.ix['2015-08-28 00:00:00']
        self.assertEqual(dataPointMatch['Match'], 1)

        dataPointMatch = rule._ruleData.ix['2015-08-31 00:00:00']
        self.assertEqual(dataPointMatch['Match'], 0)


if __name__ == '__main__':
    unittest.main()
