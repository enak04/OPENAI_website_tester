import React from 'react';
import ThemeCard from '../Card/Card';

const ThemeGrid = ({ themes, category, onThemeSelect }) => {
  return (
    <div className="space-y-3">
      <h4 className="font-medium text-gray-800 text-sm capitalize">
        {category} Themes
      </h4>
      <div className="grid gap-3">
        {themes.map((theme) => (
          <ThemeCard
            key={theme.id}
            themeTitle={theme.title}
            themeDescription={theme.description}
            mobilePreview={theme.mobilePreview}
            desktopPreview={theme.laptopPreview}
            onSelect={() => onThemeSelect(theme)}
          />
        ))}
      </div>
    </div>
  );
};

export default ThemeGrid;
