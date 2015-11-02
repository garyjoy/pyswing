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

select r1.rule, r2.rule from Rules r1 inner join Rules r2 on 1 == 1 where r1.MatchesPerDay * r2.MatchesPerDay > 0.1

select * from 'Rule Indicator_ROC ROC_5 > 20' r1
inner join 'Rule Indicator_BB20 upperbandroc < -4 and lowerbandroc > 4' r2 on r1.Date = r2.Date and r1.Code = r2.Code and r2.Match = 1
inner join 'Exit TrailingStop3.0 RiskRatio2' evb on evb.Date = r1.Date and evb.Code = r1.Code and evb.Type = 'Buy'
inner join 'Exit TrailingStop3.0 RiskRatio2' evs on evs.Date = r1.Date and evs.Code = r1.Code and evs.Type = 'Sell'
where r1.Match = 1

select * from 'Exit TrailingStop3.0 RiskRatio2' where Code = 'AIO.AX' and Date = '2015-10-22 00:00:00';


select * from ThreeRuleStrategy where numberOfTrades > 1000 and resultPerTrade > 0.6 order by numberOfTrades desc limit 1000;
select * from ThreeRuleStrategy where numberOfTrades > 500 and resultPerTrade > 0.9 order by numberOfTrades desc limit 1000;
select * from ThreeRuleStrategy where numberOfTrades > 250 and resultPerTrade > 1.3 order by numberOfTrades desc limit 1000;
select * from ThreeRuleStrategy where numberOfTrades > 125 and resultPerTrade > 1.5 order by numberOfTrades desc limit 1000;

select r1.Code, r1.Date, ev.Type, ev.ExitValue, ev.NumberOfDays, ev.ExitDetail
from 'Rule Indicator_ROC ROC_10 < -20' r1
 inner join 'Rule Indicator_STOCH STOCH_K > STOCH_D' r2 on r2.Match = 1 and r1.Date = r2.Date and r1.Code = r2.Code
 inner join 'Rule Indicator_AROON AROON_DOWN < 90' r3 on r3.Match = 1 and r1.Date = r3.Date and r1.Code = r3.Code
 inner join 'Exit TrailingStop3.0 RiskRatio2' ev on r1.Date = ev.MatchDate and r1.Code = ev.Code and ev.Type = 'Sell'
where r1.Match = 1 -- and r1.Date = (select max(Date) from Equities)
order by r1.Date desc;

select r1.Code, r1.Date, ev.Type, ev.ExitValue, ev.NumberOfDays, ev.ExitDetail
from 'Rule Equities Indicator_EMA t1.Close > 1.1 * t2.EMA_200' r1
 inner join 'Rule Indicator_STOCH STOCH_K < 20' r2 on r2.Match = 1 and r1.Date = r2.Date and r1.Code = r2.Code
 inner join 'Rule Indicator_AROON AROON_DOWN > 10' r3 on r3.Match = 1 and r1.Date = r3.Date and r1.Code = r3.Code
 inner join 'Exit TrailingStop3.0 RiskRatio2' ev on r1.Date = ev.MatchDate and r1.Code = ev.Code and ev.Type = 'Buy'
where r1.Match = 1 -- and r1.Date = (select max(Date) from Equities)
order by r1.Date desc;


select * from Strategy where numberoftrades > 200 order by maximumdrawdown desc;


update Strategy set active = 1 where sharpeRatio > 1.4 and maximumDrawdown > -110;
update Strategy set active = 1 where type = 'Sell' and sharpeRatio > 1.2 and maximumDrawdown > -50;


select * from Strategy where active = 1;


