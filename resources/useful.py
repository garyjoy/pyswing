
from pyswing.objects.equity import Equity
cbaEquity = Equity("CBA.AX")
cbaEquity.dataFrame().query("Date > '2015-01-01 00:00:00'").plot(y=['Close'], title='CBA Close 2015')

import pyswing.database
import sqlite3
from pandas.io.sql import read_sql_query
pyswing.database.initialiseDatabase("ftse")
connection = sqlite3.connect(pyswing.database.pySwingDatabase)
query = "select * from Indicator_ROC WHERE CODE = 'AAL.L'"
cbaEquityData = read_sql_query(query, connection, 'Date')
connection.close()
cbaEquityData.query("Date > '2010-01-01 00:00:00'").plot(y=['ROC_5','ROC_10','ROC_20'], title='Hello!')

import pyswing.database
import sqlite3
from pandas.io.sql import read_sql_query
connection = sqlite3.connect(pyswing.database.pySwingDatabase)
query = "select b.*, e.Close from Indicator_BB20 b inner join Equities e on b.Date = e.Date and b.Code = e.Code and b.Date > '2015-03-01 00:00:00' and b.Code = 'CBA.AX'"
cbaEquityData = read_sql_query(query, connection, 'Date')
connection.close()
cbaEquityData.query("Date > '2015-01-01 00:00:00'").plot(y=['upperband','middleband','lowerband','Close'], title='CBA BBAND 2015')

import pyswing.database
import sqlite3
from pandas.io.sql import read_sql_query
connection = sqlite3.connect("output/TestMultipleIndicatorRule.db")
query = "select e.Date, Close, SMA_200 from Equities e inner join Indicator_SMA i on e.Date = i.Date and e.Code = i.Code"
cbaEquityData = read_sql_query(query, connection, 'Date')
connection.close()
cbaEquityData.query("Date > '2015-06-01 00:00:00'").plot(y=['Close','SMA_200'], title='Testing')



from pyswing.AskHorse import askHorse
args = "-n asx".split()
askHorse(args)


from pyswing.AnalyseStrategies import analyseStrategies
args = "-n ftse -s v1.2 -r 0.4 -t 500".split
analyseStrategies(args)


# Run me to populate (emptying to begin with) the historic trades table using the strategies in active strategies (which must be put in there manually)...
from pyswing.GenerateHistoricTradesForActiveStrategies import generateHistoricTradesForActiveStrategies
args = "-n ftse".split()
generateHistoricTradesForActiveStrategies(args)


# Run me to chart the (distinct) results in active strategy
import pyswing.database
import sqlite3
from pandas.io.sql import read_sql_query
from pandas import expanding_sum
connection = sqlite3.connect(pyswing.database.pySwingDatabase)
query = ("select t.matchDate as Date, t.code as Code, t.type as Type, t.ExitValue as ExitValue from ( select distinct matchDate, Code, type, exitValue from historicTrades order by matchDate asc) t")
cbaEquityData = read_sql_query(query, connection, 'Date')
connection.close()
cbaEquityData['ExitValueAfterCosts'] = cbaEquityData['ExitValue'] - 0.2
exitValueDataFrame = cbaEquityData.ix[:,'ExitValueAfterCosts']
cbaEquityData["Sum"] = expanding_sum(exitValueDataFrame)
cbaEquityData.query("Date > '2005-01-01 00:00:00'").plot(y=['Sum'], title='v1.4')