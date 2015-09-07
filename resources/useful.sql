select Code, count(1) from Indicator_SMA group by Code;
select Code, count(1) from Indicator_EMA group by Code;
select Code, count(1) from Indicator_BB20 group by Code;
select Code, count(1) from Indicator_MOM group by Code;

select * from Indicator_BB20 b inner join Equities e on b.Date = e.Date and b.Code = e.Code and b.Date > '2015-03-01 00:00:00' and b.Code = 'CBA.AX';
