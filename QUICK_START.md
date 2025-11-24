# ⚡ Inicio Rápido - SmartRent (Windows)

## Instalación en 5 Pasos

```bash
# 1. Clonar
git clone https://github.com/alejomj19971/smartRent.git
cd appRent

# 2. Configurar API Key
# Crea el archivo .env en la raíz del proyecto y pega:
# OPENAI_API_KEY=sk-tu-api-key-aqui

# 3. Instalar Backend
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt

# 4. Instalar Frontend
cd front
npm install
cd ..

# 5. Ejecutar
start.bat
```

## URLs
- Frontend: http://localhost:5173
- Backend API: http://127.0.0.1:8000
- API Docs: http://127.0.0.1:8000/docs

## Poblar Datos (Opcional)
```bash
venv\Scripts\activate
python ejecutar_scrapings.py
```
