import React, { useMemo } from 'react'

const PropertyCard = React.memo(function PropertyCard({ property }) {
  // Memoizar el precio formateado para evitar recalcularlo
  const formattedPrice = useMemo(() => {
    return new Intl.NumberFormat('es-CO', {
      style: 'currency',
      currency: 'COP',
      minimumFractionDigits: 0
    }).format(parseInt(property.price))
  }, [property.price])

  const handleImageError = (e) => {
    e.target.src = "data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='400' height='300'%3E%3Crect fill='%23e5e7eb' width='400' height='300'/%3E%3Ctext x='50%25' y='50%25' text-anchor='middle' dy='.3em' fill='%239ca3af' font-family='sans-serif' font-size='18'%3ESin imagen%3C/text%3E%3C/svg%3E"
  }

  return (
    <div className="bg-white rounded-xl shadow-lg overflow-hidden hover:shadow-2xl transition-all duration-300 h-full flex flex-col transform hover:-translate-y-1 border border-gray-100">
      {/* Imagen con overlay sutil */}
      <div className="relative w-full h-48 overflow-hidden bg-gradient-to-br from-indigo-50 to-blue-50">
        {property.image ? (
          <img 
            src={property.image} 
            alt={property.title} 
            className="w-full h-full object-cover transition-transform duration-300 hover:scale-105"
            loading="lazy"
            decoding="async"
            onError={handleImageError}
          />
        ) : (
          <div className="w-full h-full flex items-center justify-center text-gray-400 bg-gradient-to-br from-gray-100 to-gray-200">
            <svg className="w-16 h-16 opacity-50" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M4 16l4.586-4.586a2 2 0 012.828 0L16 16m-2-2l1.586-1.586a2 2 0 012.828 0L20 14m-6-6h.01M6 20h12a2 2 0 002-2V6a2 2 0 00-2-2H6a2 2 0 00-2 2v12a2 2 0 002 2z" />
            </svg>
          </div>
        )}
        {/* Badge de precio en la esquina */}
        <div className="absolute top-3 right-3 bg-indigo-600 text-white px-3 py-1 rounded-full text-sm font-semibold shadow-lg">
          {formattedPrice}
        </div>
      </div>
      
      {/* Contenido */}
      <div className="p-5 flex-1 flex flex-col">
        <h3 className="font-semibold text-base text-gray-900 mb-3 flex-shrink-0 line-clamp-3 leading-snug">
          {property.title}
        </h3>
        
        {/* Características con iconos mejorados */}
        <div className="grid grid-cols-2 gap-4 mt-auto">
          {/* Habitaciones */}
          <div className="flex items-center space-x-2 bg-indigo-50 rounded-lg p-2">
            <svg className="w-5 h-5 text-indigo-600 flex-shrink-0" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M3 12l2-2m0 0l7-7 7 7M5 10v10a1 1 0 001 1h3m10-11l2 2m-2-2v10a1 1 0 01-1 1h-3m-6 0a1 1 0 001-1v-4a1 1 0 011-1h2a1 1 0 011 1v4a1 1 0 001 1m6 0h1a1 1 0 001-1v-4a1 1 0 00-1-1h-2a1 1 0 00-1 1v4a1 1 0 001 1z"></path>
            </svg>
            <span className="text-sm font-medium text-gray-700">{property.bedroom} hab.</span>
          </div>
          
          {/* Baños */}
          <div className="flex items-center space-x-2 bg-blue-50 rounded-lg p-2">
            <svg className="w-5 h-5 text-blue-600 flex-shrink-0" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M8 14v3m4-3v3m4-3v3M3 21h18M3 10h18M3 7l9-4 9 4M4 10h16v11H4V10z"></path>
            </svg>
            <span className="text-sm font-medium text-gray-700">{property.toilet} baños</span>
          </div>
          
          {/* Parqueaderos */}
          <div className="flex items-center space-x-2 bg-green-50 rounded-lg p-2">
            <svg className="w-5 h-5 text-green-600 flex-shrink-0" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M8 7V3m8 4V3m-9 8h10M5 21h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v12a2 2 0 002 2z"></path>
            </svg>
            <span className="text-sm font-medium text-gray-700">{property.parking} parq.</span>
          </div>
          
          {/* Metros cuadrados */}
          <div className="flex items-center space-x-2 bg-purple-50 rounded-lg p-2">
            <svg className="w-5 h-5 text-purple-600 flex-shrink-0" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M4 8V4m0 0h4M4 4l5 5m11-1V4m0 0h-4m4 0l-5 5M4 16v4m0 0h4m-4 0l5-5m11 5l-5-5m5 5v-4m0 4h-4"></path>
            </svg>
            <span className="text-sm font-medium text-gray-700">{property.squareMeters} m²</span>
          </div>
        </div>
      </div>
    </div>
  )
})

export default PropertyCard
