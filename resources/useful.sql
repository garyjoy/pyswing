
-- Use this SQL to get a list of all the Rule tables...
SELECT name FROM sqlite_master WHERE type = 'table' and name like 'Rule %';

-- Use this SQL to select Strategy candidates...
select * from ThreeRuleStrategy where numberOfTrades > 1000 and resultPerTrade > 0.6 order by numberOfTrades desc limit 1000;
select * from ThreeRuleStrategy where numberOfTrades > 500 and resultPerTrade > 0.9 order by numberOfTrades desc limit 1000;
select * from ThreeRuleStrategy where numberOfTrades > 250 and resultPerTrade > 1.3 order by numberOfTrades desc limit 1000;
select * from ThreeRuleStrategy where numberOfTrades > 125 and resultPerTrade > 1.5 order by numberOfTrades desc limit 1000;

-- Use this SQL to work out which rules are contributing to my good Strategies...
select r.rule, r.MatchesPerDay, used from rules r
left join (
select rule, sum(myCount) as used from (
select rule1 as rule, count(1) as myCount from (
select *, totalProfit / maximumDrawdown  * -1 as score from Strategy where score > 2 order by score desc) t group by rule1
union
select rule2 as rule, count(1) as myCount from (
select *, totalProfit / maximumDrawdown  * -1 as score from Strategy where score > 2 order by score desc) t group by rule2
union
select rule3 as rule, count(1) as myCount from (
select *, totalProfit / maximumDrawdown  * -1 as score from Strategy where score > 2 order by score desc) t group by rule3) x group by rule) y
on r.rule = y.rule
order by used desc
;

-- Use this SQL to find out which shares are skewing my Strategies...
select Code, sum(exitValue), count(1) from HistoricTrades group by Code;


