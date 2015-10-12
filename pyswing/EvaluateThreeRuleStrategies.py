import logging
import getopt
import sys

from utils.Logger import Logger
from pyswing.objects.strategy import Strategy, getRules, getBestUnprocessedTwoRuleStrategy, markTwoRuleStrategyAsProcessed, deleteEmptyThreeRuleStrategies
from utils.TeamCity import TeamCity
import pyswing.constants


def evaluateThreeRuleStrategies(argv):
    """
    Evaluate Three-Rule Strategies.

    :param argv: Command Line Parameters.

    -n = Name
    -N = Number of Two-Rule Strategies to Work Through
    -s = Strategy Name
    -t = Minimum Number of Trades

    Example:

    python -m pyswing.EvaluateThreeRuleStrategies -n asx -N 10 -s v4.0 -t 400
    """

    Logger.log(logging.INFO, "Log Script Call", {"scope":__name__, "arguments":" ".join(argv)})
    Logger.pushLogData("script", __name__)

    marketName = ""
    numberOfStrategies = ""
    numberOfTrades = ""

    try:
        shortOptions = "n:N:s:t:dh"
        longOptions = ["marketName=","number=", "strategy=", "trades=", "debug", "help"]
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
        elif opt in ("-N", "--number"):
            numberOfStrategies = int(arg)
        elif opt in ("-s", "--strategy"):
            pyswing.constants.pySwingStrategy = arg
        elif opt in ("-t", "--trades"):
            numberOfTrades = arg

    if marketName != "" and numberOfTrades != "" and numberOfStrategies > 0 and pyswing.constants.pySwingStrategy:

        Logger.log(logging.INFO, "Evaluate Three-Rule Strategies", {"scope":__name__, "market":marketName, "number":str(numberOfStrategies), "strategy":pyswing.constants.pySwingStrategy})

        rules = getRules()

        strategiesEvaluated = 0
        while strategiesEvaluated < numberOfStrategies:

            rule1, rule2, type = getBestUnprocessedTwoRuleStrategy(numberOfTrades)
            for rule3 in rules:
                strategy = Strategy(rule1, rule2, "Exit TrailingStop3.0 RiskRatio2", type, rule3)
                strategy.evaluateThreeRuleStrategy()

            markTwoRuleStrategyAsProcessed(rule1, rule2, type)

            strategiesEvaluated += 1

        deleteEmptyThreeRuleStrategies()

        TeamCity.setBuildResultText("Evaluated Three-Rule Strategies")

    else:
        Logger.log(logging.ERROR, "Missing Options", {"scope": __name__, "options": str(argv)})
        usage()
        sys.exit(2)


def usage():
    print("")
    print("usage:")
    print("  EvaluateThreeRuleStrategies.py -n name [-d] [-h]")
    print("")
    print("arguments:")
    print("  -n, --name        Name")
    print("  -N, --number      Number of Strategies to Evaluate")
    print("  -s, --strategy    Strategy Name")
    print("  -t, --trades      Minimum Number of Trades for Strategy")
    print("")
    print("optional arguments:")
    print("  -d, --debug       Change the Log Level to Debug")
    print("  -h, --help        Display Usage Information")


if __name__ == "__main__":
    evaluateThreeRuleStrategies(sys.argv[1:])