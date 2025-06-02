// src/components/PromptInput.jsx
import { useState } from 'react';
import TextareaAutosize from 'react-textarea-autosize';
import { FiSend, FiPaperclip } from 'react-icons/fi';

const PromptInput = ({ onSend }) => {
  const [message, setMessage] = useState('');

  const handleClick = () => {
    if (!message.trim()) return;
    onSend(message); // Call parent function
    setMessage('');
  };

  return (
    <div className="h-[100vh] flex flex-col items-center justify-center px-4 sm:px-6 md:px-12 bg-[radial-gradient(circle_at_0.5px_0.5px,_#000_0.5px,_transparent_0)] bg-[length:16px_16px]">
      <div className="mb-2 text-center">
        <h1 className="text-3xl sm:text-4xl md:text-5xl font-bold tracking-wide text-blue-500">
          Shoopy.AI
        </h1>
      </div>

      <div className="mb-6 text-center max-w-md sm:max-w-xl">
        <h1 className="text-sm sm:text-base md:text-lg text-gray-700 font-medium leading-relaxed">
          Want to build a website? Try out our new Shoopy.AI to build a functional website in seconds.
        </h1>
      </div>

      <div className="w-full max-w-3xl lg:max-w-3xl sm:max-w-xl relative bg-white rounded-2xl sm:rounded-3xl border border-gray-200 p-3 sm:p-5 shadow-lg">
        <TextareaAutosize
          value={message}
          onChange={(e) => setMessage(e.target.value)}
          onKeyDown={(e) => {
          if (e.key === 'Enter' && e.shiftKey) {
            e.preventDefault(); // prevent newline
            handleClick();
            }
          }}
          placeholder="Ask anything..."
          minRows={1}
          maxRows={12}
          className="w-full text-sm sm:text-base outline-none resize-none overflow-y-auto mb-3 sm:mb-4 font-[Noto_Sans_Mono,monospace]"
        />

        <div className="flex justify-between items-center gap-2 sm:gap-3">
          <button
            type="button"
            className="p-2 sm:p-2.5 rounded-lg sm:rounded-xl border border-gray-200 bg-white hover:bg-gray-100 transition"
          >
            <FiPaperclip className="text-gray-600 text-lg sm:text-xl" />
          </button>

          <button
            type="button"
            onClick={handleClick}
            className="p-2 sm:p-2.5 rounded-lg sm:rounded-xl bg-blue-500 hover:bg-blue-600 transition"
          >
            <FiSend className="text-white text-lg sm:text-xl" />
          </button>
        </div>
      </div>
    </div>
  );
};

export default PromptInput;
