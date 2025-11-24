# -*- coding: utf-8 -*-
"""
Módulo para matching de propiedades entre respuesta del LLM y base de datos.
Separado de chat_service.py para reducir el contexto enviado al LLM.
"""
import re
from typing import List, Dict, Any
from src.models import Casas


def extract_property_matches_from_text(output: str) -> List[Dict[str, Any]]:
    """
    Extrae información de propiedades del texto de respuesta del LLM.
    Evita duplicados basándose en precio + características únicas.
    
    Args:
        output: Texto de respuesta del LLM
        
    Returns:
        Lista de diccionarios con información de propiedades extraídas (sin duplicados)
    """
    lines = output.split('\n')
    property_matches = []
    seen_properties = set()  # Para evitar duplicados
    
    for line in lines:
        # Limpiar línea de URLs de imágenes antes de procesar
        line_clean = re.sub(r'!\[.*?\]\(https?:\/\/[^\)]+\)', '', line)
        line_clean = re.sub(r'https?:\/\/[^\s\)\]\n,;!?]+\.(jpg|jpeg|png|gif|webp|svg)', '', line_clean, flags=re.IGNORECASE)
        
        # Patrón principal: "1. [título] - Precio: $[precio] - [X] habitaciones - [X] baños - [X] parqueaderos - [X] m²"
        match = re.match(r'^\d+\.\s*(.+?)\s*-\s*Precio:\s*\$?([\d,\.]+)\s*-\s*(\d+)\s*habitaci[oóÓ]nes?\s*-\s*(\d+)\s*baños?\s*-\s*(\d+)\s*parqueaderos?\s*-\s*(\d+)\s*m².*', line_clean, re.IGNORECASE)
        if match:
            title = match.group(1).strip()
            price_str = match.group(2).replace(',', '').replace('.', '')
            bedrooms = int(match.group(3))
            toilets = int(match.group(4))
            parking_spaces = int(match.group(5))
            square_meters = int(match.group(6))
            
            try:
                price = int(price_str)
                # Crear clave única para evitar duplicados
                unique_key = (price, bedrooms, toilets, parking_spaces, square_meters)
                
                if unique_key not in seen_properties:
                    seen_properties.add(unique_key)
                    property_matches.append({
                        'title': title,
                        'price': price,
                        'bedroom': bedrooms,
                        'toilet': toilets,
                        'parking': parking_spaces,
                        'squareMeters': square_meters,
                        'line_index': len(property_matches)
                    })
            except ValueError:
                pass
        else:
            # Patrón alternativo más flexible
            alt_match = re.search(r'(\d+)\s*(?:parqueaderos?|parq\.)', line_clean, re.IGNORECASE)
            if alt_match:
                parking_alt = int(alt_match.group(1))
                price_match = re.search(r'Precio:\s*\$?([\d,\.]+)', line_clean, re.IGNORECASE)
                bedroom_match = re.search(r'(\d+)\s*habitaci[^\s\-]*', line_clean, re.IGNORECASE)
                toilet_match = re.search(r'(\d+)\s*baños?', line_clean, re.IGNORECASE)
                meters_match = re.search(r'(\d+)\s*m²', line_clean, re.IGNORECASE)
                title_match = re.search(r'^\d+\.\s*(.+?)\s*-\s*Precio:', line_clean, re.IGNORECASE)
                
                if price_match and bedroom_match and toilet_match and meters_match and title_match:
                    try:
                        price_str = price_match.group(1).replace(',', '').replace('.', '')
                        price = int(price_str)
                        bedrooms = int(bedroom_match.group(1))
                        toilets = int(toilet_match.group(1))
                        square_meters = int(meters_match.group(1))
                        title = title_match.group(1).strip()
                        
                        # Crear clave única para evitar duplicados
                        unique_key = (price, bedrooms, toilets, parking_alt, square_meters)
                        
                        if unique_key not in seen_properties:
                            seen_properties.add(unique_key)
                            property_matches.append({
                                'title': title,
                                'price': price,
                                'bedroom': bedrooms,
                                'toilet': toilets,
                                'parking': parking_alt,
                                'squareMeters': square_meters,
                                'line_index': len(property_matches)
                            })
                    except (ValueError, AttributeError):
                        pass
    
    return property_matches


def extract_image_urls(output: str) -> List[str]:
    """
    Extrae URLs de imágenes del texto de respuesta del LLM.
    Incluye URLs de fincaraiz, metrocuadrado y otros dominios.
    
    Args:
        output: Texto de respuesta del LLM
        
    Returns:
        Lista de URLs de imágenes encontradas (sin duplicados)
    """
    image_urls_markdown = re.findall(r'!\[.*?\]\((https?://[^\)]+)\)', output)
    image_urls_fincaraiz = re.findall(r'https?://cdn\d+\.fincaraiz\.com\.co/[^\s\)\]\n,;!?]+', output)
    image_urls_metrocuadrado = re.findall(r'https?://multimedia\.metrocuadrado\.com/[^\s\)\]\n,;!?]+', output)
    image_urls_metrocuadrado_alt = re.findall(r'https?://[^\s\)\]\n,;!?]*metrocuadrado[^\s\)\]\n,;!?]*', output)
    # URLs directas de imágenes (sin grupos de captura para evitar tuplas)
    image_urls_direct = re.findall(r'https?://[^\s\)\]\n,;!?]+\.(?:jpg|jpeg|png|gif|webp|svg)', output, re.IGNORECASE)
    
    # Combinar todas y eliminar duplicados
    all_urls = image_urls_markdown + image_urls_fincaraiz + image_urls_metrocuadrado + image_urls_metrocuadrado_alt + image_urls_direct
    image_urls = list(set(all_urls))
    return image_urls


def create_image_id_map(casas: List[Casas]) -> Dict[str, List[Casas]]:
    """
    Crea un mapa de IDs de imagen a casas para búsqueda rápida.
    
    Args:
        casas: Lista de objetos Casas
        
    Returns:
        Diccionario que mapea IDs de imagen a listas de casas
    """
    image_id_to_casas = {}
    for casa in casas:
        if casa.image:
            casa_img_id_match = re.search(r'/([\d]+-M[\d]+)/', casa.image)
            if casa_img_id_match:
                img_id = casa_img_id_match.group(1)
                if img_id not in image_id_to_casas:
                    image_id_to_casas[img_id] = []
                image_id_to_casas[img_id].append(casa)
    return image_id_to_casas


def match_properties_by_image(
    property_matches: List[Dict[str, Any]],
    image_urls: List[str],
    image_id_to_casas: Dict[str, List[Casas]],
    matched_ids: set,
    matched_property_indices: set
) -> List[Dict[str, Any]]:
    """
    Hace matching de propiedades por URL de imagen.
    
    Args:
        property_matches: Lista de propiedades extraídas del LLM
        image_urls: Lista de URLs de imágenes
        image_id_to_casas: Mapa de IDs de imagen a casas
        matched_ids: Set de IDs ya agregados
        matched_property_indices: Set de índices ya procesados
        
    Returns:
        Lista de propiedades con datos completos de la BD
    """
    matched_properties = []
    
    if image_urls and len(property_matches) > 0:
        for i, prop_match in enumerate(property_matches):
            matched_for_this = False
            
            # Intentar por índice
            if i < len(image_urls):
                target_img_url = image_urls[i]
                target_img_clean = target_img_url.rstrip('.,;!?')
                target_img_id_match = re.search(r'/([\d]+-M[\d]+)/', target_img_clean)
                
                if target_img_id_match:
                    target_img_id = target_img_id_match.group(1)
                    if target_img_id in image_id_to_casas:
                        for casa in image_id_to_casas[target_img_id]:
                            if casa.id not in matched_ids:
                                matched_properties.append({
                                    "id": casa.id,
                                    "title": casa.title,
                                    "price": casa.price,
                                    "bedroom": casa.bedroom,
                                    "toilet": casa.toilet,
                                    "parking": casa.parking,
                                    "squareMeters": casa.squareMeters,
                                    "image": casa.image or ""
                                })
                                matched_ids.add(casa.id)
                                matched_property_indices.add(i)
                                matched_for_this = True
                                break
            
            # Si no se encontró por índice, buscar en todas las URLs
            if not matched_for_this:
                for img_url in image_urls:
                    img_url_clean = img_url.rstrip('.,;!?')
                    img_id_match = re.search(r'/([\d]+-M[\d]+)/', img_url_clean)
                    if img_id_match:
                        img_id = img_id_match.group(1)
                        if img_id in image_id_to_casas:
                            for casa in image_id_to_casas[img_id]:
                                if casa.id not in matched_ids:
                                    price_match = abs(casa.price - prop_match.get('price', 0)) < 100000
                                    if price_match or not matched_for_this:
                                        matched_properties.append({
                                            "id": casa.id,
                                            "title": casa.title,
                                            "price": casa.price,
                                            "bedroom": casa.bedroom,
                                            "toilet": casa.toilet,
                                            "parking": casa.parking,
                                            "squareMeters": casa.squareMeters,
                                            "image": casa.image or ""
                                        })
                                        matched_ids.add(casa.id)
                                        matched_property_indices.add(i)
                                        matched_for_this = True
                                        break
                            if matched_for_this:
                                break
    
    return matched_properties


def match_properties_by_data(
    property_matches: List[Dict[str, Any]],
    all_casas: List[Casas],
    matched_ids: set,
    matched_property_indices: set
) -> List[Dict[str, Any]]:
    """
    Hace matching de propiedades por datos (fallback cuando no hay URL de imagen).
    
    Args:
        property_matches: Lista de propiedades extraídas del LLM
        all_casas: Lista de todas las casas de la BD
        matched_ids: Set de IDs ya agregados
        matched_property_indices: Set de índices ya procesados
        
    Returns:
        Lista de propiedades con datos completos de la BD
    """
    matched_properties = []
    
    for i, prop_match in enumerate(property_matches):
        if i in matched_property_indices:
            continue
        
        best_match = None
        best_score = 0
        
        for casa in all_casas:
            if casa.id not in matched_ids:
                score = 0
                
                # Scoring flexible
                parking_diff = abs(casa.parking - prop_match['parking'])
                if parking_diff == 0:
                    score += 10
                elif parking_diff <= 2:
                    score += 5
                else:
                    score += 1
                
                price_diff = abs(casa.price - prop_match['price'])
                if price_diff < 1000:
                    score += 10
                elif price_diff < 10000:
                    score += 7
                elif price_diff < 50000:
                    score += 5
                elif price_diff < 200000:
                    score += 3
                else:
                    score += 1
                
                bedroom_diff = abs(casa.bedroom - prop_match['bedroom'])
                if bedroom_diff == 0:
                    score += 10
                elif bedroom_diff <= 2:
                    score += 5
                else:
                    score += 2
                
                toilet_diff = abs(casa.toilet - prop_match['toilet'])
                if toilet_diff == 0:
                    score += 10
                elif toilet_diff <= 2:
                    score += 5
                else:
                    score += 2
                
                meters_diff = abs(casa.squareMeters - prop_match['squareMeters'])
                if meters_diff <= 15:
                    score += 10
                elif meters_diff <= 30:
                    score += 7
                elif meters_diff <= 50:
                    score += 5
                elif meters_diff <= 100:
                    score += 3
                else:
                    score += 1
                
                # Umbral más bajo para aceptar matches (antes era >= 10, ahora >= 5)
                # Esto permite matches más flexibles
                if score >= 5:
                    if score > best_score:
                        best_score = score
                        best_match = casa
        
        if best_match:
            matched_properties.append({
                "id": best_match.id,
                "title": best_match.title,
                "price": best_match.price,
                "bedroom": best_match.bedroom,
                "toilet": best_match.toilet,
                "parking": best_match.parking,
                "squareMeters": best_match.squareMeters,
                "image": best_match.image or ""
            })
            matched_ids.add(best_match.id)
            matched_property_indices.add(i)
    
    return matched_properties

