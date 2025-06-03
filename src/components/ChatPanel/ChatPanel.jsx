import React, { useState } from 'react';
import MessageBubble from '../MessageBubble/MessageBubble';
import { FiPaperclip, FiSend } from 'react-icons/fi';

const ChatPanel = ({ messages, isLoading, onThemeSelect, onSend }) => {
  const [inputValue, setInputValue] = useState('');

  const handleSend = () => {
    if (!inputValue.trim()) return;
    onSend(inputValue); // Call parent function
    setInputValue('');
  };

  console.log(messages);
  return (
    <div className="lg:max-w-1/3 h-screen bg-white border-r border-gray-200 flex flex-col animate-in slide-in-from-left duration-500">
      {/* Header */}
      <div className="p-2 border-b border-gray-200 bg-gradient-to-r from-blue-50 to-indigo-50">
        <h2 className="text-lg font-bold text-gray-800">Chat with Shoopy.AI</h2>
      </div>

      {/* Messages */}
      <div className="flex-1 overflow-y-auto px-6">
        {messages.map((message) => (
          <MessageBubble
            key={message.id}
            message={message}
            onThemeSelect={onThemeSelect}
          />
        ))}

        {isLoading && (
          <div className="py-4 border-b border-gray-100">
            <div className="flex items-center space-x-2 mb-3">
              <div className="w-6 h-6 rounded-full flex items-center justify-center text-xs font-bold text-white bg-blue-600">
                AI
              </div>
              <span className="text-sm font-medium text-gray-700">Shoopy AI</span>
            </div>
            <div className="ml-8">
              <div className="flex space-x-1">
                <div className="w-2 h-2 bg-gray-400 rounded-full animate-bounce"></div>
                <div className="w-2 h-2 bg-gray-400 rounded-full animate-bounce" style={{ animationDelay: '0.1s' }}></div>
                <div className="w-2 h-2 bg-gray-400 rounded-full animate-bounce" style={{ animationDelay: '0.2s' }}></div>
              </div>
            </div>
          </div>
        )}
      </div>

      {/* Input Area */}
      <div className="relative">
        {/* Gradient Background Behind Input */}
        <div
          className="pointer-events-none flex absolute inset-x-0 bottom-0 h-16 bg-gradient-to-t from-white to-white/0"
          style={{ zIndex: 0 }}
        />
        </div>
        {/* Input Box */}
        <div className="p-1 rounded-xl m-1 border border-gray-300 bg-gray-50 bg-gradient-to-b from-white to-gray-100">
          <div className="flex-col space-x-3 w-full">
            <input
              type="text"
              value={inputValue}
              onChange={(e) => setInputValue(e.target.value)}
              onKeyDown={(e) => {
                if (e.key === 'Enter' && e.shiftKey) {
                  e.preventDefault(); // prevent newline
                  handleSend();
                }
              }}
              placeholder="Continue the conversation..."
              className="flex-1 p-1.5 w-full focus:outline-none"
            />
            <div className="flex p-1 justify-between items-center gap-2 sm:gap-3">
              <button
                type="button"
                className="p-2 sm:p-2.5 rounded-lg sm:rounded-xl border border-gray-200 bg-white hover:bg-gray-100 transition"
              >
                <FiPaperclip className="text-gray-600 text-lg sm:text-xs" />
              </button>
              <button
                onClick={handleSend}
                className="p-2 sm:p-2.5 rounded-lg sm:rounded-xl bg-blue-500 hover:bg-blue-600 transition"
              >
                <FiSend className="text-white text-lg sm:text-xs" />
              </button>
            </div>
          </div>

        </div>
    </div>
  );
};

export default ChatPanel;

