# -*- coding: utf-8 -*-
import sqlite3
from pathlib import Path


def check_database():
    # Project root is the parent of the src directory
    project_root = Path(__file__).resolve().parent.parent
    db_path = project_root / "rents.db"

    if not db_path.exists():
        print("ERROR: No se encontró 'rents.db' en la raíz del proyecto:", str(db_path))
        return False

    print("Usando base de datos en:", str(db_path))

    try:
        conn = sqlite3.connect(str(db_path))
        cursor = conn.cursor()

        cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
        tables = cursor.fetchall()

        if not tables:
            print("No hay tablas en la base de datos.")
        else:
            print("Tablas en la base de datos:")
            for (table_name,) in tables:
                print("  - {}".format(table_name))

                cursor.execute("PRAGMA table_info({});".format(table_name))
                columns = cursor.fetchall()
                print("    Columnas: {}".format([col[1] for col in columns]))

                cursor.execute("SELECT COUNT(*) FROM {};".format(table_name))
                count = cursor.fetchone()[0]
                print("    Registros: {}".format(count))

        conn.close()
        return True

    except Exception as e:
        print("Error verificando la base de datos:", e)
        return False


if __name__ == "__main__":
    check_database()