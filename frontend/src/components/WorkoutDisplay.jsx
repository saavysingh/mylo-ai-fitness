import React from 'react';

const WorkoutDisplay = ({ workoutData }) => {
  if (!workoutData) return null;

  // Handle both string and object formats
  const workoutText = typeof workoutData === 'string' ? workoutData : workoutData.toString();

  // Format the workout text for display
  const formatWorkoutText = (text) => {
    return text
      .split('\n')
      .map((line, index) => {
        // Handle different formatting
        if (line.startsWith('**') && line.endsWith('**')) {
          // Bold headers
          return (
            <h3 key={index} className="text-lg font-bold text-gray-900 mt-6 mb-3">
              {line.replace(/\*\*/g, '')}
            </h3>
          );
        } else if (line.startsWith('*') && !line.startsWith('**')) {
          // Bullet points
          return (
            <li key={index} className="text-gray-700 ml-4 mb-1">
              {line.replace(/^\*\s?/, '')}
            </li>
          );
        } else if (line.match(/^\d+\./)) {
          // Numbered lists
          return (
            <div key={index} className="text-gray-700 font-medium mt-3 mb-2 pl-4">
              {line}
            </div>
          );
        } else if (line.trim() === '') {
          // Empty lines
          return <div key={index} className="h-2" />;
        } else {
          // Regular text
          return (
            <p key={index} className="text-gray-700 mb-2 leading-relaxed">
              {line}
            </p>
          );
        }
      });
  };

  return (
    <div className="bg-white rounded-lg shadow-sm border border-gray-200 p-6">
      <div className="mb-6">
        <h2 className="text-2xl font-bold text-gray-900 mb-2">🏋️‍♂️ Your Personalized Workout</h2>
        <div className="flex items-center space-x-2 text-sm text-gray-600">
          <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z" />
          </svg>
          <span>AI Generated Workout Plan</span>
        </div>
      </div>

      <div className="prose prose-gray max-w-none">
        <div className="bg-gray-50 rounded-lg p-4 font-mono text-sm whitespace-pre-wrap">
          {formatWorkoutText(workoutText)}
        </div>
      </div>
    </div>
  );
};

export default WorkoutDisplay;