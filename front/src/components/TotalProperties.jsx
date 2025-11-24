import React, { useState, useEffect } from 'react'

function TotalProperties() {
  const [total, setTotal] = useState(0)
  const [isLoading, setIsLoading] = useState(true)

  useEffect(() => {
    const fetchTotal = async () => {
      try {
        const response = await fetch('/casas/total')
        const data = await response.json()
        setTotal(data.total || 0)
      } catch (error) {
        console.error('Error al obtener el total de casas:', error)
        setTotal(0)
      } finally {
        setIsLoading(false)
      }
    }

    fetchTotal()
    
    // Actualizar cada 5 segundos para mantener el total actualizado
    const interval = setInterval(fetchTotal, 5000)
    
    return () => clearInterval(interval)
  }, [])

  return (
    <div className="bg-white rounded-lg shadow-lg p-6 sticky top-6 mb-6 z-10">
      <div className="text-center">
        <div className="mb-4">
          <div className="w-16 h-16 bg-indigo-100 rounded-full flex items-center justify-center mx-auto mb-3">
            <svg className="w-8 h-8 text-indigo-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M19 21V5a2 2 0 00-2-2H7a2 2 0 00-2 2v16m14 0h2m-2 0h-5m-9 0H3m2 0h5M9 7h1m-1 4h1m4-4h1m-1 4h1m-5 10v-5a1 1 0 011-1h2a1 1 0 011 1v5m-4 0h4"></path>
            </svg>
          </div>
          <h3 className="text-lg font-semibold text-gray-800 mb-2">Total de Casas</h3>
        </div>
        {isLoading ? (
          <div className="text-4xl font-bold text-indigo-600 mb-2">...</div>
        ) : (
          <>
            <div className="text-4xl font-bold text-indigo-600 mb-2">{total}</div>
            <p className="text-sm text-gray-600">
              {total === 0 
                ? 'No hay casas en la base de datos' 
                : total === 1 
                ? 'casa disponible' 
                : 'casas disponibles'}
            </p>
          </>
        )}
      </div>
    </div>
  )
}

export default TotalProperties

