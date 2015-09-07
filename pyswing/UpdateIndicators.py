import logging
import getopt
import sys

from utils.Logger import Logger
from pyswing.objects.market import Market
from pyswing.objects.equity import Equity

from pyswing.objects.indicatorSMA import IndicatorSMA
from pyswing.objects.indicatorEMA import IndicatorEMA
from pyswing.objects.indicatorBB20 import IndicatorBB20
from pyswing.objects.indicatorMOM import IndicatorMOM

from utils.TeamCity import TeamCity


def updateIndicators(argv):
    """
    Update Indicators.

    :param argv: Command Line Parameters.

    -n = Name

    Example:

    python -m pyswing.UpdateIndicators -n asx
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

        Logger.log(logging.INFO, "Update Indicators", {"scope":__name__, "market":marketName})

        tickerCodesRelativeFilePath = "resources/%s.txt" % (marketName)

        market = Market(tickerCodesRelativeFilePath)

        for index, row in market.tickers.iterrows():
            tickerCode = row[0]
            equity = Equity(tickerCode)
            equityDataFrame = equity.dataFrame()

            smaIndicator = IndicatorSMA(equityDataFrame, tickerCode)
            smaIndicator.updateIndicator()

            emaIndicator = IndicatorEMA(equityDataFrame, tickerCode)
            emaIndicator.updateIndicator()

            bbIndicator = IndicatorBB20(equityDataFrame, tickerCode)
            bbIndicator.updateIndicator()

            momIndicator = IndicatorMOM(equityDataFrame, tickerCode)
            momIndicator.updateIndicator()

        # TODO: Implement Integrety Checks for Data and Report Status (e.g. ?)
        TeamCity.setBuildResultText("Updated Indicators")

    else:
        Logger.log(logging.ERROR, "Missing Options", {"scope": __name__, "options": str(argv)})
        usage()
        sys.exit(2)


def usage():
    print("")
    print("usage:")
    print("  UpdateIndicators.py -n name [-d] [-h]")
    print("")
    print("arguments:")
    print("  -n, --name        Name")
    print("")
    print("optional arguments:")
    print("  -d, --debug       Change the Log Level to Debug")
    print("  -h, --help        Display Usage Information")


if __name__ == "__main__":
    updateIndicators(sys.argv[1:])