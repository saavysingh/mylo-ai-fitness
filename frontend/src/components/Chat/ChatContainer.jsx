import React, { useState, useRef, useEffect } from 'react';
import PropTypes from 'prop-types';
import ChatMessage from './ChatMessage';

const API_BASE_URL = import.meta.env.VITE_API_URL;

const GOALS = [
  { id: 'weight_loss', label: 'Weight Loss' },
  { id: 'muscle_gain', label: 'Muscle Gain' },
  { id: 'endurance', label: 'Endurance' },
  { id: 'strength', label: 'Strength' },
  { id: 'flexibility', label: 'Flexibility' },
  { id: 'maintenance', label: 'Maintenance' },
];

const WORKOUT_TYPES = [
  { id: 'strength_training', label: 'Strength Training' },
  { id: 'cardio', label: 'Cardio' },
  { id: 'yoga', label: 'Yoga' },
  { id: 'pilates', label: 'Pilates' },
  { id: 'HIIT', label: 'HIIT' },
];

const EQUIPMENT = [
  { id: 'bodyweight', label: 'Bodyweight Only' },
  { id: 'dumbbells', label: 'Dumbbells' },
  { id: 'resistance_bands', label: 'Resistance Bands' },
  { id: 'gym_access', label: 'Gym Access' },
];

const TIMES = [
  { id: 'morning', label: 'Morning' },
  { id: 'afternoon', label: 'Afternoon' },
  { id: 'evening', label: 'Evening' },
];

const ChatContainer = ({ onWorkoutGenerated }) => {
  const [sessionId] = useState(() => `session_${Date.now()}`);
  const [messages, setMessages] = useState([]);
  const [stage, setStage] = useState('basic');
  const [isLoading, setIsLoading] = useState(false);
  const [isRecording, setIsRecording] = useState(false);
  const [isTranscribing, setIsTranscribing] = useState(false);
  const mediaRecorderRef = useRef(null);
  const audioChunksRef = useRef([]);
  const [voicePreview, setVoicePreview] = useState({ transcript: '', selections: {}, missing: [] });
  const messagesEndRef = useRef(null);
  const hasSentInitialRef = useRef(false);

  // Form state
  const [formData, setFormData] = useState({
    // Basic info
    name: '',
    age: '',
    gender: '',
    height_cm: '',
    weight_kg: '',
    activity_level: '',
    // Goals
    goals: [],
    // Preferences
    preferred_workout_types: [],
    preferred_training_times: [],
    equipment: [],
    injuries: [],
    special_considerations: [],
  });

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  useEffect(() => {
    // Guard against double-invocation in React.StrictMode by using both ref and a window flag
    if (hasSentInitialRef.current || typeof window !== 'undefined' && window.__MYLO_INIT_SENT__) return;
    hasSentInitialRef.current = true;
    if (typeof window !== 'undefined') {
      window.__MYLO_INIT_SENT__ = true;
    }
    console.log("Sending initial message"); // Debug log
    handleChatIngest('basic', {});
  }, []);

  const handleChatIngest = async (stage, selections) => {
    console.log(`handleChatIngest called with stage: ${stage}`); // Debug log
    setIsLoading(true);
    try {
      const response = await fetch(`${API_BASE_URL}/chat/ingest`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          session_id: sessionId,
          stage,
          selections
        }),
      });

      const data = await response.json();

      // Add assistant's message
      setMessages(prev => [...prev, {
        text: data.assistant_text,
        isUser: false
      }]);

      // Handle workout if generated
      if (data.controls && data.controls.workout) {
        console.log('Workout generated:', data.controls.workout);
        onWorkoutGenerated(data.controls.workout);
      } else {
        console.log('No workout in response:', data);
      }

      setStage(data.next_stage);
      return data;
    } catch (error) {
      console.error('Error:', error);
      setMessages(prev => [...prev, {
        text: "Sorry, I encountered an error. Please try again.",
        isUser: false
      }]);
    } finally {
      setIsLoading(false);
    }
  };

  const handleBasicSubmit = async (e) => {
    e.preventDefault();
    const basicData = {
      name: formData.name || null,
      age: parseInt(formData.age),
      gender: formData.gender,
      height_cm: parseFloat(formData.height_cm),
      weight_kg: parseFloat(formData.weight_kg),
      activity_level: formData.activity_level
    };

    const displayText = formData.name
      ? `Hi, I'm ${formData.name}! Age: ${basicData.age}, Gender: ${basicData.gender}, Height: ${basicData.height_cm}cm, Weight: ${basicData.weight_kg}kg, Activity: ${basicData.activity_level}`
      : `Age: ${basicData.age}, Gender: ${basicData.gender}, Height: ${basicData.height_cm}cm, Weight: ${basicData.weight_kg}kg, Activity: ${basicData.activity_level}`;

    setMessages(prev => [...prev, {
      text: displayText,
      isUser: true
    }]);

    await handleChatIngest('basic', basicData);
  };

  const handleGoalsSubmit = async (e) => {
    e.preventDefault();
    const goalsData = {
      goals: formData.goals
    };

    setMessages(prev => [...prev, {
      text: `Goals: ${goalsData.goals.join(', ')}`,
      isUser: true
    }]);

    await handleChatIngest('goals', goalsData);
  };

  const handlePreferencesSubmit = async (e) => {
    e.preventDefault();
    const prefsData = {
      preferred_workout_types: formData.preferred_workout_types,
      preferred_training_times: formData.preferred_training_times,
      equipment: formData.equipment,
      injuries: formData.injuries,
      special_considerations: formData.special_considerations
    };

    setMessages(prev => [...prev, {
      text: `Workout types: ${prefsData.preferred_workout_types.join(', ')}, Times: ${prefsData.preferred_training_times.join(', ')}, Equipment: ${prefsData.equipment.join(', ')}`,
      isUser: true
    }]);

    await handleChatIngest('final', prefsData);
  };

  const applySelectionsToForm = (stageKey, selections) => {
    if (stageKey === 'basic') {
      setFormData(prev => ({
        ...prev,
        name: selections.name ?? prev.name,
        age: selections.age ?? prev.age,
        gender: selections.gender ?? prev.gender,
        height_cm: selections.height_cm ?? prev.height_cm,
        weight_kg: selections.weight_kg ?? prev.weight_kg,
        activity_level: selections.activity_level ?? prev.activity_level,
      }));
    } else if (stageKey === 'goals') {
      setFormData(prev => ({
        ...prev,
        goals: Array.isArray(selections.goals) ? selections.goals : prev.goals,
      }));
    } else if (stageKey === 'final') {
      setFormData(prev => ({
        ...prev,
        injuries: selections.injuries ?? prev.injuries,
        equipment: selections.equipment ?? prev.equipment,
        preferred_workout_types: selections.preferred_workout_types ?? prev.preferred_workout_types,
        preferred_training_times: selections.preferred_training_times ?? prev.preferred_training_times,
        special_considerations: selections.special_considerations ?? prev.special_considerations,
        not_preferred_exercises: selections.not_preferred_exercises ?? prev.not_preferred_exercises,
      }));
    }
  };

  const startRecording = async () => {
    if (isRecording) return;
    try {
      const stream = await navigator.mediaDevices.getUserMedia({ audio: { echoCancellation: true, noiseSuppression: true } });
      const mr = new MediaRecorder(stream, { mimeType: 'audio/webm' });
      audioChunksRef.current = [];
      mr.ondataavailable = (e) => {
        if (e.data && e.data.size > 0) {
          audioChunksRef.current.push(e.data);
        }
      };
      mr.onstop = async () => {
        const blob = new Blob(audioChunksRef.current, { type: 'audio/webm' });
        await uploadAudioForStage(blob, stage);
        stream.getTracks().forEach(t => t.stop());
      };
      mediaRecorderRef.current = mr;
      mr.start();
      setIsRecording(true);
    } catch (err) {
      console.error('Mic error:', err);
      alert('Could not access microphone');
    }
  };

  const stopRecording = () => {
    if (!isRecording || !mediaRecorderRef.current) return;
    mediaRecorderRef.current.stop();
    setIsRecording(false);
  };

  const uploadAudioForStage = async (blob, stageKey) => {
    setIsTranscribing(true);
    try {
      const fd = new FormData();
      fd.append('file', blob, 'input.webm');
      const url = `${API_BASE_URL}/speech/transcribe?stage=${stageKey}&session_id=${sessionId}`;
      const resp = await fetch(url, { method: 'POST', body: fd });
      if (!resp.ok) {
        throw new Error(`Transcribe failed: ${resp.status}`);
      }
      const data = await resp.json();
      setVoicePreview({ transcript: data.transcript, selections: data.selections || {}, missing: data.missing || [] });
      applySelectionsToForm(stageKey, data.selections || {});
    } catch (e) {
      console.error(e);
      alert('Transcription failed. Please try again.');
    } finally {
      setIsTranscribing(false);
    }
  };

  const acceptVoiceAndSubmit = async () => {
    const stageKey = stage;
    const selections = voicePreview.selections || {};
    setMessages(prev => [...prev, { text: voicePreview.transcript || '[voice input]', isUser: true }]);
    await handleChatIngest(stageKey, selections);
    setVoicePreview({ transcript: '', selections: {}, missing: [] });
  };

  const toggleArrayValue = (field, value) => {
    setFormData(prev => ({
      ...prev,
      [field]: prev[field].includes(value)
        ? prev[field].filter(item => item !== value)
        : [...prev[field], value]
    }));
  };

  const renderBasicForm = () => (
    <form onSubmit={handleBasicSubmit} className="space-y-4 bg-white p-6 rounded-lg shadow-sm">
      <div className="flex items-center justify-between">
        <span className="text-sm text-gray-600">You can type or use voice</span>
        <button type="button" onClick={isRecording ? stopRecording : startRecording} className={`flex items-center gap-2 px-3 py-2 rounded-md border ${isRecording ? 'bg-red-50 border-red-300 text-red-700' : 'bg-gray-50 border-gray-300 text-gray-700'}`}>
          <span className={`h-2 w-2 rounded-full ${isRecording ? 'bg-red-600 animate-pulse' : 'bg-gray-400'}`}></span>
          {isRecording ? 'Stop' : 'Speak'}
        </button>
      </div>
      {isTranscribing && <div className="text-sm text-gray-500">Transcribing…</div>}
      {voicePreview.transcript && (
        <div className="p-3 border rounded-md bg-gray-50 text-sm">
          <div className="font-medium mb-1">Transcript</div>
          <div className="mb-2">{voicePreview.transcript}</div>
          {voicePreview.missing?.length > 0 && (
            <div className="text-yellow-700 text-xs mb-2">Missing: {voicePreview.missing.join(', ')}</div>
          )}
          <div className="flex gap-2">
            <button type="button" onClick={acceptVoiceAndSubmit} className="px-3 py-2 bg-blue-600 text-white rounded-md">Use & Continue</button>
            <button type="button" onClick={() => setVoicePreview({ transcript: '', selections: {}, missing: [] })} className="px-3 py-2 bg-white border rounded-md">Discard</button>
          </div>
        </div>
      )}
      <input
        type="text"
        placeholder="Name (optional)"
        value={formData.name}
        onChange={(e) => setFormData(prev => ({ ...prev, name: e.target.value }))}
        className="w-full p-3 border rounded-lg focus:ring-2 focus:ring-blue-500"
      />

      <div className="grid grid-cols-2 gap-4">
        <input
          type="number"
          placeholder="Age"
          required
          value={formData.age}
          onChange={(e) => setFormData(prev => ({ ...prev, age: e.target.value }))}
          className="p-3 border rounded-lg focus:ring-2 focus:ring-blue-500"
        />
        <select
          required
          value={formData.gender}
          onChange={(e) => setFormData(prev => ({ ...prev, gender: e.target.value }))}
          className="p-3 border rounded-lg focus:ring-2 focus:ring-blue-500"
        >
          <option value="">Gender</option>
          <option value="male">Male</option>
          <option value="female">Female</option>
          <option value="other">Other</option>
        </select>
      </div>

      <div className="grid grid-cols-2 gap-4">
        <input
          type="number"
          placeholder="Height (cm)"
          required
          value={formData.height_cm}
          onChange={(e) => setFormData(prev => ({ ...prev, height_cm: e.target.value }))}
          className="p-3 border rounded-lg focus:ring-2 focus:ring-blue-500"
        />
        <input
          type="number"
          placeholder="Weight (kg)"
          required
          value={formData.weight_kg}
          onChange={(e) => setFormData(prev => ({ ...prev, weight_kg: e.target.value }))}
          className="p-3 border rounded-lg focus:ring-2 focus:ring-blue-500"
        />
      </div>

      <select
        required
        value={formData.activity_level}
        onChange={(e) => setFormData(prev => ({ ...prev, activity_level: e.target.value }))}
        className="w-full p-3 border rounded-lg focus:ring-2 focus:ring-blue-500"
      >
        <option value="">Activity Level</option>
        <option value="sedentary">Sedentary</option>
        <option value="lightly_active">Lightly Active</option>
        <option value="moderately_active">Moderately Active</option>
        <option value="very_active">Very Active</option>
      </select>

      <button
        type="submit"
        disabled={isLoading}
        className="w-full bg-blue-600 text-white py-3 px-4 rounded-lg hover:bg-blue-700 disabled:opacity-50"
      >
        {isLoading ? 'Processing...' : 'Continue'}
      </button>
    </form>
  );

  const renderGoalsForm = () => (
    <form onSubmit={handleGoalsSubmit} className="space-y-4 bg-white p-6 rounded-lg shadow-sm">
      <div className="flex items-center justify-between">
        <span className="text-sm text-gray-600">You can type or use voice</span>
        <button type="button" onClick={isRecording ? stopRecording : startRecording} className={`flex items-center gap-2 px-3 py-2 rounded-md border ${isRecording ? 'bg-red-50 border-red-300 text-red-700' : 'bg-gray-50 border-gray-300 text-gray-700'}`}>
          <span className={`h-2 w-2 rounded-full ${isRecording ? 'bg-red-600 animate-pulse' : 'bg-gray-400'}`}></span>
          {isRecording ? 'Stop' : 'Speak'}
        </button>
      </div>
      {isTranscribing && <div className="text-sm text-gray-500">Transcribing…</div>}
      {voicePreview.transcript && (
        <div className="p-3 border rounded-md bg-gray-50 text-sm">
          <div className="font-medium mb-1">Transcript</div>
          <div className="mb-2">{voicePreview.transcript}</div>
          {voicePreview.missing?.length > 0 && (
            <div className="text-yellow-700 text-xs mb-2">Missing: {voicePreview.missing.join(', ')}</div>
          )}
          <div className="flex gap-2">
            <button type="button" onClick={acceptVoiceAndSubmit} className="px-3 py-2 bg-blue-600 text-white rounded-md">Use & Continue</button>
            <button type="button" onClick={() => setVoicePreview({ transcript: '', selections: {}, missing: [] })} className="px-3 py-2 bg-white border rounded-md">Discard</button>
          </div>
        </div>
      )}
      <div className="grid grid-cols-2 gap-3">
        {GOALS.map(goal => (
          <label
            key={goal.id}
            className={`flex items-center p-3 border rounded-lg cursor-pointer transition-colors ${formData.goals.includes(goal.id)
              ? 'border-blue-500 bg-blue-50 text-blue-700'
              : 'border-gray-300 hover:border-gray-400'
              }`}
          >
            <input
              type="checkbox"
              checked={formData.goals.includes(goal.id)}
              onChange={() => toggleArrayValue('goals', goal.id)}
              className="sr-only"
            />
            <span className="text-sm font-medium">{goal.label}</span>
          </label>
        ))}
      </div>

      <button
        type="submit"
        disabled={isLoading || formData.goals.length === 0}
        className="w-full bg-blue-600 text-white py-3 px-4 rounded-lg hover:bg-blue-700 disabled:opacity-50"
      >
        {isLoading ? 'Processing...' : 'Continue'}
      </button>
    </form>
  );

  const renderPreferencesForm = () => (
    <form onSubmit={handlePreferencesSubmit} className="space-y-6 bg-white p-6 rounded-lg shadow-sm">
      <div className="flex items-center justify-between">
        <span className="text-sm text-gray-600">You can type or use voice</span>
        <button type="button" onClick={isRecording ? stopRecording : startRecording} className={`flex items-center gap-2 px-3 py-2 rounded-md border ${isRecording ? 'bg-red-50 border-red-300 text-red-700' : 'bg-gray-50 border-gray-300 text-gray-700'}`}>
          <span className={`h-2 w-2 rounded-full ${isRecording ? 'bg-red-600 animate-pulse' : 'bg-gray-400'}`}></span>
          {isRecording ? 'Stop' : 'Speak'}
        </button>
      </div>
      {isTranscribing && <div className="text-sm text-gray-500">Transcribing…</div>}
      {voicePreview.transcript && (
        <div className="p-3 border rounded-md bg-gray-50 text-sm">
          <div className="font-medium mb-1">Transcript</div>
          <div className="mb-2">{voicePreview.transcript}</div>
          {voicePreview.missing?.length > 0 && (
            <div className="text-yellow-700 text-xs mb-2">Missing: {voicePreview.missing.join(', ')}</div>
          )}
          <div className="flex gap-2">
            <button type="button" onClick={acceptVoiceAndSubmit} className="px-3 py-2 bg-blue-600 text-white rounded-md">Use & Continue</button>
            <button type="button" onClick={() => setVoicePreview({ transcript: '', selections: {}, missing: [] })} className="px-3 py-2 bg-white border rounded-md">Discard</button>
          </div>
        </div>
      )}
      <div>
        <h3 className="text-lg font-medium mb-3">Preferred Workout Types</h3>
        <div className="grid grid-cols-2 gap-3">
          {WORKOUT_TYPES.map(type => (
            <label
              key={type.id}
              className={`flex items-center p-3 border rounded-lg cursor-pointer transition-colors ${formData.preferred_workout_types.includes(type.id)
                ? 'border-blue-500 bg-blue-50 text-blue-700'
                : 'border-gray-300 hover:border-gray-400'
                }`}
            >
              <input
                type="checkbox"
                checked={formData.preferred_workout_types.includes(type.id)}
                onChange={() => toggleArrayValue('preferred_workout_types', type.id)}
                className="sr-only"
              />
              <span className="text-sm font-medium">{type.label}</span>
            </label>
          ))}
        </div>
      </div>

      <div>
        <h3 className="text-lg font-medium mb-3">Available Equipment</h3>
        <div className="grid grid-cols-2 gap-3">
          {EQUIPMENT.map(item => (
            <label
              key={item.id}
              className={`flex items-center p-3 border rounded-lg cursor-pointer transition-colors ${formData.equipment.includes(item.id)
                ? 'border-blue-500 bg-blue-50 text-blue-700'
                : 'border-gray-300 hover:border-gray-400'
                }`}
            >
              <input
                type="checkbox"
                checked={formData.equipment.includes(item.id)}
                onChange={() => toggleArrayValue('equipment', item.id)}
                className="sr-only"
              />
              <span className="text-sm font-medium">{item.label}</span>
            </label>
          ))}
        </div>
      </div>

      <div>
        <h3 className="text-lg font-medium mb-3">Preferred Times</h3>
        <div className="flex gap-3">
          {TIMES.map(time => (
            <label
              key={time.id}
              className={`flex items-center p-3 border rounded-lg cursor-pointer transition-colors flex-1 ${formData.preferred_training_times.includes(time.id)
                ? 'border-blue-500 bg-blue-50 text-blue-700'
                : 'border-gray-300 hover:border-gray-400'
                }`}
            >
              <input
                type="checkbox"
                checked={formData.preferred_training_times.includes(time.id)}
                onChange={() => toggleArrayValue('preferred_training_times', time.id)}
                className="sr-only"
              />
              <span className="text-sm font-medium mx-auto">{time.label}</span>
            </label>
          ))}
        </div>
      </div>

      <button
        type="submit"
        disabled={isLoading}
        className="w-full bg-blue-600 text-white py-3 px-4 rounded-lg hover:bg-blue-700 disabled:opacity-50"
      >
        {isLoading ? 'Generating Workout...' : 'Generate My Workout'}
      </button>
    </form>
  );

  const footerRef = useRef(null);
  const [footerHeight, setFooterHeight] = useState(0);

  useEffect(() => {
    if (!footerRef.current) return;
    const ro = new ResizeObserver(entries => {
      const h = entries[0]?.contentRect?.height ?? 0;
      setFooterHeight(h);
    });
    ro.observe(footerRef.current);
    return () => ro.disconnect();
  }, []);

  return (
    <div className="flex flex-col h-full">
      {/* Chat messages */}
      <div className="flex-1 px-4 py-6 overflow-y-auto" style={{ paddingBottom: footerHeight - 24 }}>
        <div className="max-w-3xl mx-auto space-y-6">
          {messages.map((message, index) => (
            <ChatMessage key={index} message={message.text} isUser={message.isUser} />
          ))}
          {isLoading && (
            <div className="flex justify-center py-4">
              <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-blue-600"></div>
            </div>
          )}
          <div ref={messagesEndRef} />
        </div>
      </div>

      {/* Bottom fixed panel */}
      <div ref={footerRef} className="border-t bg-white p-4 fixed bottom-0 left-0 right-0 max-h-[50vh] overflow-y-auto">
        <div className="max-w-3xl mx-auto">
          {stage === 'basic' && renderBasicForm()}
          {stage === 'goals' && renderGoalsForm()}
          {stage === 'final' && renderPreferencesForm()}
        </div>
      </div>
    </div>
  );
};

ChatContainer.propTypes = {
  onWorkoutGenerated: PropTypes.func.isRequired,
};

export default ChatContainer;