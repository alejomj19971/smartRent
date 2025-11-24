from typing import Annotated
from sqlalchemy.orm import Session
from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from pathlib import Path
from src.database import engine,SessionLocal
import src.models
from src.models import Casas
from src.crud import guardar_casas
from src.chat_service import chat_with_agent
from src.scraping_queue import scraping_queue

app=FastAPI()

# Configurar CORS para permitir requests del frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # En producción, especifica el dominio exacto
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

src.models.Base.metadata.create_all(bind=engine)

def get_db():
    db=SessionLocal()
    try:
        yield db
    finally:
        db.close()

db_dependency=Annotated[Session, Depends(get_db)]

@app.get("/casas")
async def read_all(db:db_dependency):
    return db.query(Casas).all()

@app.get("/casas/total")
async def get_total_casas(db:db_dependency):
    """Obtiene el total de casas en la base de datos"""
    total = db.query(Casas).count()
    return {"total": total}


@app.post("/actualizar")
async def actualizar_datos():
    """Endpoint legacy - ahora usa la cola (por defecto Copacabana)"""
    task_id = scraping_queue.add_scraping_task("Copacabana")
    return {"mensaje": "Tarea de scraping agregada a la cola", "task_id": task_id, "city": "Copacabana"}

class ScrapingStartRequest(BaseModel):
    city: str

@app.post("/scraping/start")
async def start_scraping(request: ScrapingStartRequest):
    """Inicia trabajos de scraping y los agrega a la cola.
    Busca TODOS los scripts que contengan el nombre de la ciudad y los ejecuta en orden."""
    try:
        task_ids = scraping_queue.add_scraping_task(request.city)
        status = scraping_queue.get_status()
        return {
            "success": True,
            "task_ids": task_ids,
            "task_count": len(task_ids),
            "status": status["status"],
            "city": request.city,
            "message": f"Scraping iniciado" if status["status"] == "running" else f"{len(task_ids)} script(s) agregado(s) a la cola"
        }
    except ValueError as e:
        return {
            "success": False,
            "error": str(e),
            "city": request.city
        }

@app.get("/scraping/status")
async def get_scraping_status():
    """Obtiene el estado actual del scraping"""
    status = scraping_queue.get_status()
    return status

@app.post("/scraping/reset")
async def reset_scraping_status():
    """Resetea el estado del scraping después de completar o error"""
    scraping_queue.reset_status()
    return {"success": True, "message": "Estado reseteado"}


# Modelo para el request de chat
class ChatRequest(BaseModel):
    message: str
    city: str = None  # Ciudad opcional para filtrar propiedades

# Endpoint para el chat
@app.post("/chat")
async def chat(request: ChatRequest):
    """Endpoint para procesar mensajes del chat.
    chat_service solo retorna string, aquí se hace todo el procesamiento post-consulta."""
    import json
    from src.database import SessionLocal
    from src.models import Casas
    from src.property_matcher import (
        extract_property_matches_from_text,
        extract_image_urls,
        create_image_id_map,
        match_properties_by_image,
        match_properties_by_data
    )
    
    # 1. Detectar municipio automáticamente en el mensaje si no se proporciona
    query_lower = request.message.lower()
    detected_city = request.city
    
    # Mapeo de municipios para detección automática (mejorado)
    municipio_keywords = {
        "bello": ["bello"],
        "copacabana": ["copacabana"],
        "medellin": ["medellín", "medellin", "medellin"],
        "envigado": ["envigado"],
        "caldas": ["caldas"],
        "sabaneta": ["sabaneta"],
        "estrella": ["la estrella", "estrella", "estrella"]
    }
    
    if not detected_city:
        # Buscar municipio en el mensaje (búsqueda mejorada)
        # Primero buscar patrones específicos como "casas en [municipio]"
        import re
        municipio_pattern = re.search(r'(?:casas|propiedades)\s+(?:en|de)?\s+([a-záéíóúñ\s]+)', query_lower)
        if municipio_pattern:
            municipio_text = municipio_pattern.group(1).strip()
            for municipio_key, keywords in municipio_keywords.items():
                for keyword in keywords:
                    if keyword in municipio_text:
                        city_names = {
                            "bello": "Bello",
                            "copacabana": "Copacabana",
                            "medellin": "Medellín",
                            "envigado": "Envigado",
                            "caldas": "Caldas",
                            "sabaneta": "Sabaneta",
                            "estrella": "La Estrella"
                        }
                        detected_city = city_names.get(municipio_key)
                        break
                if detected_city:
                    break
        
        # Si no se encontró con el patrón, buscar en todo el mensaje
        if not detected_city:
            for municipio_key, keywords in municipio_keywords.items():
                for keyword in keywords:
                    if keyword in query_lower:
                        city_names = {
                            "bello": "Bello",
                            "copacabana": "Copacabana",
                            "medellin": "Medellín",
                            "envigado": "Envigado",
                            "caldas": "Caldas",
                            "sabaneta": "Sabaneta",
                            "estrella": "La Estrella"
                        }
                        detected_city = city_names.get(municipio_key)
                        break
                if detected_city:
                    break
    
    # 2. Obtener respuesta del LLM (solo string)
    llm_output = chat_with_agent(request.message, city=detected_city)
    
    # 3. Detectar si es consulta de "todas las casas" o "casas en [municipio]" - obtener directamente de BD
    is_all_casas_query = any(phrase in query_lower for phrase in [
        "todas las casas", "todas las propiedades", "casas disponibles", 
        "cuántas casas", "lista todas", "todas disponibles", "mostrar todas"
    ])
    
    # Detectar consultas simples por municipio: "casas en [municipio]", "casas en [municipio]", etc.
    is_simple_municipio_query = False
    if detected_city:
        simple_patterns = [
            f"casas en {detected_city.lower()}",
            f"casas en {query_lower.split('en')[-1].strip() if 'en' in query_lower else ''}",
            f"casas {detected_city.lower()}",
            f"propiedades en {detected_city.lower()}",
            f"propiedades {detected_city.lower()}"
        ]
        is_simple_municipio_query = any(
            pattern.strip() in query_lower or 
            query_lower.startswith(pattern.strip()) or
            query_lower.endswith(pattern.strip())
            for pattern in simple_patterns
        ) or (
            "casas" in query_lower and 
            detected_city.lower() in query_lower and 
            len(query_lower.split()) <= 5  # Consulta simple (máximo 5 palabras)
        )
    
    db = SessionLocal()
    try:
        # Obtener casas filtradas por municipio si hay ciudad detectada
        if detected_city:
            city_to_municipio = {
                "Medellín": "medellin", "Medellin": "medellin",
                "Copacabana": "copacabana", "Sabaneta": "sabaneta",
                "La Estrella": "estrella", "La estrella": "estrella", "Estrella": "estrella",
                "Envigado": "envigado", "Caldas": "caldas", "Bello": "bello"
            }
            municipio = city_to_municipio.get(detected_city, detected_city.lower().replace(" ", "_").replace("í", "i").replace("ó", "o").replace("é", "e").replace("á", "a").replace("ú", "u"))
            all_casas = db.query(Casas).filter(Casas.municipio == municipio).all()
        else:
            all_casas = db.query(Casas).all()
        
        # Si es consulta de "todas las casas" o consulta simple por municipio, retornar directamente
        if is_all_casas_query or is_simple_municipio_query:
            properties = []
            for casa in all_casas:
                properties.append({
                    "id": casa.id, "title": casa.title, "price": casa.price,
                    "bedroom": casa.bedroom, "toilet": casa.toilet,
                    "parking": casa.parking, "squareMeters": casa.squareMeters,
                    "image": casa.image or ""
                })
            
            total_count = len(properties)
            if detected_city:
                text = f"Encontré {total_count} casas disponibles en {detected_city}."
            else:
                text = f"Encontré {total_count} casas disponibles."
            
            MAX_PROPERTIES = 25
            if len(properties) > MAX_PROPERTIES:
                properties = properties[:MAX_PROPERTIES]
                if detected_city:
                    text = f"Encontré {total_count} casas disponibles en {detected_city}. Se muestran las primeras {MAX_PROPERTIES}."
                else:
                    text = f"Encontré {total_count} casas disponibles. Se muestran las primeras {MAX_PROPERTIES}."
            
            response_data = {"text": text, "properties": properties}
            return {"response": json.dumps(response_data, ensure_ascii=False)}
        
        # 3. Procesar output del LLM: extraer propiedades e imágenes
        response_data = {"text": llm_output, "properties": []}
        
        property_matches = extract_property_matches_from_text(llm_output)
        image_urls = extract_image_urls(llm_output)
        
        # 4. Hacer matching con BD
        matched_ids = set()
        matched_property_indices = set()
        
        if property_matches:
            image_id_to_casas = create_image_id_map(all_casas)
            
            # Matching por imagen
            matched_by_image = match_properties_by_image(
                property_matches, image_urls, image_id_to_casas,
                matched_ids, matched_property_indices
            )
            response_data["properties"].extend(matched_by_image)
            
            # Matching por datos (fallback)
            matched_by_data = match_properties_by_data(
                property_matches, all_casas, matched_ids, matched_property_indices
            )
            response_data["properties"].extend(matched_by_data)
        
        # Si hay property_matches pero no se matchearon todas, intentar matchear las restantes de forma más flexible
        if property_matches and len(response_data["properties"]) < len(property_matches):
            # Intentar matchear las propiedades que no se encontraron con un matching más flexible
            unmatched_indices = [i for i in range(len(property_matches)) if i not in matched_property_indices]
            if unmatched_indices:
                for idx in unmatched_indices:
                    prop_match = property_matches[idx]
                    # Buscar cualquier propiedad que tenga características similares
                    for casa in all_casas:
                        if casa.id not in matched_ids:
                            # Matching muy flexible: solo verificar que al menos 2 características coincidan aproximadamente
                            matches = 0
                            if abs(casa.price - prop_match.get('price', 0)) < 500000:  # Precio dentro de 500k
                                matches += 1
                            if abs(casa.bedroom - prop_match.get('bedroom', 0)) <= 1:  # Habitaciones ±1
                                matches += 1
                            if abs(casa.toilet - prop_match.get('toilet', 0)) <= 1:  # Baños ±1
                                matches += 1
                            if abs(casa.parking - prop_match.get('parking', 0)) <= 1:  # Parqueaderos ±1
                                matches += 1
                            if abs(casa.squareMeters - prop_match.get('squareMeters', 0)) < 50:  # m² ±50
                                matches += 1
                            
                            # Si al menos 2 características coinciden, agregar
                            if matches >= 2:
                                response_data["properties"].append({
                                    "id": casa.id,
                                    "title": casa.title,
                                    "price": casa.price,
                                    "bedroom": casa.bedroom,
                                    "toilet": casa.toilet,
                                    "parking": casa.parking,
                                    "squareMeters": casa.squareMeters,
                                    "image": casa.image or ""
                                })
                                matched_ids.add(casa.id)
                                matched_property_indices.add(idx)
                                break
        
        # 5. Si no se encontraron suficientes propiedades, intentar búsqueda directa mejorada
        # Si hay property_matches pero no se matchearon todas, o si no hay property_matches pero el LLM menciona resultados
        needs_fallback = (
            len(response_data["properties"]) == 0 or  # No se encontró ninguna
            (property_matches and len(response_data["properties"]) < len(property_matches) * 0.7)  # Se encontraron menos del 70%
        )
        
        if needs_fallback:
            # Detectar si el LLM menciona que encontró propiedades
            import re
            mentions_properties = re.search(r'(encontr[oé]|hay|existen|list[ao]|muestr[ao]|resultado).*\d+', llm_output.lower())
            
            if mentions_properties or len(all_casas) > 0:
                # Intentar extraer criterios de búsqueda del mensaje original
                query_lower = request.message.lower()
                
                # Extraer criterios básicos
                filters = {}
                
                # Precio
                if "millón" in query_lower or "millones" in query_lower:
                    price_match = re.search(r'(\d+)\s*mill[oó]n', query_lower)
                    if price_match:
                        max_price = int(price_match.group(1)) * 1000000
                        filters['max_price'] = max_price
                elif "mil" in query_lower:
                    price_match = re.search(r'(\d+)\s*mil', query_lower)
                    if price_match:
                        max_price = int(price_match.group(1)) * 1000
                        filters['max_price'] = max_price
                
                # Habitaciones
                bedroom_match = re.search(r'(\d+)\s*(?:cuartos?|habitaciones?)', query_lower)
                if bedroom_match:
                    filters['bedroom'] = int(bedroom_match.group(1))
                
                # Baños
                toilet_match = re.search(r'(\d+)\s*baños?', query_lower)
                if toilet_match:
                    filters['toilet'] = int(toilet_match.group(1))
                
                # Parqueadero
                if "parqueadero" in query_lower or "parqueaderos" in query_lower or "parq" in query_lower:
                    filters['parking'] = 1  # Al menos 1
                
                # Metros cuadrados
                meters_match = re.search(r'(\d+)\s*m[²2]', query_lower)
                if meters_match:
                    filters['squareMeters'] = int(meters_match.group(1))
                
                # Aplicar filtros a la BD
                filtered_casas = all_casas
                if filters:
                    filtered_casas = []
                    for casa in all_casas:
                        match = True
                        if 'max_price' in filters and casa.price > filters['max_price']:
                            match = False
                        if 'bedroom' in filters and casa.bedroom != filters['bedroom']:
                            match = False
                        if 'toilet' in filters and casa.toilet != filters['toilet']:
                            match = False
                        if 'parking' in filters and casa.parking < filters['parking']:
                            match = False
                        if 'squareMeters' in filters and abs(casa.squareMeters - filters['squareMeters']) > 20:
                            match = False
                        if match:
                            filtered_casas.append(casa)
                
                # Si hay casas filtradas, agregarlas
                if filtered_casas:
                    for casa in filtered_casas[:25]:  # Limitar a 25
                        response_data["properties"].append({
                            "id": casa.id,
                            "title": casa.title,
                            "price": casa.price,
                            "bedroom": casa.bedroom,
                            "toilet": casa.toilet,
                            "parking": casa.parking,
                            "squareMeters": casa.squareMeters,
                            "image": casa.image or ""
                        })
        
        # 6. Limitar a 25 propiedades
        MAX_PROPERTIES = 25
        if len(response_data["properties"]) > MAX_PROPERTIES:
            total = len(response_data["properties"])
            response_data["properties"] = response_data["properties"][:MAX_PROPERTIES]
            response_data["text"] = f"{response_data['text']}\n\n⚠️ Se encontraron {total} propiedades, pero solo se muestran las primeras {MAX_PROPERTIES}."
        
        # 7. Retornar respuesta estructurada o texto plano
        if response_data["properties"]:
            return {"response": json.dumps(response_data, ensure_ascii=False)}
        else:
            return {"response": llm_output}
            
    finally:
        db.close()

# Servir archivos estáticos del frontend (React build)
frontend_dist = Path(__file__).parent.parent / "front" / "dist"
if frontend_dist.exists():
    app.mount("/assets", StaticFiles(directory=str(frontend_dist / "assets")), name="assets")
    
    @app.get("/")
    async def read_root():
        index_file = frontend_dist / "index.html"
        if index_file.exists():
            return FileResponse(str(index_file))
        return {"message": "Frontend no encontrado. Ejecuta 'npm run build' en el directorio front"}
    
    # Servir otros archivos estáticos
    app.mount("/static", StaticFiles(directory=str(frontend_dist)), name="static")
else:
    # Fallback: servir el HTML original si no hay build de React
    frontend_path = Path(__file__).parent.parent / "front"
    if frontend_path.exists():
        app.mount("/static", StaticFiles(directory=str(frontend_path)), name="static")
    
    @app.get("/")
    async def read_root():
        return {"message": "Frontend no construido. Ejecuta 'cd front && npm install && npm run build'"}