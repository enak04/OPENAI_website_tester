import React from 'react';

const ThemeCard = ({ themeTitle, themeDescription, mobilePreview, desktopPreview, onSelect }) => {
  return (
    <div
      className="w-full max-w-[360px] pb-4 box-border"
      data-category-name="artsandcrafts"
      onClick={onSelect}
    >
      <div className="mb-2">
        <div className="rounded border border-black overflow-hidden group">
          <a href="#" id="api-call-link" data-title={themeTitle}>
            <div className="relative max-h-80 lg:max-h-96 bg-white overflow-hidden">
              <img
                className="w-full h-auto object-cover"
                alt={`Desktop preview for ${themeTitle} style`}
                src={desktopPreview}
              />
              <img
                className="absolute top-24 bottom-0 right-5 w-36 lg:top-32 lg:w-40 border border-black rounded-lg"
                alt={`Mobile preview for ${themeTitle} style`}
                src={mobilePreview}
              />
            </div>
          </a>
        </div>
        <div className="flex-col mt-3">
          <h4
            className="text-lg font-medium pb-0.5"
            data-theme-name={themeTitle}
          >
            {themeTitle}
          </h4>
          <h5
            className="text-sm font-light text-gray-600"
            data-theme-description={themeTitle}
          >
            {themeDescription}
          </h5>
        </div>
      </div>
    </div>
  );
};

export default ThemeCard;

