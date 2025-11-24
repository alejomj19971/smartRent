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

    base_url = "https://www.fincaraiz.com.co/arriendo/casas/la-estrella/antioquia"
    url = f"{base_url}?&gad_campaignid=6479174048"

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
            new_len = len(driver.find_elements(By.CSS_SELECTOR, "article, [class*='property'], [class*='inmueble'], [class*='listing'], [class*='card']"))
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

        # Buscar propiedades - Fincaraíz usa diferentes estructuras
        propiedades = soup.find_all("article")
        
        if not propiedades:
            # Intentar buscar por clases comunes en Fincaraíz
            propiedades = soup.find_all("div", class_=re.compile("property|inmueble|listing|card|result", re.I))
        
        if not propiedades:
            # Buscar por estructura de enlaces de propiedades
            propiedades = soup.find_all("a", href=re.compile("/arriendo|/propiedad|/inmueble", re.I))
            # Si encontramos enlaces, buscar el contenedor padre
            if propiedades:
                propiedades = [p.parent if p.parent else p for p in propiedades if p.parent]

        print(f"Encontradas {len(propiedades)} propiedades en la página {current_page}")

        for prop in propiedades:
            try:
                texto_completo = prop.get_text()
                
                # Extraer título/ubicación - En Fincaraíz el formato es "Casa en arriendo en [barrio], la estrella"
                titulo = ""
                
                # Buscar el patrón típico de Fincaraíz: "Casa en arriendo en [barrio], la estrella"
                titulo_match = re.search(r'(Casa|Apartamento|Local|Oficina|Apartaestudio|Lote).*?en arriendo.*?en\s+([^,]+),\s*la estrella', texto_completo, re.I)
                if titulo_match:
                    tipo = titulo_match.group(1)
                    barrio = titulo_match.group(2).strip()
                    titulo = f"{tipo} en arriendo, La Estrella, {barrio}"
                else:
                    # Buscar formato alternativo: "Casa en La estrella, Antioquia"
                    titulo_match = re.search(r'(Casa|Apartamento|Local|Oficina|Apartaestudio|Lote)\s+en\s+La estrella[^,]*,\s*Antioquia', texto_completo, re.I)
                    if titulo_match:
                        tipo = titulo_match.group(1)
                        # Intentar extraer barrio del texto completo
                        barrio_match = re.search(r'La estrella[^,]*,\s*Antioquia[^,]*?([^,]+)', texto_completo, re.I)
                        if barrio_match:
                            barrio = barrio_match.group(1).strip()
                            titulo = f"{tipo} en arriendo, La Estrella, {barrio}"
                        else:
                            titulo = f"{tipo} en arriendo, La Estrella"
                    else:
                        # Buscar en elementos específicos
                        titulo_elem = (
                            prop.find("h2") or 
                            prop.find("h3") or 
                            prop.find("a", class_=re.compile("title|name|ubicacion|location", re.I)) or
                            prop.find("div", class_=re.compile("title|name|ubicacion|location", re.I)) or
                            prop.find("span", class_=re.compile("title|name|ubicacion|location", re.I)) or
                            prop.find("p", class_=re.compile("title|name|ubicacion|location", re.I))
                        )
                        if titulo_elem:
                            titulo = titulo_elem.get_text(strip=True)
                
                if not titulo or titulo == "":
                    titulo = "N/A"

                # Extraer precio - Fincaraíz usa formato "$ 16.500.000" o "$ 3.800.000"
                precio = 0
                precio_text = prop.find(string=re.compile(r'\$\s*[\d,\.]+'))
                if precio_text:
                    precio_str = re.search(r'\$\s*([\d,\.]+)', precio_text)
                    if precio_str:
                        precio = int(precio_str.group(1).replace(".", "").replace(",", ""))
                else:
                    precio_elem = (
                        prop.find("div", class_=re.compile("price|precio", re.I)) or
                        prop.find("span", class_=re.compile("price|precio", re.I)) or
                        prop.find("p", class_=re.compile("price|precio", re.I)) or
                        prop.find("strong", class_=re.compile("price|precio", re.I))
                    )
                    if precio_elem:
                        precio_text = precio_elem.get_text()
                        precio_match = re.search(r'\$\s*([\d,\.]+)', precio_text)
                        if precio_match:
                            precio = int(precio_match.group(1).replace(".", "").replace(",", ""))

                # Extraer especificaciones del texto completo
                # Formato típico: "4 Habs." "5 Baños" "450 m²"
                
                # Buscar habitaciones - formato "4 Habs." o "3 Hab"
                habitaciones = 0
                habit_match = re.search(r'(\d+)\s*(?:Habs?\.?|habitaciones?|hab\.?|cuartos?)', texto_completo, re.I)
                if habit_match:
                    habitaciones = int(habit_match.group(1))
                else:
                    # Buscar en elementos específicos
                    habit_elem = prop.find(attrs={"class": re.compile("bedroom|habitacion|room", re.I)})
                    if habit_elem:
                        habit_text = habit_elem.get_text()
                        habit_match = re.search(r'(\d+)', habit_text)
                        if habit_match:
                            habitaciones = int(habit_match.group(1))

                # Buscar baños - formato "5 Baños"
                banios_count = 0
                banio_match = re.search(r'(\d+)\s*(?:Baños?|baños?|bath)', texto_completo, re.I)
                if banio_match:
                    banios_count = int(banio_match.group(1))
                else:
                    banio_elem = prop.find(attrs={"class": re.compile("bath|baño|bathroom", re.I)})
                    if banio_elem:
                        banio_text = banio_elem.get_text()
                        banio_match = re.search(r'(\d+)', banio_text)
                        if banio_match:
                            banios_count = int(banio_match.group(1))

                # Buscar parqueaderos - puede estar como "Parqueadero" o "Garaje" en el texto
                parqueaderos_count = 0
                parq_match = re.search(r'(\d+)\s*(?:parqueaderos?|garajes?|parq\.?|parking)', texto_completo, re.I)
                if parq_match:
                    parqueaderos_count = int(parq_match.group(1))
                else:
                    # Buscar en el texto si menciona parqueadero (asumir 1 si se menciona)
                    if re.search(r'parqueadero|garaje|parking', texto_completo, re.I):
                        parqueaderos_count = 1
                    else:
                        parq_elem = prop.find(attrs={"class": re.compile("parking|garage|parqueadero", re.I)})
                        if parq_elem:
                            parq_text = parq_elem.get_text()
                            parq_match = re.search(r'(\d+)', parq_text)
                            if parq_match:
                                parqueaderos_count = int(parq_match.group(1))

                # Buscar metros cuadrados - formato "450 m²" o "120 m²"
                metros = 0
                metros_match = re.search(r'(\d+)\s*m[²2]', texto_completo, re.I)
                if metros_match:
                    metros = int(metros_match.group(1))
                else:
                    # Buscar formato alternativo "450 mt2" o "120 mt2"
                    metros_match = re.search(r'(\d+)\s*mt2?', texto_completo, re.I)
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
                        img.get("data-image") or
                        ""
                    )
                    # Si la URL es relativa, convertirla a absoluta
                    if imagen_url and not imagen_url.startswith("http"):
                        imagen_url = urljoin("https://www.fincaraiz.com.co", imagen_url)
                    # Limpiar parámetros de tamaño si existen
                    if imagen_url:
                        imagen_url = re.sub(r'[?&]w=\d+[&]?', '', imagen_url)
                        imagen_url = re.sub(r'[?&]h=\d+[&]?', '', imagen_url)
                        imagen_url = imagen_url.rstrip('?&')

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
            # Fincaraíz usa paginación típica
            siguientepag = (
                soup.select_one("a[aria-label*='siguiente'], a[aria-label*='next']") or
                soup.select_one("li.next > a") or
                soup.select_one("a.next") or
                soup.find("a", string=re.compile("siguiente|next|>", re.I)) or
                soup.find("a", href=re.compile(f"page={current_page}"))
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
                    url = f"{base_url}?page={current_page}"
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

