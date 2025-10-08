from database import SessionLocal
from models import Casas

def guardar_casas(df):
    db = SessionLocal()
    try:
        for _, row in df.iterrows():
            casa = Casas(
                title=row["title"],
                price = row["price"],
                squareMeters = row["squareMeters"],
                bedroom = row["bedroom"],
                toilet = row["toilet"],
                parking = row["parking"]
                
            )
            db.add(casa)
        db.commit()
        print("Casas guardadas correctamente")
    except Exception as e:
        db.rollback()
        print("Error al guardar las casas:", e)
    finally:
        db.close()

