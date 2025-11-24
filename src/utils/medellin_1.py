from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup
import pandas as pd
import time
from urllib.parse import urljoin
import re

def obtener_casas():
    options = Options()
    options.add_argument("--headless")  # para que no se abra la ventana (opcional)
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")

    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

    base_url = "https://www.ciencuadras.com/arriendo/medellin"
    url = f"{base_url}?gad_campaignid=13163942603"

    titulos = []
    precios = []
    banios = []
    cuartos = []
    metroscuadrados = []
    parqueaderos = []
    imagenes = []

    max_pages = 1  # Solo primera página
    current_page = 1

    while current_page <= max_pages:
        print(f"Procesando página {current_page} de {max_pages}...")
        driver.get(url)
        time.sleep(5)

        # Scroll dinámico para cargar contenido
        prev_len = 0
        scroll_attempts = 0
        max_scroll_attempts = 5
        
        while scroll_attempts < max_scroll_attempts:
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(2)
            new_len = len(driver.find_elements(By.CSS_SELECTOR, "article, .property-card, [class*='property'], [class*='inmueble']"))
            if new_len == prev_len:
                break
            prev_len = new_len
            scroll_attempts += 1

        # Scroll adicional hacia arriba para asegurar que todo esté cargado
        driver.execute_script("window.scrollTo(0, 0);")
        time.sleep(2)

        # Analizar contenido
        contenido = driver.page_source
        soup = BeautifulSoup(contenido, "html.parser")

        # Buscar propiedades - intentar diferentes selectores comunes en Ciencuadras
        propiedades = soup.find_all("article")
        
        if not propiedades:
            # Intentar buscar por clases comunes
            propiedades = soup.find_all("div", class_=re.compile("property|inmueble|card|listing", re.I))
        
        if not propiedades:
            # Intentar buscar por estructura de datos
            propiedades = soup.find_all("div", attrs={"data-testid": re.compile("property|listing", re.I)})
        
        if not propiedades:
            # Buscar por enlaces que contengan información de propiedades
            propiedades = soup.find_all("a", href=re.compile("/arriendo|/propiedad|/inmueble", re.I))
            # Si encontramos enlaces, buscar el contenedor padre
            if propiedades:
                propiedades = [p.parent if p.parent else p for p in propiedades]

        print(f"Encontradas {len(propiedades)} propiedades en la página {current_page}")

        for prop in propiedades:
            try:
                # Extraer título/ubicación
                titulo = ""
                texto_completo = prop.get_text()
                
                # Buscar en diferentes lugares donde puede estar la ubicación
                ubicacion_elem = (
                    prop.find("h2") or 
                    prop.find("h3") or 
                    prop.find("a", class_=re.compile("title|name|ubicacion|location", re.I)) or
                    prop.find("div", class_=re.compile("title|name|ubicacion|location", re.I)) or
                    prop.find("span", class_=re.compile("title|name|ubicacion|location", re.I)) or
                    prop.find("p", class_=re.compile("title|name|ubicacion|location", re.I))
                )
                
                if ubicacion_elem:
                    titulo = ubicacion_elem.get_text(strip=True)
                else:
                    # Intentar extraer ubicación de patrones comunes en Ciencuadras
                    # Formato típico: "Apartamento en arriendo Antioquia Medellín [Barrio]"
                    ubicacion_match = re.search(r'(?:Apartamento|Casa|Local|Oficina|Apartaestudio).*?Medellín[^,]*?([^,]+)', texto_completo, re.I)
                    if ubicacion_match:
                        # Extraer el barrio/ubicación específica
                        barrio = ubicacion_match.group(1).strip()
                        # Construir título completo
                        tipo_match = re.search(r'(Apartamento|Casa|Local|Oficina|Apartaestudio)', texto_completo, re.I)
                        tipo = tipo_match.group(1) if tipo_match else "Inmueble"
                        titulo = f"{tipo} en arriendo, Medellín, {barrio}"
                    else:
                        # Buscar cualquier texto que parezca una ubicación
                        ubicacion_match = re.search(r'Medellín[^,]*?([^,]+)', texto_completo, re.I)
                        if ubicacion_match:
                            titulo = f"Inmueble en arriendo, Medellín, {ubicacion_match.group(1).strip()}"
                
                if not titulo or titulo == "":
                    titulo = "N/A"

                # Extraer precio
                precio = 0
                precio_text = prop.find(string=re.compile(r'\$\d+'))
                if precio_text:
                    precio_str = re.search(r'\$?([\d,\.]+)', precio_text)
                    if precio_str:
                        precio = int(precio_str.group(1).replace(".", "").replace(",", ""))
                else:
                    precio_elem = (
                        prop.find("div", class_=re.compile("price|precio", re.I)) or
                        prop.find("span", class_=re.compile("price|precio", re.I)) or
                        prop.find("p", class_=re.compile("price|precio", re.I))
                    )
                    if precio_elem:
                        precio_text = precio_elem.get_text()
                        precio_match = re.search(r'\$?([\d,\.]+)', precio_text)
                        if precio_match:
                            precio = int(precio_match.group(1).replace(".", "").replace(",", ""))

                # Extraer especificaciones (habitaciones, baños, parqueaderos, metros)
                texto_completo = prop.get_text()
                
                # Buscar habitaciones
                habitaciones = 0
                habit_match = re.search(r'(\d+)\s*(?:habitaciones?|hab\.?|cuartos?)', texto_completo, re.I)
                if habit_match:
                    habitaciones = int(habit_match.group(1))
                else:
                    # Buscar en atributos data o clases
                    habit_elem = prop.find(attrs={"class": re.compile("bedroom|habitacion", re.I)})
                    if habit_elem:
                        habit_text = habit_elem.get_text()
                        habit_match = re.search(r'(\d+)', habit_text)
                        if habit_match:
                            habitaciones = int(habit_match.group(1))

                # Buscar baños
                banios_count = 0
                banio_match = re.search(r'(\d+)\s*(?:baños?|bath)', texto_completo, re.I)
                if banio_match:
                    banios_count = int(banio_match.group(1))
                else:
                    banio_elem = prop.find(attrs={"class": re.compile("bath|baño", re.I)})
                    if banio_elem:
                        banio_text = banio_elem.get_text()
                        banio_match = re.search(r'(\d+)', banio_text)
                        if banio_match:
                            banios_count = int(banio_match.group(1))

                # Buscar parqueaderos
                parqueaderos_count = 0
                parq_match = re.search(r'(\d+)\s*(?:parqueaderos?|garajes?|parq\.?)', texto_completo, re.I)
                if parq_match:
                    parqueaderos_count = int(parq_match.group(1))
                else:
                    parq_elem = prop.find(attrs={"class": re.compile("parking|garage|parqueadero", re.I)})
                    if parq_elem:
                        parq_text = parq_elem.get_text()
                        parq_match = re.search(r'(\d+)', parq_text)
                        if parq_match:
                            parqueaderos_count = int(parq_match.group(1))

                # Buscar metros cuadrados
                metros = 0
                metros_match = re.search(r'(\d+)\s*m[²2]', texto_completo, re.I)
                if metros_match:
                    metros = int(metros_match.group(1))
                else:
                    metros_elem = prop.find(attrs={"class": re.compile("area|metros|square", re.I)})
                    if metros_elem:
                        metros_text = metros_elem.get_text()
                        metros_match = re.search(r'(\d+)', metros_text)
                        if metros_match:
                            metros = int(metros_match.group(1))

                # Extraer URL de la imagen
                imagen_url = ""
                img = prop.find("img")
                if img:
                    imagen_url = (
                        img.get("data-src") or 
                        img.get("data-lazy-src") or 
                        img.get("src") or 
                        img.get("data-original") or
                        ""
                    )
                    # Si la URL es relativa, convertirla a absoluta
                    if imagen_url and not imagen_url.startswith("http"):
                        imagen_url = urljoin("https://www.ciencuadras.com", imagen_url)

                # Solo agregar si tenemos al menos un precio válido
                if precio > 0:
                    titulos.append(titulo)
                    precios.append(precio)
                    banios.append(banios_count)
                    cuartos.append(habitaciones)
                    metroscuadrados.append(metros)
                    parqueaderos.append(parqueaderos_count)
                    imagenes.append(imagen_url)
                    print(f"  - Agregada: {titulo[:50]}... - ${precio:,}")

            except Exception as e:
                print(f"  Error procesando propiedad: {e}")
                continue

        # Buscar el enlace a la siguiente página
        current_page += 1
        if current_page <= max_pages:
            # Intentar diferentes selectores para el botón de siguiente página
            siguientepag = (
                soup.select_one("a[aria-label*='siguiente'], a[aria-label*='next']") or
                soup.select_one("li.next > a") or
                soup.select_one("a.next") or
                soup.find("a", string=re.compile("siguiente|next", re.I))
            )
            
            if siguientepag and siguientepag.get("href"):
                url = urljoin(base_url, siguientepag.get("href"))
            else:
                # Intentar construir la URL de la siguiente página manualmente
                if "page=" in url:
                    url = re.sub(r'page=(\d+)', f'page={current_page}', url)
                elif "?" in url:
                    url = f"{url}&page={current_page}"
                else:
                    url = f"{url}?page={current_page}"
        else:
            break

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

    print(f"\nTotal de propiedades obtenidas: {len(df)}")
    return df

