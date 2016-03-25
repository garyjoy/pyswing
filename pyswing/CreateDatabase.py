import logging
import getopt
import sys
import sqlite3

import pyswing.constants
import pyswing.database

from pyswing.utils.Logger import Logger
from pyswing.utils.TeamCity import TeamCity


def createDatabase(argv):
    """
    Create Database.

    :param argv: Command Line Parameters.

    -n = Name

    Example:

    python -m pyswing.CreateDatabase -n asx
    """

    Logger.log(logging.INFO, "Log Script Call", {"scope":__name__, "arguments":" ".join(argv)})
    Logger.pushLogData("script", __name__)

    marketName = ""

    try:
        shortOptions = "n:dh"
        longOptions = ["marketName=", "debug", "help"]
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
        elif opt in ("-n", "--marketName"):
            marketName = arg

    if marketName != "":

        pyswing.database.initialiseDatabase(marketName)
        databaseFilePath = pyswing.database.pySwingDatabase
        scriptFilePath = pyswing.constants.pySwingDatabaseScript

        Logger.log(logging.INFO, "Creating Database", {"scope":__name__, "databaseFilePath":databaseFilePath, "scriptFilePath":scriptFilePath})

        query = open(pyswing.constants.pySwingDatabaseScript, 'r').read()
        connection = sqlite3.connect(databaseFilePath)
        c = connection.cursor()
        c.executescript(query)
        connection.commit()
        c.close()
        connection.close()
        TeamCity.setBuildResultText("Created Database")

    else:
        Logger.log(logging.ERROR, "Missing Options", {"scope": __name__, "options": str(argv)})
        usage()
        sys.exit(2)


def usage():
    print("")
    print("usage:")
    print("  CreateDatabase.py -D databaseFilePath -s scriptFilePath [-d] [-h]")
    print("")
    print("arguments:")
    print("  -n, --name        Name")
    print("")
    print("optional arguments:")
    print("  -d, --debug       Change the Log Level to Debug")
    print("  -h, --help        Display Usage Information")


if __name__ == "__main__":
    createDatabase(sys.argv[1:])