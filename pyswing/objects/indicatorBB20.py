from talib import abstract

from pyswing.objects.indicator import Indicator


class IndicatorBB20(Indicator):
    """
    Bollinger Band Indicator(s).

    20 Day SMA with 2x Standard Deviations
    """

    def __init__(self, equityDataFrame, tickerCode):
        """
        Create the Bollinger Band-specific logic. Everything else lives in the Indicator Base Class.

        :param equityDataFrame: A Pandas DataFrame from the Equity Class.
        :param tickerCode: Ticker Code (String).
        """

        tableName = "Indicator_BB20"
        tickerCode = tickerCode

        insertQuery = "insert or replace into %s (Date, upperband, middleband, lowerband, Code, upperbandmom, middlebandmom, lowerbandmom) values (?,?,?,?,?,?,?,?)" % (tableName)

        equityDataFrame = equityDataFrame

        # Stick the Indicator Values into the new DataFrame
        indicatorDataFrame = abstract.BBANDS(equityDataFrame, 20, 2, 2, price='Close')
        indicatorDataFrame['Code'] = tickerCode
        indicatorDataFrame['upperbandmom'] = abstract.MOM(indicatorDataFrame, timeperiod=5, price='upperband')
        indicatorDataFrame['middlebandmom'] = abstract.MOM(indicatorDataFrame, timeperiod=5, price='middleband')
        indicatorDataFrame['lowerbandmom'] = abstract.MOM(indicatorDataFrame, timeperiod=5, price='lowerband')

        Indicator.__init__(self, tableName, tickerCode, insertQuery, equityDataFrame, indicatorDataFrame)