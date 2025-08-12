import React from 'react';

const GamePanel = ({ 
  title, 
  children, 
  className = '',
  variant = 'default',
  ...props 
}) => {
  const baseClasses = 'rounded-lg border shadow-sm';
  
  const variantClasses = {
    default: 'bg-gray-800/50 border-gray-700 text-white',
    dark: 'bg-gray-900/80 border-gray-600 text-gray-100',
    light: 'bg-gray-700/50 border-gray-600 text-gray-200'
  };
  
  const combinedClasses = `${baseClasses} ${variantClasses[variant] || variantClasses.default} ${className}`.trim();
  
  return (
    <div className={combinedClasses} {...props}>
      {title && (
        <div className="px-6 py-4 border-b border-gray-700">
          <h3 className="text-lg font-semibold text-purple-300">{title}</h3>
        </div>
      )}
      <div className="p-6">
        {children}
      </div>
    </div>
  );
};

export default GamePanel;

