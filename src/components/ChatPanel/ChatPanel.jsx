import React, { useState, useRef, useEffect  } from 'react';
import MessageBubble from '../MessageBubble/MessageBubble';
import { FiPaperclip, FiSend } from 'react-icons/fi';
import { FaArrowDown } from 'react-icons/fa';
import TextareaAutosize from 'react-textarea-autosize';

const ChatPanel = ({ messages, isLoading, onThemeSelect, onSend }) => {
  const [inputValue, setInputValue] = useState('');
  const messagesEndRef = useRef(null);

  const handleSend = () => {
    if (!inputValue.trim()) return;
    onSend(inputValue); // Call parent function
    setInputValue('');
  };

  // Scroll to bottom when messages change
  useEffect(() => {
  messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, [messages]);



  console.log(messages);
  return (
    <div className="w-screen h-[100vh] flex flex-col items-start justify-center bg-[radial-gradient(#e5e7eb_1px,transparent_1px)] [background-size:16px_16px]">
    <div className="h-screen lg:w-xl sm:w-sm bg-white border border-black rounded-t-md flex flex-col">
      {/* Header */}
      {/* MacOS Style Header */}
      <div className="flex items-center justify-between px-3 py-1 mb-3 bg-gray-200 border-b border-gray-300 rounded-t-md">
        <div className="flex-1 text-start">
          <h2 className="text-base font-semibold text-gray-600 font-[Noto_Sans_Mono,monospace]">
            Chat with Shoopy.AI
          </h2>
        </div>
      </div>



      {/* Messages */}
      <div className="flex-1 overflow-y-auto no-scrollbar">
        {messages.map((message) => (
          <MessageBubble
            key={message.id}
            message={message}
            onThemeSelect={onThemeSelect}
          />
        ))}
        <div ref={messagesEndRef} /> {/* Scroll target */}
        {/* Loading Indicator */} 
        {isLoading && (
          <div className="py-4 px-6">
            <div className="flex items-center space-x-2 mb-3">
              <div className="w-8 h-8 rounded-full flex items-center justify-center text-xs font-bold text-white bg-blue-600">
                AI
              </div>
              <span className="text-base font-medium text-gray-700">Shoopy AI</span>
            </div>
            <div className="ml-10">
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
          className="flex absolute inset-x-0 bottom-0 h-16 bg-gradient-to-t from-white to-white/0"
          style={{ zIndex: 0 }}
        />
        {/*Drop Down Arrow*/}
        <div className="absolute inset-x-0 bottom-0 h-16 flex items-center justify-center">
          <button
            onClick={() => messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' })}
            className="p-2 rounded-full bg-white hover:bg-gray-50 text-black border border-gray-300 shadow-md transition"
          >
            <FaArrowDown/>
          </button>
        </div>
        </div>
        {/* Input Box */}
        <div className="p-1 rounded-xl mx-6 mb-2 border border-gray-300 bg-gradient-to-b fromwhite/0 to-gray-100 shadow-md flex items-center justify-between space-x-2" style={{ zIndex: 1 }}>
          <div className="flex-col space-x-3 w-full">
            <TextareaAutosize
              minRows={1}
              maxRows={3}
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
    </div>
  );
};

export default ChatPanel;

