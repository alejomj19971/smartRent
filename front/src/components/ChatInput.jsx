import React, { useState } from 'react'

function ChatInput({ onSendMessage, isLoading, disabled = false }) {
  const [message, setMessage] = useState('')

  const handleSubmit = (e) => {
    e.preventDefault()
    if (message.trim() && !isLoading && !disabled) {
      if (message.toLowerCase() === 'salir' || message.toLowerCase() === 'exit') {
        onSendMessage('👋 ¡Hasta luego!')
        return
      }
      onSendMessage(message)
      setMessage('')
    }
  }

  return (
    <div className="border-t border-gray-200 p-4 bg-white">
      <form onSubmit={handleSubmit} className="flex space-x-3">
        <input
          type="text"
          value={message}
          onChange={(e) => setMessage(e.target.value)}
          placeholder="Escribe tu pregunta sobre propiedades..."
          className="flex-1 px-4 py-3 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-indigo-500 focus:border-transparent disabled:bg-gray-100 disabled:cursor-not-allowed"
          disabled={isLoading}
          autoComplete="off"
        />
        <button
          type="submit"
          disabled={isLoading || !message.trim()}
          className="px-6 py-3 bg-indigo-600 text-white rounded-lg hover:bg-indigo-700 focus:outline-none focus:ring-2 focus:ring-indigo-500 focus:ring-offset-2 transition-colors duration-200 font-medium disabled:opacity-50 disabled:cursor-not-allowed"
        >
          Enviar
        </button>
      </form>
      <p className="text-xs text-gray-500 mt-2 text-center">
        Presiona Enter para enviar
      </p>
    </div>
  )
}

export default ChatInput

