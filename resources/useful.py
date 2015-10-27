
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
query = ("select r1.Code, r1.Date, ev.Type, ev.ExitValue, ev.NumberOfDays, ev.ExitDetail "
"from 'Rule Indicator_RSI RSI < 30' r1 "
" inner join 'Rule Indicator_AROON AROON_UP < 10' r2 on r2.Match = 1 and r1.Date = r2.Date and r1.Code = r2.Code "
" inner join 'Rule Equities Indicator_SMA t1.Close > t2.SMA_200' r3 on r3.Match = 1 and r1.Date = r3.Date and r1.Code = r3.Code "
" inner join 'Exit TrailingStop3.0 RiskRatio2' ev on r1.Date = ev.MatchDate and r1.Code = ev.Code and ev.Type = 'Buy' "
"where r1.Match = 1 "
"order by r1.Date asc")
cbaEquityData = read_sql_query(query, connection, 'Date')
connection.close()

cbaEquityData['ExitValueAfterCosts'] = cbaEquityData['ExitValue'] - 0.2
exitValueDataFrame = cbaEquityData.ix[:,'ExitValueAfterCosts']
cbaEquityData["Sum"] = expanding_sum(exitValueDataFrame)
cbaEquityData.query("Date > '2005-01-01 00:00:00'").plot(y=['Sum'], title='Testing')
