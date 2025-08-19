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
      <header className="fixed top-0 left-0 right-0 bg-white shadow">
        <div className="max-w-4xl mx-auto py-4 px-4 sm:px-6 lg:px-8">
          <h1 className="text-2xl font-bold text-gray-900">
            🏋️‍♂️ Mylo AI Fitness
          </h1>
          <p className="text-gray-600 mt-1">Your personalized AI fitness coach</p>
        </div>
      </header>

      <main className="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8 pt-20 h-[calc(100vh-5rem)]">
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
