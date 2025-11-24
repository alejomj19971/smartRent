import React from 'react'

function PropertySummary({ count }) {
  return (
    <div className="bg-white rounded-lg shadow-lg p-6 sticky top-6 z-10">
      <div className="text-center">
        <div className="mb-4">
          <div className="w-16 h-16 bg-indigo-100 rounded-full flex items-center justify-center mx-auto mb-3">
            <svg className="w-8 h-8 text-indigo-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M3 12l2-2m0 0l7-7 7 7M5 10v10a1 1 0 001 1h3m10-11l2 2m-2-2v10a1 1 0 01-1 1h-3m-6 0a1 1 0 001-1v-4a1 1 0 011-1h2a1 1 0 011 1v4a1 1 0 001 1m6 0h6"></path>
            </svg>
          </div>
          <h3 className="text-lg font-semibold text-gray-800 mb-2">Propiedades Encontradas</h3>
        </div>
        <div className="text-4xl font-bold text-indigo-600 mb-2">{count}</div>
        <p className="text-sm text-gray-600">
          {count === 0 
            ? 'No hay propiedades para mostrar' 
            : count === 1 
            ? 'propiedad disponible' 
            : 'propiedades disponibles'}
        </p>
      </div>
    </div>
  )
}

export default PropertySummary

