import React, { useState } from 'react';

const WorkoutDisplay = ({ workoutData, onRegenerate, isLoading }) => {
  const [expandedSections, setExpandedSections] = useState(new Set());

  const toggleSection = (sectionName) => {
    setExpandedSections(prev => {
      const newSet = new Set(prev);
      if (newSet.has(sectionName)) {
        newSet.delete(sectionName);
      } else {
        newSet.add(sectionName);
      }
      return newSet;
    });
  };

  if (!workoutData) return null;

  return (
    <div className="card">
      <div className="flex items-center justify-between mb-6">
        <h2 className="text-2xl font-bold text-gray-900">Your Personalized Workout</h2>
        <button
          onClick={onRegenerate}
          disabled={isLoading}
          className="btn-secondary disabled:opacity-50 disabled:cursor-not-allowed flex items-center space-x-2"
        >
          <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M4 4v5h.582m15.356 2A8.001 8.001 0 004.582 9m0 0H9m11 11v-5h-.581m0 0a8.003 8.003 0 01-15.357-2m15.357 2H15" />
          </svg>
          <span>Regenerate</span>
        </button>
      </div>

      {/* Workout Header */}
      <div className="bg-gradient-to-r from-primary-50 to-secondary-50 rounded-lg p-6 mb-6">
        <h3 className="text-xl font-bold text-gray-900 mb-2">{workoutData.title}</h3>
        <p className="text-gray-600 mb-4">{workoutData.description}</p>
        
        <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
          <div className="flex items-center space-x-2">
            <svg className="w-5 h-5 text-primary-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z" />
            </svg>
            <span className="text-sm font-medium text-gray-700">Duration: {workoutData.total_duration}</span>
          </div>
          
          <div className="flex items-center space-x-2">
            <svg className="w-5 h-5 text-secondary-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M13 10V3L4 14h7v7l9-11h-7z" />
            </svg>
            <span className="text-sm font-medium text-gray-700">Level: {workoutData.difficulty}</span>
          </div>
          
          <div className="flex items-center space-x-2">
            <svg className="w-5 h-5 text-green-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z" />
            </svg>
            <span className="text-sm font-medium text-gray-700">AI Generated</span>
          </div>
        </div>
      </div>

      {/* Workout Sections */}
      <div className="space-y-4">
        {workoutData.sections.map((section, sectionIndex) => (
          <div key={sectionIndex} className="border border-gray-200 rounded-lg overflow-hidden">
            <button
              onClick={() => toggleSection(section.name)}
              className="w-full px-6 py-4 bg-gray-50 hover:bg-gray-100 transition-colors flex items-center justify-between"
            >
              <div className="flex items-center space-x-3">
                <div className="w-8 h-8 bg-primary-100 rounded-full flex items-center justify-center">
                  <span className="text-primary-700 font-bold text-sm">{sectionIndex + 1}</span>
                </div>
                <div>
                  <h4 className="font-semibold text-gray-900">{section.name}</h4>
                  <p className="text-sm text-gray-600">{section.duration}</p>
                </div>
              </div>
              <svg 
                className={`w-5 h-5 text-gray-500 transition-transform ${expandedSections.has(section.name) ? 'rotate-180' : ''}`} 
                fill="none" 
                stroke="currentColor" 
                viewBox="0 0 24 24"
              >
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M19 9l-7 7-7-7" />
              </svg>
            </button>
            
            {expandedSections.has(section.name) && (
              <div className="px-6 py-4 bg-white">
                <div className="space-y-4">
                  {section.exercises.map((exercise, exerciseIndex) => (
                    <div key={exerciseIndex} className="border-l-4 border-primary-200 pl-4">
                      <div className="flex items-start justify-between">
                        <div className="flex-1">
                          <h5 className="font-medium text-gray-900 mb-1">
                            {exerciseIndex + 1}. {exercise.name}
                          </h5>
                          <div className="flex items-center space-x-4 text-sm text-gray-600 mb-2">
                            <span className="flex items-center space-x-1">
                              <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z" />
                              </svg>
                              <span>{exercise.duration}</span>
                            </span>
                          </div>
                          <p className="text-gray-700 mb-2">{exercise.instructions}</p>
                          {exercise.modifications && (
                            <div className="bg-yellow-50 border border-yellow-200 rounded-lg p-3">
                              <div className="flex items-start space-x-2">
                                <svg className="w-4 h-4 text-yellow-600 mt-0.5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M13 16h-1v-4h-1m1-4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
                                </svg>
                                <div>
                                  <p className="text-sm font-medium text-yellow-800">Modifications</p>
                                  <p className="text-sm text-yellow-700">{exercise.modifications}</p>
                                </div>
                              </div>
                            </div>
                          )}
                        </div>
                      </div>
                    </div>
                  ))}
                </div>
              </div>
            )}
          </div>
        ))}
      </div>

      {/* Notes */}
      {workoutData.notes && workoutData.notes.length > 0 && (
        <div className="mt-6 p-4 bg-blue-50 border border-blue-200 rounded-lg">
          <h4 className="font-semibold text-blue-900 mb-2 flex items-center space-x-2">
            <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M13 16h-1v-4h-1m1-4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
            </svg>
            <span>Important Notes</span>
          </h4>
          <ul className="space-y-1">
            {workoutData.notes.map((note, index) => (
              <li key={index} className="text-sm text-blue-800 flex items-start space-x-2">
                <span className="text-blue-600 mt-1">•</span>
                <span>{note}</span>
              </li>
            ))}
          </ul>
        </div>
      )}

      {/* Progression Plan */}
      {workoutData.progression && (
        <div className="mt-6 p-4 bg-green-50 border border-green-200 rounded-lg">
          <h4 className="font-semibold text-green-900 mb-2 flex items-center space-x-2">
            <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M13 10V3L4 14h7v7l9-11h-7z" />
            </svg>
            <span>Progression Plan</span>
          </h4>
          <p className="text-sm text-green-800">{workoutData.progression}</p>
        </div>
      )}
    </div>
  );
};

export default WorkoutDisplay; 