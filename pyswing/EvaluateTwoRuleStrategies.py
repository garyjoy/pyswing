import logging
import getopt
import sys

from utils.Logger import Logger
from pyswing.objects.strategy import Strategy, getStrategies
from utils.TeamCity import TeamCity


def evaluateTwoRuleStrategies(argv):
    """
    Evaluate Two-Rule Strategies.

    :param argv: Command Line Parameters.

    -n = Name

    Example:

    python -m pyswing.EvaluateTwoRuleStrategies -n asx
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

        Logger.log(logging.INFO, "Evaluate Two-Rule Strategies", {"scope":__name__, "market":marketName})

        strategies = getStrategies()
        inverseStrategies = set()
        for rules in strategies:
            if rules not in inverseStrategies:
                buyStrategy = Strategy(rules[0], rules[1], "Exit TrailingStop3.0 RiskRatio2", 'Buy')
                buyStrategy.evaluateStrategy()
                sellStrategy = Strategy(rules[0], rules[1], "Exit TrailingStop3.0 RiskRatio2", 'Sell')
                sellStrategy.evaluateStrategy()
                inverseStrategies.add((rules[1], rules[0]))

        TeamCity.setBuildResultText("Evaluated Two-Rule Strategies")

    else:
        Logger.log(logging.ERROR, "Missing Options", {"scope": __name__, "options": str(argv)})
        usage()
        sys.exit(2)


def usage():
    print("")
    print("usage:")
    print("  EvaluateTwoRuleStrategies.py -n name [-d] [-h]")
    print("")
    print("arguments:")
    print("  -n, --name        Name")
    print("")
    print("optional arguments:")
    print("  -d, --debug       Change the Log Level to Debug")
    print("  -h, --help        Display Usage Information")


if __name__ == "__main__":
    evaluateTwoRuleStrategies(sys.argv[1:])