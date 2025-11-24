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

# 5. Ejecutar (Abre DOS terminales en la carpeta appRent)

# Terminal 1 - Backend:
venv\Scripts\activate
python -m uvicorn src.main:app --reload --host 127.0.0.1 --port 8000

# Terminal 2 - Frontend:
cd front
npm run dev
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
