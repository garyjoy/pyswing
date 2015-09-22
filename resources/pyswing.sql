
--DROP TABLE 'Equities';

--DROP TABLE Indicator_SMA;
--DROP TABLE Indicator_EMA;
--DROP TABLE Indicator_BB20;
--DROP TABLE Indicator_ROC;

--DROP TABLE 'Rule ?';


CREATE TABLE IF NOT EXISTS Equities (
    Date TEXT,
    Open REAL,
    High REAL,
    Low REAL,
    Volume INT,
    Close REAL,
    Code TEXT,
    PRIMARY KEY (Date, Code)    
);
CREATE INDEX IF NOT EXISTS ix_Equities_Date ON Equities (Date);
CREATE INDEX IF NOT EXISTS ix_Equities_Code ON Equities (Code);

CREATE TABLE IF NOT EXISTS Indicator_SMA
(
    Date TEXT,
    Code TEXT,
    SMA_5 REAL,
    SMA_10 REAL,
    SMA_15 REAL,
    SMA_20 REAL,
    SMA_50 REAL,
    SMA_200 REAL,
    PRIMARY KEY (Date, Code)
);
CREATE INDEX IF NOT EXISTS ix_Indicator_SMA_Date ON Indicator_SMA (Date);
CREATE INDEX IF NOT EXISTS ix_Indicator_SMA_Code ON Indicator_SMA (Code);

CREATE TABLE IF NOT EXISTS Indicator_EMA
(
    Date TEXT,
    Code TEXT,
    EMA_5 REAL,
    EMA_10 REAL,
    EMA_15 REAL,
    EMA_20 REAL,
    EMA_50 REAL,
    EMA_200 REAL,
    PRIMARY KEY (Date, Code)
);
CREATE INDEX IF NOT EXISTS ix_Indicator_EMA_Date ON Indicator_EMA (Date);
CREATE INDEX IF NOT EXISTS ix_Indicator_EMA_Code ON Indicator_EMA (Code);

CREATE TABLE IF NOT EXISTS Indicator_BB20
(
    Date TEXT,
    Code TEXT,
    lowerband REAL,
    middleband REAL,
    upperband REAL,
    lowerbandroc REAL,
    middlebandroc REAL,
    upperbandroc REAL,
    PRIMARY KEY (Date, Code)
);
CREATE INDEX IF NOT EXISTS ix_Indicator_BB20_Date ON Indicator_BB20 (Date);
CREATE INDEX IF NOT EXISTS ix_Indicator_BB20_Code ON Indicator_BB20 (Code);

CREATE TABLE IF NOT EXISTS Indicator_ROC
(
    Date TEXT,
    Code TEXT,
    ROC_5 REAL,
    ROC_10 REAL,
    ROC_20 REAL,
    PRIMARY KEY (Date, Code)
);
CREATE INDEX IF NOT EXISTS ix_Indicator_ROC_Date ON Indicator_ROC (Date);
CREATE INDEX IF NOT EXISTS ix_Indicator_ROC_Code ON Indicator_ROC (Code);

CREATE TABLE IF NOT EXISTS Rules
(
    Rule TEXT,
    MatchesPerDay REAL,
    PRIMARY KEY (Rule)
);

-- Rule Tables (and Indices) are Created 'On Demand'
