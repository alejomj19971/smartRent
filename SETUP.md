# 🚀 Guía de Configuración Detallada

Esta guía te ayudará a configurar SmartRent paso a paso.

## 📋 Tabla de Contenidos

1. [Requisitos Previos](#requisitos-previos)
2. [Instalación en Windows](#instalación-en-windows)
3. [Instalación en Linux/Mac](#instalación-en-linuxmac)
4. [Configuración de OpenAI](#configuración-de-openai)
5. [Primera Ejecución](#primera-ejecución)
6. [Poblar Base de Datos](#poblar-base-de-datos)

## 🔧 Requisitos Previos

### Windows
- Python 3.8+ ([Descargar](https://www.python.org/downloads/))
- Node.js 16+ ([Descargar](https://nodejs.org/))
- Git ([Descargar](https://git-scm.com/downloads))

### Linux (Ubuntu/Debian)
```bash
sudo apt update
sudo apt install python3 python3-pip python3-venv nodejs npm git
```

### Mac
```bash
# Instalar Homebrew si no lo tienes
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"

# Instalar dependencias
brew install python3 node git
```

## 💻 Instalación en Windows

### Paso 1: Clonar el Repositorio
```bash
git clone https://github.com/tu-usuario/appRent.git
cd appRent
```

### Paso 2: Crear Entorno Virtual
```bash
python -m venv venv
venv\Scripts\activate
```

### Paso 3: Instalar Dependencias Python
```bash
pip install -r requirements.txt
```

### Paso 4: Instalar Dependencias Node.js
```bash
cd front
npm install
cd ..
```

### Paso 5: Configurar Variables de Entorno

Crea el archivo `.env` en la raíz del proyecto (misma carpeta donde está `requirements.txt`) y pega:
```
OPENAI_API_KEY=sk-tu-api-key-aqui
```
(Reemplaza `sk-tu-api-key-aqui` con tu API key real)

### Paso 6: Ejecutar la Aplicación

**Opción A: Usar script de inicio (Recomendado)**
```bash
start.bat
```

**Opción B: Manual**
```bash
# Terminal 1 - Backend
venv\Scripts\activate
python -m uvicorn src.main:app --reload --host 127.0.0.1 --port 8000

# Terminal 2 - Frontend
cd front
npm run dev
```

## 🐧 Instalación en Linux/Mac

### Paso 1: Clonar el Repositorio
```bash
git clone https://github.com/tu-usuario/appRent.git
cd appRent
```

### Paso 2: Crear Entorno Virtual
```bash
python3 -m venv venv
source venv/bin/activate
```

### Paso 3: Instalar Dependencias Python
```bash
pip install -r requirements.txt
```

### Paso 4: Instalar Dependencias Node.js
```bash
cd front
npm install
cd ..
```

### Paso 5: Configurar Variables de Entorno
```bash
# Copiar archivo de ejemplo
cp .env.example .env

# Editar .env
nano .env
# o
vim .env
```

Agrega tu API key de OpenAI:
```
OPENAI_API_KEY=sk-tu-api-key-aqui
```

### Paso 6: Dar Permisos al Script
```bash
chmod +x start.sh
```

### Paso 7: Ejecutar la Aplicación

**Opción A: Usar script de inicio (Recomendado)**
```bash
./start.sh
```

**Opción B: Manual**
```bash
# Terminal 1 - Backend
source venv/bin/activate
python -m uvicorn src.main:app --reload --host 127.0.0.1 --port 8000

# Terminal 2 - Frontend
cd front
npm run dev
```

## 🔑 Configuración de OpenAI

1. **Crear cuenta en OpenAI**
   - Ve a [platform.openai.com](https://platform.openai.com)
   - Crea una cuenta o inicia sesión

2. **Obtener API Key**
   - Ve a [API Keys](https://platform.openai.com/api-keys)
   - Haz clic en "Create new secret key"
   - Copia la clave (solo se muestra una vez)

3. **Configurar en el proyecto**
   - Abre el archivo `.env`
   - Pega tu API key:
     ```
     OPENAI_API_KEY=sk-tu-api-key-aqui
     ```

## 🎯 Primera Ejecución

1. **Verificar que todo funciona**
   - Backend: Abre http://127.0.0.1:8000/docs (deberías ver la documentación de la API)
   - Frontend: Abre http://localhost:5173 (deberías ver la interfaz)

2. **Probar el chat**
   - Escribe "casas disponibles" en el chat
   - Si no hay datos, verás un mensaje (esto es normal)

## 📊 Poblar Base de Datos

Para tener propiedades en la base de datos, ejecuta los scrapings:

```bash
# Activar entorno virtual primero
# Windows:
venv\Scripts\activate
# Linux/Mac:
source venv/bin/activate

# Ejecutar scrapings
python ejecutar_scrapings.py
```

**Nota:** Los scrapings pueden tardar varios minutos dependiendo de la cantidad de páginas.

## ✅ Verificación

### Verificar Backend
```bash
curl http://127.0.0.1:8000/casas/total
```
Deberías recibir: `{"total":0}` (o el número de propiedades si ya hay datos)

### Verificar Base de Datos
```bash
# Windows
python -m sqlite3 rents.db "SELECT COUNT(*) FROM casas;"

# Linux/Mac
sqlite3 rents.db "SELECT COUNT(*) FROM casas;"
```

## 🐛 Problemas Comunes

### "python: command not found"
- Windows: Usa `py` en lugar de `python`
- Linux/Mac: Usa `python3` en lugar de `python`

### "npm: command not found"
- Instala Node.js desde [nodejs.org](https://nodejs.org/)

### Error de permisos en Linux/Mac
```bash
chmod +x start.sh
```

### Puerto 8000 o 5173 ya en uso
- Cambia el puerto en los comandos de inicio
- O cierra la aplicación que está usando el puerto

## 📞 ¿Necesitas Ayuda?

Si tienes problemas:
1. Revisa los logs en las terminales
2. Verifica que todas las dependencias están instaladas
3. Asegúrate de que el archivo `.env` existe y tiene la API key
4. Abre un issue en GitHub con los detalles del error

