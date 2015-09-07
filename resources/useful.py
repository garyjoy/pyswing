
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
