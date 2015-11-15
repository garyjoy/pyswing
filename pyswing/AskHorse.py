import logging
import getopt
import sys
import smtplib

from pyswing.utils.Logger import Logger
from pyswing.objects.strategy import getActiveStrategies, getLatestDate
from pyswing.utils.TeamCity import TeamCity


def askHorse(argv):
    """
    "Ask Horse" i.e. Check the Active Strategies against the most recent data...

    :param argv: Command Line Parameters.

    -n = Name

    Example:

    python -m pyswing.AskHorse -n asx
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

        latestDate = getLatestDate()
        # latestDate = '2015-10-07 00:00:00'

        Logger.log(logging.INFO, "Ask Horse", {"scope":__name__, "market":marketName, "latestDate":latestDate})

        strategies = getActiveStrategies()

        tradeDetails = []
        for strategy in strategies:
            rulesDetail = ("Rules: '%s', '%s' and '%s'") % (strategy._rule1, strategy._rule2, strategy._rule3)
            Logger.log(logging.INFO, "Checking Strategy", {"scope":__name__, "strategy":rulesDetail})
            if strategy.askHorse(latestDate):
                tradeDetails.extend(strategy.tradeDetails)

        sendEmail(tradeDetails)

        if len(tradeDetails) > 0:
            TeamCity.setBuildResultText("Horse Says Trade! (x%s)" % len(tradeDetails))
        else:
            TeamCity.setBuildResultText("Horse Says Go Back To Bed!")

    else:
        Logger.log(logging.ERROR, "Missing Options", {"scope": __name__, "options": str(argv)})
        usage()
        sys.exit(2)


def sendEmail(tradeDetails):

    message = "Hello!\n\n"
    for trade in tradeDetails:
        message += trade
        message += "\n\n"

    message += "x"

    subject = None
    if len(tradeDetails) > 0:
        subject = "Horse Says Trade!"
    else:
        subject = "Horse Says Go Back To Bed!"

    header  = 'From: %s\n' % "horseofjoy@gmail.com"
    header += 'To: %s\n' % ','.join(["gary.joy@gmail.com"])
    header += 'Subject: %s\n\n' % subject
    message = header + message

    server = smtplib.SMTP("smtp.gmail.com:587")
    server.starttls()
    server.login("horseofjoy@gmail.com", "abcABC1234567890")
    problems = server.sendmail("horseofjoy@gmail.com", ["gary.joy@gmail.com"], message)
    server.quit()

    if problems:
        Logger.log(logging.ERROR, "Error Sending E-mail", {"scope": __name__, "problems": str(problems)})


def usage():
    print("")
    print("usage:")
    print("  AskHorse.py -n name [-d] [-h]")
    print("")
    print("arguments:")
    print("  -n, --name        Name")
    print("")
    print("optional arguments:")
    print("  -d, --debug       Change the Log Level to Debug")
    print("  -h, --help        Display Usage Information")


if __name__ == "__main__":
    askHorse(sys.argv[1:])