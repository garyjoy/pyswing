import logging
import getopt
import sys

from pyswing.utils.Logger import Logger
from pyswing.objects.strategy import Strategy, getTwoRuleStrategies
from pyswing.objects.exitValues import getExitStrategies
from pyswing.utils.TeamCity import TeamCity

import pyswing.constants
import pyswing.database


def evaluateTwoRuleStrategies(argv):
    """
    Evaluate Two-Rule Strategies.

    :param argv: Command Line Parameters.

    -n = Name
    -m = Minimum Matches Per Day
    -s = Strategy Name

    Example:

    python -m pyswing.EvaluateTwoRuleStrategies -n asx -m 0.1 -s v4.0
    """

    Logger.log(logging.INFO, "Log Script Call", {"scope":__name__, "arguments":" ".join(argv)})
    Logger.pushLogData("script", __name__)

    marketName = ""
    minimumMatchesPerDay = None

    try:
        shortOptions = "n:m:s:dh"
        longOptions = ["marketName=", "matches=", "strategy=", "debug", "help"]
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
        elif opt in ("-m", "--matches"):
            minimumMatchesPerDay = arg
        elif opt in ("-s", "--strategy"):
            pyswing.constants.pySwingStrategy = arg

    if marketName != "" and minimumMatchesPerDay and pyswing.constants.pySwingStrategy:

        pyswing.database.initialiseDatabase(marketName)

        Logger.log(logging.INFO, "Evaluate Two-Rule Strategies", {"scope":__name__, "market":marketName, "matches":minimumMatchesPerDay, "strategy":pyswing.constants.pySwingStrategy})

        strategies = getTwoRuleStrategies(minimumMatchesPerDay)

        exits = getExitStrategies()

        inverseStrategies = set()

        for rules in strategies:
            if rules not in inverseStrategies:

                for exit in exits:

                    buyStrategy = Strategy(rules[0], rules[1], exit, 'Buy')
                    buyStrategy.evaluateTwoRuleStrategy()

                    sellStrategy = Strategy(rules[0], rules[1], exit, 'Sell')
                    sellStrategy.evaluateTwoRuleStrategy()

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
    print("  -m, --matches     Minimum Matches Per Day")
    print("  -s, --strategy    Strategy Name")
    print("")
    print("optional arguments:")
    print("  -d, --debug       Change the Log Level to Debug")
    print("  -h, --help        Display Usage Information")


if __name__ == "__main__":
    evaluateTwoRuleStrategies(sys.argv[1:])