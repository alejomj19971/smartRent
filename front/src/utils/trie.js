/**
 * Árbol de prefijos (Trie) para el frontend
 * Almacena propiedades inmobiliarias indexadas por prefijos del título
 */

class TrieNode {
  constructor() {
    this.children = {}
    this.properties = []
    this.isEnd = false
  }
}

class PropertyTrie {
  constructor() {
    this.root = new TrieNode()
    this.propertyCount = 0
    this.allProperties = new Map() // Cache por ID
  }

  /**
   * Normaliza un texto a minúsculas y elimina espacios
   * Complejidad: O(n) donde n es la longitud del texto
   */
  normalizeKey(text) {
    return text.toLowerCase().trim()
  }

  /**
   * Divide un texto en todos sus prefijos posibles
   * Complejidad: O(n²) donde n es la longitud del texto
   * Ejemplo: "casa" -> ["c", "ca", "cas", "casa"]
   */
  splitIntoPrefixes(text) {
    const normalized = this.normalizeKey(text)
    const prefixes = []
    for (let i = 1; i <= normalized.length; i++) {
      prefixes.push(normalized.substring(0, i))
    }
    return prefixes
  }

  /**
   * Inserta una propiedad en el árbol Trie
   * Complejidad: O(m * n) donde:
   *   - m es la longitud del título de la propiedad
   *   - n es el número de prefijos generados (m)
   * En el peor caso: O(m²) donde m es la longitud del título
   */
  insertProperty(propertyData) {
    if (!propertyData || !propertyData.title || !propertyData.id) {
      return false
    }

    const propertyId = propertyData.id

    // Si la propiedad ya existe, actualizarla
    if (this.allProperties.has(propertyId)) {
      this.removeProperty(propertyId)
    }

    const title = propertyData.title
    const normalizedTitle = this.normalizeKey(title)
    const prefixes = this.splitIntoPrefixes(normalizedTitle)

    // Insertar en el árbol usando cada prefijo
    for (const prefix of prefixes) {
      let node = this.root
      for (const char of prefix) {
        if (!node.children[char]) {
          node.children[char] = new TrieNode()
        }
        node = node.children[char]
      }

      // Agregar la propiedad a este nodo si no está ya presente
      const exists = node.properties.some(p => p.id === propertyId)
      if (!exists) {
        node.properties.push(propertyData)
        node.isEnd = true
      }
    }

    // Guardar en el cache
    this.allProperties.set(propertyId, propertyData)
    this.propertyCount = this.allProperties.size

    return true
  }

  /**
   * Busca propiedades por prefijo (puede ser múltiples palabras)
   * Complejidad: O(m + k + n) donde:
   *   - m es la longitud del prefijo
   *   - k es el número de propiedades encontradas en el Trie
   *   - n es el número total de propiedades (para búsqueda por contenido)
   * En el peor caso: O(n) si se busca en todas las propiedades
   */
  searchByPrefix(prefix) {
    if (!prefix) {
      return []
    }

    const normalizedPrefix = this.normalizeKey(prefix)
    const searchWords = normalizedPrefix.split(/\s+/).filter(word => word.length > 0)

    // Si hay múltiples palabras, buscar propiedades que contengan todas
    if (searchWords.length > 1) {
      const firstWordResults = this.searchByWordPrefix(searchWords[0])
      const filtered = firstWordResults.filter(prop => {
        const titleLower = this.normalizeKey(prop.title || '')
        return searchWords.every(word => titleLower.includes(word))
      })
      return filtered
    }

    // Búsqueda por prefijo de una sola palabra
    const trieResults = this.searchByWordPrefix(normalizedPrefix)
    
    // También buscar por contenido directo (palabra contenida en el título)
    const allResults = new Set()
    
    // Agregar resultados del Trie
    trieResults.forEach(prop => allResults.add(prop.id))
    
    // Buscar también por contenido directo
    this.allProperties.forEach(prop => {
      const titleLower = this.normalizeKey(prop.title || '')
      if (titleLower.includes(normalizedPrefix)) {
        allResults.add(prop.id)
      }
    })

    // Convertir IDs de vuelta a propiedades
    const finalResults = []
    allResults.forEach(id => {
      if (this.allProperties.has(id)) {
        finalResults.push(this.allProperties.get(id))
      }
    })

    return finalResults
  }

  /**
   * Busca propiedades por prefijo de una palabra en el Trie
   * Complejidad: O(m + k) donde:
   *   - m es la longitud del prefijo (navegación en el árbol)
   *   - k es el número de propiedades encontradas (recopilación)
   */
  searchByWordPrefix(prefix) {
    if (!prefix) {
      return []
    }

    const normalizedPrefix = this.normalizeKey(prefix)
    let node = this.root

    // Navegar hasta el nodo correspondiente al prefijo
    for (const char of normalizedPrefix) {
      if (!node.children[char]) {
        return [] // Prefijo no encontrado
      }
      node = node.children[char]
    }

    // Recopilar todas las propiedades desde este nodo hacia abajo
    const properties = []
    this.collectProperties(node, properties)

    // Eliminar duplicados
    const seenIds = new Set()
    const uniqueProperties = []
    for (const prop of properties) {
      if (prop.id && !seenIds.has(prop.id)) {
        seenIds.add(prop.id)
        uniqueProperties.push(prop)
      }
    }

    return uniqueProperties
  }

  /**
   * Recopila todas las propiedades desde un nodo hacia abajo (recursivo)
   * Complejidad: O(k) donde k es el número de propiedades en el subárbol
   * Nota: Recorre todos los nodos del subárbol, pero solo agrega propiedades
   */
  collectProperties(node, properties) {
    if (node.isEnd) {
      properties.push(...node.properties)
    }

    for (const child of Object.values(node.children)) {
      this.collectProperties(child, properties)
    }
  }

  /**
   * Elimina una propiedad del árbol Trie
   * Complejidad: O(m * n) donde:
   *   - m es la longitud del título de la propiedad
   *   - n es el número de prefijos generados (m)
   * En el peor caso: O(m²) donde m es la longitud del título
   */
  removeProperty(propertyId) {
    if (!this.allProperties.has(propertyId)) {
      return false
    }

    const propertyData = this.allProperties.get(propertyId)
    const title = propertyData.title || ''

    if (!title) {
      return false
    }

    const normalizedTitle = this.normalizeKey(title)
    const prefixes = this.splitIntoPrefixes(normalizedTitle)

    // Eliminar de cada nodo
    for (const prefix of prefixes) {
      let node = this.root
      for (const char of prefix) {
        if (!node.children[char]) {
          break
        }
        node = node.children[char]
      }

      // Eliminar la propiedad de este nodo
      node.properties = node.properties.filter(p => p.id !== propertyId)
      if (node.properties.length === 0) {
        node.isEnd = false
      }
    }

    // Eliminar del cache
    this.allProperties.delete(propertyId)
    this.propertyCount = this.allProperties.size

    return true
  }

  /**
   * Obtiene todas las propiedades almacenadas
   * Complejidad: O(n) donde n es el número de propiedades
   */
  getAllProperties() {
    return Array.from(this.allProperties.values())
  }

  /**
   * Obtiene el conteo de propiedades
   * Complejidad: O(1) - acceso directo a variable
   */
  getCount() {
    return this.propertyCount
  }

  /**
   * Limpia el árbol Trie, eliminando todas las propiedades
   * Complejidad: O(1) - operación constante (solo resetea referencias)
   */
  clear() {
    this.root = new TrieNode()
    this.allProperties.clear()
    this.propertyCount = 0
  }
}

// Exportar instancia única del árbol
export const propertyTrie = new PropertyTrie()

