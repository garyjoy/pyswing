import logging
import sqlite3

from pandas.io.sql import read_sql_query

from pyswing.objects.exitValues import ExitValues
from utils.Logger import Logger
import pyswing.constants


class ExitValuesTrailingStop(ExitValues):
    """
    Exit Values Trailing Stop Class.
    """

    def __init__(self, tickerCode, maximumLoss, riskRatio):
        """
        Base Class Constructor.

        :param tickerCode: Ticker Code
        :param maximumLoss: The Maximum Loss (e.g. 0.03)
        :param riskRatio: The Risk Ratio (e.g. 2)
        """

        # Logger.log(logging.DEBUG, "Log Object Creation", {"scope":__name__, "arguments":" ".join({""})})

        self._tableName = "Exit TrailingStop%s RiskRatio%s" % (str(maximumLoss * 100), str(riskRatio))

        self._maximumLoss = maximumLoss
        self._riskRatio = riskRatio

        ExitValues.__init__(self, tickerCode)

    def calculateExitValueForBuy(self, rowIndex, numberOfRows):

        fillDay = self._buyExitValueDataFrame.irow(rowIndex, "Open")
        fillValue = fillDay["Open"]

        stop = fillValue * (1 - self._maximumLoss)
        limit = fillValue * (1 + (2 * self._maximumLoss))

        numberOfDays = 0
        exitValue = None
        exitDetail = None

        ended = False

        while not ended and numberOfDays < numberOfRows:

            day = self._buyExitValueDataFrame.irow(rowIndex + numberOfDays)
            open = day["Open"]
            high = day["High"]
            low = day["Low"]

            if open < stop and numberOfDays > 0:
                exitValue = open
                ended = True
                exitDetail = "Gapped Below Stop (%f) on Day %i (Open=%f and Close=%f)" % (stop, (numberOfDays + 1), fillValue, exitValue)

            elif open > limit and numberOfDays > 0:
                exitValue = open
                ended = True
                exitDetail = "Gapped Above Limit (%f) on Day %i (Open=%i and Close=%f)" % (limit, (numberOfDays + 1), fillValue, exitValue)

            elif low < stop:
                exitValue = stop
                ended = True
                exitDetail = "Dropped Below Stop (%f) on Day %i (Open=%f and Close=%f)" % (stop, (numberOfDays + 1), fillValue, exitValue)

            elif high > limit:
                exitValue = limit
                ended = True
                exitDetail = "Passed Limit (%f) on Day %i (Open=%f and Close=%f)" % (limit, (numberOfDays + 1), fillValue, exitValue)

            if not ended:
                potentialStop = high * (1 - self._maximumLoss)
                if potentialStop > stop:
                    stop = potentialStop

            numberOfDays = numberOfDays + 1

        if ended:

            self._buyExitValueDataFrame.loc[fillDay.name, "Type"] = "Buy"
            self._buyExitValueDataFrame.loc[fillDay.name, "ExitValue"] = ((exitValue - fillValue) / fillValue * 100)
            self._buyExitValueDataFrame.loc[fillDay.name, "NumberOfDays"] = numberOfDays
            self._buyExitValueDataFrame.loc[fillDay.name, "ExitDetail"] = exitDetail

    def calculateExitValueForSell(self, rowIndex, numberOfRows):

        fillDay = self._sellExitValueDataFrame.irow(rowIndex, "Open")
        fillValue = fillDay["Open"]

        stop = fillValue * (1 + self._maximumLoss)
        limit = fillValue * (1 - (2 * self._maximumLoss))

        numberOfDays = 0
        exitValue = None
        exitDetail = None

        ended = False

        while not ended and numberOfDays < numberOfRows:

            day = self._sellExitValueDataFrame.irow(rowIndex + numberOfDays)
            open = day["Open"]
            high = day["High"]
            low = day["Low"]

            if open > stop and numberOfDays > 0:
                exitValue = open
                ended = True
                exitDetail = "Gapped Above Stop (%f) on Day %i (Open=%f and Close=%f)" % (stop, (numberOfDays + 1), fillValue, exitValue)

            elif open < limit and numberOfDays > 0:
                exitValue = open
                ended = True
                exitDetail = "Gapped Below Limit (%f) on Day %i (Open=%i and Close=%f)" % (limit, (numberOfDays + 1), fillValue, exitValue)

            elif high > stop:
                exitValue = stop
                ended = True
                exitDetail = "Passed Stop (%f) on Day %i (Open=%f and Close=%f)" % (stop, (numberOfDays + 1), fillValue, exitValue)

            elif low < limit:
                exitValue = limit
                ended = True
                exitDetail = "Dropped Below Limit (%f) on Day %i (Open=%f and Close=%f)" % (limit, (numberOfDays + 1), fillValue, exitValue)

            if not ended:
                potentialStop = low * (1 + self._maximumLoss)
                if potentialStop < stop:
                    stop = potentialStop

            numberOfDays = numberOfDays + 1

        if ended:
            exitValueAsPercent = ((fillValue - exitValue) / fillValue * 100)

            if exitValueAsPercent > 10:
                exitValueAsPercent = 10.0
                exitDetail = exitDetail + " (Modified)"

            if exitValueAsPercent < -10:
                exitValueAsPercent = -10.0
                exitDetail = exitDetail + " (Modified)"

            self._sellExitValueDataFrame.loc[fillDay.name, "Type"] = "Sell"
            self._sellExitValueDataFrame.loc[fillDay.name, "ExitValue"] = exitValueAsPercent
            self._sellExitValueDataFrame.loc[fillDay.name, "NumberOfDays"] = numberOfDays
            self._sellExitValueDataFrame.loc[fillDay.name, "ExitDetail"] = exitDetail
