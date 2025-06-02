// src/App.jsx
import React, { useState } from 'react';
import PromptInput from './components/PromptInput/PromptInput';
import ChatPanel from './components/ChatPanel/ChatPanel';
import themesData from './data/themes.json';

const App = () => {
  const [started, setStarted] = useState(false);
  const [messages, setMessages] = useState([]);

  const handleSendMessage = (userMessage) => {
    const userMsg = {
      id: Date.now().toString(),
      content: userMessage,
      isUser: true,
      timestamp: new Date()
    };

    const aiMsg = {
      id: (Date.now() + 1).toString(),
      content: 'Here are some themes you can explore based on your input:',
      isUser: false,
      timestamp: new Date(),
      themes: {
        category: 'artsandcrafts',
        themes: themesData
      }
    };

    setMessages(prev => [...prev, userMsg, aiMsg]);
    setStarted(true);
  };


  const handleThemeSelect = (theme) => {
    alert(`Selected theme: ${theme.title}`);
  };

  return (
    <>
      {!started ? (
        <PromptInput onSend={handleSendMessage} />
      ) : (
        <ChatPanel
          messages={messages}
          isLoading={false}
          onThemeSelect={handleThemeSelect}
          onSend={handleSendMessage}
        />
      )}
    </>
  );
};

export default App;
