import datetime
import logging
import sqlite3

from pandas.io.data import DataReader
from pandas.io.sql import read_sql_query
from pandas import expanding_max, expanding_min, expanding_sum
from numpy import sqrt

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
        Logger.log(logging.INFO, "Error Getting Rules", {"scope":__name__})

    connection.close()

    rulesList = []
    for rule in rules:
        rulesList.append(rule[0])

    return rulesList


def getStrategies(numberOfTrades, returnPerTrade):

    connection = sqlite3.connect(pyswing.constants.pySwingDatabase)

    query = "select rule1, rule2, rule3, exit, type from ThreeRuleStrategy where numberOfTrades > %s and resultPerTrade > %s" % (numberOfTrades, returnPerTrade)

    strategies = None

    cursor = connection.cursor()
    try:
        cursor.execute(query)
        strategies = cursor.fetchall()
    except sqlite3.OperationalError:
        Logger.log(logging.INFO, "Error Getting Strategies", {"scope":__name__})

    connection.close()

    strategiesList = []
    for strategyRow in strategies:
        strategy = Strategy(strategyRow[0], strategyRow[1], strategyRow[3], strategyRow[4], strategyRow[2])
        strategiesList.append(strategy)

    return strategiesList


def getLatestDate():

    connection = sqlite3.connect(pyswing.constants.pySwingDatabase)

    query = "select max(Date) from Equities"

    latestDate = None

    cursor = connection.cursor()
    try:
        cursor.execute(query)
        resultSet = cursor.fetchall()
        latestDate = resultSet[0][0]
    except sqlite3.OperationalError:
        Logger.log(logging.INFO, "Error Getting Latest Date", {"scope":__name__})

    connection.close()

    return latestDate


def getActiveStrategies():

    connection = sqlite3.connect(pyswing.constants.pySwingDatabase)

    query = "select rule1, rule2, exit, type, rule3, meanResultPerTrade, medianResultPerTrade, totalProfit, numberOfTrades, sharpeRatio, maximumDrawdown from Strategy where active = 1"

    strategies = None

    cursor = connection.cursor()
    try:
        cursor.execute(query)
        strategies = cursor.fetchall()
    except sqlite3.OperationalError:
        Logger.log(logging.INFO, "Error Getting Strategies", {"scope":__name__})

    connection.close()

    strategiesList = []
    for strategyRow in strategies:

        strategy = Strategy(strategyRow[0], strategyRow[1], strategyRow[2], strategyRow[3], strategyRow[4])
        strategiesList.append(strategy)

        strategy.meanResultPerTrade = strategyRow[5]
        strategy.medianResultPerTrade = strategyRow[6]
        strategy.totalProfit = strategyRow[7]
        strategy.numberOfTrades = strategyRow[8]
        strategy.sharpeRatio = strategyRow[9]
        strategy.maximumDrawdown = strategyRow[10]

    return strategiesList


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

    # TODO:  Implement Sell
    query = "select rule1, rule2, type from TwoRuleStrategy where numberOfTrades > %s and Searched = 0 order by resultPerTrade desc limit 1;" % numberOfTrades

    rowData = None

    cursor = connection.cursor()
    try:
        cursor.execute(query)
        rowData = cursor.fetchall()
    except sqlite3.OperationalError:
        Logger.log(logging.INFO, "Error Getting Strategy", {"scope":__name__})

    connection.close()

    return (rowData[0][0], rowData[0][1], rowData[0][2])


def markTwoRuleStrategyAsProcessed(rule1, rule2, type):

    connection = sqlite3.connect(pyswing.constants.pySwingDatabase)

    query = "update TwoRuleStrategy set Searched = 1 where rule1 = '%s' and rule2 = '%s' and type = '%s';" % (rule1, rule2, type)

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


def emptyHistoricTradesTable():

    connection = sqlite3.connect(pyswing.constants.pySwingDatabase)

    query = "delete from HistoricTrades"

    cursor = connection.cursor()
    try:
        cursor.execute(query)
        connection.commit()
    except sqlite3.OperationalError:
        Logger.log(logging.INFO, "Error Deleting Historic Trades", {"scope":__name__})

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

    analyseStrategySql = ("select r1.Code, r1.Date, ev.Type, ev.ExitValue, ev.NumberOfDays, ev.ExitDetail \n"
        "from '%s' r1  \n"
        " inner join '%s' r2 on r2.Match = 1 and r1.Date = r2.Date and r1.Code = r2.Code \n"
        " inner join '%s' r3 on r3.Match = 1 and r1.Date = r3.Date and r1.Code = r3.Code \n"
        " inner join '%s' ev on r1.Date = ev.MatchDate and r1.Code = ev.Code and ev.Type = '%s' \n"
        " where r1.Match = 1 \n"
        "order by r1.Date asc")

    deleteStrategySql = ("delete from Strategy where strategy = '%s' and rule1 = '%s' and rule2='%s' and rule3= '%s' and exit = '%s' and type = '%s'")

    insertStrategySql = ("insert into Strategy (strategy,rule1,rule2,rule3,exit,type,meanResultPerTrade,medianResultPerTrade,totalProfit,numberOfTrades,sharpeRatio,maximumDrawdown,active) "
                         "values ('%s', '%s', '%s', '%s', '%s', '%s', %s, %s, %s, %s, %s, %s, 0);")

    insertIntoHistoricTradesSql = ("insert into HistoricTrades\n"
        "select r1.Date as matchDate, r1.Code, '%s' as type from '%s' r1\n"
        "inner join '%s' r2 on r1.Date = r2.Date and r1.Code = r2.Code and r2.Match = 1\n"
        "inner join '%s' r3 on r1.Date = r3.Date and r1.Code = r3.Code and r2.Match = 1\n"
        "inner join '%s' evs on evs.Date = r1.Date and evs.Code = r1.Code and evs.Type = '%s'\n"
        "where r1.Match = 1")


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

        Logger.log(logging.INFO, "Evaluating Three-Rule Strategy", {"scope":__name__, "Rule 1":self._rule1, "Rule 2":self._rule2, "Rule 3":self._rule3, "Type":self._type})

        connection = sqlite3.connect(pyswing.constants.pySwingDatabase)
        c = connection.cursor()
        sql = self.evaluateThreeRuleSql % (pyswing.constants.pySwingStrategy, self._rule1, self._rule2, self._rule3, self._exit, self._type, self._rule1, self._rule2, self._rule3, self._exit, self._type)
        c.executescript(sql)
        connection.commit()
        c.close()
        connection.close()

    def analyse(self):

        # Logger.log(logging.INFO, "Analyse Strategy", {"scope":__name__, "Rule 1":self._rule1, "Rule 2":self._rule2, "Rule 3":self._rule3, "Type":self._type})

        connection = sqlite3.connect(pyswing.constants.pySwingDatabase)
        query = self.analyseStrategySql % (self._rule1, self._rule2, self._rule3, self._exit, self._type)
        self._strategyData = read_sql_query(query, connection, 'Date')
        self._strategyData['ExitValueAfterCosts'] = self._strategyData['ExitValue'] - 0.2
        connection.close()

        exitValueDataFrame = self._strategyData.ix[:,'ExitValueAfterCosts']

        mean = exitValueDataFrame.mean()
        median = exitValueDataFrame.median()
        sum = exitValueDataFrame.sum()
        count = exitValueDataFrame.count()

        tradesPerYear = count / 10
        sharpeRatio = sqrt(tradesPerYear) * exitValueDataFrame.mean() / exitValueDataFrame.std()

        self._strategyData["Sum"] = expanding_sum(exitValueDataFrame)
        self._strategyData["Max"] = expanding_max(self._strategyData["Sum"])
        self._strategyData["Min"] = expanding_min(self._strategyData["Sum"])
        self._strategyData["DD"] = self._strategyData["Max"] - self._strategyData["Min"]

        runningSum = expanding_sum(exitValueDataFrame)
        max2here = expanding_max(runningSum)
        dd2here = runningSum - max2here
        drawDown = dd2here.min()

        Logger.log(logging.INFO, "Analysing Strategy", {"scope":__name__, "Rule 1":self._rule1, "Rule 2":self._rule2, "Rule 3":self._rule3, "Exit":self._exit, "Type":self._type, "Mean":str(mean), "Median":str(median), "Sum":str(sum), "Count":str(count), "SharpeRatio":str(sharpeRatio), "DrawDown":str(drawDown)})

        connection = sqlite3.connect(pyswing.constants.pySwingDatabase)
        c = connection.cursor()

        deleteSql = self.deleteStrategySql % (pyswing.constants.pySwingStrategy, self._rule1, self._rule2, self._rule3, self._exit, self._type)
        c.executescript(deleteSql)
        connection.commit()

        insertSql = self.insertStrategySql % (pyswing.constants.pySwingStrategy, self._rule1, self._rule2, self._rule3, self._exit, self._type, str(mean), str(median), str(sum), str(count), str(sharpeRatio), str(drawDown))
        c.executescript(insertSql)
        connection.commit()

        c.close()
        connection.close()

    def askHorse(self, latestDate):

        self.tradeDetails = []

        connection = sqlite3.connect(pyswing.constants.pySwingDatabase)

        query = ("select r1.Code, r1.Date "
            "from '%s' r1 "
            " inner join '%s' r2 on r2.Match = 1 and r1.Date = r2.Date and r1.Code = r2.Code "
            " inner join '%s' r3 on r3.Match = 1 and r1.Date = r3.Date and r1.Code = r3.Code "
            "where r1.Match = 1 and r1.Date = '%s'") % (self._rule1, self._rule2, self._rule3, latestDate)

        trades = None

        cursor = connection.cursor()
        try:
            cursor.execute(query)
            trades = cursor.fetchall()
        except sqlite3.OperationalError:
            Logger.log(logging.INFO, "Error Getting Trades", {"scope":__name__})

        connection.close()

        for trade in trades:
            tradeSummary = ("%s %s using %s") % (self._type, trade[0], self._exit)
            strategyDetail = ("Strategy: Mean: %s, Median: %s, Total: %s, Trades: %s, Sharpe Ratio: %s, Drawdown: %s") % (str(self.meanResultPerTrade), str(self.medianResultPerTrade), str(self.totalProfit), str(self.numberOfTrades), str(self.sharpeRatio), str(self.maximumDrawdown))
            rulesDetail = ("Rules: '%s', '%s' and '%s'") % (self._rule1, self._rule2, self._rule3)

            tradeDetail = "%s (%s)\n%s" % (tradeSummary, strategyDetail, rulesDetail)
            self.tradeDetails.append(tradeDetail)
            Logger.log(logging.INFO, "Suggested Trade", {"scope":__name__, "tradeDetail":tradeDetail})

        return len(self.tradeDetails) > 0

    def generateHistoricTrades(self):
        """
        ?
        """

        Logger.log(logging.INFO, "Generating Historic Trades", {"scope":__name__, "Rule 1":self._rule1, "Rule 2":self._rule2, "Rule 3":self._rule3, "Type":self._type})

        connection = sqlite3.connect(pyswing.constants.pySwingDatabase)
        c = connection.cursor()
        sql = self.insertIntoHistoricTradesSql % (self._type, self._rule1, self._rule2, self._rule3, self._exit, self._type)
        c.executescript(sql)
        connection.commit()
        c.close()
        connection.close()
