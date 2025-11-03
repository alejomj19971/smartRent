# debug_sql_db.py
# Small debug helper to verify SQLAlchemy engine, tables and sample rows

from langchain_community.utilities import SQLDatabase
import src.database as d
from sqlalchemy import inspect
import sqlite3
import pathlib
import sys

try:
    print('DB url:', d.engine.url)
    ins = inspect(d.engine)
    tables = ins.get_table_names()
    print('Tables:', tables)

    if 'casas' in tables:
        cols = [c['name'] for c in ins.get_columns('casas')]
        print("Columns for 'casas':", cols)

        # derive sqlite file path from engine url
        db_path = pathlib.Path(str(d.engine.url).replace('sqlite:///', ''))
        print('Resolved sqlite path:', db_path)
        if not db_path.exists():
            print('ERROR: sqlite file not found at', db_path)
            sys.exit(1)

        conn = sqlite3.connect(str(db_path))
        cur = conn.cursor()
        cur.execute('SELECT id, title, price FROM casas LIMIT 3;')
        rows = cur.fetchall()
        print('Sample rows (up to 3):')
        for r in rows:
            print(r)
        conn.close()
    else:
        print("Table 'casas' not found in database")

except Exception as e:
    print('ERROR during debug:', e)
    sys.exit(1)
