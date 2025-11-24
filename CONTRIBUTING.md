# 🤝 Guía para Colaboradores

## Para Nuevos Colaboradores

### 1. Obtener la API Key

**IMPORTANTE:** El propietario del repositorio te proporcionará la API key de OpenAI. 

Una vez que la tengas:
1. Copia `.env.example` a `.env`
2. Edita `.env` y pega tu API key

```bash
# Windows
copy .env.example .env
notepad .env

# Linux/Mac
cp .env.example .env
nano .env
```

### 2. Instalación

Sigue las instrucciones en [INSTALL.md](INSTALL.md) o [QUICK_START.md](QUICK_START.md).

### 3. Estructura del Proyecto

- `front/` - Frontend React
- `src/` - Backend FastAPI
- `src/utils/` - Scripts de scraping
- `.env` - Variables de entorno (NO subir a Git)

### 4. Comandos Útiles

```bash
# Limpiar base de datos
python limpiar_db.py

# Ejecutar scrapings
python ejecutar_scrapings.py

# Ejecutar tests
pytest
```

### 5. Antes de Hacer Commit

- ✅ Verifica que `.env` NO está en el commit
- ✅ Ejecuta los tests: `pytest`
- ✅ Verifica que el código funciona localmente

### 6. Hacer Pull Request

1. Crea una rama: `git checkout -b mi-feature`
2. Haz tus cambios
3. Commit: `git commit -m "Descripción de cambios"`
4. Push: `git push origin mi-feature`
5. Abre un Pull Request en GitHub

## 🚫 No Subir a Git

- `.env` (contiene API keys)
- `venv/` (entorno virtual)
- `node_modules/` (dependencias Node)
- `*.db` (bases de datos)
- `__pycache__/` (archivos compilados)

Todos estos están en `.gitignore`.

