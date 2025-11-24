import React from 'react'

function NewChatButton({ onNewChat }) {
  return (
    <button
      onClick={onNewChat}
      className="flex items-center space-x-2 px-4 py-2 bg-indigo-600 text-white rounded-lg hover:bg-indigo-700 transition-colors duration-200 shadow-md hover:shadow-lg"
      title="Iniciar una nueva consulta"
    >
      <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M12 4v16m8-8H4"></path>
      </svg>
      <span className="font-medium">Nueva Consulta</span>
    </button>
  )
}

export default NewChatButton

