import React, { useState, useEffect, useMemo } from 'react'

function PropertyFilters({ properties, onFilterChange }) {
  // Estructura de datos para filtros (equivalente a HashMap)
  const [filters, setFilters] = useState({
    priceMin: null,
    priceMax: null,
    bedrooms: null, // mínimo de habitaciones
    toilets: null, // mínimo de baños
    parking: null, // mínimo de parqueaderos (null = todos, 0 = sin parqueadero, 1+ = con parqueadero)
    squareMetersMin: null,
    squareMetersMax: null
  })

  /**
   * Calcula valores máximos y mínimos de las propiedades para los rangos
   * Complejidad: O(n) donde n es el número de propiedades
   * Recorre todas las propiedades una vez para calcular min/max de cada campo
   */
  const propertyStats = useMemo(() => {
    if (!properties || properties.length === 0) {
      return {
        minPrice: 0,
        maxPrice: 0,
        minBedrooms: 0,
        maxBedrooms: 0,
        minToilets: 0,
        maxToilets: 0,
        minParking: 0,
        maxParking: 0,
        minSquareMeters: 0,
        maxSquareMeters: 0
      }
    }

    const prices = properties.map(p => p.price).filter(p => p > 0)
    const bedrooms = properties.map(p => p.bedroom).filter(b => b >= 0)
    const toilets = properties.map(p => p.toilet).filter(t => t >= 0)
    const parking = properties.map(p => p.parking).filter(p => p >= 0)
    const squareMeters = properties.map(p => p.squareMeters).filter(s => s > 0)

    return {
      minPrice: Math.min(...prices),
      maxPrice: Math.max(...prices),
      minBedrooms: Math.min(...bedrooms),
      maxBedrooms: Math.max(...bedrooms),
      minToilets: Math.min(...toilets),
      maxToilets: Math.max(...toilets),
      minParking: Math.min(...parking),
      maxParking: Math.max(...parking),
      minSquareMeters: Math.min(...squareMeters),
      maxSquareMeters: Math.max(...squareMeters)
    }
  }, [properties])

  /**
   * Aplica filtros a las propiedades cuando cambian los filtros o las propiedades
   * Complejidad: O(n) donde n es el número de propiedades
   * Recorre todas las propiedades una vez aplicando cada filtro
   */
  useEffect(() => {
    const filtered = properties.filter(property => {
      // Filtro de precio mínimo
      if (filters.priceMin !== null && property.price < filters.priceMin) {
        return false
      }
      
      // Filtro de precio máximo
      if (filters.priceMax !== null && property.price > filters.priceMax) {
        return false
      }
      
      // Filtro de habitaciones mínimo
      if (filters.bedrooms !== null && property.bedroom < filters.bedrooms) {
        return false
      }
      
      // Filtro de baños mínimo
      if (filters.toilets !== null && property.toilet < filters.toilets) {
        return false
      }
      
      // Filtro de parqueaderos
      if (filters.parking !== null) {
        if (filters.parking === 0 && property.parking > 0) {
          return false // Si se busca sin parqueadero, excluir las que tienen
        } else if (filters.parking > 0 && property.parking < filters.parking) {
          return false // Si se busca con parqueadero, debe tener al menos ese número
        }
      }
      
      // Filtro de metros cuadrados mínimo
      if (filters.squareMetersMin !== null && property.squareMeters < filters.squareMetersMin) {
        return false
      }
      
      // Filtro de metros cuadrados máximo
      if (filters.squareMetersMax !== null && property.squareMeters > filters.squareMetersMax) {
        return false
      }
      
      return true
    })

    // Notificar al componente padre sobre los cambios
    onFilterChange(filtered, filters)
  }, [filters, properties, onFilterChange])

  /**
   * Maneja el cambio de un filtro individual
   * Complejidad: O(1) - actualización de estado (operación constante)
   * HashMap lookup y actualización son O(1)
   */
  const handleFilterChange = (key, value) => {
    setFilters(prev => ({
      ...prev,
      [key]: value === '' ? null : (isNaN(value) ? null : Number(value))
    }))
  }

  /**
   * Limpia todos los filtros
   * Complejidad: O(1) - operación constante (solo resetea el objeto de filtros)
   */
  const clearFilters = () => {
    setFilters({
      priceMin: null,
      priceMax: null,
      bedrooms: null,
      toilets: null,
      parking: null,
      squareMetersMin: null,
      squareMetersMax: null
    })
  }

  const hasActiveFilters = Object.values(filters).some(val => val !== null)

  const formatPrice = (price) => {
    return new Intl.NumberFormat('es-CO', {
      style: 'currency',
      currency: 'COP',
      minimumFractionDigits: 0,
      maximumFractionDigits: 0
    }).format(price)
  }

  return (
    <div className="bg-white rounded-lg shadow-lg p-6 sticky top-6 z-10">
      <div className="flex items-center justify-between mb-4">
        <h3 className="text-lg font-semibold text-gray-800 flex items-center">
          <svg className="w-5 h-5 mr-2 text-indigo-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M3 4a1 1 0 011-1h16a1 1 0 011 1v2.586a1 1 0 01-.293.707l-6.414 6.414a1 1 0 00-.293.707V17l-4 4v-6.586a1 1 0 00-.293-.707L3.293 7.293A1 1 0 013 6.586V4z" />
          </svg>
          Filtros
        </h3>
        {hasActiveFilters && (
          <button
            onClick={clearFilters}
            className="text-sm text-indigo-600 hover:text-indigo-800 font-medium"
          >
            Limpiar
          </button>
        )}
      </div>

      <div className="space-y-4">
        {/* Filtro de Precio */}
        <div>
          <label className="block text-sm font-medium text-gray-700 mb-2">
            Precio
          </label>
          <div className="grid grid-cols-2 gap-2">
            <div>
              <input
                type="number"
                placeholder="Mín"
                value={filters.priceMin || ''}
                onChange={(e) => handleFilterChange('priceMin', e.target.value)}
                className="w-full px-3 py-2 border border-gray-300 rounded-md text-sm focus:outline-none focus:ring-2 focus:ring-indigo-500"
              />
            </div>
            <div>
              <input
                type="number"
                placeholder="Máx"
                value={filters.priceMax || ''}
                onChange={(e) => handleFilterChange('priceMax', e.target.value)}
                className="w-full px-3 py-2 border border-gray-300 rounded-md text-sm focus:outline-none focus:ring-2 focus:ring-indigo-500"
              />
            </div>
          </div>
          {propertyStats.maxPrice > 0 && (
            <p className="text-xs text-gray-500 mt-1">
              Rango: {formatPrice(propertyStats.minPrice)} - {formatPrice(propertyStats.maxPrice)}
            </p>
          )}
        </div>

        {/* Filtro de Habitaciones */}
        <div>
          <label className="block text-sm font-medium text-gray-700 mb-2">
            Mín. Habitaciones
          </label>
          <select
            value={filters.bedrooms || ''}
            onChange={(e) => handleFilterChange('bedrooms', e.target.value)}
            className="w-full px-3 py-2 border border-gray-300 rounded-md text-sm focus:outline-none focus:ring-2 focus:ring-indigo-500"
          >
            <option value="">Todas</option>
            {Array.from({ length: propertyStats.maxBedrooms + 1 }, (_, i) => (
              <option key={i} value={i}>{i}+</option>
            ))}
          </select>
        </div>

        {/* Filtro de Baños */}
        <div>
          <label className="block text-sm font-medium text-gray-700 mb-2">
            Mín. Baños
          </label>
          <select
            value={filters.toilets || ''}
            onChange={(e) => handleFilterChange('toilets', e.target.value)}
            className="w-full px-3 py-2 border border-gray-300 rounded-md text-sm focus:outline-none focus:ring-2 focus:ring-indigo-500"
          >
            <option value="">Todos</option>
            {Array.from({ length: propertyStats.maxToilets + 1 }, (_, i) => (
              <option key={i} value={i}>{i}+</option>
            ))}
          </select>
        </div>

        {/* Filtro de Parqueaderos */}
        <div>
          <label className="block text-sm font-medium text-gray-700 mb-2">
            Parqueaderos
          </label>
          <select
            value={filters.parking !== null ? filters.parking : ''}
            onChange={(e) => handleFilterChange('parking', e.target.value)}
            className="w-full px-3 py-2 border border-gray-300 rounded-md text-sm focus:outline-none focus:ring-2 focus:ring-indigo-500"
          >
            <option value="">Todos</option>
            <option value="0">Sin parqueadero</option>
            <option value="1">1+ parqueaderos</option>
            {propertyStats.maxParking > 1 && Array.from({ length: propertyStats.maxParking }, (_, i) => (
              <option key={i + 2} value={i + 2}>{i + 2}+ parqueaderos</option>
            ))}
          </select>
        </div>

        {/* Filtro de Metros Cuadrados */}
        <div>
          <label className="block text-sm font-medium text-gray-700 mb-2">
            Metros Cuadrados
          </label>
          <div className="grid grid-cols-2 gap-2">
            <div>
              <input
                type="number"
                placeholder="Mín m²"
                value={filters.squareMetersMin || ''}
                onChange={(e) => handleFilterChange('squareMetersMin', e.target.value)}
                className="w-full px-3 py-2 border border-gray-300 rounded-md text-sm focus:outline-none focus:ring-2 focus:ring-indigo-500"
              />
            </div>
            <div>
              <input
                type="number"
                placeholder="Máx m²"
                value={filters.squareMetersMax || ''}
                onChange={(e) => handleFilterChange('squareMetersMax', e.target.value)}
                className="w-full px-3 py-2 border border-gray-300 rounded-md text-sm focus:outline-none focus:ring-2 focus:ring-indigo-500"
              />
            </div>
          </div>
          {propertyStats.maxSquareMeters > 0 && (
            <p className="text-xs text-gray-500 mt-1">
              Rango: {propertyStats.minSquareMeters} - {propertyStats.maxSquareMeters} m²
            </p>
          )}
        </div>
      </div>
    </div>
  )
}

export default PropertyFilters

