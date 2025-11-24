# SmartRent Frontend - React

Frontend de SmartRent construido con React y Vite.

## Instalación

```bash
npm install
```

## Desarrollo

Para ejecutar el servidor de desarrollo:

```bash
npm run dev
```

El frontend estará disponible en `http://localhost:5173` (puerto por defecto de Vite).

## Construcción para Producción

Para construir la aplicación para producción:

```bash
npm run build
```

Los archivos se generarán en el directorio `dist/`, que será servido por FastAPI.

## Estructura del Proyecto

```
front/
├── src/
│   ├── components/
│   │   ├── ChatMessages.jsx    # Componente para mostrar mensajes
│   │   ├── MessageBubble.jsx   # Burbuja de mensaje individual
│   │   ├── PropertyCard.jsx    # Tarjeta de propiedad con imagen e iconos
│   │   ├── ChatInput.jsx       # Input para enviar mensajes
│   │   └── QuickQuestions.jsx # Botones de preguntas rápidas
│   ├── App.jsx                 # Componente principal
│   ├── main.jsx                # Punto de entrada
│   └── index.css               # Estilos globales
├── index.html                  # HTML base
├── package.json                # Dependencias
└── vite.config.js              # Configuración de Vite
```

## Componentes

### PropertyCard
Componente que muestra una propiedad inmobiliaria con:
- Imagen de la propiedad
- Título
- Precio formateado
- Iconos para: habitaciones, baños, parqueaderos, metros cuadrados

