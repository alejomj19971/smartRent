import React from 'react'

function MessageBubble({ message, showProperties = false }) {
  const { text, isUser, properties } = message

  // Función simple para limpiar el texto (más rápida)
  const cleanText = (text) => {
    if (!text) return ''
    
    return text
      // Eliminar URLs de imágenes en formato markdown completo (incluyendo "![Imagen](...)" o "![...](...)")
      .replace(/!\[[^\]]*\]\([^\)]+\)/g, '')
      // Eliminar líneas que solo contienen "![Imagen](No disponible)" o similares
      .replace(/^\s*!\[[^\]]*\]\([^\)]*\)\s*$/gm, '')
      // Eliminar URLs de fincaraiz (cualquier formato)
      .replace(/https?:\/\/cdn\d+\.fincaraiz\.com\.co[^\s\)\]\n,;!?]+/gi, '')
      // Eliminar URLs de fincaraiz en formato markdown
      .replace(/!\[.*?\]\(https?:\/\/cdn\d+\.fincaraiz\.com\.co[^\)]+\)/gi, '')
      // Eliminar URLs directas de imágenes (cualquier dominio)
      .replace(/https?:\/\/[^\s\)\]\n,;!?]+\.(jpg|jpeg|png|gif|webp|svg)/gi, '')
      // Eliminar URLs específicas de metrocuadrado
      .replace(/https?:\/\/multimedia\.metrocuadrado\.com[^\s\)\]\n,;!?]+/g, '')
      // Eliminar URLs de ciencuadras
      .replace(/https?:\/\/[^\s\)\]\n,;!?]*ciencuadras[^\s\)\]\n,;!?]*/gi, '')
      // Eliminar líneas que solo contienen espacios y guiones
      .replace(/^\s*-\s*$/gm, '')
      // Eliminar líneas vacías después de números de lista
      .replace(/^\d+\.\s*$/gm, '')
      // Limpiar múltiples espacios en blanco
      .replace(/[ \t]+/g, ' ')
      // Limpiar líneas vacías múltiples (máximo 2 líneas vacías seguidas)
      .replace(/\n{3,}/g, '\n\n')
      // Limpiar espacios al inicio y final de cada línea
      .split('\n').map(line => line.trim()).filter(line => line.length > 0).join('\n')
      .trim()
  }

  return (
    <div className={`flex items-start space-x-2 ${isUser ? 'flex-row-reverse space-x-reverse' : ''}`}>
      <div className="flex-shrink-0">
        <div className={`w-8 h-8 rounded-full flex items-center justify-center ${
          isUser ? 'bg-indigo-600' : 'bg-indigo-500'
        }`}>
          <span className="text-white text-xs font-semibold">
            {isUser ? 'Tú' : 'AI'}
          </span>
        </div>
      </div>
      
      <div className={`flex-1 ${isUser ? 'text-right' : ''}`}>
        <div className={`rounded-lg p-3 inline-block max-w-full ${
          isUser 
            ? 'bg-indigo-600 text-white' 
            : 'bg-gray-100 text-gray-800'
        }`}>
          <p className={`whitespace-pre-wrap text-sm leading-relaxed ${isUser ? 'text-white' : 'text-gray-800'}`}>
            {isUser ? text : cleanText(text)}
          </p>
        </div>
      </div>
    </div>
  )
}

export default MessageBubble

