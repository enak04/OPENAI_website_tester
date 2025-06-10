// src/components/WebPreviewPanel/WebPreviewPanel.jsx
import React, { useState } from 'react';
import { FiSmartphone, FiMonitor } from 'react-icons/fi';

const WebPreviewPanel = ({ selectedTheme }) => {
  const [device, setDevice] = useState('laptop'); // 'mobile' or 'laptop'

  // If no theme is selected, show a placeholder message
  // This is to ensure that the preview area is not empty
  if (!selectedTheme) {
    return (
      <div className="flex-1 lg:w-full h-screen bg-gray-100 flex items-center justify-center">
        <p className="text-gray-900">Select a theme to preview</p>
      </div>
    );
  }

  // Determine the preview URL based on the selected theme and device type
  const previewUrl = device === 'mobile' ? `${selectedTheme.URL}?mobile=true` : selectedTheme.URL;
  
  console.log('previewUrl', previewUrl);

  // Dynamic class for iframe based on device type
  const iframeClass =
  device === 'mobile'
    ? 'transition-all duration-1000 w-[375px] h-[667px] border rounded-lg shadow-lg mx-auto my-6'
    : 'transition-all duration-1000 w-full h-full overflow-x-auto border rounded-lg shadow-lg';

  return (
    <div className="flex-1 h-full border-l border-gray-200 flex flex-col">
      {/* Header */}
      <div className="p-1 flex justify-end gap-2">
        <button
          onClick={() => setDevice('mobile')}
          className={`p-2 rounded-md hover:bg-gray-50 ${device === 'mobile' ? 'bg-blue-200' : ''}`}
          title="Mobile View"
        >
          <FiSmartphone className="text-xl" />
        </button>
        <button
          onClick={() => setDevice('laptop')}
          className={`p-2 rounded-md hover:bg-gray-50 ${device === 'laptop' ? 'bg-blue-200' : ''}`}
          title="Laptop View"
        >
          <FiMonitor className="text-xl" />
        </button>
      </div>
      {/* Preview Area */}
      <div className="flex-1 flex items-center justify-center">
        <iframe
          src={previewUrl}
          title="Theme Preview"
          className= {iframeClass + ' m-5 mb-0 overflow-x-hidden'}
          frameBorder="0"
        />
      </div>
    </div>
  );
};

export default WebPreviewPanel;
