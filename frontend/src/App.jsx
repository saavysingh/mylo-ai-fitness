import React, { useState } from 'react';
import ChatContainer from './components/Chat/ChatContainer';
import WorkoutDisplay from './components/WorkoutDisplay';

const App = () => {
  const [workout, setWorkout] = useState(null);

  const handleWorkoutGenerated = (workoutData) => {
    setWorkout(workoutData);
  };

  return (
    <div className="min-h-screen bg-gray-50">
      <header className="bg-white shadow">
        <div className="max-w-4xl mx-auto py-6 px-4 sm:px-6 lg:px-8">
          <h1 className="text-3xl font-bold text-gray-900">
            🏋️‍♂️ Mylo AI Fitness
          </h1>
          <p className="text-gray-600 mt-2">Your personalized AI fitness coach</p>
        </div>
      </header>

      <main className="max-w-4xl mx-auto py-6 px-4 sm:px-6 lg:px-8">
        {!workout ? (
          <ChatContainer onWorkoutGenerated={handleWorkoutGenerated} />
        ) : (
          <div>
            <WorkoutDisplay workoutData={workout} />
            <button
              onClick={() => setWorkout(null)}
              className="mt-6 px-6 py-3 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition-colors"
            >
              Create New Workout Plan
            </button>
          </div>
        )}
      </main>
    </div>
  );
};

export default App;
