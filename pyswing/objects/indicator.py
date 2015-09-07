import logging

import pandas
import talib
import numpy

from utils.Logger import Logger
from pyswing.objects.equity import Equity
from talib import abstract

import pandas.io.data as web
import datetime


class Indicator(object):
    """
    An Indicator...
    """

    def __init__(self):
        """
        ?

        :param ?: ?
        """

        Logger.log(logging.DEBUG, "Log Object Creation", {"scope":__name__, "arguments":" ".join({""})})

        close = numpy.random.random(100)
        output = talib.SMA(close)

        print(close)
        print(output)

        equity = Equity("TLS.AX")
        cbaDataFrame = equity.dataFrame()

        # print(cbaDataFrame)


        sma = abstract.EMA
        cbaDataFrame['SMA_50'] = sma(cbaDataFrame, timeperiod=50, price='Close')
        cbaDataFrame['SMA_100'] = sma(cbaDataFrame, timeperiod=100, price='Close')

        # print(cbaDataFrame.ix['2015-09-01 00:00:00'])

        # myPlot = cbaDataFrame.plot(y= ['Close','SMA_50','SMA_100'], title='Gary')
        # fig = myPlot.get_figure()
        # fig.savefig('tls.png')

        bbFrame = abstract.BBANDS(cbaDataFrame, 20, 2, 2, price='Close')
        joinFrame = pandas.concat([cbaDataFrame, bbFrame], axis=1, join='inner')
        bbLimitFrame = joinFrame.query("Date > '2015-01-01 00:00:00'")
        print(bbLimitFrame.ix['2015-09-01 00:00:00'])
        myPlot = bbLimitFrame.plot(y=['Close','upperband','middleband','lowerband'], title='Gary')
        fig = myPlot.get_figure()
        fig.savefig('bb.png')

        #Download data from yahoo finance

        # start = datetime.datetime(2010,1,1)
        # end = datetime.datetime(2014,3,24)
        # ticker = "AAPL"
        # f=web.DataReader(ticker,'yahoo',start,end)
        #
        # f['SMA_20'] = talib.SMA(numpy.asarray(f['Close']), 20)
        # f['SMA_50'] = talib.SMA(numpy.asarray(f['Close']), 50)
        # myPlot = f.plot(y= ['Close','SMA_20','SMA_50'], title='AAPL Close & Moving Averages')
