import React from 'react';
import ThemeGrid from '../ThemeGrid/ThemeGrid';

const MessageBubble = ({ message, onThemeSelect }) => {
  return (
    <div className="py-4 border-b border-gray-100 last:border-b-0">
      {/* User/AI Label */}
      <div className="flex items-center space-x-2 mb-3">
        <div
          className={`w-6 h-6 rounded-full flex items-center justify-center text-xs font-bold text-white ${
            message.isUser ? 'bg-gray-600' : 'bg-blue-600'
          }`}
        >
          {message.isUser ? 'U' : 'AI'}
        </div>
        <span className="text-sm font-medium text-gray-700">
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
      <div className="ml-8">
        <p className="text-gray-800 text-sm leading-relaxed mb-3">
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
