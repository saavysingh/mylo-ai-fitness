import React from 'react';

const FormSection = ({ formData, setFormData, onSubmit, isLoading }) => {
  const handleInputChange = (field, value) => {
    setFormData(prev => ({
      ...prev,
      [field]: value
    }));
  };

  const handleMultiSelectChange = (field, value) => {
    setFormData(prev => ({
      ...prev,
      [field]: prev[field].includes(value)
        ? prev[field].filter(item => item !== value)
        : [...prev[field], value]
    }));
  };

  return (
    <div className="card">
      <h2 className="text-2xl font-bold text-gray-900 mb-6">Your Fitness Profile</h2>
      
      <form onSubmit={onSubmit} className="space-y-6">
        {/* Basic Information */}
        <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">
              Name *
            </label>
            <input
              type="text"
              value={formData.name}
              onChange={(e) => handleInputChange('name', e.target.value)}
              className="input-field"
              required
            />
          </div>
          
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">
              Age *
            </label>
            <input
              type="number"
              min="13"
              max="100"
              value={formData.age}
              onChange={(e) => handleInputChange('age', parseInt(e.target.value))}
              className="input-field"
              required
            />
          </div>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">
              Gender *
            </label>
            <select
              value={formData.gender}
              onChange={(e) => handleInputChange('gender', e.target.value)}
              className="select-field"
              required
            >
              <option value="">Select gender</option>
              <option value="male">Male</option>
              <option value="female">Female</option>
              <option value="other">Other</option>
            </select>
          </div>
          
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">
              Activity Level *
            </label>
            <select
              value={formData.activityLevel}
              onChange={(e) => handleInputChange('activityLevel', e.target.value)}
              className="select-field"
              required
            >
              <option value="">Select activity level</option>
              <option value="sedentary">Sedentary</option>
              <option value="lightly_active">Lightly Active</option>
              <option value="moderately_active">Moderately Active</option>
              <option value="very_active">Very Active</option>
              <option value="extremely_active">Extremely Active</option>
            </select>
          </div>
        </div>

        {/* Physical Stats */}
        <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">
              Height (cm) *
            </label>
            <input
              type="number"
              min="100"
              max="250"
              value={formData.height}
              onChange={(e) => handleInputChange('height', parseFloat(e.target.value))}
              className="input-field"
              required
            />
          </div>
          
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">
              Weight (kg) *
            </label>
            <input
              type="number"
              min="30"
              max="300"
              step="0.1"
              value={formData.weight}
              onChange={(e) => handleInputChange('weight', parseFloat(e.target.value))}
              className="input-field"
              required
            />
          </div>
        </div>

        {/* Fitness Goals */}
        <div>
          <label className="block text-sm font-medium text-gray-700 mb-2">
            Fitness Goals *
          </label>
          <div className="grid grid-cols-2 md:grid-cols-3 gap-3">
            {[
              { value: 'weight_loss', label: 'Weight Loss' },
              { value: 'muscle_gain', label: 'Muscle Gain' },
              { value: 'endurance', label: 'Endurance' },
              { value: 'strength', label: 'Strength' },
              { value: 'flexibility', label: 'Flexibility' }
            ].map(goal => (
              <label key={goal.value} className="flex items-center space-x-2 cursor-pointer">
                <input
                  type="checkbox"
                  checked={formData.goals.includes(goal.value)}
                  onChange={() => handleMultiSelectChange('goals', goal.value)}
                  className="rounded border-gray-300 text-primary-600 focus:ring-primary-500"
                />
                <span className="text-sm text-gray-700">{goal.label}</span>
              </label>
            ))}
          </div>
        </div>

        {/* Equipment */}
        <div>
          <label className="block text-sm font-medium text-gray-700 mb-2">
            Available Equipment
          </label>
          <div className="grid grid-cols-2 md:grid-cols-3 gap-3">
            {[
              { value: 'bodyweight_only', label: 'Bodyweight Only' },
              { value: 'dumbbells', label: 'Dumbbells' },
              { value: 'resistance_bands', label: 'Resistance Bands' },
              { value: 'gym_access', label: 'Gym Access' }
            ].map(equipment => (
              <label key={equipment.value} className="flex items-center space-x-2 cursor-pointer">
                <input
                  type="checkbox"
                  checked={formData.equipment.includes(equipment.value)}
                  onChange={() => handleMultiSelectChange('equipment', equipment.value)}
                  className="rounded border-gray-300 text-primary-600 focus:ring-primary-500"
                />
                <span className="text-sm text-gray-700">{equipment.label}</span>
              </label>
            ))}
          </div>
        </div>

        {/* Injuries */}
        <div>
          <label className="block text-sm font-medium text-gray-700 mb-2">
            Injuries (if any)
          </label>
          <div className="grid grid-cols-2 md:grid-cols-3 gap-3">
            {[
              { value: 'none', label: 'None' },
              { value: 'knee_injury', label: 'Knee Injury' },
              { value: 'back_injury', label: 'Back Injury' },
              { value: 'shoulder_injury', label: 'Shoulder Injury' }
            ].map(injury => (
              <label key={injury.value} className="flex items-center space-x-2 cursor-pointer">
                <input
                  type="checkbox"
                  checked={formData.injuries.includes(injury.value)}
                  onChange={() => handleMultiSelectChange('injuries', injury.value)}
                  className="rounded border-gray-300 text-primary-600 focus:ring-primary-500"
                />
                <span className="text-sm text-gray-700">{injury.label}</span>
              </label>
            ))}
          </div>
        </div>

        {/* Preferred Workout Types */}
        <div>
          <label className="block text-sm font-medium text-gray-700 mb-2">
            Preferred Workout Types *
          </label>
          <div className="grid grid-cols-2 md:grid-cols-3 gap-3">
            {[
              { value: 'cardio', label: 'Cardio' },
              { value: 'strength_training', label: 'Strength Training' },
              { value: 'yoga', label: 'Yoga' },
              { value: 'pilates', label: 'Pilates' },
              { value: 'hiit', label: 'HIIT' }
            ].map(type => (
              <label key={type.value} className="flex items-center space-x-2 cursor-pointer">
                <input
                  type="checkbox"
                  checked={formData.preferredWorkoutTypes.includes(type.value)}
                  onChange={() => handleMultiSelectChange('preferredWorkoutTypes', type.value)}
                  className="rounded border-gray-300 text-primary-600 focus:ring-primary-500"
                />
                <span className="text-sm text-gray-700">{type.label}</span>
              </label>
            ))}
          </div>
        </div>

        {/* Preferred Training Times */}
        <div>
          <label className="block text-sm font-medium text-gray-700 mb-2">
            Preferred Training Times *
          </label>
          <div className="grid grid-cols-2 md:grid-cols-3 gap-3">
            {[
              { value: 'morning', label: 'Morning' },
              { value: 'afternoon', label: 'Afternoon' },
              { value: 'evening', label: 'Evening' }
            ].map(time => (
              <label key={time.value} className="flex items-center space-x-2 cursor-pointer">
                <input
                  type="checkbox"
                  checked={formData.preferredTrainingTimes.includes(time.value)}
                  onChange={() => handleMultiSelectChange('preferredTrainingTimes', time.value)}
                  className="rounded border-gray-300 text-primary-600 focus:ring-primary-500"
                />
                <span className="text-sm text-gray-700">{time.label}</span>
              </label>
            ))}
          </div>
        </div>

        {/* Submit Button */}
        <div className="pt-4">
          <button
            type="submit"
            disabled={isLoading}
            className="w-full btn-primary disabled:opacity-50 disabled:cursor-not-allowed flex items-center justify-center space-x-2"
          >
            {isLoading ? (
              <>
                <svg className="animate-spin -ml-1 mr-3 h-5 w-5 text-white" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
                  <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4"></circle>
                  <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
                </svg>
                <span>Generating Workout...</span>
              </>
            ) : (
              <span>Generate My Workout</span>
            )}
          </button>
        </div>
      </form>
    </div>
  );
};

export default FormSection; 