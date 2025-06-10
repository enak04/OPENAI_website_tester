import React, { useState } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
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
      <AnimatePresence mode="wait">
        {/* After chat starts */}
        {started ? (
          <div key="layout" className="flex w-full h-full items-start">
            {/* Chat Panel with animation */}
            <motion.div
              key="chat"
              initial={{ width: '100%' }}
              animate={{ width: showPreview ? '40%' : '100%' }}
              exit={{ width: '100%' }}
              transition={{ duration: 0.6}}
              className="h-full flex justify-center items-end overflow-hidden border-r border-gray-300 bg-white"
            >
              <ChatPanel
                messages={messages}
                isLoading={false}
                onThemeSelect={handleThemeSelect}
                onSend={handleSendMessage}
              />
            </motion.div>

            {/* WebPreview Panel slide in */}
            {showPreview && (
              <motion.div
                key="preview"
                initial={{ x: '100%', opacity: 0 }}
                animate={{ x: 0, opacity: 1 }}
                exit={{ x: '100%', opacity: 0 }}
                transition={{ duration: 0.6 }}
                className="w-2/3 h-full overflow-auto bg-white"
              >
                <WebPreviewPanel selectedTheme={selectedTheme} />
              </motion.div>
            )}
          </div>
        ) : (
          // Initial centered ChatPanel
          <motion.div
            key="initial"
            initial={{ opacity: 1 }}
            animate={{ opacity: 1 }}
            exit={{ opacity: 1 }}
            className="w-full h-full flex"
          >
            <ChatPanel
              messages={messages}
              isLoading={false}
              onThemeSelect={handleThemeSelect}
              onSend={handleSendMessage}
            />
          </motion.div>
        )}
      </AnimatePresence>
    </div>
  );
};

export default App;
