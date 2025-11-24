# 🏠 SmartRent - Asistente Inmobiliario Inteligente

Sistema de chat inteligente para búsqueda de propiedades inmobiliarias con integración de IA (OpenAI GPT-4o-mini) y scraping web automatizado.

## 📋 Características

- 💬 Chat interactivo con IA para consultas sobre propiedades
- 🔍 Búsqueda inteligente con árbol de prefijos (Trie)
- 🏘️ Filtros avanzados por precio, habitaciones, baños, parqueaderos y metros cuadrados
- 📍 Soporte para múltiples municipios (Bello, Copacabana, Medellín, Envigado, Caldas, Sabaneta, La Estrella)
- 🖼️ Visualización de propiedades con tarjetas interactivas
- 🤖 Scraping automatizado de sitios inmobiliarios
- 📊 Base de datos SQLite para almacenamiento local

## 🚀 Inicio Rápido

### Prerrequisitos

- Python 3.8 o superior
- Node.js 16 o superior
- npm o yarn
- Clave API de OpenAI

### Instalación

1. **Clonar el repositorio**
```bash
git clone https://github.com/tu-usuario/appRent.git
cd appRent
```

2. **Configurar variables de entorno**
```bash
# Copiar el archivo de ejemplo
cp .env.example .env

# Editar .env y agregar tu API key de OpenAI
# OPENAI_API_KEY=tu-api-key-aqui
```

3. **Instalar dependencias del backend**
```bash
# Crear entorno virtual
python -m venv venv

# Activar entorno virtual
# Windows:
venv\Scripts\activate
# Linux/Mac:
source venv/bin/activate

# Instalar dependencias
pip install -r requirements.txt
```

4. **Instalar dependencias del frontend**
```bash
cd front
npm install
cd ..
```

5. **Inicializar la base de datos**
```bash
# La base de datos se creará automáticamente al ejecutar el servidor
# Si necesitas limpiarla:
python limpiar_db.py
```

6. **Ejecutar la aplicación**

**IMPORTANTE:** Abre DOS terminales (CMD o PowerShell) en la carpeta `appRent`

**Terminal 1 - Backend:**
```bash
venv\Scripts\activate
python -m uvicorn src.main:app --reload --host 127.0.0.1 --port 8000
```
Espera a ver: `Uvicorn running on http://127.0.0.1:8000`

**Terminal 2 - Frontend:**
```bash
cd front
npm run dev
```
Espera a ver: `Local: http://localhost:5173`

7. **Abrir en el navegador**
```
http://localhost:5173
```

## 📁 Estructura del Proyecto

```
appRent/
├── front/                 # Frontend React + Vite
│   ├── src/
│   │   ├── components/   # Componentes React
│   │   ├── utils/        # Utilidades (Trie, etc.)
│   │   └── App.jsx       # Componente principal
│   ├── package.json
│   └── vite.config.js
├── src/                  # Backend FastAPI
│   ├── main.py          # Servidor FastAPI
│   ├── chat_service.py  # Servicio de chat con IA
│   ├── crud.py          # Operaciones CRUD
│   ├── models.py        # Modelos SQLAlchemy
│   ├── database.py      # Configuración de BD
│   ├── property_matcher.py  # Matching de propiedades
│   ├── scraping_queue.py    # Cola de scraping
│   └── utils/           # Scripts de scraping
├── requirements.txt      # Dependencias Python
├── .env.example         # Ejemplo de variables de entorno
├── .gitignore
└── README.md
```

## 🔧 Configuración

### Variables de Entorno

Crea un archivo `.env` en la raíz del proyecto:

```env
OPENAI_API_KEY=sk-tu-api-key-aqui
```

### Base de Datos

La aplicación usa SQLite. La base de datos `rents.db` se crea automáticamente en la raíz del proyecto.

**Tabla `casas`:**
- `id`: ID único
- `title`: Título de la propiedad
- `price`: Precio en COP
- `bedroom`: Número de habitaciones
- `toilet`: Número de baños
- `parking`: Número de parqueaderos
- `squareMeters`: Metros cuadrados
- `image`: URL de la imagen
- `municipio`: Municipio (bello, copacabana, medellin, etc.)

## 📝 Uso

### Consultas de Ejemplo

- "casas en Bello"
- "2 cuartos en Medellín"
- "casas con parqueadero y más de 3 habitaciones"
- "casas disponibles"
- "1 millón, 2 baños, parqueadero"
- "casas en La Estrella, menos de 50 m²"

### Scraping de Datos

Para poblar la base de datos con propiedades:

```bash
# Ejecutar todos los scrapings
python ejecutar_scrapings.py
```

Esto ejecutará los scrapings para todos los municipios configurados.

## 🛠️ Scripts Útiles

### Limpiar Base de Datos
```bash
python limpiar_db.py
```

### Ejecutar Scrapings
```bash
python ejecutar_scrapings.py
```

## 🧪 Testing

```bash
# Ejecutar tests
pytest
```

## 📦 Dependencias Principales

### Backend
- FastAPI: Framework web
- SQLAlchemy: ORM para base de datos
- LangChain: Integración con OpenAI
- BeautifulSoup4 + Selenium: Web scraping
- pandas: Procesamiento de datos

### Frontend
- React 18
- Vite: Build tool
- Tailwind CSS: Estilos (via CDN)

## 🔍 Características Técnicas

### Estructuras de Datos
- **Trie (Árbol de Prefijos)**: Para búsqueda eficiente de propiedades en el frontend
- **Cola (Queue)**: Para gestión de tareas de scraping
- **HashMap**: Para filtros y mapeo de datos

### Algoritmos
- Búsqueda por prefijos: O(m + k) donde m es la longitud del prefijo y k el número de resultados
- Matching de propiedades: Sistema de scoring flexible con múltiples niveles de fallback

## 🐛 Solución de Problemas

### Error: "OPENAI_API_KEY no encontrada"
- Verifica que el archivo `.env` existe en la raíz del proyecto
- Verifica que la variable `OPENAI_API_KEY` está configurada correctamente

### Error: "No module named 'src'"
- Asegúrate de estar en la raíz del proyecto al ejecutar comandos
- Verifica que el entorno virtual está activado

### El frontend no se conecta al backend
- Verifica que el backend está corriendo en `http://127.0.0.1:8000`
- Verifica la configuración de CORS en `src/main.py`

### No aparecen tarjetas de propiedades
- Verifica que la base de datos tiene datos: `python -m sqlite3 rents.db "SELECT COUNT(*) FROM casas;"`
- Ejecuta los scrapings: `python ejecutar_scrapings.py`

## 📄 Licencia

Este proyecto es de código abierto.

## 👥 Contribuir

Las contribuciones son bienvenidas. Por favor:
1. Fork el proyecto
2. Crea una rama para tu feature (`git checkout -b feature/AmazingFeature`)
3. Commit tus cambios (`git commit -m 'Add some AmazingFeature'`)
4. Push a la rama (`git push origin feature/AmazingFeature`)
5. Abre un Pull Request

## 📞 Soporte

Para problemas o preguntas, abre un issue en GitHub.

---

**Desarrollado con ❤️ usando FastAPI, React y OpenAI**

