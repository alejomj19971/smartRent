"""
Sistema de cola para gestionar los scrapings de propiedades
"""
import threading
import queue
import os
import importlib
from pathlib import Path
from enum import Enum
from datetime import datetime
from typing import Optional, Dict, Any, Callable, List, Tuple
from src.crud import guardar_casas

# Mapeo de ciudades a sus funciones de scraping
SCRAPING_FUNCTIONS = {
    "Copacabana": None  # Se importará dinámicamente
}

class ScrapingStatus(Enum):
    """Estados posibles del scraping"""
    IDLE = "idle"  # Sin trabajo
    QUEUED = "queued"  # En cola
    RUNNING = "running"  # Ejecutándose
    COMPLETED = "completed"  # Completado
    ERROR = "error"  # Error

class ScrapingQueue:
    """Maneja la cola de scrapings"""
    
    def __init__(self):
        self._queue = queue.Queue()
        self._current_status = ScrapingStatus.IDLE
        self._current_task_id = None
        self._current_city = None
        self._error_message = None
        self._start_time = None
        self._end_time = None
        self._lock = threading.Lock()
        self._worker_thread = None
        self._cities_being_processed = {}  # Track ciudades: {city: count_of_remaining_tasks}
        self._start_worker()
    
    def _start_worker(self):
        """Inicia el hilo trabajador que procesa la cola"""
        if self._worker_thread is None or not self._worker_thread.is_alive():
            self._worker_thread = threading.Thread(target=self._worker, daemon=True)
            self._worker_thread.start()
    
    def _worker(self):
        """Procesa los trabajos de la cola
        
        Complejidad por operación:
            - queue.get(): O(1) - operación de cola (FIFO)
            - Procesamiento de cada tarea: O(1) en términos de estructura de datos
            - El tiempo total depende del scraping en sí, no de la estructura de datos
        
        Nota: Este método se ejecuta en un loop infinito, pero cada operación de cola es O(1)"""
        while True:
            try:
                task_data = self._queue.get(timeout=1)
                if task_data is None:
                    continue
                
                task_id, city, script_name = task_data
                
                # Extraer el municipio del nombre del script (ej: "copacabana_1" -> "copacabana")
                municipio = script_name.split('_')[0].lower() if '_' in script_name else script_name.lower()
                
                # Verificar si es el primer script de esta ciudad (para limpiar solo una vez)
                with self._lock:
                    total_scripts = self._cities_being_processed.get(city, 0)
                    should_clean = (total_scripts == len(self._find_scraping_files_for_city(city)))  # Es el primero si el contador es igual al total
                
                with self._lock:
                    self._current_status = ScrapingStatus.RUNNING
                    self._current_task_id = task_id
                    self._current_city = city
                    self._start_time = datetime.now()
                    self._error_message = None
                
                try:
                    # Importar dinámicamente la función de scraping según el script
                    scraping_func = self._get_scraping_function(script_name)
                    if scraping_func is None:
                        raise ValueError(f"No hay función de scraping disponible para {script_name}")
                    
                    print(f"Ejecutando scraping: {script_name} para {city} (municipio: {municipio}, limpiar: {should_clean})")
                    
                    # Ejecutar el scraping
                    df = scraping_func()
                    
                    # Guardar en la base de datos (limpiando datos anteriores solo en el primer script del municipio)
                    guardar_casas(df, municipio=municipio if should_clean else None)
                    
                    print(f"Completado scraping: {script_name} para {city} ({len(df)} propiedades)")
                    
                    # Decrementar contador de tareas para esta ciudad
                    with self._lock:
                        if city in self._cities_being_processed:
                            self._cities_being_processed[city] -= 1
                            if self._cities_being_processed[city] <= 0:
                                del self._cities_being_processed[city]
                        
                        # Si no hay más tareas en la cola, marcar como completado
                        if self._queue.qsize() == 0:
                            self._current_status = ScrapingStatus.COMPLETED
                            self._end_time = datetime.now()
                            self._current_task_id = None
                            self._current_city = None
                        else:
                            # Hay más tareas, mantener el estado como RUNNING
                            self._current_task_id = None
                        
                except Exception as e:
                    print(f"Error en scraping {script_name} para {city}: {e}")
                    with self._lock:
                        # Remover la ciudad del diccionario de procesamiento
                        if city in self._cities_being_processed:
                            del self._cities_being_processed[city]
                        self._current_status = ScrapingStatus.ERROR
                        self._error_message = str(e)
                        self._end_time = datetime.now()
                        self._current_task_id = None
                        # Si no hay más tareas, limpiar también current_city
                        if self._queue.qsize() == 0:
                            self._current_city = None
                
                self._queue.task_done()
                
            except queue.Empty:
                # Si no hay trabajos, cambiar a IDLE si estaba en RUNNING
                with self._lock:
                    if self._current_status == ScrapingStatus.RUNNING:
                        # Esto no debería pasar, pero por si acaso
                        pass
                continue
    
    def _find_scraping_files_for_city(self, city: str) -> List[str]:
        """Busca todos los archivos de scraping que contengan el nombre de la ciudad.
        La búsqueda es específica: el archivo debe empezar con el nombre de la ciudad seguido de '_número'
        
        Complejidad: O(f) donde f es el número de archivos en el directorio utils/
        En el peor caso, recorre todos los archivos .py del directorio"""
        utils_path = Path(__file__).parent / "utils"
        if not utils_path.exists():
            return []
        
        # Mapeo de ciudades a patrones de búsqueda exactos
        city_patterns = {
            "Copacabana": "copacabana",
            "Medellín": "medellin",
            "Medellin": "medellin",
            "Sabaneta": "sabaneta",
            "La Estrella": "estrella",
            "La estrella": "estrella",
            "Estrella": "estrella",
            "Envigado": "envigado",
            "Caldas": "caldas",
            "Bello": "bello"
        }
        
        # Obtener patrón para esta ciudad
        pattern = city_patterns.get(city, city.lower().replace(" ", "_").replace("í", "i").replace("ó", "o").replace("é", "e").replace("á", "a").replace("ú", "u"))
        pattern_normalized = pattern.lower()
        
        # Buscar todos los archivos Python que empiecen EXACTAMENTE con el patrón seguido de '_número'
        # Ejemplo: "copacabana_1.py", "copacabana_2.py", etc.
        scraping_files = []
        for file in utils_path.glob("*.py"):
            if file.name.startswith("_") or file.name == "__init__.py":
                continue
            
            file_stem = file.stem.lower()
            
            # Verificar si el archivo empieza EXACTAMENTE con el patrón seguido de '_' y un número
            # Usar regex para verificar el patrón: ciudad_número
            import re
            pattern_regex = re.compile(rf'^{re.escape(pattern_normalized)}_\d+$')
            if pattern_regex.match(file_stem):
                scraping_files.append(file.stem)  # Nombre sin extensión
        
        return sorted(scraping_files)  # Ordenar para ejecutar en orden
    
    def _get_scraping_function(self, script_name: str) -> Optional[Callable]:
        """Obtiene la función de scraping para un script específico
        
        Complejidad: O(1) - importación de módulo Python (operación constante)
        Nota: La importación puede ser costosa la primera vez, pero es O(1) en términos de complejidad algorítmica"""
        try:
            # Importar dinámicamente el módulo
            module_name = f"src.utils.{script_name}"
            module = importlib.import_module(module_name)
            # Obtener la función obtener_casas del módulo
            if hasattr(module, 'obtener_casas'):
                return module.obtener_casas
        except (ImportError, AttributeError) as e:
            print(f"Error al importar {script_name}: {e}")
        return None
    
    def add_scraping_task(self, city: str) -> List[str]:
        """Agrega trabajos de scraping a la cola para una ciudad específica.
        Busca TODOS los scripts que contengan el nombre de la ciudad y los agrega a la cola.
        
        Complejidad: O(f + s) donde:
            - f es el número de archivos en el directorio (búsqueda de archivos)
            - s es el número de scripts encontrados (agregar a la cola)
        En el peor caso: O(f) si todos los archivos deben ser verificados
        
        Returns:
            Lista de task_ids creados
        """
        # Buscar todos los scripts de scraping para esta ciudad
        scraping_files = self._find_scraping_files_for_city(city)
        
        if not scraping_files:
            raise ValueError(f"No se encontraron scripts de scraping para {city}")
        
        task_ids = []
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        
        with self._lock:
            # Inicializar contador de tareas para esta ciudad
            self._cities_being_processed[city] = len(scraping_files)
            
            for idx, script_name in enumerate(scraping_files):
                task_id = f"task_{city}_{script_name}_{timestamp}_{idx}"
                task_ids.append(task_id)
                
                # Agregar cada script a la cola
                self._queue.put((task_id, city, script_name))
            
            # Actualizar el estado
            if self._current_status == ScrapingStatus.IDLE:
                self._current_status = ScrapingStatus.QUEUED
            elif self._current_status in [ScrapingStatus.COMPLETED, ScrapingStatus.ERROR]:
                self._current_status = ScrapingStatus.QUEUED
        
        print(f"Agregados {len(scraping_files)} scripts de scraping para {city}: {scraping_files}")
        return task_ids
    
    def get_status(self) -> Dict[str, Any]:
        """Obtiene el estado actual del scraping
        
        Complejidad: O(1) - acceso directo a variables de estado (operación constante)
        Todas las operaciones son accesos directos a variables y cálculos simples"""
        with self._lock:
            status = {
                "status": self._current_status.value,
                "task_id": self._current_task_id,
                "city": self._current_city,
                "error": self._error_message,
                "start_time": self._start_time.isoformat() if self._start_time else None,
                "end_time": self._end_time.isoformat() if self._end_time else None,
                "queue_size": self._queue.qsize()
            }
            
            # Calcular duración si está corriendo
            if self._current_status == ScrapingStatus.RUNNING and self._start_time:
                duration = (datetime.now() - self._start_time).total_seconds()
                status["duration_seconds"] = int(duration)
            elif self._end_time and self._start_time:
                duration = (self._end_time - self._start_time).total_seconds()
                status["duration_seconds"] = int(duration)
            else:
                status["duration_seconds"] = None
            
            return status
    
    def reset_status(self):
        """Resetea el estado después de completar o error
        
        Complejidad: O(1) - operación constante (solo resetea variables de estado)"""
        with self._lock:
            if self._current_status in [ScrapingStatus.COMPLETED, ScrapingStatus.ERROR]:
                self._current_status = ScrapingStatus.IDLE
                self._current_task_id = None
                self._current_city = None
                self._error_message = None
                self._start_time = None
                self._end_time = None

# Instancia global de la cola
scraping_queue = ScrapingQueue()

