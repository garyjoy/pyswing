
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