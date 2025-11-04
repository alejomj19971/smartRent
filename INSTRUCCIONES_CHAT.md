# 📱 Cómo Acceder a la Ventana de Chat

## Pasos para usar el chat:

### 1. Activar el entorno virtual (si no está activo)
```bash
# En Windows PowerShell
.\venv\Scripts\Activate.ps1

# O en CMD
venv\Scripts\activate.bat
```

### 2. Iniciar el servidor FastAPI
Desde la raíz del proyecto (appRent):
```bash
cd src
uvicorn main:app --reload
```

**O desde la raíz directamente:**
```bash
uvicorn src.main:app --reload
```

### 3. Abrir el navegador
Una vez que veas el mensaje:
```
Uvicorn running on http://127.0.0.1:8000
```

Abre tu navegador y ve a:
```
http://127.0.0.1:8000
```

O también puedes usar:
```
http://localhost:8000
```

### 4. ¡Listo! 🎉
Verás la interfaz del chat con:
- Mensaje de bienvenida
- Campo para escribir preguntas
- Botones de preguntas rápidas
- Historial de conversación

## Notas importantes:
- ✅ Asegúrate de tener el archivo `.env` con tu `OPENAI_API_KEY`
- ✅ La base de datos `rents.db` debe existir en la raíz del proyecto
- ✅ El servidor debe estar corriendo para que el chat funcione

## Endpoints disponibles:
- `http://127.0.0.1:8000` - Interfaz de chat (frontend)
- `http://127.0.0.1:8000/docs` - Documentación de la API (Swagger)
- `http://127.0.0.1:8000/chat` - Endpoint POST para el chat (API)

## Ejemplos de preguntas:
- "Cuántas casas hay disponibles?"
- "Casas con parqueadero"
- "Buscar casas menores a 2 millones"
- "Lista las 5 casas más caras"

