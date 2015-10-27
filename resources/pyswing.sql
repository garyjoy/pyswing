
-- It's very important that this script can run over an existing database with no detrimental effects...

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

CREATE TABLE IF NOT EXISTS Indicator_MACD
(
    Date TEXT,
    Code TEXT,
    MACD_12_26 REAL,
    MACD_12_26_9 REAL,
    MACD_12_26_9_DIVERGENCE REAL,
    PRIMARY KEY (Date, Code)
);
CREATE INDEX IF NOT EXISTS ix_Indicator_MACD_Date ON Indicator_MACD (Date);
CREATE INDEX IF NOT EXISTS ix_Indicator_MACD_Code ON Indicator_MACD (Code);

CREATE TABLE IF NOT EXISTS Indicator_STOCH
(
    Date TEXT,
    Code TEXT,
    STOCH_K REAL,
    STOCH_D REAL,
    STOCH_K_ROC REAL,
    STOCH_D_ROC REAL,
    PRIMARY KEY (Date, Code)
);
CREATE INDEX IF NOT EXISTS ix_Indicator_STOCH_Date ON Indicator_STOCH (Date);
CREATE INDEX IF NOT EXISTS ix_Indicator_STOCH_Code ON Indicator_STOCH (Code);

CREATE TABLE IF NOT EXISTS Indicator_AROON
(
    Date TEXT,
    Code TEXT,
    AROON_UP REAL,
    AROON_DOWN REAL,
    PRIMARY KEY (Date, Code)
);
CREATE INDEX IF NOT EXISTS ix_Indicator_AROON_Date ON Indicator_AROON (Date);
CREATE INDEX IF NOT EXISTS ix_Indicator_AROON_Code ON Indicator_AROON (Code);

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

CREATE TABLE IF NOT EXISTS Indicator_ADX
(
    Date TEXT,
    Code TEXT,
    ADX REAL,
    ADX_ROC REAL,
    PRIMARY KEY (Date, Code)
);
CREATE INDEX IF NOT EXISTS ix_Indicator_ADX_Date ON Indicator_ADX (Date);
CREATE INDEX IF NOT EXISTS ix_Indicator_ADX_Code ON Indicator_ADX (Code);

CREATE TABLE IF NOT EXISTS Indicator_ADI
(
    Date TEXT,
    ADI REAL,
    ADI_ROC REAL,
    ADI_EMA REAL,
    ADI_SUM REAL,
    PRIMARY KEY (Date)
);
CREATE INDEX IF NOT EXISTS ix_Indicator_ADI_Date ON Indicator_ADI (Date);

CREATE TABLE IF NOT EXISTS Indicator_DX
(
    Date TEXT,
    Code TEXT,
    DX REAL,
    DX_ROC REAL,
    PRIMARY KEY (Date, Code)
);
CREATE INDEX IF NOT EXISTS ix_Indicator_DX_Date ON Indicator_DX (Date);
CREATE INDEX IF NOT EXISTS ix_Indicator_DX_Code ON Indicator_DX (Code);

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

CREATE TABLE IF NOT EXISTS Indicator_RSI
(
    Date TEXT,
    Code TEXT,
    RSI REAL,
    PRIMARY KEY (Date, Code)
);
CREATE INDEX IF NOT EXISTS ix_Indicator_RSI_Date ON Indicator_RSI (Date);
CREATE INDEX IF NOT EXISTS ix_Indicator_RSI_Code ON Indicator_RSI (Code);

CREATE TABLE IF NOT EXISTS Rules
(
    Rule TEXT,
    MatchesPerDay REAL,
    PRIMARY KEY (Rule)
);

-- Rule Tables (and Indices) are Created 'On Demand'

CREATE TABLE IF NOT EXISTS TwoRuleStrategy
(
    strategy TEXT,
    rule1 TEXT,
    rule2 TEXT,
    exit TEXT,
    resultPerTrade REAL,
    numberOfTrades INT,
    type TEXT,
    Searched INT
);

CREATE TABLE IF NOT EXISTS ThreeRuleStrategy
(
    strategy TEXT,
    rule1 TEXT,
    rule2 TEXT,
    rule3 TEXT,
    exit TEXT,
    resultPerTrade REAL,
    numberOfTrades INT,
    type TEXT,
    Searched INT
);

CREATE TABLE IF NOT EXISTS Strategy
(
    strategy TEXT,
    rule1 TEXT,
    rule2 TEXT,
    rule3 TEXT,
    exit TEXT,
    type TEXT,
    meanResultPerTrade REAL,
    medianResultPerTrade REAL,
    totalProfit REAL,
    numberOfTrades INT,
    sharpeRatio REAL,
    maximumDrawdown REAL,
    active INT
);