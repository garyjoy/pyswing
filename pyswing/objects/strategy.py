import datetime
import logging
import sqlite3

from pandas.io.data import DataReader
from pandas.io.sql import read_sql_query

from utils.Logger import Logger
import pyswing.constants


def getRules():

    connection = sqlite3.connect(pyswing.constants.pySwingDatabase)

    query = "select rule from Rules"

    rules = None

    cursor = connection.cursor()
    try:
        cursor.execute(query)
        rules = cursor.fetchall()
    except sqlite3.OperationalError:
        Logger.log(logging.INFO, "Error Getting Strategies", {"scope":__name__})

    connection.close()

    rulesList = []
    for rule in rules:
        rulesList.append(rule[0])

    return rulesList


def getTwoRuleStrategies(minimumMatchesPerDay):

    connection = sqlite3.connect(pyswing.constants.pySwingDatabase)

    query = "select distinct r1.rule, r2.rule from Rules r1 inner join Rules r2 on 1 == 1 where r1.MatchesPerDay * r2.MatchesPerDay > %s and r1.rule != r2.rule" % minimumMatchesPerDay

    strategies = None

    cursor = connection.cursor()
    try:
        cursor.execute(query)
        strategies = cursor.fetchall()
    except sqlite3.OperationalError:
        Logger.log(logging.INFO, "Error Getting Strategies", {"scope":__name__})

    connection.close()

    return [(rules[0], rules[1]) for rules in strategies]


def getBestUnprocessedTwoRuleStrategy(numberOfTrades):

    connection = sqlite3.connect(pyswing.constants.pySwingDatabase)

    query = "select rule1, rule2 from TwoRuleStrategy where numberOfTrades > %s and Searched = 0 order by resultPerTrade desc limit 1;" % numberOfTrades

    rules = None

    cursor = connection.cursor()
    try:
        cursor.execute(query)
        rules = cursor.fetchall()
    except sqlite3.OperationalError:
        Logger.log(logging.INFO, "Error Getting Strategy", {"scope":__name__})

    connection.close()

    return (rules[0][0], rules[0][1])


def markTwoRuleStrategyAsProcessed(rule1, rule2):

    connection = sqlite3.connect(pyswing.constants.pySwingDatabase)

    query = "update TwoRuleStrategy set Searched = 1 where rule1 = '%s' and rule2 = '%s';" % (rule1, rule2)

    cursor = connection.cursor()
    try:
        cursor.execute(query)
        connection.commit()
    except sqlite3.OperationalError:
        Logger.log(logging.INFO, "Error Updating Strategy", {"scope":__name__})

    connection.close()


def deleteEmptyThreeRuleStrategies():

    connection = sqlite3.connect(pyswing.constants.pySwingDatabase)

    query = "delete from ThreeRuleStrategy where resultPerTrade is NULL"

    cursor = connection.cursor()
    try:
        cursor.execute(query)
        connection.commit()
    except sqlite3.OperationalError:
        Logger.log(logging.INFO, "Error Deleting Empty Three Rule Strategies", {"scope":__name__})

    connection.close()


class Strategy(object):
    """
    ?
    """

    evaluateTwoRuleSql = ("insert into TwoRuleStrategy \n"
                   "select \n"
                   " '%s' as strategy,\n"
                   " '%s' as rule1,\n"
                   " '%s' as rule2, \n"
                   " '%s' as exit, \n"
                   " sum(ExitValue) / count(1) as resultPerTrade,\n"
                   " count(1) as numberOfTrades,\n"
                   " '%s' as type,\n"
                   " 0 as Searched\n"
                   "from '%s' r1\n"
                   " inner join '%s' r2 on r1.Date = r2.Date and r1.Code = r2.Code and r2.Match = 1\n"
                   " inner join '%s' evb on evb.MatchDate = r1.Date and evb.Code = r1.Code and evb.Type = '%s'\n"
                   "where\n"
                   " r1.Match = 1")

    evaluateThreeRuleSql = ("insert into ThreeRuleStrategy \n"
                   "select \n"
                   " '%s' as strategy,\n"
                   " '%s' as rule1,\n"
                   " '%s' as rule2, \n"
                   " '%s' as rule3, \n"
                   " '%s' as exit, \n"
                   " sum(ExitValue) / count(1) as resultPerTrade,\n"
                   " count(1) as numberOfTrades,\n"
                   " '%s' as type,\n"
                   " 0 as Searched\n"
                   "from '%s' r1\n"
                   " inner join '%s' r2 on r1.Date = r2.Date and r1.Code = r2.Code and r2.Match = 1\n"
                   " inner join '%s' r3 on r1.Date = r3.Date and r1.Code = r3.Code and r3.Match = 1\n"
                   " inner join '%s' evb on evb.MatchDate = r1.Date and evb.Code = r1.Code and evb.Type = '%s'\n"
                   "where\n"
                   " r1.Match = 1")

    def __init__(self, rule1, rule2, exit, type, rule3=None):
        """
        Constructor.

        :param rule: ?
        :param anotherRule: ?
        """

        # Logger.log(logging.DEBUG, "Log Object Creation", {"scope":__name__, "arguments":" ".join({rule, anotherRule})})

        self._rule1 = rule1
        self._rule2 = rule2
        self._rule3 = rule3
        self._exit = exit
        self._type = type


    def evaluateTwoRuleStrategy(self):
        """
        ?
        """

        Logger.log(logging.INFO, "Evaluating Two-Rule Strategy", {"scope":__name__, "Rule 1":self._rule1, "Rule 2":self._rule2})

        connection = sqlite3.connect(pyswing.constants.pySwingDatabase)
        c = connection.cursor()
        sql = self.evaluateTwoRuleSql % (pyswing.constants.pySwingStrategy, self._rule1, self._rule2, self._exit, self._type, self._rule1, self._rule2, self._exit, self._type)
        # print(sql)
        c.executescript(sql)
        connection.commit()
        c.close()
        connection.close()

    def evaluateThreeRuleStrategy(self):
        """
        ?
        """

        Logger.log(logging.INFO, "Evaluating Three-Rule Strategy", {"scope":__name__, "Rule 1":self._rule1, "Rule 2":self._rule2, "Rule 3":self._rule3})

        connection = sqlite3.connect(pyswing.constants.pySwingDatabase)
        c = connection.cursor()
        sql = self.evaluateThreeRuleSql % (pyswing.constants.pySwingStrategy, self._rule1, self._rule2, self._rule3, self._exit, self._type, self._rule1, self._rule2, self._rule3, self._exit, self._type)
        # print(sql)
        c.executescript(sql)
        connection.commit()
        c.close()
        connection.close()
