SmartRent es una aplicación web diseñada para facilitar la gestión y reserva de propiedades en arriendo de manera rápida, segura y completamente digital.
El proyecto busca ofrecer una solución moderna tanto para propietarios como para arrendatarios, optimizando el proceso de alquiler mediante una interfaz intuitiva y un sistema automatizado de reservas.

En su primera versión (MVP – Mínimo Producto Viable), el objetivo es validar la funcionalidad principal del sistema: permitir que los usuarios se registren, consulten propiedades disponibles y realicen una reserva simulada.
Este MVP servirá como base para integrar más adelante módulos adicionales, como pagos en línea, calificaciones de usuarios y gestión avanzada de contratos.


Diseño : 

1.Realizar Web Scrapping con BeautifulSoup de plataformas de arriendos en Copacabana y medellín.

2.Alimentar una base de datos sqlite3.

3.Utilizar langchain para conectar con modelos locales  y consumir las consultas 
a la base de datos generados.

3.1Conexión con modelo de análisis de contexto o NPL como GPT 4

4.Crear una interfaz sencilla con js y react.

5.Publicar en vercel o alguna plataforma.

6.Realizar pruebas con pytest y con consultas.



Tecnologías utilizadas:


Este stack de tecnologías es compacto y funcional para el análisis,  y minado de datos necesarios en el proyecto.

Lenguaje: Python

Framework Backend: FastAPI

Base de datos: SQLite3

ORM: SQLAlchemy

Procesamiento de datos: Pandas

Scraping: BeautifulSoup

API y conexión: Requests

Conexión a modelos: Langchain

Modelo de lenguaje (LLM): para análisis inteligente de arriendos , OpenAI es fácil de integrar y reconoce a bajo costo la base de datos entregada, no necesitamos un modelo de última versión sino uno que podamos ofrecerle suficiente contexto para que realice lo que el usuario necesita.





Instrucciones: 

1)En una carpeta abrir el buscador de archivos y colocar cmd
 
2)git clone https://github.com/alejomj19971/smartRent.git

3) en la terminal cd appRent.

4)venv\Scripts\activate en la terminal

5) pip install -r requirements.txt

6) uvicorn main:app --reload

7)http://127.0.0.1:8000 encontraras el formulario y en  http://127.0.0.1:8000/docs  esta la documentación de la API

8) Se puede ver los datos cargados en la base de datos después de hacer scrapping a una pagina de arriendos.

9) Para realizar las pruebas vaya a la raiz del proyecto una carpeta antes de src y user pytest -v
