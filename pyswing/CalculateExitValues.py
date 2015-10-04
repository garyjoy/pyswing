import logging
import getopt
import sys

from utils.Logger import Logger
from pyswing.objects.exitValuesTrailingStop import ExitValuesTrailingStop
from pyswing.objects.market import Market
from utils.TeamCity import TeamCity


def calculateExitValues(argv):
    """
    Calculate Exit Values.

    :param argv: Command Line Parameters.

    -n = Name

    Example:

    python -m pyswing.CalculateExitValues -n asx
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

        Logger.log(logging.INFO, "Calculate Exit Values", {"scope":__name__, "market":marketName})

        tickerCodesRelativeFilePath = "resources/%s.txt" % (marketName)

        market = Market(tickerCodesRelativeFilePath)

        for index, row in market.tickers.iterrows():
            tickerCode = row[0]
            exitValuesTrailingStop = ExitValuesTrailingStop(tickerCode, 0.03, 2)
            exitValuesTrailingStop.calculateExitValues()

        TeamCity.setBuildResultText("Calculated Exit Values")

    else:
        Logger.log(logging.ERROR, "Missing Options", {"scope": __name__, "options": str(argv)})
        usage()
        sys.exit(2)


def usage():
    print("")
    print("usage:")
    print("  CalculateExitValues.py -n name [-d] [-h]")
    print("")
    print("arguments:")
    print("  -n, --name        Name")
    print("")
    print("optional arguments:")
    print("  -d, --debug       Change the Log Level to Debug")
    print("  -h, --help        Display Usage Information")


if __name__ == "__main__":
    calculateExitValues(sys.argv[1:])