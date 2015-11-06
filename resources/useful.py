
from pyswing.objects.equity import Equity
cbaEquity = Equity("CBA.AX")
cbaEquity.dataFrame().query("Date > '2015-01-01 00:00:00'").plot(y=['Close'], title='CBA Close 2015')

import pyswing.constants
import sqlite3
from pandas.io.sql import read_sql_query
connection = sqlite3.connect(pyswing.constants.pySwingDatabase)
query = "select * from Indicator_BB20 where Code = 'CBA.AX'"
cbaEquityData = read_sql_query(query, connection, 'Date')
connection.close()
cbaEquityData.query("Date > '2015-01-01 00:00:00'").plot(y=['upperband','middleband','lowerband'], title='CBA BBAND 2015')

import pyswing.constants
import sqlite3
from pandas.io.sql import read_sql_query
connection = sqlite3.connect(pyswing.constants.pySwingDatabase)
query = "select b.*, e.Close from Indicator_BB20 b inner join Equities e on b.Date = e.Date and b.Code = e.Code and b.Date > '2015-03-01 00:00:00' and b.Code = 'CBA.AX'"
cbaEquityData = read_sql_query(query, connection, 'Date')
connection.close()
cbaEquityData.query("Date > '2015-01-01 00:00:00'").plot(y=['upperband','middleband','lowerband','Close'], title='CBA BBAND 2015')


import pyswing.constants
import sqlite3
from pandas.io.sql import read_sql_query
connection = sqlite3.connect("output/TestMultipleIndicatorRule.db")
query = "select e.Date, Close, SMA_200 from Equities e inner join Indicator_SMA i on e.Date = i.Date and e.Code = i.Code"
cbaEquityData = read_sql_query(query, connection, 'Date')
connection.close()
cbaEquityData.query("Date > '2015-06-01 00:00:00'").plot(y=['Close','SMA_200'], title='Testing')


import pyswing.constants
import sqlite3
from pandas.io.sql import read_sql_query
from pandas import expanding_sum

connection = sqlite3.connect(pyswing.constants.pySwingDatabase)
query = ("select t.matchDate as Date, ev.ExitValue from ( select distinct matchDate, Code, type from historicTrades order by matchDate asc) t inner join 'Exit TrailingStop3.0 RiskRatio2' ev on t.matchDate = ev.matchDate and t.code = ev.code and t.type = ev.type")
cbaEquityData = read_sql_query(query, connection, 'Date')
connection.close()

cbaEquityData['ExitValueAfterCosts'] = cbaEquityData['ExitValue'] - 0.2
exitValueDataFrame = cbaEquityData.ix[:,'ExitValueAfterCosts']
cbaEquityData["Sum"] = expanding_sum(exitValueDataFrame)
cbaEquityData.query("Date > '2005-01-01 00:00:00'").plot(y=['Sum'], title='sharpeRatio > 1.0 and medianResultPerTrade > 0')



from pyswing.AskHorse import askHorse
args = "-n asx".split()
askHorse(args)


from pyswing.GenerateHistoricTradesForActiveStrategies import generateHistoricTradesForActiveStrategies
args = "-n asx".split()
generateHistoricTradesForActiveStrategies(args)
