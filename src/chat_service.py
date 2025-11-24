# -*- coding: utf-8 -*-
"""
Servicio de chat simplificado: SOLO obtiene contexto del LLM y ejecuta consultas SQL.
Todo el procesamiento post-consulta se hace fuera de este módulo.
"""
import os
from pathlib import Path
from dotenv import load_dotenv

# Cargar variables de entorno
project_root = Path(__file__).resolve().parent.parent
env_path = project_root / '.env'
load_dotenv(dotenv_path=env_path)

from langchain_community.utilities import SQLDatabase
from langchain_community.agent_toolkits import create_sql_agent
from langchain_openai import ChatOpenAI
from langchain_community.agent_toolkits.sql.toolkit import SQLDatabaseToolkit

def create_agent():
    """
    Crea un NUEVO agente SIN memoria para cada consulta.
    Esto evita que LangChain acumule historial de conversación.
    """
    # Obtener la ruta de la base de datos
    db_path = project_root / "rents.db"
    db_uri = f"sqlite:///{db_path.absolute()}"
    
    # Conectar con la base de datos - MUY limitado para reducir tokens
    db = SQLDatabase.from_uri(
        db_uri,
        sample_rows_in_table_info=0,  # NO enviar filas de ejemplo (reduce tokens)
        include_tables=['casas']
    )
    
    # Configurar el modelo OpenAI
    api_key = os.getenv('OPENAI_API_KEY')
    if not api_key:
        raise ValueError('OPENAI_API_KEY no encontrada en el archivo .env')
    
    os.environ['OPENAI_API_KEY'] = api_key
    
    llm = ChatOpenAI(
        model='gpt-4o-mini',
        temperature=0,
        max_tokens=500  # Limitar tokens de respuesta
    )
    
    # Crear toolkit SQL
    toolkit = SQLDatabaseToolkit(db=db, llm=llm)
    
    # Prompt con ejemplos cortos de consultas SQL
    custom_prompt = """SQL para propiedades. Tabla: casas(id,title,price,toilet,bedroom,squareMeters,parking,image,municipio). SIEMPRE LIMIT 25.

Ejemplos sin municipio:
- "2 cuartos, 2 baños, parqueadero" = SELECT * FROM casas WHERE bedroom=2 AND toilet=2 AND parking>0 LIMIT 25;
- "1 millón, 1 baño, 1 cuarto" = SELECT * FROM casas WHERE price<=1000000 AND toilet=1 AND bedroom=1 LIMIT 25;
- "menos de 35 m², parqueadero" = SELECT * FROM casas WHERE squareMeters<35 AND parking>0 LIMIT 25;
- "3 cuartos, más de 70 m²" = SELECT * FROM casas WHERE bedroom=3 AND squareMeters>70 LIMIT 25;
- "900 mil, mínimo 50 m², parqueadero" = SELECT * FROM casas WHERE price<=900000 AND squareMeters>=50 AND parking>0 LIMIT 25;
- "baratas, 1 cuarto, 1 baño" = SELECT * FROM casas WHERE bedroom=1 AND toilet=1 ORDER BY price ASC LIMIT 25;
- "mínimo 60 m², 2 cuartos" = SELECT * FROM casas WHERE squareMeters>=60 AND bedroom=2 LIMIT 25;
- "2 baños, parqueadero, menos de 1 millón" = SELECT * FROM casas WHERE toilet=2 AND parking>0 AND price<1000000 LIMIT 25;
- "3 cuartos, más de 2 baños" = SELECT * FROM casas WHERE bedroom=3 AND toilet>2 LIMIT 25;

Ejemplos con municipio (municipio en minúsculas: bello, copacabana, medellin, envigado, caldas, sabaneta, estrella):
Casas en cada municipio (SIEMPRE usar WHERE municipio='nombre'):
- "casas en Bello" = SELECT * FROM casas WHERE municipio='bello' LIMIT 25;
- "casas en Copacabana" = SELECT * FROM casas WHERE municipio='copacabana' LIMIT 25;
- "casas en Medellín" = SELECT * FROM casas WHERE municipio='medellin' LIMIT 25;
- "casas en Envigado" = SELECT * FROM casas WHERE municipio='envigado' LIMIT 25;
- "casas en Caldas" = SELECT * FROM casas WHERE municipio='caldas' LIMIT 25;
- "casas en Sabaneta" = SELECT * FROM casas WHERE municipio='sabaneta' LIMIT 25;
- "casas en La Estrella" = SELECT * FROM casas WHERE municipio='estrella' LIMIT 25;
- "Casas en Medellín" = SELECT * FROM casas WHERE municipio='medellin' LIMIT 25;
- "Casas en Sabaneta" = SELECT * FROM casas WHERE municipio='sabaneta' LIMIT 25;
- "Casas en Caldas" = SELECT * FROM casas WHERE municipio='caldas' LIMIT 25;

Ejemplos combinados con municipio:
- "2 cuartos en Medellín" = SELECT * FROM casas WHERE municipio='medellin' AND bedroom=2 LIMIT 25;
- "Copacabana, 1 millón, parqueadero" = SELECT * FROM casas WHERE municipio='copacabana' AND price<=1000000 AND parking>0 LIMIT 25;
- "Envigado, 3 cuartos, 2 baños" = SELECT * FROM casas WHERE municipio='envigado' AND bedroom=3 AND toilet=2 LIMIT 25;
- "Caldas, menos de 50 m²" = SELECT * FROM casas WHERE municipio='caldas' AND squareMeters<50 LIMIT 25;
- "Sabaneta, 2 baños, parqueadero" = SELECT * FROM casas WHERE municipio='sabaneta' AND toilet=2 AND parking>0 LIMIT 25;
- "La Estrella, 1 cuarto, 1 baño" = SELECT * FROM casas WHERE municipio='estrella' AND bedroom=1 AND toilet=1 LIMIT 25;
- "Bello, baratas" = SELECT * FROM casas WHERE municipio='bello' ORDER BY price ASC LIMIT 25;
- "Medellín, más de 70 m², 3 cuartos" = SELECT * FROM casas WHERE municipio='medellin' AND squareMeters>70 AND bedroom=3 LIMIT 25;

Español."""
    
    # Crear el agente SIN memoria (nuevo cada vez)
    # No usar variable global - crear nuevo agente cada vez para evitar historial
    agent = create_sql_agent(
        llm=llm,
        toolkit=toolkit,
        verbose=False,
        agent_type="openai-tools",
        handle_parsing_errors=True,
        prefix=custom_prompt,
    )
    
    return agent

def chat_with_agent(query: str, city: str = None) -> str:
    """
    Procesa una consulta y retorna SOLO el string de respuesta del LLM.
    Crea un agente NUEVO cada vez (sin memoria) para evitar acumulación de tokens.
    
    Args:
        query: Consulta del usuario
        city: Ciudad opcional para filtrar (se agrega al query)
    
    Returns:
        String con la respuesta del LLM
    """
    try:
        # Si hay ciudad, agregar filtro al query
        if city:
            city_to_municipio = {
                "Medellín": "medellin", "Medellin": "medellin",
                "Copacabana": "copacabana", "Sabaneta": "sabaneta",
                "La Estrella": "estrella", "La estrella": "estrella", "Estrella": "estrella",
                "Envigado": "envigado", "Caldas": "caldas", "Bello": "bello"
            }
            municipio = city_to_municipio.get(city, city.lower().replace(" ", "_").replace("í", "i").replace("ó", "o").replace("é", "e").replace("á", "a").replace("ú", "u"))
            query = f"Filtrar por municipio='{municipio}'. {query}"
        
        # Agregar LIMIT 25 explícitamente al query
        query = f"{query} IMPORTANTE: Usa LIMIT 25 en la consulta SQL."
        
        # Crear agente NUEVO cada vez (sin memoria/historial)
        agent = create_agent()
        
        # Ejecutar consulta y retornar solo el string
        # Usar invoke con input limpio (sin historial)
        result = agent.invoke({'input': query})
        output = result.get('output') if isinstance(result, dict) else str(result)
        
        return output
        
    except Exception as e:
        return f"Error al procesar la consulta: {str(e)}"
