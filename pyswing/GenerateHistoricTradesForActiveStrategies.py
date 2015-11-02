import logging
import getopt
import sys

from utils.Logger import Logger
from pyswing.objects.strategy import Strategy, getActiveStrategies, emptyHistoricTradesTable


def generateHistoricTradesForActiveStrategies(argv):
    """
    Generate (in the HistoricTrades database table) Historic Trades for the Active Strategies.

    Empty the database table and then fill it with the historic trades for all the active strategies.

    :param argv: Command Line Parameters.

    -n = Name

    Example:

    python -m pyswing.GenerateHistoricTradesForActiveStrategies -n asx
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

        Logger.log(logging.INFO, "Generate Historic Trades for Active Strategies", {"scope":__name__, "market":marketName})

        emptyHistoricTradesTable()

        strategies = getActiveStrategies()

        for strategy in strategies:
            strategy.generateHistoricTrades()

    else:
        Logger.log(logging.ERROR, "Missing Options", {"scope": __name__, "options": str(argv)})
        usage()
        sys.exit(2)


def usage():
    print("")
    print("usage:")
    print("  GenerateHistoricTradesForActiveStrategies.py -n name [-d] [-h]")
    print("")
    print("arguments:")
    print("  -n, --name        Name")
    print("")
    print("optional arguments:")
    print("  -d, --debug       Change the Log Level to Debug")
    print("  -h, --help        Display Usage Information")


if __name__ == "__main__":
    generateHistoricTradesForActiveStrategies(sys.argv[1:])