
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
    lowerbandmom REAL,
    middlebandmom REAL,
    upperbandmom REAL
);

CREATE INDEX IF NOT EXISTS ix_Indicator_BB20_Date ON Indicator_BB20 (Date);

CREATE TABLE IF NOT EXISTS Indicator_MOM
(
    Date TEXT,
    Code TEXT,
    MOM_5 REAL,
    MOM_10 REAL,
    MOM_20 REAL
);

CREATE INDEX IF NOT EXISTS ix_Indicator_MOM_Date ON Indicator_MOM (Date);
