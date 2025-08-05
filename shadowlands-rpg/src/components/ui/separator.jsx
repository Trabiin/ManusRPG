import React from 'react';

// Simple Separator component
export function Separator({ 
  className, 
  orientation = 'horizontal', 
  decorative = true,
  ...props 
}) {
  const baseStyles = {
    flexShrink: 0,
    backgroundColor: '#374151'
  };

  const orientationStyles = {
    horizontal: {
      height: '1px',
      width: '100%'
    },
    vertical: {
      height: '100%',
      width: '1px'
    }
  };

  const separatorStyles = {
    ...baseStyles,
    ...orientationStyles[orientation]
  };

  return (
    <div
      className={`separator ${className || ''}`}
      style={separatorStyles}
      role={decorative ? 'none' : 'separator'}
      aria-orientation={orientation}
      {...props}
    />
  );
}

