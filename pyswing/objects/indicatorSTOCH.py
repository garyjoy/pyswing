from talib import abstract

from pyswing.objects.indicator import Indicator


class IndicatorSTOCH(Indicator):
    """
    (Slow) Stochastic Indicator(s).
    """

    def __init__(self, equityDataFrame, tickerCode):
        """
        Create the STOCH-specific logic. Everything else lives in the Indicator Base Class.

        :param equityDataFrame: A Pandas DataFrame from the Equity Class.
        :param tickerCode: Ticker Code (String).
        """

        tableName = "Indicator_STOCH"
        tickerCode = tickerCode

        insertQuery = "insert or replace into %s (Date, STOCH_K, STOCH_D, STOCH_K_ROC, STOCH_D_ROC, Code) values (?,?,?,?,?,?)" % (tableName)

        # Stick the Indicator Values into the new DataFrame
        indicatorDataFrame = abstract.STOCH(equityDataFrame, fastk_period=5, slowk_period=3, slowk_matype=0, slowd_period=3, slowd_matype=0, prices=['High', 'Low', 'Close'])
        indicatorDataFrame['STOCH_K_ROC'] = abstract.ROC(indicatorDataFrame, timeperiod=5, price='slowk')
        indicatorDataFrame['STOCH_D_ROC'] = abstract.ROC(indicatorDataFrame, timeperiod=5, price='slowd')
        indicatorDataFrame['Code'] = tickerCode

        Indicator.__init__(self, tableName, tickerCode, insertQuery, equityDataFrame, indicatorDataFrame)