
--DROP TABLE 'Equities';

--DROP TABLE Indicator_SMA;
--DROP TABLE Indicator_EMA;
--DROP TABLE Indicator_BB20;
--DROP TABLE Indicator_ROC;

--DROP TABLE 'Rule ?';


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


-- Rule Tables (and Indices) are Created 'On Demand'
