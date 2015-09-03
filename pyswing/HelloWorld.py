import logging
import getopt
import sys
import datetime
import sqlite3

import pandas.io.data as web

from utils.Logger import Logger


def helloWorld(argv):
    """
    ?

    :param argv: Command Line Parameters.

    -n = Name

    Example:

    python -m pyswing.HelloWorld -n Gary
    """

    Logger.log(logging.INFO, "Log Script Call", {"scope":__name__, "arguments":" ".join(argv)})
    Logger.pushLogData("script", __name__)

    name = ""

    try:
        shortOptions = "n:dh"
        longOptions = ["name=", "debug", "help"]
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
        elif opt in ("-n", "--name"):
            name = arg

    if name != "":

        print("Loading Data for %s..." % (name))

        start = datetime.datetime(2010, 1, 1)
        end = datetime.datetime(2010, 2, 1)
        f = web.DataReader(name, 'yahoo', start, end)

        f['Equity'] = name

        print(f.ix['2010-01-04'])

        connection = sqlite3.connect('output/helloWorld.db')
        f.to_sql("helloWorld", connection)

    else:
        Logger.log(logging.ERROR, "Missing Options", {"scope": __name__, "options": str(argv)})
        usage()
        sys.exit(2)


def usage():
    print("")
    print("usage:")
    print("  HelloWorld.py -n name [-d] [-h]")
    print("")
    print("arguments:")
    print("  -n, --name        Name")
    print("")
    print("optional arguments:")
    print("  -d, --debug       Change the Log Level to Debug")
    print("  -h, --help        Display Usage Information")


if __name__ == "__main__":
    helloWorld(sys.argv[1:])