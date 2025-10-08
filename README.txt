Descripción

Este proyecto recopila información de algunas plataformas de arriendo del Valle de Aburra  con el fin de  alimentar y entrenar un modelo de LLM o de clasificación para ayudar a las personas  a optimizar el tiempo de busqueda de la propiedad ideal según sus condiciones.


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
