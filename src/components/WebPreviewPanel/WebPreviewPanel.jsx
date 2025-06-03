// src/components/WebPreviewPanel/WebPreviewPanel.jsx
import React, { useState } from 'react';
import { FiSmartphone, FiMonitor } from 'react-icons/fi';

const WebPreviewPanel = ({ selectedTheme }) => {
  const [device, setDevice] = useState('laptop'); // 'mobile' or 'laptop'

  if (!selectedTheme) {
    return (
      <div className="flex-1 lg:max-w-2/3 h-screen bg-gray-100 flex items-center justify-center">
        <p className="text-gray-500">Select a theme to preview</p>
      </div>
    );
  }

  const previewUrl = device === 'mobile' ? selectedTheme.mobilePreview : selectedTheme.laptopPreview;
  console.log('previewUrl', previewUrl);
  const iframeClass =
    device === 'mobile'
      ? 'w-[375px] h-[667px] border rounded-lg shadow-lg mx-auto my-6'
      : 'w-full h-full overflow-hidden';

  return (
    <div className="flex-1 h-screen border-l border-gray-200 flex flex-col">
      {/* Header */}
      <div className="p-1 border-b border-gray-300 flex justify-end gap-2 bg-white">
        <button
          onClick={() => setDevice('mobile')}
          className={`p-2 rounded-md hover:bg-gray-100 ${device === 'mobile' ? 'bg-gray-200' : ''}`}
          title="Mobile View"
        >
          <FiSmartphone className="text-xl" />
        </button>
        <button
          onClick={() => setDevice('laptop')}
          className={`p-2 rounded-md hover:bg-gray-100 ${device === 'laptop' ? 'bg-gray-200' : ''}`}
          title="Laptop View"
        >
          <FiMonitor className="text-xl" />
        </button>
      </div>
      {/* Preview Area */}
      <div className="flex-1 flex items-center justify-center bg-gray-50">
        <iframe
          src="https://freshgo.store.shoopy.in/"
          title="Theme Preview"
          className= {iframeClass}
          frameBorder="0"
        />
      </div>
    </div>
  );
};

export default WebPreviewPanel;
