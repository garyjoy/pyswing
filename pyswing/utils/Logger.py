import logging
import inspect

from datetime import datetime


class Logger(object):
    """
    The (Static) Logger class provides a logging interface for us to use. It ensures that log entries follow a standard
    (self-contained) format and it provides support for name=value pairs (that Splunk etc. loves).

    You should only generate log entries using this interface (feel free to extend or improve it).
    """

    # Default Log Level
    _defaultLogLevel = logging.DEBUG

    # Persistent Log Data
    _logData = {}

    logging.getLogger("").setLevel(_defaultLogLevel)

    @staticmethod
    def log(logLevel, logMessage, logData):
        """
        log() will generate write the specified Message (and Data) at the specified Level to the Log.

        Example: Logger.log(logging.INFO, "Test Log Entry", {"key1":"value1","key2","value2"})

        :param logLevel: One of the Log Levels defined in the Logging Module (e.g. logging.DEBUG)
        :param logMessage: The Log Message (as a String)
        :param logData: A dictionary (names and values as Strings) of Log Data
        """

        logger = Logger._getLogger();
        logEntry = Logger._buildLogMessage(logLevel, logMessage, logData)

        if logLevel == logging.DEBUG:
            logger.debug(logEntry)
        if logLevel == logging.INFO:
            logger.info(logEntry)
        if logLevel == logging.WARN:
            logger.warn(logEntry)
        if logLevel == logging.ERROR:
            logger.error(logEntry)

    @staticmethod
    def pushLogData(name, value):
        """
        Push the specified data (Name and Value) on to the Persistent Log Data.

        The persistent log data (Name and Value) will be included in every subsequent log entry that is generated
        until the Name is "popped" using popLogData().

        :param name: Log Data Name (String) e.g. teamCityBuildId
        :param value: Log Data Data (String) e.g. 2238344
        """

        Logger._logData[name] = value;

    @staticmethod
    def popLogData(name):
        """
        Pop (remove) the specified data (Name) from the Persistent Log Data.

        :param name: Log Data Name (String) e.g. teamCityBuildId
        """

        del Logger._logData[name];

    @staticmethod
    def setLevel(logLevel):
        """
        setLevel() will (persistently) update the the Log Level.

        For example, when the Log Level is logging.INFO any calls to log() using logging.DEBUG will not generate logs.

        :param logLevel: One of the Log Levels defined in the Logging Module (e.g. logging.DEBUG)
        """

        logger = Logger._getLogger();
        logger.setLevel(logLevel)
        for handler in logger.handlers:
            handler.setLevel(logLevel)

        Logger.log(logging.INFO, "Log Level Changed", {"logLevel":str(logLevel)})

    @staticmethod
    def _buildLogMessage(logLevel, logMessage, logData):
        """
        __buildLogMessage() is used by log() to build the log entry string from constituent parts.

        Example: Logger.__buildLogMessage(logging.INFO, "Test Log Entry", {"key1":"value1","key2":"value2"}) returns
        "2015-06-17 10:27:46.859823 level="INFO" message="Test Log Entry" key1="value1" key2="value2""

        It will also include anything in the Persistent Log Data (see pushLogData() and popLogData()).

        :param logLevel: One of the Log Levels defined in the Logging Module (e.g. logging.DEBUG)
        :param logMessage: The Log Message (as a String)
        :param logData: A dictionary (names and values as Strings) of Log Data
        :returns: A Log Entry (as a String)
        """

        logEntry = str(datetime.now()) + " " + "level=\"" + logging.getLevelName(logLevel) + "\"" + " " + "message=\"" + logMessage + "\""

        try:
            functionName = inspect.stack()[2][3]
            logEntry += " function=\"" + functionName + "\""
        except Exception as exception:
            pass

        for key in sorted(logData):
            logEntry += " " + key + "=\"" + logData[key] + "\""

        for key in sorted(Logger._logData):
            logEntry += " " + key + "=\"" + Logger._logData[key] + "\""

        return logEntry

    @staticmethod
    def _getLogger():
        """
        __getLogger() will return a Logger (logging.Logger) object with a Stream Handler (with the default Log Level).

        The implementation ensures that no superfluous Stream Handlers are attached.
        """

        logger = logging.getLogger("")

        # Add a Log Handler if there isn't one already
        if logger.handlers == []:
            streamHandler = logging.StreamHandler()
            streamHandler.setLevel(Logger._defaultLogLevel)
            logger.addHandler(streamHandler)
            Logger.log(logging.INFO, "Created Stream Handler", {})

        return logger;
