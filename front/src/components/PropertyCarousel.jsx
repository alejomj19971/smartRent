import React, { useState, useEffect, useRef } from 'react'
import PropertyCard from './PropertyCard'

function PropertyCarousel({ properties }) {
  const [visibleCount, setVisibleCount] = useState(10) // Mostrar 10 inicialmente
  const [isIntersecting, setIsIntersecting] = useState(false)
  const observerRef = useRef(null)
  const loadMoreRef = useRef(null)

  // Resetear contador cuando cambian las propiedades
  useEffect(() => {
    setVisibleCount(10)
  }, [properties])

  // Intersection Observer para cargar más tarjetas cuando se acerca al final
  useEffect(() => {
    if (!loadMoreRef.current) return

    const observer = new IntersectionObserver(
      (entries) => {
        const entry = entries[0]
        if (entry.isIntersecting && visibleCount < properties.length) {
          // Cargar más tarjetas en lotes de 10
          setVisibleCount(prev => Math.min(prev + 10, properties.length))
        }
      },
      { threshold: 0.1 }
    )

    observer.observe(loadMoreRef.current)

    return () => {
      if (loadMoreRef.current) {
        observer.unobserve(loadMoreRef.current)
      }
    }
  }, [visibleCount, properties.length])

  if (!properties || properties.length === 0) {
    return null
  }

  const visibleProperties = properties.slice(0, visibleCount)
  const hasMore = visibleCount < properties.length

  return (
    <div className="mt-6">
      <div className="mb-4">
        <h3 className="text-lg font-semibold text-gray-800">
          Propiedades ({properties.length})
        </h3>
      </div>

      <div className="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 lg:grid-cols-3 xl:grid-cols-4 gap-4">
        {visibleProperties.map((property) => (
          <PropertyCard key={property.id} property={property} />
        ))}
      </div>

      {/* Trigger para cargar más */}
      {hasMore && (
        <div ref={loadMoreRef} className="h-20 flex items-center justify-center">
          <div className="text-gray-500 text-sm">
            Cargando más propiedades...
          </div>
        </div>
      )}
    </div>
  )
}

export default PropertyCarousel

