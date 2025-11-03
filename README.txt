SmartRent es una aplicación web diseñada para facilitar la gestión y reserva de propiedades en arriendo de manera rápida, segura y completamente digital.
El proyecto busca ofrecer una solución moderna tanto para propietarios como para arrendatarios, optimizando el proceso de alquiler mediante una interfaz intuitiva y un sistema automatizado de reservas.

En su primera versión (MVP – Mínimo Producto Viable), el objetivo es validar la funcionalidad principal del sistema: permitir que los usuarios se registren, consulten propiedades disponibles y realicen una reserva simulada.
Este MVP servirá como base para integrar más adelante módulos adicionales, como pagos en línea, calificaciones de usuarios y gestión avanzada de contratos.


Diseño : 

1.Realizar Web Scrapping con BeautifulSoup de plataformas de arriendos.

2.Alimentar una base de datos postgreSQL o MongoDB según lo homogeneidad de los datos.

3.Entrenar un modelo con Pytorch y Tranformers u otras tecnologías.

4.Crear una interfaz sencilla con js y react.

5.Publicar en vercel o alguna plataforma.

6.Realizar pruebas con pytest y con consultas.



Tecnologías utilizadas:


Este stack de tecnologías es compacto y funcional para el análisis,  y minado de datos necesarios en el proyecto.

Lenguaje: Python

Framework Backend: FastAPI

Base de datos: SQLite

ORM: SQLAlchemy

Procesamiento de datos: Pandas

Scraping: BeautifulSoup

API y conexión: Requests

Modelo de lenguaje (LLM): para análisis inteligente de arriendos




Instrucciones: 

1)En una carpeta abrir el buscador de archivos y colocar cmd
 
2)git clone https://github.com/alejomj19971/smartRent.git

3) cd smartRent

4) pip install -r requirements.txt

5)cd src

6) uvicorn main:app --reload

7)http://127.0.0.1:8000  estan todos los endpoints  http://127.0.0.1:8000/docs 

8) Se puede ver los datos cargados en la base de datos después de hacer scrapping a una pagina de arriendos.

9) Para realizar las pruebas vaya a la raiz del proyecto una carpeta antes de src y user pytest -v
