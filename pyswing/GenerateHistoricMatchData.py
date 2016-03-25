import logging
import getopt
import sys

from pyswing.utils.Logger import Logger
from pyswing.objects.historicMatches import HistoricMatches

import pyswing.database


def generateHistoricMatchData(argv):
    """
    Generate (in the HistoricMatches database table) Historic Match Data.

    Empty the database table and then fill it with the historic match data.

    :param argv: Command Line Parameters.

    -n = Name

    Example:

    python -m pyswing.GenerateHistoricMatchData -n asx
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

        Logger.log(logging.INFO, "Generate Historic Match Data", {"scope":__name__, "market":marketName})

        historicMatches = HistoricMatches()
        historicMatches.createTable();

    else:
        Logger.log(logging.ERROR, "Missing Options", {"scope": __name__, "options": str(argv)})
        usage()
        sys.exit(2)


def usage():
    print("")
    print("usage:")
    print("  GenerateHistoricMatchData.py -n name [-d] [-h]")
    print("")
    print("arguments:")
    print("  -n, --name        Name")
    print("")
    print("optional arguments:")
    print("  -d, --debug       Change the Log Level to Debug")
    print("  -h, --help        Display Usage Information")


if __name__ == "__main__":
    generateHistoricMatchData(sys.argv[1:])