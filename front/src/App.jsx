import React, { useState, useRef, useEffect } from 'react'
import ChatMessages from './components/ChatMessages'
import ChatInput from './components/ChatInput'
import PropertyCarousel from './components/PropertyCarousel'
import PropertySummary from './components/PropertySummary'
import TotalProperties from './components/TotalProperties'
import PropertySearch from './components/PropertySearch'
import PropertyFilters from './components/PropertyFilters'
import NewChatButton from './components/NewChatButton'
import QuickQuestions from './components/QuickQuestions'
import { propertyTrie } from './utils/trie'

function App() {
  const [messages, setMessages] = useState([])
  const [isLoading, setIsLoading] = useState(false)
  const messagesEndRef = useRef(null)
  const [searchResults, setSearchResults] = useState(null)
  const [searchTerm, setSearchTerm] = useState('')
  const [filteredProperties, setFilteredProperties] = useState(null)
  
  // Extraer todas las propiedades de todos los mensajes
  const allProperties = messages.reduce((acc, message) => {
    if (message.properties && Array.isArray(message.properties)) {
      return [...acc, ...message.properties]
    }
    return acc
  }, [])

  // Propiedades base para filtros (sin filtros aplicados)
  const baseProperties = filteredProperties !== null ? filteredProperties : allProperties

  // Propiedades a mostrar: si hay búsqueda activa, usar resultados; si no, usar todas o filtradas
  const displayProperties = searchResults !== null ? searchResults : baseProperties

  const handleSearch = (term, results = null) => {
    setSearchTerm(term)
    if (term === '') {
      setSearchResults(null)
    } else {
      setSearchResults(results || [])
    }
  }

  const handleFilterChange = (filtered, activeFilters) => {
    setFilteredProperties(activeFilters && Object.values(activeFilters).some(v => v !== null && v !== '') ? filtered : null)
  }

  const handleNewChat = () => {
    setMessages([])
    setSearchTerm('')
    setSearchResults(null)
    propertyTrie.clear()
    setFilteredProperties(null)
    
  }




  // Mensaje de bienvenida inicial
  useEffect(() => {
    if (messages.length === 0) {
      setMessages([
        {
          id: 1,
          text: `¡Hola! 👋 Soy tu asistente de SmartRent. Puedo ayudarte a buscar propiedades.\n\nEjemplos de preguntas:\n• "Buscar casas que valgan menos de un millón doscientos"\n• "Cuántas casas hay disponibles?"\n• "Casas con parqueadero y más de 3 habitaciones"\n• "Lista las 5 casas más caras"`,
          isUser: false,
          properties: []
        }
      ])
    }
  }, [])

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' })
  }

  useEffect(() => {
    scrollToBottom()
  }, [messages])

  const sendMessage = async (message) => {
    if (!message.trim() || isLoading) return

    setMessages([])
    setSearchTerm('')
    setSearchResults(null)
    propertyTrie.clear()
    setFilteredProperties(null)

    const userMessage = {
      id: Date.now(),
      text: message,
      isUser: true,
      properties: []
    }
    setMessages([userMessage])
    setIsLoading(true)

    try {
      const response = await fetch('/chat', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ 
          message: message
        })
      })

      const data = await response.json()

      let responseText = data.response
      let properties = []

      try {
        const parsed = JSON.parse(data.response)
        if (parsed.properties && Array.isArray(parsed.properties)) {
          responseText = parsed.text || data.response
          properties = parsed.properties
          
          properties.forEach(property => {
            propertyTrie.insertProperty(property)
          })
        }
      } catch (e) {
        // Si no es JSON, usar el texto directamente
      }

      const aiMessage = {
        id: Date.now() + 1,
        text: responseText,
        isUser: false,
        properties: properties
      }

      setMessages(prev => [...prev, aiMessage])
    } catch (error) {
      const errorMessage = {
        id: Date.now() + 1,
        text: 'Error de conexión. Por favor, verifica que el servidor esté ejecutándose.',
        isUser: false,
        properties: []
      }
      setMessages(prev => [...prev, errorMessage])
      console.error('Error:', error)
    } finally {
      setIsLoading(false)
    }
  }

  return (
    <div className="bg-gradient-to-br from-blue-50 to-indigo-100 min-h-screen">
      <div className="container mx-auto max-w-[1600px] px-4 py-8">
        {/* Header */}
        <div className="bg-white rounded-lg shadow-lg p-6 mb-6">
          <div className="flex items-center justify-between flex-wrap gap-4">
            <div>
              <h1 className="text-3xl font-bold text-indigo-600">🏠 SmartRent Chat</h1>
              <p className="text-gray-600 mt-1">Asistente inteligente para consultas sobre propiedades</p>
            </div>
            <div className="flex items-center space-x-4">
              <NewChatButton onNewChat={handleNewChat} />
              <div className="flex items-center space-x-2">
                <div className="w-3 h-3 bg-green-500 rounded-full"></div>
                <span className="text-sm text-gray-600">Conectado</span>
              </div>
            </div>
          </div>
        </div>

        <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
          {/* Columna izquierda: Chat y Carrusel */}
          <div className="lg:col-span-2 space-y-6">
            {/* Preguntas Rápidas */}
            {messages.length <= 1 && (
              <QuickQuestions onSelectQuestion={sendMessage} />
            )}
            
            {/* Chat Container */}
            <div className="bg-white rounded-lg shadow-lg overflow-hidden">
              <ChatMessages 
                messages={messages} 
                isLoading={isLoading}
                messagesEndRef={messagesEndRef}
              />
              <ChatInput onSendMessage={sendMessage} isLoading={isLoading} />
            </div>

            {/* Buscador de Propiedades */}
            {allProperties.length > 0 && (
              <div className="bg-white rounded-lg shadow-lg p-6">
                <h3 className="text-lg font-semibold text-gray-800 mb-4 flex items-center">
                  <svg className="w-5 h-5 mr-2 text-indigo-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z" />
                  </svg>
                  Buscar Propiedades
                </h3>
                <PropertySearch 
                  onSearch={handleSearch} 
                  allProperties={allProperties}
                  placeholder="Buscar por título de propiedad..." 
                />
                {searchTerm && (
                  <p className="mt-3 text-sm text-gray-600">
                    {searchResults !== null && searchResults.length === 0 ? (
                      <span className="text-orange-600">No se encontraron propiedades con "{searchTerm}"</span>
                    ) : searchResults !== null ? (
                      <span className="text-green-600">Se encontraron {searchResults.length} {searchResults.length === 1 ? 'propiedad' : 'propiedades'}</span>
                    ) : null}
                  </p>
                )}
              </div>
            )}

            {/* Carrusel de Propiedades */}
            <PropertyCarousel properties={displayProperties} />
          </div>

          {/* Columna derecha: Resumen y Filtros */}
          <div className="lg:col-span-1 space-y-6">
            <TotalProperties />
            <PropertySummary count={displayProperties.length} />
            {baseProperties.length > 0 && (
              <PropertyFilters 
                properties={baseProperties} 
                onFilterChange={handleFilterChange}
              />
            )}
          </div>
        </div>
      </div>
    </div>
  )
}

export default App
