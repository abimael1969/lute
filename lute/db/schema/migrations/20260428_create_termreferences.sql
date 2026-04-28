-- Store reader-origin snapshots for terms.

CREATE TABLE IF NOT EXISTS "termreferences" (
       "TrID" INTEGER NOT NULL,
       "TrWoID" INTEGER NOT NULL,
       "TrBookID" INTEGER NULL,
       "TrTextID" INTEGER NULL,
       "TrPageNumber" INTEGER NULL,
       "TrBookTitle" VARCHAR(200) NOT NULL,
       "TrSentenceHTML" TEXT NOT NULL,
       "TrCreated" DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
       PRIMARY KEY ("TrID"),
       FOREIGN KEY("TrWoID") REFERENCES "words" ("WoID") ON DELETE CASCADE
);

CREATE INDEX "TrWoID" ON "termreferences" ("TrWoID");
CREATE INDEX "TrCreated" ON "termreferences" ("TrCreated");
