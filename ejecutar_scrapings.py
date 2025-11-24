# -*- coding: utf-8 -*-
"""Script para ejecutar todos los scrapings usando la cola (uno a uno)"""
import sys
import time
# Configurar encoding UTF-8 para evitar errores con caracteres especiales
if sys.platform == 'win32':
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8', errors='replace')

from src.scraping_queue import scraping_queue

def ejecutar_todos():
    """Ejecuta todos los scrapings usando la cola, uno a uno"""
    ciudades = [
        "Copacabana",
        "Medellín",
        "Sabaneta",
        "La Estrella",
        "Envigado",
        "Caldas",
        "Bello"
    ]
    
    print("="*60)
    print("INICIANDO SCRAPINGS CON COLA (uno a uno)")
    print("="*60)
    
    for ciudad in ciudades:
        try:
            print(f"\n{'='*60}")
            print(f"Agregando {ciudad} a la cola...")
            print(f"{'='*60}")
            
            # Agregar a la cola
            task_ids = scraping_queue.add_scraping_task(ciudad)
            print(f"OK {ciudad}: {len(task_ids)} script(s) agregado(s) a la cola")
            
            # Esperar a que termine el scraping actual
            print(f"Esperando a que termine el scraping de {ciudad}...")
            while True:
                status = scraping_queue.get_status()
                current_status = status.get("status")
                current_city = status.get("city")
                
                if current_status == "idle" or current_status == "completed":
                    # Verificar si ya terminó esta ciudad
                    if current_city != ciudad or current_status == "idle":
                        break
                
                if current_status == "error":
                    print(f"⚠ Error en scraping de {current_city}")
                    break
                
                # Mostrar progreso
                if current_status == "running" and current_city == ciudad:
                    queue_size = status.get("queue_size", 0)
                    print(f"  -> Procesando {ciudad}... (En cola: {queue_size})")
                
                time.sleep(2)  # Esperar 2 segundos antes de verificar de nuevo
            
            print(f"OK {ciudad} completado")
            
        except Exception as e:
            print(f"X Error al procesar {ciudad}: {e}")
            continue
    
    # Esperar a que termine el último scraping
    print(f"\n{'='*60}")
    print("Esperando a que termine el último scraping...")
    print(f"{'='*60}")
    
    while True:
        status = scraping_queue.get_status()
        current_status = status.get("status")
        
        if current_status == "idle" or current_status == "completed":
            break
        
        if current_status == "error":
            print(f"⚠ Error en último scraping")
            break
        
        time.sleep(2)
    
    # Obtener estado final
    final_status = scraping_queue.get_status()
    print(f"\n{'='*60}")
    print("SCRAPINGS COMPLETADOS")
    print(f"{'='*60}")
    print(f"Estado final: {final_status.get('status')}")
    print(f"{'='*60}")

if __name__ == "__main__":
    ejecutar_todos()
