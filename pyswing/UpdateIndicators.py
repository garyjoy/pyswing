import logging
import getopt
import sys

from utils.Logger import Logger
from pyswing.objects.market import Market
from pyswing.objects.equity import Equity
from pyswing.objects.indicators.indicatorSMA import IndicatorSMA
from pyswing.objects.indicators.indicatorEMA import IndicatorEMA
from pyswing.objects.indicators.indicatorBB20 import IndicatorBB20
from pyswing.objects.indicators.indicatorROC import IndicatorROC
from pyswing.objects.indicators.indicatorMACD import IndicatorMACD
from pyswing.objects.indicators.indicatorSTOCH import IndicatorSTOCH
from pyswing.objects.indicators.indicatorRSI import IndicatorRSI
from pyswing.objects.indicators.indicatorAROON import IndicatorAROON
from pyswing.objects.indicators.indicatorADX import IndicatorADX
from pyswing.objects.indicators.indicatorDX import IndicatorDX
from pyswing.objects.indicators.indicatorADI import IndicatorADI
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

        # Market Indicators
        adiIndicator = IndicatorADI()
        adiIndicator.updateIndicator()

        # Equity Indicators
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

            rocIndicator = IndicatorROC(equityDataFrame, tickerCode)
            rocIndicator.updateIndicator()

            macdIndicator = IndicatorMACD(equityDataFrame, tickerCode)
            macdIndicator.updateIndicator()

            stochIndicator = IndicatorSTOCH(equityDataFrame, tickerCode)
            stochIndicator.updateIndicator()

            rsiIndicator = IndicatorRSI(equityDataFrame, tickerCode)
            rsiIndicator.updateIndicator()

            adxIndicator = IndicatorADX(equityDataFrame, tickerCode)
            adxIndicator.updateIndicator()

            aroonIndicator = IndicatorAROON(equityDataFrame, tickerCode)
            aroonIndicator.updateIndicator()

            dxIndicator = IndicatorDX(equityDataFrame, tickerCode)
            dxIndicator.updateIndicator()

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