import logging
import getopt
import sys
import sqlite3

import pyswing.constants
from pyswing.utils.Logger import Logger
from pyswing.utils.TeamCity import TeamCity


def createDatabase(argv):
    """
    Create Database.

    :param argv: Command Line Parameters.

    -D = Database File
    -s = Script File

    Example:

    python -m pyswing.ImportData -D /Users/garyjoy/pyswing.db -s resources/pyswing.sql
    """

    Logger.log(logging.INFO, "Log Script Call", {"scope":__name__, "arguments":" ".join(argv)})
    Logger.pushLogData("script", __name__)

    databaseFilePath = pyswing.constants.pySwingDatabase
    scriptFilePath = pyswing.constants.pySwingDatabaseScript

    try:
        shortOptions = "D:s:dh"
        longOptions = ["databaseFilePath=", "scriptFilePath=", "debug", "help"]
        opts, __ = getopt.getopt(argv, shortOptions, longOptions)
    except getopt.GetoptError as e:
        Logger.log(logging.ERROR, "Error Reading Options", {"scope": __name__, "exception": str(e)})
        usage()
        sys.exit(2)

    for opt, arg in opts:
        if opt in ("-d", "--debug"):
            Logger().setLevel(logging.DEBUG)
        elif opt in ("-h", "--help"):
            print("?")
            usage()
            sys.exit()
        elif opt in ("-D", "--databaseFilePath"):
            databaseFilePath = arg
        elif opt in ("-s", "--scriptFilePath"):
            scriptFilePath = arg

    Logger.log(logging.INFO, "Creating Database", {"scope":__name__, "databaseFilePath":databaseFilePath, "scriptFilePath":scriptFilePath})

    query = open(pyswing.constants.pySwingDatabaseScript, 'r').read()
    connection = sqlite3.connect(databaseFilePath)
    c = connection.cursor()
    c.executescript(query)
    connection.commit()
    c.close()
    connection.close()
    TeamCity.setBuildResultText("Created Database")


def usage():
    print("")
    print("usage:")
    print("  CreateDatabase.py -D databaseFilePath -s scriptFilePath [-d] [-h]")
    print("")
    print("arguments:")
    print("  -D, --databaseFilePath     Database Name")
    print("  -s, --scriptFilePath       Relative Script File Path")
    print("")
    print("optional arguments:")
    print("  -d, --debug                Change the Log Level to Debug")
    print("  -h, --help                 Display Usage Information")


if __name__ == "__main__":
    createDatabase(sys.argv[1:])