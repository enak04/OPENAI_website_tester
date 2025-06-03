// src/App.jsx
import React, { useState } from 'react';
import PromptInput from './components/PromptInput/PromptInput';
import ChatPanel from './components/ChatPanel/ChatPanel';
import themesData from './data/themes.json';
import WebPreviewPanel from './components/WebPreviewPanel/WebPreviewPanel';


const App = () => {
  const [started, setStarted] = useState(false);
  const [messages, setMessages] = useState([]);
  const [selectedTheme, setSelectedTheme] = useState(null); // NEW STATE


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
    setSelectedTheme(theme);
  };

  if(started && messages.length > 0) {
    console.log('started', started);
    console.log('messages', messages);
    console.log('selectedTheme', selectedTheme);
    return(
      <div className='flex h-screen'>
          <ChatPanel
          messages={messages}
          isLoading={false}
          onThemeSelect={handleThemeSelect}
          onSend={handleSendMessage}
        />
        <WebPreviewPanel
          selectedTheme={selectedTheme}
        />
      </div>
    )
  }

  return (
    <>
      <PromptInput onSend={handleSendMessage} />
    </>
  );
};

export default App;
