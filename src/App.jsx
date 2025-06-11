import React, { useState } from 'react';
import ChatPanel from './components/ChatPanel/ChatPanel';
import WebPreviewPanel from './components/WebPreviewPanel/WebPreviewPanel';
import themesData from './data/themes.json';

const App = () => {
  const [started, setStarted] = useState(false);
  const [showPreview, setShowPreview] = useState(false);
  const [messages, setMessages] = useState([
    {
      id: Date.now().toString(),
      content: 'Welcome to Shoopy.AI! How can I assist you today?',
      isUser: false,
      timestamp: new Date(),
    }
  ]);
  const [selectedTheme, setSelectedTheme] = useState(null);

  // Handle user sending a message
  const handleSendMessage = (userMessage) => {
    const userMsg = {
      id: (Date.now() + 1).toString(),
      content: userMessage,
      isUser: true,
      timestamp: new Date(),
    };

    const aiMsg = {
      id: (Date.now() + 2).toString(),
      content: 'Please select the category of your store',
      isUser: false,
      timestamp: new Date(),
      themes: {
        category: 'Select a theme',
        themes: themesData,
      },
    };

    setMessages((prev) => [...prev, userMsg, aiMsg]);
    setStarted(true);
    setShowPreview(true);
  };

  // Handle theme selection
  const handleThemeSelect = (theme) => {
    alert(`Selected theme: ${theme.title}`);
    setSelectedTheme(theme);
    setShowPreview(true);
  };

  return (
    <div className="relative w-screen h-screen overflow-hidden bg-gray-100">
      {/* After chat starts */}
      {started ? (
        <div className="flex w-full h-full items-start">
          {/* Chat Panel */}
          <div
            className={`h-full flex justify-center items-end overflow-hidden border-r border-gray-300 bg-white ${
              showPreview ? 'w-2/5' : 'w-full'
            }`}
          >
            <ChatPanel
              messages={messages}
              isLoading={false}
              onThemeSelect={handleThemeSelect}
              onSend={handleSendMessage}
            />
          </div>

          {/* WebPreview Panel */}
          {showPreview && (
            <div className="w-2/3 h-full overflow-auto bg-white">
              <WebPreviewPanel selectedTheme={selectedTheme} />
            </div>
          )}
        </div>
      ) : (
        // Initial centered ChatPanel
        <div className="w-full h-full flex">
          <ChatPanel
            messages={messages}
            isLoading={false}
            onThemeSelect={handleThemeSelect}
            onSend={handleSendMessage}
          />
        </div>
      )}
    </div>
  );
};

export default App;
