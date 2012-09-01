CREATE TABLE "SongInfo" (
    "id" INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
    "artist" TEXT NOT NULL,
    "song" TEXT NOT NULL
);
CREATE TABLE sqlite_sequence(name,seq);
CREATE TABLE "TraitInfo" (
    "id" INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
    "songInfoId" INTEGER NOT NULL,
    "type" TEXT NOT NULL,
    "value" TEXT NOT NULL,
    "durationType" TEXT NOT NULL
);
