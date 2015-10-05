import datetime
import logging
import sqlite3

from pandas.io.data import DataReader
from pandas.io.sql import read_sql_query

from utils.Logger import Logger
import pyswing.constants


def getStrategies():

    connection = sqlite3.connect(pyswing.constants.pySwingDatabase)

    query = "select distinct r1.rule, r2.rule from Rules r1 inner join Rules r2 on 1 == 1 where r1.MatchesPerDay * r2.MatchesPerDay > 0.1 and r1.rule != r2.rule"

    strategies = None

    cursor = connection.cursor()
    try:
        cursor.execute(query)
        strategies = cursor.fetchall()
    except sqlite3.OperationalError:
        Logger.log(logging.INFO, "Error Getting Strategies", {"scope":__name__})

    connection.close()

    return [(rules[0], rules[1]) for rules in strategies]


class Strategy(object):
    """
    ?
    """

    evaluateSql = ("insert into TwoRuleStrategy \n"
                   "select \n"
                   " %i as strategy,\n"
                   " '%s' as rule1,\n"
                   " '%s' as rule2, \n"
                   " '%s' as exit, \n"
                   " sum(ExitValue) / count(1) as resultPerTrade,\n"
                   " count(1) as numberOfTrades,\n"
                   " '%s' as type\n"
                   "from '%s' r1\n"
                   " inner join '%s' r2 on r1.Date = r2.Date and r1.Code = r2.Code and r2.Match = 1\n"
                   " inner join '%s' evb on evb.Date = r1.Date and evb.Code = r1.Code and evb.Type = '%s'\n"
                   "where\n"
                   " r1.Match = 1")

    def __init__(self, rule1, rule2, exit, type):
        """
        Constructor.

        :param rule: ?
        :param anotherRule: ?
        """

        # Logger.log(logging.DEBUG, "Log Object Creation", {"scope":__name__, "arguments":" ".join({rule, anotherRule})})

        self._rule1 = rule1
        self._rule2 = rule2
        self._exit = exit
        self._type = type


    def evaluateStrategy(self):
        """
        ?
        """

        Logger.log(logging.INFO, "Evaluating Strategy", {"scope":__name__, "Strategy":str(self)})

        connection = sqlite3.connect(pyswing.constants.pySwingDatabase)
        c = connection.cursor()
        c.executescript(self.evaluateSql % (pyswing.constants.pySwingStrategy, self._rule1, self._rule2, self._exit, self._type, self._rule1, self._rule2, self._exit, self._type))
        connection.commit()
        c.close()
        connection.close()

