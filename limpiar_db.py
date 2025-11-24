# -*- coding: utf-8 -*-
"""Script para limpiar la base de datos"""
from src.database import SessionLocal
from src.models import Casas

def limpiar_base_datos():
    """Elimina todas las propiedades de la base de datos"""
    db = SessionLocal()
    try:
        count = db.query(Casas).count()
        db.query(Casas).delete()
        db.commit()
        print(f"Base de datos limpiada. Se eliminaron {count} propiedades.")
    except Exception as e:
        db.rollback()
        print(f"Error al limpiar la base de datos: {e}")
    finally:
        db.close()

if __name__ == "__main__":
    limpiar_base_datos()

