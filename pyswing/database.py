import logging
import os
import pwd

from pyswing.utils.Logger import Logger


pySwingDatabase = None

pySwingDatabaseInitialised = False
pySwingDatabaseOverridden = False

pySwingTestDatabase = "resources/TestDatabase.db"


def initialiseDatabase(market):
    """
    Initialise "pySwingDatabase" (i.e. file path to the SQL Lite database) for the specified market.

    :param market: String (e.g. "ASX", "FTSE" or "unitTesting")
    """

    Logger.log(logging.INFO, "Initialise Database", {"scope": __name__, "market": market})

    pySwingDatabaseTemplate = "%s/pyswing_%s.db"

    homeDirectory = pwd.getpwuid(os.getuid()).pw_dir

    global pySwingDatabase
    global pySwingDatabaseInitialised

    if not pySwingDatabaseOverridden:
        if pySwingDatabaseInitialised:
            Logger.log(logging.WARN, "Database Already Initialised", {"scope": __name__, "market": market, "pySwingDatabase": pySwingDatabase})
        pySwingDatabase = pySwingDatabaseTemplate % (homeDirectory, market)
        pySwingDatabaseInitialised = True
    else:
        Logger.log(logging.INFO, "Cannot Initialise on Overriden Database", {"scope": __name__, "market": market, "pySwingDatabase": pySwingDatabase})


def overrideDatabase(override):
    """
    Override "pySwingDatabase" (i.e. file path to the SQL Lite database).

    This should only be used for Unit Testing.

    :param override: String (e.g. "output/TestEvaluateRules.db")
    """

    Logger.log(logging.INFO, "Override Database", {"scope": __name__, "override": override})

    global pySwingDatabase
    pySwingDatabase = override

    global pySwingDatabaseOverridden
    pySwingDatabaseOverridden = True
