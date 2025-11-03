from langchain_community.utilities import SQLDatabase
import src.database as d
from sqlalchemy import inspect

print('DB url:', d.engine.url)
ins = inspect(d.engine)
print('Tables:', ins.get_table_names())
if 'casas' in ins.get_table_names():
    cols = [c['name'] for c in ins.get_columns('casas')]
    print('Columns for casas:', cols)
    # Show 3 sample rows using sqlite3
    import sqlite3, pathlib
    db = pathlib.Path(str(d.engine.url).replace('sqlite:///', ''))
    conn = sqlite3.connect(db)
    cur = conn.cursor()
    cur.execute('SELECT * FROM casas LIMIT 3;')
    print('Sample rows:', cur.fetchall())
    conn.close()