import React, { useState } from 'react';
import Sidebar from './components/Sidebar';
import FormSection from './components/FormSection';
import WorkoutDisplay from './components/WorkoutDisplay';

const API_BASE_URL = import.meta.env.VITE_API_URL;

const App = () => {
  const [sidebarOpen, setSidebarOpen] = useState(false);
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState(null);
  const [workoutData, setWorkoutData] = useState(null);
  const [formData, setFormData] = useState({
    name: '',
    age: '',
    gender: '',
    height: '',
    weight: '',
    activityLevel: '',
    goals: [],
    equipment: [],
    injuries: [],
    preferredWorkoutTypes: [],
    preferredTrainingTimes: []
  });

  const buildUserProfile = () => {
    return {
      user_id: `user_${Date.now()}`,
      name: formData.name,
      physical_stats: {
        height: parseFloat(formData.height),
        weight: parseFloat(formData.weight),
        gender: formData.gender,
        age: parseInt(formData.age)
      },
      goals: formData.goals.map(goal => ({ goal_type: goal })),
      preferences: {
        preferred_workout_types: formData.preferredWorkoutTypes,
        preferred_training_times: formData.preferredTrainingTimes
      },
      activity_level: formData.activityLevel,
      restrictions: {
        injuries: formData.injuries.filter(injury => injury !== 'none'),
        equipment: formData.equipment,
        not_preferred_exercises: [],
        special_considerations: []
      },
      created_at: null
    };
  };

  const generateWorkout = async (userProfile = null) => {
    setIsLoading(true);
    setError(null);

    try {
      const profile = userProfile || buildUserProfile();
      
      const response = await fetch(`${API_BASE_URL}/generate-workout`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(profile),
      });

      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }

      const data = await response.json();
      
      if (data.status === 'success') {
        setWorkoutData(data.raw_workout);
      } else {
        throw new Error(data.message || 'Failed to generate workout');
      }
    } catch (err) {
      setError(err.message);
      console.error('Error generating workout:', err);
    } finally {
      setIsLoading(false);
    }
  };

  const handleFormSubmit = (e) => {
    e.preventDefault();
    generateWorkout();
  };

  const handleRegenerate = () => {
    generateWorkout();
  };

  return (
    <div className="flex h-screen bg-gray-50">
      {/* Mobile menu button */}
      <div className="lg:hidden fixed top-4 left-4 z-50">
        <button
          onClick={() => setSidebarOpen(!sidebarOpen)}
          className="p-2 rounded-md bg-white shadow-lg"
        >
          <svg className="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M4 6h16M4 12h16M4 18h16" />
          </svg>
        </button>
      </div>

      {/* Sidebar */}
      <Sidebar isOpen={sidebarOpen} onToggle={() => setSidebarOpen(!sidebarOpen)} />

      {/* Main content */}
      <div className="flex-1 flex flex-col lg:ml-64">
        <main className="flex-1 overflow-y-auto">
          <div className="max-w-4xl mx-auto p-6">
            {/* Error Display */}
            {error && (
              <div className="mb-6 p-4 bg-red-50 border border-red-200 rounded-lg">
                <div className="flex items-center space-x-2">
                  <svg className="w-5 h-5 text-red-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 8v4m0 4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
                  </svg>
                  <span className="font-medium text-red-800">Error</span>
                </div>
                <p className="text-red-700 mt-1">{error}</p>
              </div>
            )}

            {/* Content */}
            {!workoutData ? (
              <FormSection
                formData={formData}
                setFormData={setFormData}
                onSubmit={handleFormSubmit}
                isLoading={isLoading}
              />
            ) : (
              <div className="space-y-6">
                <WorkoutDisplay
                  workoutData={workoutData}
                  onRegenerate={handleRegenerate}
                  isLoading={isLoading}
                />
                
                {/* Back to form button */}
                <div className="text-center">
                  <button
                    onClick={() => setWorkoutData(null)}
                    className="btn-secondary"
                  >
                    ← Back to Profile Form
                  </button>
                </div>
              </div>
            )}
          </div>
        </main>
      </div>
    </div>
  );
};

export default App; 