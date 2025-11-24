# 📦 Guía de Instalación - SmartRent (Windows)

## Requisitos Previos
- Python 3.8+ ([Descargar](https://www.python.org/downloads/))
- Node.js 16+ ([Descargar](https://nodejs.org/))
- Git ([Descargar](https://git-scm.com/downloads))
- API Key de OpenAI (te la proporcionará el propietario)

## Instalación Paso a Paso

### 1. Clonar el Repositorio
```bash
git clone https://github.com/alejomj19971/smartRent.git
cd appRent
```

### 2. Configurar API Key

**Obtén la API key del propietario** y luego:

Crea el archivo `.env` en la raíz del proyecto (misma carpeta donde está `requirements.txt`) y pega:
```
OPENAI_API_KEY=sk-tu-api-key-aqui
```
(Reemplaza `sk-tu-api-key-aqui` con la API key real)

### 3. Instalar Backend

```bash
# Crear entorno virtual
python -m venv venv

# Activar entorno virtual
venv\Scripts\activate

# Instalar dependencias
pip install -r requirements.txt
```

### 4. Instalar Frontend

```bash
cd front
npm install
cd ..
```

### 5. Ejecutar

**IMPORTANTE:** Abre **DOS terminales** (CMD o PowerShell) en la carpeta `appRent`

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

### ✅ Verificar

1. Abre http://localhost:5173 en tu navegador
2. Deberías ver la interfaz de chat
3. Prueba escribiendo: "casas disponibles"

### 📊 Poblar Datos (Opcional)

Para tener propiedades en la base de datos:
```bash
venv\Scripts\activate
python ejecutar_scrapings.py
```

## 🆘 Problemas Comunes

### "python: command not found"
- Usa `py` en lugar de `python`

### "npm: command not found"
- Instala Node.js desde [nodejs.org](https://nodejs.org/)

### Error: "OPENAI_API_KEY no encontrada"
- Verifica que el archivo `.env` existe en la raíz del proyecto
- Verifica que tiene el formato correcto: `OPENAI_API_KEY=sk-...`

### Puerto 8000 o 5173 ya en uso
- Cierra otras aplicaciones que usen esos puertos

## 📞 ¿Necesitas Ayuda?

Si tienes problemas:
1. Revisa los logs en las terminales
2. Verifica que todas las dependencias están instaladas
3. Asegúrate de que el archivo `.env` existe y tiene la API key
