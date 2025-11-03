# -*- coding: utf-8 -*-
import os
from pathlib import Path
from dotenv import load_dotenv

# Cargar variables de entorno desde .env
project_root = Path(__file__).resolve().parent.parent
env_path = project_root / '.env'
load_dotenv(dotenv_path=env_path)

try:
    from langchain_community.utilities import SQLDatabase
    from langchain_community.agent_toolkits import create_sql_agent
    from langchain_openai import ChatOpenAI
    from langchain_community.agent_toolkits.sql.toolkit import SQLDatabaseToolkit

except Exception as e:
    print('Error importing required packages:', e)
    print('Make sure you run this script with Python 3 and have installed the requirements.')
    raise

# Obtener la ruta absoluta del directorio raíz del proyecto (ya definido arriba)
db_path = project_root / "rents.db"
db_uri = f"sqlite:///{db_path.absolute()}"

print(f'Buscando rents.db en: {db_path}')
print(f'¿Existe rents.db?: {db_path.exists()}')

# 1) Conectar con tu base de datos usando la ruta absoluta
try:
    if not db_path.exists():
        print(f'ERROR: No se encontró la base de datos en: {db_path}')
        print('Asegúrate de que rents.db existe en la raíz del proyecto.')
        exit(1)
    
    db = SQLDatabase.from_uri(
        db_uri,
        sample_rows_in_table_info=3,
        include_tables=['casas']
    )
    print(f'Base de datos conectada correctamente. DB URI: {db_uri}')
    
    # Verificar que la tabla existe y tiene datos
    table_info = db.get_table_info()
    print(f'Información de la tabla:\n{table_info[:500]}...')  # Primeros 500 caracteres
    
except Exception as e:
    print('Error conectando a la base de datos:', e)
    import traceback
    traceback.print_exc()
    exit()

# 2) Configurar el modelo OpenAI
try:
    api_key = os.getenv('OPENAI_API_KEY')
    if not api_key:
        print('ERROR: No se encontró OPENAI_API_KEY en el archivo .env')
        print(f'Por favor, verifica que el archivo .env existe en: {env_path}')
        print('El archivo .env debe contener:')
        print('OPENAI_API_KEY=tu_api_key_completa')
        print('\nObtén tu API key en: https://platform.openai.com/api-keys')
        exit(1)
    
    # Configurar la API key de OpenAI
    os.environ['OPENAI_API_KEY'] = api_key
    
    llm = ChatOpenAI(
        model='gpt-4o-mini',  # Puedes cambiar a 'gpt-4' si tienes acceso
        temperature=0
    )
    print('Modelo OpenAI cargado correctamente')
except Exception as e:
    print('Error cargando modelo OpenAI:', e)
    import traceback
    traceback.print_exc()
    exit()


# Crear toolkit SQL con las herramientas necesarias
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

# Crear el agente con acceso real a la base de datos y prompt personalizado
# Para OpenAI, usar "openai-tools" es mejor que "zero-shot-react-description"
agent_executor = create_sql_agent(
    llm=llm,
    toolkit=toolkit,
    verbose=True,
    agent_type="openai-tools",
    handle_parsing_errors=True,
    prefix=custom_prompt,
)

# 4) Interacción: ejemplos de preguntas
print('SmartRent AI conectado. Pregunta sobre las propiedades:')
print('\nEjemplos de preguntas:')
print("- 'Buscar casas que valgan menos de un millón doscientos'")
print("- 'Cuántas casas hay disponibles?' (columna: active)")
print("- 'Cuál es el precio promedio de las casas?'")
print("- 'Cuántas casas tienen más de 3 habitaciones?' (columna: bedroom)")
print("- 'Cuántas casas tienen parqueadero?' (columna: parking)")
print("- 'Lista las 5 casas más caras'")
print("- 'Cuántos baños tiene la casa más grande?' (columnas: toilet, squareMeters)")

while True:
    query = input('\nTu pregunta: ')
    if query.lower() in ["salir", "exit", "quit"]:
        print("👋 Adiós.")
        break

    try:
        print('Procesando...')
        # Forzar uso de la tabla correcta y respuestas en español
        forced_query = f"Responde en español. {query}"
        result = agent_executor.invoke({'input': forced_query})
        output = result.get('output') if isinstance(result, dict) else str(result)
        print('\n' + '='*70)
        print('SmartRent:')
        print(output)
        print('='*70)
    except Exception as e:
        print('\nError al procesar la consulta:', e)
        import traceback
        traceback.print_exc()
        print('Consejo: intenta reformular tu pregunta')

# Información del esquema para referencia
print('\nEsquema de la base de datos:')
print('Tabla: casas')
print('Columnas: id, title, price, toilet, bedroom, squareMeters, parking, active')
print('- toilet = Integer (número de baños, ej: 0, 1, 2, 3...)')
print('- bedroom = Integer (número de habitaciones, ej: 0, 1, 2, 3...)')
print('- squareMeters = Integer (metros cuadrados)')
print('- parking = Integer (número de parqueaderos, ej: 0=sin parqueadero, 1, 2, 3...)')
print('- active = Boolean (disponible/no disponible)')