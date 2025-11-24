from src.database import SessionLocal
from src.models import Casas

def limpiar_casas_por_municipio(municipio: str):
    """Elimina todas las propiedades de un municipio específico antes de insertar nuevas"""
    db = SessionLocal()
    try:
        # Normalizar el nombre del municipio para búsqueda
        municipio_normalized = municipio.lower()
        
        # Eliminar todas las propiedades que tengan el mismo municipio
        deleted_count = db.query(Casas).filter(Casas.municipio == municipio_normalized).delete(synchronize_session=False)
        db.commit()
        print(f"Eliminadas {deleted_count} propiedades de {municipio} antes de insertar nuevas")
        return deleted_count
    except Exception as e:
        db.rollback()
        print(f"Error al limpiar propiedades de {municipio}: {e}")
        return 0
    finally:
        db.close()

def guardar_casas(df, municipio: str = None):
    """Guarda casas en la base de datos. Si se especifica un municipio, limpia las propiedades existentes de ese municipio primero."""
    db = SessionLocal()
    try:
        # Si se especifica un municipio, limpiar las propiedades existentes de ese municipio
        if municipio:
            limpiar_casas_por_municipio(municipio)
        
        # Normalizar el nombre del municipio para guardarlo
        municipio_normalized = municipio.lower() if municipio else None
        
        # Insertar las nuevas propiedades
        for _, row in df.iterrows():
            # Obtener municipio: primero del parámetro, luego del DataFrame si existe
            municipio_final = municipio_normalized
            if not municipio_final and "municipio" in row:
                municipio_final = str(row["municipio"]).lower()
            
            casa = Casas(
                title=row["title"],
                price = row["price"],
                squareMeters = row["squareMeters"],
                bedroom = row["bedroom"],
                toilet = row["toilet"],
                parking = row["parking"],
                image = row.get("image", ""),
                municipio = municipio_final or ""
            )
            db.add(casa)
        db.commit()
        print(f"Casas guardadas correctamente ({len(df)} propiedades) para municipio: {municipio_normalized}")
    except Exception as e:
        db.rollback()
        print("Error al guardar las casas:", e)
        raise
    finally:
        db.close()

