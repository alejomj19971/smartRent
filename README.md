# 🏠 SmartRent - Sistema de Gestión y Reserva de Propiedades

SmartRent es una aplicación web diseñada para facilitar la gestión y reserva de propiedades en arriendo de manera rápida, segura y completamente digital.

El proyecto busca ofrecer una solución moderna tanto para propietarios como para arrendatarios, optimizando el proceso de alquiler mediante una interfaz intuitiva y un sistema automatizado de reservas.

## 📋 Sobre el MVP (Mínimo Producto Viable)

En su primera versión (MVP), el objetivo es validar la funcionalidad principal del sistema: permitir que los usuarios consulten propiedades disponibles mediante un chat inteligente con IA y realicen búsquedas avanzadas.

Este MVP sirve como base para integrar más adelante módulos adicionales, como pagos en línea, calificaciones de usuarios y gestión avanzada de contratos.

## ✨ Características

- 💬 Chat interactivo con IA (GPT-4o-mini) para consultas sobre propiedades
- 🔍 Búsqueda inteligente con filtros avanzados
- 📍 Soporte multi-municipio (Bello, Copacabana, Medellín, Envigado, Caldas, Sabaneta, La Estrella)
- 🖼️ Visualización moderna con tarjetas interactivas
- 🤖 Scraping automatizado de sitios inmobiliarios

## 🚀 Instalación Rápida (Windows)

### Prerrequisitos
- Python 3.8+ ([Descargar](https://www.python.org/downloads/))
- Node.js 16+ ([Descargar](https://nodejs.org/))
- Git ([Descargar](https://git-scm.com/downloads))
- API Key de OpenAI (te la proporcionará el propietario)

### Pasos de Instalación

1. **Clonar el repositorio**
```bash
git clone https://github.com/alejomj19971/smartRent.git
cd appRent
```

2. **Configurar API Key**

Crea el archivo `.env` en la raíz del proyecto (misma carpeta donde está `requirements.txt`) y pega:
```
OPENAI_API_KEY=sk-tu-api-key-aqui
```
(Reemplaza `sk-tu-api-key-aqui` con la API key que te proporcionaron)

3. **Instalar Backend**
```bash
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
```

4. **Instalar Frontend**
```bash
cd front
npm install
cd ..
```

5. **Ejecutar la aplicación**
```bash
start.bat
```

6. **Abrir en el navegador**
```
http://localhost:5173
```

### Poblar Base de Datos (Opcional)
```bash
venv\Scripts\activate
python ejecutar_scrapings.py
```

## 📁 Estructura del Proyecto

```
appRent/
├── front/              # Frontend React
├── src/                # Backend FastAPI
├── requirements.txt    # Dependencias Python
├── .env.example        # Plantilla de variables de entorno
└── start.bat           # Script de inicio
```

## 🛠️ Stack Tecnológico

**Backend:** Python, FastAPI, SQLAlchemy, SQLite, LangChain, OpenAI  
**Frontend:** React, Vite, Tailwind CSS  
**Scraping:** BeautifulSoup4, Selenium

## 📝 Uso

### Consultas de Ejemplo
- "casas en Bello"
- "2 cuartos en Medellín"
- "casas con parqueadero y más de 3 habitaciones"
- "1 millón, 2 baños, parqueadero"

### Scripts Útiles
```bash
# Limpiar base de datos
python limpiar_db.py

# Ejecutar scrapings
python ejecutar_scrapings.py

# Ejecutar tests
pytest -v
```

## 🐛 Solución de Problemas

**Error: "OPENAI_API_KEY no encontrada"**
- Verifica que `.env` existe y tiene la API key

**Error: "No module named 'src'"**
- Asegúrate de estar en la raíz del proyecto
- Activa el entorno virtual: `venv\Scripts\activate`

**Puerto 8000 o 5173 ya en uso**
- Cierra otras aplicaciones que usen esos puertos

## 📚 Documentación Adicional

- **[INSTALL.md](INSTALL.md)** - Guía detallada
- **[QUICK_START.md](QUICK_START.md)** - Inicio rápido
- **[SETUP.md](SETUP.md)** - Configuración avanzada

## 🔐 Seguridad

⚠️ **IMPORTANTE:** Nunca subas el archivo `.env` al repositorio. Comparte la API key de forma segura.

---

**Desarrollado con ❤️ usando FastAPI, React y OpenAI**
