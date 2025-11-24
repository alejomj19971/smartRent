from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup
import pandas as pd
import time
from urllib.parse import urljoin

def obtener_casas():
    options = Options()
    options.add_argument("--headless")  # para que no se abra la ventana (opcional)
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")

    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

    url = "https://www.metrocuadrado.com/apartamentos/arriendo/copacabana/"

    titulos = []
    precios = []
    banios = []
    cuartos = []
    metroscuadrados = []
    parqueaderos = []
    imagenes = []

    while True:
        driver.get(url)
        time.sleep(5)

        # Scroll dinámico hasta que no carguen más tarjetas
        prev_len = 0
        while True:
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(3)
            new_len = len(driver.find_elements(By.CSS_SELECTOR, ".property-card__container"))
            if new_len == prev_len:
                break
            prev_len = new_len

        # Analizar contenido
        contenido = driver.page_source
        soup = BeautifulSoup(contenido, "html.parser")
        for casa in soup.find_all("div", attrs={"class": "property-card__container property-card__default property-card__default-normal"}):
            titulo = casa.find("h2")
            titulos.append(titulo.text[:-12] if titulo else "N/A")

            precio = casa.find("div", attrs={"class": "property-card__detail-price"})
            precios.append(int(precio.text.replace("$", "").replace(".", "")) if precio else 0)

            # Extraer URL de la imagen
            # Intentar primero con data-src (lazy loading), luego con src
            img = casa.find("img")
            imagen_url = ""
            if img:
                # Probar data-src primero (lazy loading común)
                imagen_url = img.get("data-src") or img.get("data-lazy-src") or img.get("src") or ""
                # Si la URL es relativa, convertirla a absoluta
                if imagen_url and not imagen_url.startswith("http"):
                    imagen_url = urljoin("https://www.metrocuadrado.com", imagen_url)
            imagenes.append(imagen_url)

            specs = casa.find("pt-main-specs")
            if specs:
                banios.append(int(specs.get("toilets", 0)))
                cuartos.append(int(specs.get("bedrooms", 0)))
                metroscuadrados.append(int(specs.get("squaremeter", 0)))
                parqueaderos.append(int(specs.get("parking", 0)))
            else:
                banios.append(0)
                cuartos.append(0)
                metroscuadrados.append(0)
                parqueaderos.append(0)

        # Buscar el enlace a la siguiente página
        siguientepag = soup.select_one("li.next > a")
        if siguientepag:
            url = urljoin(url, siguientepag.get("href"))
        else:
            break  # no hay más páginas

    driver.quit()

    df = pd.DataFrame({
        "title": titulos,
        "price": precios,
        "squareMeters": metroscuadrados,
        "bedroom": cuartos,
        "toilet": banios,
        "parking": parqueaderos,
        "image": imagenes
    })



    return df

