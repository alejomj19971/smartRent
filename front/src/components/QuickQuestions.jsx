import React from 'react'

function QuickQuestions({ onSelectQuestion }) {
  const quickQuestions = [
    {
      text: "casas disponibles",
      icon: "🏠"
    },
    {
      text: "casas en Bello",
      icon: "📍"
    },
    {
      text: "casas en Medellín",
      icon: "📍"
    },
    {
      text: "2 cuartos, 2 baños, parqueadero",
      icon: "🔍"
    },
    {
      text: "1 millón, 1 baño, 1 cuarto",
      icon: "💰"
    },
    {
      text: "casas con parqueadero",
      icon: "🚗"
    },
    {
      text: "casas en La Estrella",
      icon: "📍"
    },
    {
      text: "menos de 50 m², parqueadero",
      icon: "📐"
    },
    {
      text: "3 cuartos, más de 70 m²",
      icon: "🏡"
    },
    {
      text: "casas baratas",
      icon: "💵"
    }
  ]

  return (
    <div className="bg-white rounded-lg shadow-lg p-4 mb-4">
      <h3 className="text-sm font-semibold text-gray-700 mb-3 flex items-center">
        <svg className="w-4 h-4 mr-2 text-indigo-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M13 10V3L4 14h7v7l9-11h-7z" />
        </svg>
        Preguntas Rápidas
      </h3>
      <div className="flex flex-wrap gap-2">
        {quickQuestions.map((question, index) => (
          <button
            key={index}
            onClick={() => onSelectQuestion(question.text)}
            className="px-3 py-2 text-xs bg-indigo-50 hover:bg-indigo-100 text-indigo-700 rounded-lg transition-colors duration-200 border border-indigo-200 hover:border-indigo-300 flex items-center space-x-1"
          >
            <span>{question.icon}</span>
            <span className="whitespace-nowrap">{question.text}</span>
          </button>
        ))}
      </div>
    </div>
  )
}

export default QuickQuestions

