Instrucciones: 

1)En una carpeta abrir el buscador de archivos y colocar cmd
 
2)git clone https://github.com/alejomj19971/smartRent.git

3) cd smartRent

4) pip install -r requirements.txt

5)cd src

6) uvicorn main:app --reload

7)http://127.0.0.1:8000 

8) Se puede ver los datos cargados en la base de datos después de hacer scrapping a una pagina de arriendos.

9) Para realizar las pruebas vaya a la raiz del proyecto una carpeta antes de src y user pytest -v