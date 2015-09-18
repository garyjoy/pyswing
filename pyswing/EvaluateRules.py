import logging
import getopt
import sys

from utils.Logger import Logger
from pyswing.objects.market import Market
from pyswing.objects.simpleRule import SimpleRule
from pyswing.objects.relativeRule import RelativeRule, Comparison
from pyswing.objects.crossingRule import CrossingRule
from pyswing.objects.multipleIndicatorRule import MultipleIndicatorRule
from utils.TeamCity import TeamCity


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

        Logger.log(logging.INFO, "Evaluate Rules", {"scope":__name__, "market":marketName})

        tickerCodesRelativeFilePath = "resources/%s.txt" % (marketName)

        market = Market(tickerCodesRelativeFilePath)

        rules = []
        rules.append(SimpleRule("Indicator_ROC", "ROC_5 > 20"))
        rules.append(SimpleRule("Indicator_ROC", "ROC_5 > 15"))
        rules.append(SimpleRule("Indicator_ROC", "ROC_5 > 10"))

        rules.append(SimpleRule("Indicator_ROC", "ROC_5 < -20"))
        rules.append(SimpleRule("Indicator_ROC", "ROC_5 < -15"))
        rules.append(SimpleRule("Indicator_ROC", "ROC_5 < -10"))

        rules.append(SimpleRule("Indicator_ROC", "ROC_10 > 25"))
        rules.append(SimpleRule("Indicator_ROC", "ROC_10 > 20"))
        rules.append(SimpleRule("Indicator_ROC", "ROC_10 > 15"))

        rules.append(SimpleRule("Indicator_ROC", "ROC_10 < -25"))
        rules.append(SimpleRule("Indicator_ROC", "ROC_10 < -20"))
        rules.append(SimpleRule("Indicator_ROC", "ROC_10 < -15"))

        rules.append(SimpleRule("Indicator_ROC", "ROC_20 > 35"))
        rules.append(SimpleRule("Indicator_ROC", "ROC_20 > 30"))
        rules.append(SimpleRule("Indicator_ROC", "ROC_20 > 20"))

        rules.append(SimpleRule("Indicator_ROC", "ROC_20 < -35"))
        rules.append(SimpleRule("Indicator_ROC", "ROC_20 < -30"))
        rules.append(SimpleRule("Indicator_ROC", "ROC_20 < -20"))

        rules.append(RelativeRule("Equities", "Close", -1, Comparison.GreaterThan, 1.01))
        rules.append(RelativeRule("Equities", "Close", -1, Comparison.LessThan, 0.99))

        rules.append(RelativeRule("Equities", "Close", -1, Comparison.GreaterThan, 1.02))
        rules.append(RelativeRule("Equities", "Close", -1, Comparison.LessThan, 0.98))

        rules.append(RelativeRule("Equities", "Close", -1, Comparison.GreaterThan, 1.03))
        rules.append(RelativeRule("Equities", "Close", -1, Comparison.LessThan, 0.97))

        rules.append(RelativeRule("Equities", "Close", -1, Comparison.GreaterThan, 1.05))
        rules.append(RelativeRule("Equities", "Close", -1, Comparison.LessThan, 0.95))

        rules.append(RelativeRule("Equities", "Close", -5, Comparison.GreaterThan, 1.10))
        rules.append(RelativeRule("Equities", "Close", -5, Comparison.LessThan, 0.90))

        rules.append(RelativeRule("Equities", "Close", -5, Comparison.GreaterThan, 1.20))
        rules.append(RelativeRule("Equities", "Close", -5, Comparison.LessThan, 0.80))

        rules.append(CrossingRule("Indicator_SMA","SMA_5","Indicator_SMA","SMA_20"))
        rules.append(CrossingRule("Indicator_SMA","SMA_10","Indicator_SMA","SMA_50"))
        rules.append(CrossingRule("Indicator_SMA","SMA_10","Indicator_SMA","SMA_200"))
        rules.append(CrossingRule("Indicator_SMA","SMA_20","Indicator_SMA","SMA_200"))

        rules.append(MultipleIndicatorRule("Equities", "Indicator_SMA", "t1.Close > t2.SMA_200"))
        rules.append(MultipleIndicatorRule("Equities", "Indicator_SMA", "t1.Close > 1.1 * t2.SMA_200"))
        rules.append(MultipleIndicatorRule("Equities", "Indicator_SMA", "t1.Close > 1.2 * t2.SMA_200"))

        rules.append(MultipleIndicatorRule("Equities", "Indicator_SMA", "t1.Close < t2.SMA_200"))
        rules.append(MultipleIndicatorRule("Equities", "Indicator_SMA", "t1.Close < 0.9 * t2.SMA_200"))
        rules.append(MultipleIndicatorRule("Equities", "Indicator_SMA", "t1.Close < 0.8 * t2.SMA_200"))

        for index, row in market.tickers.iterrows():

            tickerCode = row[0]

            for rule in rules:
                rule.evaluateRule(tickerCode)

        TeamCity.setBuildResultText("Evaluated Rules")

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
    evaluateRules(sys.argv[1:])