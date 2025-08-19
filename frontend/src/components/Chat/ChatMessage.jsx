import React from 'react';
import PropTypes from 'prop-types';

const ChatMessage = ({ message, isUser }) => {
  return (
    <div className={`flex ${isUser ? 'justify-end' : 'justify-start'} mb-3`}>
      <div
        className={`max-w-[72%] p-3 sm:p-4 rounded-2xl shadow-sm border ${
          isUser
            ? 'bg-blue-600 text-white border-blue-600 rounded-br-md'
            : 'bg-white text-gray-800 border-gray-200 rounded-bl-md'
        }`}
      >
        {!isUser && (
          <div className="flex items-center gap-2 mb-1.5">
            <div className="w-7 h-7 sm:w-8 sm:h-8 bg-gradient-to-br from-blue-500 to-purple-500 rounded-full flex items-center justify-center">
              <span className="text-white font-bold text-xs sm:text-sm">M</span>
            </div>
            <span className="font-semibold text-xs sm:text-sm text-gray-700">Mylo</span>
          </div>
        )}
        <div className="whitespace-pre-wrap leading-relaxed text-sm sm:text-base">{message}</div>
      </div>
    </div>
  );
};

ChatMessage.propTypes = {
  message: PropTypes.string.isRequired,
  isUser: PropTypes.bool,
};

export default ChatMessage;
