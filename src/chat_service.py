# -*- coding: utf-8 -*-
import os
from pathlib import Path
from dotenv import load_dotenv

# Cargar variables de entorno desde .env
project_root = Path(__file__).resolve().parent.parent
env_path = project_root / '.env'
load_dotenv(dotenv_path=env_path)

from langchain_community.utilities import SQLDatabase
from langchain_community.agent_toolkits import create_sql_agent
from langchain_openai import ChatOpenAI
from langchain_community.agent_toolkits.sql.toolkit import SQLDatabaseToolkit

# Variable global para el agente
_agent_executor = None

def get_agent():
    """Inicializa y retorna el agente de chat SQL"""
    global _agent_executor
    
    if _agent_executor is not None:
        return _agent_executor
    
    # Obtener la ruta de la base de datos
    db_path = project_root / "rents.db"
    db_uri = f"sqlite:///{db_path.absolute()}"
    
    # Conectar con la base de datos
    db = SQLDatabase.from_uri(
        db_uri,
        sample_rows_in_table_info=3,
        include_tables=['casas']
    )
    
    # Configurar el modelo OpenAI
    api_key = os.getenv('OPENAI_API_KEY')
    if not api_key:
        raise ValueError('OPENAI_API_KEY no encontrada en el archivo .env')
    
    os.environ['OPENAI_API_KEY'] = api_key
    
    llm = ChatOpenAI(
        model='gpt-4o-mini',
        temperature=0
    )
    
    # Crear toolkit SQL
    toolkit = SQLDatabaseToolkit(db=db, llm=llm)
    
    # Prompt personalizado para el agente
    custom_prompt = """Eres un asistente experto en consultas sobre propiedades inmobiliarias.
Cuando el usuario pregunte sobre casas con precios específicos:
1. Primero responde con la CANTIDAD de casas encontradas
2. Luego lista TODAS las casas con sus detalles (título, precio, habitaciones, baños, parqueaderos, metros cuadrados)

FORMATO DE RESPUESTA ESPERADO:
"Encontré X casas con precio menor a [precio]. Son las siguientes:
1. [título] - Precio: $[precio] - [X] habitaciones - [X] baños - [X] parqueaderos - [X] m²
2. [título] - Precio: $[precio] - [X] habitaciones - [X] baños - [X] parqueaderos - [X] m²
..."

ESQUEMA DE LA BASE DE DATOS - TABLA "casas":
- id: Integer (clave primaria)
- title: String (título de la casa)
- price: Integer (precio en números enteros)
- toilet: Integer (número de baños, puede ser 0, 1, 2, 3, etc.)
- bedroom: Integer (número de habitaciones, puede ser 0, 1, 2, 3, etc.)
- squareMeters: Integer (metros cuadrados)
- parking: Integer (número de parqueaderos, puede ser 0, 1, 2, etc. - 0 significa sin parqueadero)
- active: Boolean (disponible/no disponible)

INSTRUCCIONES PARA CONSULTAS:
- Para buscar casas CON parqueadero: parking > 0 o parking >= 1
- Para buscar casas SIN parqueadero: parking = 0 o parking < 1
- Para buscar casas con X parqueaderos: parking = X
- Para buscar casas con más de X parqueaderos: parking > X
- Para buscar casas con baños: toilet > 0 o toilet >= 1
- Para buscar casas sin baños: toilet = 0
- Para buscar casas con X baños: toilet = X
- Para buscar casas con más de X baños: toilet > X
- "un millón doscientos" puede referirse a 1,200,000 o 1,200,000,000. Si el usuario no especifica, asume que es en millones (1,200,000)
- Si preguntan por casas "menores a" un precio, usa: price < [precio]
- Si preguntan por casas "menores o iguales a" un precio, usa: price <= [precio]
- Siempre muestra el precio formateado con separadores de miles (ej: $1,200,000)
- SIEMPRE incluye en las respuestas: título, precio, habitaciones, baños, parqueaderos y metros cuadrados

EJEMPLOS DE CONSULTAS SQL CORRECTAS:
- "Casas con parqueadero": SELECT * FROM casas WHERE parking > 0;
- "Casas sin parqueadero": SELECT * FROM casas WHERE parking = 0;
- "Casas con 2 baños": SELECT * FROM casas WHERE toilet = 2;
- "Casas con más de 2 baños": SELECT * FROM casas WHERE toilet > 2;
- "Casas con parqueadero y más de 3 habitaciones": SELECT * FROM casas WHERE parking > 0 AND bedroom > 3;

Responde SIEMPRE en español y con el formato especificado arriba. INCLUYE siempre la información de baños y parqueaderos en tus respuestas."""
    
    # Crear el agente
    _agent_executor = create_sql_agent(
        llm=llm,
        toolkit=toolkit,
        verbose=False,
        agent_type="openai-tools",
        handle_parsing_errors=True,
        prefix=custom_prompt,
    )
    
    return _agent_executor

def chat_with_agent(query: str) -> str:
    """Procesa una consulta del usuario y retorna la respuesta del agente"""
    try:
        agent = get_agent()
        forced_query = f"Responde en español. {query}"
        result = agent.invoke({'input': forced_query})
        output = result.get('output') if isinstance(result, dict) else str(result)
        return output
    except Exception as e:
        return f"Error al procesar la consulta: {str(e)}. Por favor, intenta reformular tu pregunta."

