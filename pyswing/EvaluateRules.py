import logging
import getopt
import sys

from pyswing.utils.Logger import Logger
from pyswing.objects.market import Market
from pyswing.objects.rules.simpleRule import SimpleRule
from pyswing.objects.rules.marketRule import MarketRule
from pyswing.objects.rules.relativeRule import RelativeRule, Comparison
from pyswing.objects.rules.crossingRule import CrossingRule
from pyswing.objects.rules.multipleIndicatorRule import MultipleIndicatorRule
from pyswing.utils.TeamCity import TeamCity

import pyswing.database


def evaluateRules(argv):
    """
    Evaluate Rules.

    :param argv: Command Line Parameters.

    -n = Name

    Example:

    python -m pyswing.EvaluateRules -n asx
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

        Logger.log(logging.INFO, "Evaluate Rules", {"scope":__name__, "market":marketName})

        tickerCodesRelativeFilePath = "resources/%s.txt" % (marketName)

        market = Market(tickerCodesRelativeFilePath)

        rules = []
        rules.append(SimpleRule("Indicator_ROC", "ROC_5 > 1"))
        rules.append(SimpleRule("Indicator_ROC", "ROC_5 > 3"))
        rules.append(SimpleRule("Indicator_ROC", "ROC_5 > 5"))

        rules.append(SimpleRule("Indicator_ROC", "ROC_5 < -1"))
        rules.append(SimpleRule("Indicator_ROC", "ROC_5 < -3"))
        rules.append(SimpleRule("Indicator_ROC", "ROC_5 < -5"))

        rules.append(SimpleRule("Indicator_ROC", "ROC_10 > 1"))
        rules.append(SimpleRule("Indicator_ROC", "ROC_10 > 4"))
        rules.append(SimpleRule("Indicator_ROC", "ROC_10 > 8"))

        rules.append(SimpleRule("Indicator_ROC", "ROC_10 < -1"))
        rules.append(SimpleRule("Indicator_ROC", "ROC_10 < -4"))
        rules.append(SimpleRule("Indicator_ROC", "ROC_10 < -8"))

        rules.append(SimpleRule("Indicator_ROC", "ROC_20 > 1"))
        rules.append(SimpleRule("Indicator_ROC", "ROC_20 > 5"))
        rules.append(SimpleRule("Indicator_ROC", "ROC_20 > 10"))

        rules.append(SimpleRule("Indicator_ROC", "ROC_20 < -1"))
        rules.append(SimpleRule("Indicator_ROC", "ROC_20 < -5"))
        rules.append(SimpleRule("Indicator_ROC", "ROC_20 < -10"))

        #

        # rules.append(RelativeRule("Equities", "Close", -1, Comparison.GreaterThan, 1.01))
        # rules.append(RelativeRule("Equities", "Close", -1, Comparison.LessThan, 0.99))
        #
        # rules.append(RelativeRule("Equities", "Close", -1, Comparison.GreaterThan, 1.02))
        # rules.append(RelativeRule("Equities", "Close", -1, Comparison.LessThan, 0.98))
        #
        # rules.append(RelativeRule("Equities", "Close", -1, Comparison.GreaterThan, 1.03))
        # rules.append(RelativeRule("Equities", "Close", -1, Comparison.LessThan, 0.97))
        #
        # rules.append(RelativeRule("Equities", "Close", -1, Comparison.GreaterThan, 1.05))
        # rules.append(RelativeRule("Equities", "Close", -1, Comparison.LessThan, 0.95))
        #
        # rules.append(RelativeRule("Equities", "Close", -5, Comparison.GreaterThan, 1.10))
        # rules.append(RelativeRule("Equities", "Close", -5, Comparison.LessThan, 0.90))
        #
        # rules.append(RelativeRule("Equities", "Close", -5, Comparison.GreaterThan, 1.20))
        # rules.append(RelativeRule("Equities", "Close", -5, Comparison.LessThan, 0.80))

        #

        # rules.append(CrossingRule("Indicator_SMA","SMA_5","Indicator_SMA","SMA_20"))
        # rules.append(CrossingRule("Indicator_SMA","SMA_10","Indicator_SMA","SMA_50"))
        # rules.append(CrossingRule("Indicator_SMA","SMA_10","Indicator_SMA","SMA_200"))
        # rules.append(CrossingRule("Indicator_SMA","SMA_20","Indicator_SMA","SMA_200"))
        # rules.append(CrossingRule("Indicator_SMA","SMA_20","Indicator_SMA","SMA_5"))
        # rules.append(CrossingRule("Indicator_SMA","SMA_50","Indicator_SMA","SMA_10"))
        # rules.append(CrossingRule("Indicator_SMA","SMA_200","Indicator_SMA","SMA_10"))
        # rules.append(CrossingRule("Indicator_SMA","SMA_200","Indicator_SMA","SMA_20"))

        rules.append(MultipleIndicatorRule("Equities", "Indicator_SMA", "t1.Close > t2.SMA_100"))
        rules.append(MultipleIndicatorRule("Equities", "Indicator_SMA", "t1.Close > 1.1 * t2.SMA_100"))
        rules.append(MultipleIndicatorRule("Equities", "Indicator_SMA", "t1.Close > 1.2 * t2.SMA_100"))

        rules.append(MultipleIndicatorRule("Equities", "Indicator_SMA", "t1.Close > t2.SMA_200"))
        rules.append(MultipleIndicatorRule("Equities", "Indicator_SMA", "t1.Close > 1.1 * t2.SMA_200"))
        rules.append(MultipleIndicatorRule("Equities", "Indicator_SMA", "t1.Close > 1.2 * t2.SMA_200"))

        rules.append(MultipleIndicatorRule("Equities", "Indicator_SMA", "t1.Close > t2.SMA_300"))
        rules.append(MultipleIndicatorRule("Equities", "Indicator_SMA", "t1.Close > 1.1 * t2.SMA_300"))
        rules.append(MultipleIndicatorRule("Equities", "Indicator_SMA", "t1.Close > 1.2 * t2.SMA_300"))

        rules.append(MultipleIndicatorRule("Equities", "Indicator_SMA", "t1.Close < t2.SMA_100"))
        rules.append(MultipleIndicatorRule("Equities", "Indicator_SMA", "t1.Close < 0.9 * t2.SMA_100"))
        rules.append(MultipleIndicatorRule("Equities", "Indicator_SMA", "t1.Close < 0.8 * t2.SMA_100"))

        rules.append(MultipleIndicatorRule("Equities", "Indicator_SMA", "t1.Close < t2.SMA_200"))
        rules.append(MultipleIndicatorRule("Equities", "Indicator_SMA", "t1.Close < 0.9 * t2.SMA_200"))
        rules.append(MultipleIndicatorRule("Equities", "Indicator_SMA", "t1.Close < 0.8 * t2.SMA_200"))

        rules.append(MultipleIndicatorRule("Equities", "Indicator_SMA", "t1.Close < t2.SMA_300"))
        rules.append(MultipleIndicatorRule("Equities", "Indicator_SMA", "t1.Close < 0.9 * t2.SMA_300"))
        rules.append(MultipleIndicatorRule("Equities", "Indicator_SMA", "t1.Close < 0.8 * t2.SMA_300"))

        #

        # rules.append(CrossingRule("Indicator_EMA","EMA_5","Indicator_EMA","EMA_20"))
        # rules.append(CrossingRule("Indicator_EMA","EMA_10","Indicator_EMA","EMA_50"))
        # rules.append(CrossingRule("Indicator_EMA","EMA_10","Indicator_EMA","EMA_200"))
        # rules.append(CrossingRule("Indicator_EMA","EMA_20","Indicator_EMA","EMA_200"))
        # rules.append(CrossingRule("Indicator_EMA","EMA_20","Indicator_EMA","EMA_5"))
        # rules.append(CrossingRule("Indicator_EMA","EMA_50","Indicator_EMA","EMA_10"))
        # rules.append(CrossingRule("Indicator_EMA","EMA_200","Indicator_EMA","EMA_10"))
        # rules.append(CrossingRule("Indicator_EMA","EMA_200","Indicator_EMA","EMA_20"))

        rules.append(MultipleIndicatorRule("Equities", "Indicator_EMA", "t1.Close > t2.EMA_100"))
        rules.append(MultipleIndicatorRule("Equities", "Indicator_EMA", "t1.Close > 1.1 * t2.EMA_100"))
        rules.append(MultipleIndicatorRule("Equities", "Indicator_EMA", "t1.Close > 1.2 * t2.EMA_100"))

        rules.append(MultipleIndicatorRule("Equities", "Indicator_EMA", "t1.Close > t2.EMA_200"))
        rules.append(MultipleIndicatorRule("Equities", "Indicator_EMA", "t1.Close > 1.1 * t2.EMA_200"))
        rules.append(MultipleIndicatorRule("Equities", "Indicator_EMA", "t1.Close > 1.2 * t2.EMA_200"))

        rules.append(MultipleIndicatorRule("Equities", "Indicator_EMA", "t1.Close > t2.EMA_300"))
        rules.append(MultipleIndicatorRule("Equities", "Indicator_EMA", "t1.Close > 1.1 * t2.EMA_300"))
        rules.append(MultipleIndicatorRule("Equities", "Indicator_EMA", "t1.Close > 1.2 * t2.EMA_300"))

        rules.append(MultipleIndicatorRule("Equities", "Indicator_EMA", "t1.Close < t2.EMA_100"))
        rules.append(MultipleIndicatorRule("Equities", "Indicator_EMA", "t1.Close < 0.9 * t2.EMA_100"))
        rules.append(MultipleIndicatorRule("Equities", "Indicator_EMA", "t1.Close < 0.8 * t2.EMA_100"))

        rules.append(MultipleIndicatorRule("Equities", "Indicator_EMA", "t1.Close < t2.EMA_200"))
        rules.append(MultipleIndicatorRule("Equities", "Indicator_EMA", "t1.Close < 0.9 * t2.EMA_200"))
        rules.append(MultipleIndicatorRule("Equities", "Indicator_EMA", "t1.Close < 0.8 * t2.EMA_200"))

        rules.append(MultipleIndicatorRule("Equities", "Indicator_EMA", "t1.Close < t2.EMA_300"))
        rules.append(MultipleIndicatorRule("Equities", "Indicator_EMA", "t1.Close < 0.9 * t2.EMA_300"))
        rules.append(MultipleIndicatorRule("Equities", "Indicator_EMA", "t1.Close < 0.8 * t2.EMA_300"))

        rules.append(CrossingRule("Indicator_SMA","SMA_20","Indicator_EMA","EMA_200"))
        rules.append(CrossingRule("Indicator_EMA","EMA_200","Indicator_SMA","SMA_20"))

        rules.append(MultipleIndicatorRule("Equities", "Indicator_BB20", "t1.Close > t2.upperband"))
        rules.append(MultipleIndicatorRule("Equities", "Indicator_BB20", "abs(t1.Close - t2.upperband) < abs(t1.Close - t2.middleband)"))
        rules.append(MultipleIndicatorRule("Equities", "Indicator_BB20", "t1.Close < t2.lowerband"))
        rules.append(MultipleIndicatorRule("Equities", "Indicator_BB20", "abs(t1.Close - t2.lowerband) < abs(t1.Close - t2.middleband)"))

        rules.append(SimpleRule("Indicator_BB20", "upperbandroc < 0 and lowerbandroc > 0"))
        rules.append(SimpleRule("Indicator_BB20", "upperbandroc < -1 and lowerbandroc > 1"))
        rules.append(SimpleRule("Indicator_BB20", "upperbandroc > 0 and lowerbandroc < 0"))
        rules.append(SimpleRule("Indicator_BB20", "upperbandroc > 1 and lowerbandroc <- 1"))

        rules.append(SimpleRule("Indicator_BB20", "upperbandroc > 1"))
        rules.append(SimpleRule("Indicator_BB20", "upperbandroc > 2"))
        rules.append(SimpleRule("Indicator_BB20", "upperbandroc > 3"))
        rules.append(SimpleRule("Indicator_BB20", "upperbandroc < -1"))
        rules.append(SimpleRule("Indicator_BB20", "upperbandroc < -2"))
        rules.append(SimpleRule("Indicator_BB20", "upperbandroc < -3"))

        rules.append(SimpleRule("Indicator_BB20", "lowerbandroc > 1"))
        rules.append(SimpleRule("Indicator_BB20", "lowerbandroc > 2"))
        rules.append(SimpleRule("Indicator_BB20", "lowerbandroc > 3"))
        rules.append(SimpleRule("Indicator_BB20", "lowerbandroc < -1"))
        rules.append(SimpleRule("Indicator_BB20", "lowerbandroc < -2"))
        rules.append(SimpleRule("Indicator_BB20", "lowerbandroc < -3"))

        rules.append(SimpleRule("Equities", "abs(Close - High) * 2 < abs(Close - Low)"))
        rules.append(SimpleRule("Equities", "abs(Close - High) * 5 < abs(Close - Low)"))
        rules.append(SimpleRule("Equities", "abs(Close - High) * 10 < abs(Close - Low)"))

        rules.append(SimpleRule("Equities", "abs(Close - High) > 2 * abs(Close - Low)"))
        rules.append(SimpleRule("Equities", "abs(Close - High) > 5 * abs(Close - Low)"))
        rules.append(SimpleRule("Equities", "abs(Close - High) > 10 * abs(Close - Low)"))

        rules.append(SimpleRule("Indicator_MACD", "MACD_12_26_9_DIVERGENCE < 0"))
        rules.append(SimpleRule("Indicator_MACD", "MACD_12_26_9_DIVERGENCE > 0"))

        rules.append(SimpleRule("Indicator_MACD", "MACD_12_26_9 > MACD_12_26"))
        rules.append(SimpleRule("Indicator_MACD", "MACD_12_26_9 < MACD_12_26"))

        rules.append(SimpleRule("Indicator_STOCH", "STOCH_K < 5"))
        rules.append(SimpleRule("Indicator_STOCH", "STOCH_K < 10"))
        rules.append(SimpleRule("Indicator_STOCH", "STOCH_K < 15"))
        rules.append(SimpleRule("Indicator_STOCH", "STOCH_K < 20"))
        rules.append(SimpleRule("Indicator_STOCH", "STOCH_K < 30"))

        rules.append(SimpleRule("Indicator_STOCH", "STOCH_K > 95"))
        rules.append(SimpleRule("Indicator_STOCH", "STOCH_K > 90"))
        rules.append(SimpleRule("Indicator_STOCH", "STOCH_K > 85"))
        rules.append(SimpleRule("Indicator_STOCH", "STOCH_K > 80"))
        rules.append(SimpleRule("Indicator_STOCH", "STOCH_K > 70"))

        rules.append(SimpleRule("Indicator_STOCH", "STOCH_D < 5"))
        rules.append(SimpleRule("Indicator_STOCH", "STOCH_D < 10"))
        rules.append(SimpleRule("Indicator_STOCH", "STOCH_D < 15"))
        rules.append(SimpleRule("Indicator_STOCH", "STOCH_D < 20"))
        rules.append(SimpleRule("Indicator_STOCH", "STOCH_D < 30"))

        rules.append(SimpleRule("Indicator_STOCH", "STOCH_D > 95"))
        rules.append(SimpleRule("Indicator_STOCH", "STOCH_D > 90"))
        rules.append(SimpleRule("Indicator_STOCH", "STOCH_D > 85"))
        rules.append(SimpleRule("Indicator_STOCH", "STOCH_D > 80"))
        rules.append(SimpleRule("Indicator_STOCH", "STOCH_D > 70"))

        rules.append(SimpleRule("Indicator_STOCH", "STOCH_K > STOCH_D"))
        rules.append(SimpleRule("Indicator_STOCH", "STOCH_K < STOCH_D"))

        rules.append(SimpleRule("Indicator_STOCH", "STOCH_K_ROC > 50"))
        rules.append(SimpleRule("Indicator_STOCH", "STOCH_K_ROC > 100"))
        rules.append(SimpleRule("Indicator_STOCH", "STOCH_K_ROC > 200"))

        rules.append(SimpleRule("Indicator_STOCH", "STOCH_K_ROC < -50"))
        rules.append(SimpleRule("Indicator_STOCH", "STOCH_K_ROC < -60"))
        rules.append(SimpleRule("Indicator_STOCH", "STOCH_K_ROC < -70"))

        rules.append(SimpleRule("Indicator_STOCH", "STOCH_D_ROC > 50"))
        rules.append(SimpleRule("Indicator_STOCH", "STOCH_D_ROC > 100"))
        rules.append(SimpleRule("Indicator_STOCH", "STOCH_D_ROC > 200"))

        rules.append(SimpleRule("Indicator_STOCH", "STOCH_D_ROC < -50"))
        rules.append(SimpleRule("Indicator_STOCH", "STOCH_D_ROC < -60"))
        rules.append(SimpleRule("Indicator_STOCH", "STOCH_D_ROC < -70"))

        rules.append(SimpleRule("Indicator_ADX", "ADX > 30"))
        rules.append(SimpleRule("Indicator_ADX", "ADX > 40"))
        rules.append(SimpleRule("Indicator_ADX", "ADX > 50"))

        rules.append(SimpleRule("Indicator_ADX", "ADX_ROC > 10"))
        rules.append(SimpleRule("Indicator_ADX", "ADX_ROC > 20"))

        rules.append(SimpleRule("Indicator_ADX", "ADX_ROC < -10"))
        rules.append(SimpleRule("Indicator_ADX", "ADX_ROC < -20"))


        rules.append(SimpleRule("Indicator_DX", "DX > 40"))
        rules.append(SimpleRule("Indicator_DX", "DX > 50"))
        rules.append(SimpleRule("Indicator_DX", "DX > 60"))

        # rules.append(SimpleRule("Indicator_DX", "DX_ROC > 1000"))
        # rules.append(SimpleRule("Indicator_DX", "DX_ROC > 2000"))
        # rules.append(SimpleRule("Indicator_DX", "DX_ROC > 3000"))
        # rules.append(SimpleRule("Indicator_DX", "DX_ROC > 4000"))
        #
        # rules.append(SimpleRule("Indicator_DX", "DX_ROC < -95"))
        # rules.append(SimpleRule("Indicator_DX", "DX_ROC < -97"))
        # rules.append(SimpleRule("Indicator_DX", "DX_ROC < -98"))

        rules.append(SimpleRule("Indicator_RSI", "RSI > 20"))
        rules.append(SimpleRule("Indicator_RSI", "RSI > 30"))
        rules.append(SimpleRule("Indicator_RSI", "RSI > 40"))
        rules.append(SimpleRule("Indicator_RSI", "RSI > 50"))
        rules.append(SimpleRule("Indicator_RSI", "RSI > 60"))
        rules.append(SimpleRule("Indicator_RSI", "RSI > 70"))
        rules.append(SimpleRule("Indicator_RSI", "RSI > 80"))

        rules.append(SimpleRule("Indicator_RSI", "RSI < 80"))
        rules.append(SimpleRule("Indicator_RSI", "RSI < 70"))
        rules.append(SimpleRule("Indicator_RSI", "RSI < 60"))
        rules.append(SimpleRule("Indicator_RSI", "RSI < 50"))
        rules.append(SimpleRule("Indicator_RSI", "RSI < 40"))
        rules.append(SimpleRule("Indicator_RSI", "RSI < 30"))
        rules.append(SimpleRule("Indicator_RSI", "RSI < 20"))

        rules.append(SimpleRule("Indicator_AROON", "AROON_UP = 100"))
        rules.append(SimpleRule("Indicator_AROON", "AROON_UP = 0"))
        rules.append(SimpleRule("Indicator_AROON", "AROON_UP > 50"))
        rules.append(SimpleRule("Indicator_AROON", "AROON_UP < 50"))
        rules.append(SimpleRule("Indicator_AROON", "AROON_UP > 90"))
        rules.append(SimpleRule("Indicator_AROON", "AROON_UP < 90"))
        rules.append(SimpleRule("Indicator_AROON", "AROON_UP > 10"))
        rules.append(SimpleRule("Indicator_AROON", "AROON_UP < 10"))

        rules.append(SimpleRule("Indicator_AROON", "AROON_DOWN = 100"))
        rules.append(SimpleRule("Indicator_AROON", "AROON_DOWN = 0"))
        rules.append(SimpleRule("Indicator_AROON", "AROON_DOWN > 50"))
        rules.append(SimpleRule("Indicator_AROON", "AROON_DOWN < 50"))
        rules.append(SimpleRule("Indicator_AROON", "AROON_DOWN > 90"))
        rules.append(SimpleRule("Indicator_AROON", "AROON_DOWN < 90"))
        rules.append(SimpleRule("Indicator_AROON", "AROON_DOWN > 10"))
        rules.append(SimpleRule("Indicator_AROON", "AROON_DOWN < 10"))

        rules.append(SimpleRule("Equities", "abs(High - Close) > 10 * abs(Low - Close)"))
        rules.append(SimpleRule("Equities", "abs(High - Close) * 10 < abs(Low - Close)"))

        rules.append(SimpleRule("Equities", "abs(High - Close) > 100 * abs(Low - Close)"))
        rules.append(SimpleRule("Equities", "abs(High - Close) * 100 < abs(Low - Close)"))

        for index, row in market.tickers.iterrows():
            tickerCode = row[0]
            for rule in rules:
                rule.evaluateRule(tickerCode)

        marketRules = []

        marketRules.append(MarketRule("Indicator_ADI", "ADI > 0"))
        marketRules.append(MarketRule("Indicator_ADI", "ADI > 25"))
        marketRules.append(MarketRule("Indicator_ADI", "ADI > 50"))
        marketRules.append(MarketRule("Indicator_ADI", "ADI < 0"))
        marketRules.append(MarketRule("Indicator_ADI", "ADI < -25"))
        marketRules.append(MarketRule("Indicator_ADI", "ADI < -50"))

        marketRules.append(MarketRule("Indicator_ADI", "ADI_ROC > 1"))
        marketRules.append(MarketRule("Indicator_ADI", "ADI_ROC > 3"))
        marketRules.append(MarketRule("Indicator_ADI", "ADI_ROC > 7"))
        marketRules.append(MarketRule("Indicator_ADI", "ADI_ROC < -1"))
        marketRules.append(MarketRule("Indicator_ADI", "ADI_ROC < -3"))
        marketRules.append(MarketRule("Indicator_ADI", "ADI_ROC < -7"))

        marketRules.append(MarketRule("Indicator_ADI", "ADI_EMA > 5"))
        marketRules.append(MarketRule("Indicator_ADI", "ADI_EMA > 10"))
        marketRules.append(MarketRule("Indicator_ADI", "ADI_EMA > 20"))
        marketRules.append(MarketRule("Indicator_ADI", "ADI_EMA < -5"))
        marketRules.append(MarketRule("Indicator_ADI", "ADI_EMA < -10"))
        marketRules.append(MarketRule("Indicator_ADI", "ADI_EMA < -20"))

        for marketRule in marketRules:
            marketRule.evaluateRule()

        TeamCity.setBuildResultText("Evaluated Rules")

    else:
        Logger.log(logging.ERROR, "Missing Options", {"scope": __name__, "options": str(argv)})
        usage()
        sys.exit(2)


def usage():
    print("")
    print("usage:")
    print("  EvaluateRules.py -n name [-d] [-h]")
    print("")
    print("arguments:")
    print("  -n, --name        Name")
    print("")
    print("optional arguments:")
    print("  -d, --debug       Change the Log Level to Debug")
    print("  -h, --help        Display Usage Information")


if __name__ == "__main__":
    evaluateRules(sys.argv[1:])