
--DROP TABLE 'Equities';

--DROP TABLE Indicator_SMA;
--DROP TABLE Indicator_EMA;
--DROP TABLE Indicator_BB20;
--DROP TABLE Indicator_ROC;

--DROP TABLE 'Rule Indicator_ROC ROC_5 > 20';
--DROP TABLE 'Rule Indicator_ROC ROC_5 > 15';
--DROP TABLE 'Rule Indicator_ROC ROC_5 > 10';


CREATE TABLE IF NOT EXISTS "Equities" (
"Date" TIMESTAMP,
  "Open" REAL,
  "High" REAL,
  "Low" REAL,
  "Volume" INT,
  "Close" REAL,
  "Code" TEXT,
  PRIMARY KEY ("Code", "Date")
);
CREATE INDEX IF NOT EXISTS "ix_Equities_Date"ON "Equities" ("Date");


CREATE TABLE IF NOT EXISTS Indicator_SMA
(
    Date TEXT,
    Code TEXT,
    SMA_5 REAL,
    SMA_10 REAL,
    SMA_15 REAL,
    SMA_20 REAL,
    SMA_50 REAL,
    SMA_200 REAL
);
CREATE INDEX IF NOT EXISTS ix_Indicator_SMA_Date ON Indicator_SMA (Date);

CREATE TABLE IF NOT EXISTS Indicator_EMA
(
    Date TEXT,
    Code TEXT,
    EMA_5 REAL,
    EMA_10 REAL,
    EMA_15 REAL,
    EMA_20 REAL,
    EMA_50 REAL,
    EMA_200 REAL
);
CREATE INDEX IF NOT EXISTS ix_Indicator_EMA_Date ON Indicator_EMA (Date);

CREATE TABLE IF NOT EXISTS Indicator_BB20
(
    Date TEXT,
    Code TEXT,
    lowerband REAL,
    middleband REAL,
    upperband REAL,
    lowerbandroc REAL,
    middlebandroc REAL,
    upperbandroc REAL
);
CREATE INDEX IF NOT EXISTS ix_Indicator_BB20_Date ON Indicator_BB20 (Date);

CREATE TABLE IF NOT EXISTS Indicator_ROC
(
    Date TEXT,
    Code TEXT,
    ROC_5 REAL,
    ROC_10 REAL,
    ROC_20 REAL
);
CREATE INDEX IF NOT EXISTS ix_Indicator_ROC_Date ON Indicator_ROC (Date);

-- Rules

--CREATE TABLE 'Rule Indicator_ROC ROC_5 > 20'
--(
--    Date TEXT,
--    Code TEXT,
--    Match INT
--);
--CREATE INDEX 'ix_Rule Indicator_ROC ROC_5 > 20_Date' ON 'Rule Indicator_ROC ROC_5 > 20' (Date);
--
--CREATE TABLE 'Rule Indicator_ROC ROC_5 > 15'
--(
--    Date TEXT,
--    Code TEXT,
--    Match INT
--);
--CREATE INDEX 'ix_Rule Indicator_ROC ROC_5 > 15_Date' ON 'Rule Indicator_ROC ROC_5 > 15' (Date);
--
--CREATE TABLE 'Rule Indicator_ROC ROC_5 > 10'
--(
--    Date TEXT,
--    Code TEXT,
--    Match INT
--);
--CREATE INDEX 'ix_Rule Indicator_ROC ROC_5 > 10_Date' ON 'Rule Indicator_ROC ROC_5 > 10' (Date);
--
--CREATE TABLE 'Rule Equities Close -1 Comparison.GreaterThan 1.01'
--(
--    Date TEXT,
--    Code TEXT,
--    Match INT
--);
--CREATE INDEX 'ix_Rule Equities Close -1 Comparison.GreaterThan 1.01_Date' ON 'Rule Equities Close -1 Comparison.GreaterThan 1.01' (Date);
--
--CREATE TABLE IF NOT EXISTS 'Rule Equities Close -1 Comparison.LessThan 0.99' (Date TEXT, Code TEXT, Match INT);
--CREATE INDEX IF NOT EXISTS 'ix_Rule Equities Close -1 Comparison.LessThan 0.99_Date' ON 'Rule Equities Close -1 Comparison.LessThan 0.99' (Date);
