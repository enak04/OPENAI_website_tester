import React from 'react';
import ThemeGrid from '../ThemeGrid/ThemeGrid';

const MessageBubble = ({ message, onThemeSelect }) => {
  return (
    <div className={`p-4 m-2 mt-0 ${message.isUser ? 'bg-blue-50 border rounded-2xl border-gray-50' : 'bg-white'}`}>
      {/* User/AI Label */}
      <div className="flex items-center align-middle space-x-2">
        <div
          className={`w-8 h-8 rounded-full flex items-center justify-center text-md font-bold text-white ${
            message.isUser ? 'bg-gray-600' : 'bg-blue-600'
          }`}
        >
          {message.isUser ? 'U' : 'AI'}
        </div>
        <span className="text-base font-medium text-gray-700">
          {message.isUser ? 'You' : 'Shoopy AI'}
        </span>
        <span className="text-xs text-gray-400">
          {new Date(message.timestamp).toLocaleTimeString([], {
            hour: '2-digit',
            minute: '2-digit',
          })}
        </span>
      </div>

      {/* Message Content */}
      <div className="ml-10">
        <p className="text-gray-800 text-base leading-relaxed mb-3">
          {message.content}
        </p>

        {/* Theme Cards (if AI message includes themes) */}
        {message.themes && onThemeSelect && (
          <div className="mt-4">
            <ThemeGrid
              themes={message.themes.themes}
              category={message.themes.category}
              onThemeSelect={onThemeSelect}
            />
          </div>
        )}
      </div>
    </div>
  );
};

export default MessageBubble;
