
import sqlite3
from collections import namedtuple, OrderedDict


def dbase(database):
    db = sqlite3.connect(database)
    table_query = '''
    CREATE TABLE IF NOT EXISTS "notes"(
		"id"  INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
		"title"  TEXT,
		"content"  TEXT NOT NULL,
		"date_created"  TEXT NOT NULL,
		"date_modified"  TEXT NOT NULL
		);
    '''
    db.execute(table_query)
    db.commit()
    # prefer
    # db.row_factory = sqlite3.Row
    db.row_factory = dict_factory

    return db


def dict_factory(cursor, row):
    d = {}
    for idx, col in enumerate(cursor.description):
        d[col[0]] = row[idx]
    return d
