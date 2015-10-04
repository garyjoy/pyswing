select Code, count(1) from Indicator_SMA group by Code;
select Code, count(1) from Indicator_EMA group by Code;
select Code, count(1) from Indicator_BB20 group by Code;
select Code, count(1) from Indicator_MOM group by Code;

select * from Indicator_BB20 b inner join Equities e on b.Date = e.Date and b.Code = e.Code and b.Date > '2015-03-01 00:00:00' and b.Code = 'CBA.AX';

SELECT name FROM sqlite_master WHERE type = 'table' and name like 'Rule %';

select *, r1.MatchesPerDay * r2.MatchesPerDay * r3.MatchesPerDay from Rules r1
inner join Rules r2 on 1 == 1
inner join Rules r3 on 1 == 1
where r1.MatchesPerDay * r2.MatchesPerDay * r3.MatchesPerDay > 0.2 and r1.MatchesPerDay * r2.MatchesPerDay * r3.MatchesPerDay < 1 and r1.Rule != r2.Rule and r1.Rule != r3.Rule and r2.Rule != r3.Rule

-- 592704 records for ALL
-- 178139 records for 0.1 < x < 2
-- 96737 records for 0.2 < x < 1