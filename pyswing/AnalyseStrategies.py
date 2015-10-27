import logging
import getopt
import sys

from utils.Logger import Logger
from pyswing.objects.strategy import Strategy, getStrategies
from utils.TeamCity import TeamCity
import pyswing.constants


def analyseStrategies(argv):
    """
    Analyse Strategies.

    :param argv: Command Line Parameters.

    -n = Name
    -s = Strategy Name
    -r = Minimum Return per Trade
    -t = Minimum Number of Trades

    Example:

    python -m pyswing.AnalyseStrategies -n asx -s v4.0 -r 1.0 -t 500
    """

    Logger.log(logging.INFO, "Log Script Call", {"scope":__name__, "arguments":" ".join(argv)})
    Logger.pushLogData("script", __name__)

    marketName = ""
    returnPerTrade = ""
    numberOfTrades = ""

    try:
        shortOptions = "n:r:s:t:dh"
        longOptions = ["marketName=","return=", "strategy=", "trades=", "debug", "help"]
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
        elif opt in ("-r", "--return"):
            returnPerTrade = arg
        elif opt in ("-s", "--strategy"):
            pyswing.constants.pySwingStrategy = arg
        elif opt in ("-t", "--trades"):
            numberOfTrades = arg

    if marketName != "" and numberOfTrades != "" and returnPerTrade != "" and pyswing.constants.pySwingStrategy:

        Logger.log(logging.INFO, "Analyse Strategies", {"scope":__name__, "market":marketName, "numberOfTrades":numberOfTrades, "returnPerTrade":returnPerTrade, "strategy":pyswing.constants.pySwingStrategy})

        strategies = getStrategies(numberOfTrades, returnPerTrade)

        for strategy in strategies:
            strategy.analyse()

        TeamCity.setBuildResultText("Analysed Strategies")

    else:
        Logger.log(logging.ERROR, "Missing Options", {"scope": __name__, "options": str(argv)})
        usage()
        sys.exit(2)


def usage():
    print("")
    print("usage:")
    print("  AnalyseStrategies.py -n name [-d] [-h]")
    print("")
    print("arguments:")
    print("  -n, --name        Name")
    print("  -r, --return      Minimum Return per Trade")
    print("  -s, --strategy    Strategy Name")
    print("  -t, --trades      Minimum Number of Trades for Strategy")
    print("")
    print("optional arguments:")
    print("  -d, --debug       Change the Log Level to Debug")
    print("  -h, --help        Display Usage Information")


if __name__ == "__main__":
    analyseStrategies(sys.argv[1:])