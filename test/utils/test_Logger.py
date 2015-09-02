import logging
import unittest

from utils.Logger import Logger
from unittest.mock import patch
from utils.FileHelper import forceWorkingDirectory


class testLogger(unittest.TestCase):
    """
    Unit Tests for the Logger (static) Class.
    """

    @classmethod
    def setUpClass(self):
        Logger.pushLogData("unitTesting", __name__)
        forceWorkingDirectory()


    def test_getLogger(self):

        myLogger = Logger._getLogger()

        self.assertIsNotNone(myLogger, "Check My Logger")

    def test_lotsOfLoggers(self):

        aLogger = Logger._getLogger()
        anotherLogger = Logger._getLogger()

        self.assertIsNotNone(aLogger, "Check A Logger")
        self.assertIsNotNone(anotherLogger, "Check Another Logger")
        self.assertEqual(len(anotherLogger.handlers), 1, "Check Handlers")

    def test_pushLogData(self):

        myLogEntry = Logger._buildLogMessage(logging.INFO, "Test Log Entry", {"key1":"value1","key2":"value2"})
        self.assertTrue('key1="value1" key2="value2"' in myLogEntry, 'Expected key1="value1" key2="value2" in %s' % myLogEntry)

        Logger.pushLogData("key3","value3")
        myLogEntry = Logger._buildLogMessage(logging.INFO, "Test Log Entry", {"key1":"value1","key2":"value2"})
        self.assertTrue('key1="value1" key2="value2"' in myLogEntry, 'Expected key1="value1" key2="value2" in %s' % myLogEntry)
        self.assertTrue('key3="value3"' in myLogEntry, 'Expected key3="value3" in %s' % myLogEntry)

        Logger.popLogData("key3")
        myLogEntry = Logger._buildLogMessage(logging.INFO, "Test Log Entry", {"key1":"value1","key2":"value2"})
        self.assertTrue('key1="value1" key2="value2"' in myLogEntry, 'Expected key1="value1" key2="value2" in %s' % myLogEntry)
        self.assertFalse('key3="value3"' in myLogEntry, 'Did Not Expect key3="value3" in %s' % myLogEntry)

    def test_buildLogMessage(self):

        myLogEntry = Logger._buildLogMessage(logging.INFO, "Test Log Entry", {"key1":"value1","key2":"value2"})
        self.assertTrue('level="INFO"' in myLogEntry, "Expected level=\"INFO\" in %s" % myLogEntry)
        self.assertTrue('message="Test Log Entry"' in myLogEntry, "Expected message=\"Test Log Entry\" in %s" % myLogEntry)
        self.assertTrue('key1="value1" key2="value2"' in myLogEntry, "Expected key1=\"value1\" key2=\"value2\" in %s" % myLogEntry)

    def test_log(self):
        with patch.object(Logger._getLogger(), '_log', return_value=None) as mock_method:

            # Assumes that the default log level is INFO

            Logger.log(logging.DEBUG, "Test Debug Log Entry", {"key1":"value1","key2":"value2"})
            self.assertEqual(0, mock_method.call_count)

            Logger.log(logging.INFO, "Test Info Log Entry", {"key1":"value1","key2":"value2"})
            self.assertEqual(1, mock_method.call_count)

            Logger.log(logging.WARN, "Test Warning Log Entry", {"key1":"value1","key2":"value2"})
            self.assertEqual(2, mock_method.call_count)

            Logger.log(logging.ERROR, "Test Error Log Entry", {"key1":"value1","key2":"value2"})
            self.assertEqual(3, mock_method.call_count)

    def test_setLevel(self):

        aLogger = Logger._getLogger()
        Logger.setLevel(logging.INFO)

        self.assertEqual(aLogger.level, logging.INFO, "Check Log Level")

        Logger.setLevel(logging.DEBUG)
        aLogger = Logger._getLogger()

        self.assertEqual(aLogger.level, logging.DEBUG, "Check Log Level")

        Logger.setLevel(logging.INFO)


if __name__ == "__main__":
    unittest.main()