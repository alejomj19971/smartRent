import React, { useState, useEffect, useRef } from 'react'
import { propertyTrie } from '../utils/trie'

function PropertySearch({ onSearch, allProperties = [], placeholder = "Buscar propiedades..." }) {
  const [searchTerm, setSearchTerm] = useState('')
  const debounceTimer = useRef(null)

  useEffect(() => {
    // Limpiar timer anterior
    if (debounceTimer.current) {
      clearTimeout(debounceTimer.current)
    }

    // Si el término de búsqueda está vacío, mostrar todas las propiedades
    if (searchTerm === '') {
      onSearch('', allProperties)
      return
    }

    // Debounce: esperar 200ms después de que el usuario deje de escribir
    debounceTimer.current = setTimeout(() => {
      // Buscar usando el árbol de prefijos del frontend
      const foundProperties = propertyTrie.searchByPrefix(searchTerm)
      
      onSearch(searchTerm, foundProperties)
    }, 200)

    return () => {
      if (debounceTimer.current) {
        clearTimeout(debounceTimer.current)
      }
    }
  }, [searchTerm, allProperties, onSearch])

  const handleClear = () => {
    setSearchTerm('')
    onSearch('')
  }

  return (
    <div className="relative w-full">
      <div className="relative">
        {/* Icono de lupa */}
        <div className="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none">
          <svg className="h-5 w-5 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z" />
          </svg>
        </div>

        {/* Input de búsqueda */}
        <input
          type="text"
          value={searchTerm}
          onChange={(e) => setSearchTerm(e.target.value)}
          placeholder={placeholder}
          className="block w-full pl-10 pr-10 py-3 border border-gray-300 rounded-lg leading-5 bg-white placeholder-gray-500 focus:outline-none focus:placeholder-gray-400 focus:ring-1 focus:ring-indigo-500 focus:border-indigo-500 text-sm"
        />

        {/* Botón de limpiar */}
        {searchTerm && (
          <div className="absolute inset-y-0 right-0 pr-3 flex items-center">
            <button
              onClick={handleClear}
              className="text-gray-400 hover:text-gray-600 focus:outline-none"
            >
              <svg className="h-5 w-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M6 18L18 6M6 6l12 12" />
              </svg>
            </button>
          </div>
        )}
      </div>

      {/* Indicador de resultados (opcional) */}
      {searchTerm && (
        <p className="mt-2 text-sm text-gray-600">
          Buscando propiedades que contengan: <span className="font-semibold text-indigo-600">"{searchTerm}"</span>
        </p>
      )}
    </div>
  )
}

export default PropertySearch

