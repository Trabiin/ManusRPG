import React from 'react';

const GamePanel = ({ 
  children, 
  title = '',
  variant = 'primary',
  corruption = 0,
  className = '',
  padding = 'md' 
}) => {
  const corruptionClass = `corruption-level-${Math.floor(corruption / 25)}`;
  
  const paddingClasses = {
    sm: 'p-2',
    md: 'p-4',
    lg: 'p-6'
  };

  const variantClasses = {
    primary: 'bg-gradient-to-br from-gray-700 to-gray-800 border-gray-600',
    secondary: 'bg-gradient-to-br from-gray-600 to-gray-700 border-gray-500',
    accent: 'bg-gradient-to-br from-yellow-600/20 to-gray-800 border-yellow-600/50'
  };

  return (
    <div className={`
      shadowlands-panel 
      ${variantClasses[variant]}
      ${paddingClasses[padding]}
      ${corruptionClass}
      ${className}
      border-2 rounded-lg shadow-lg backdrop-blur-sm relative overflow-hidden
    `}>
      {title && (
        <div className="mb-4 pb-2 border-b border-gray-600">
          <h3 className="text-lg font-semibold text-gray-200 font-primary">
            {title}
          </h3>
        </div>
      )}
      {children}
      
      {/* Corruption overlay effect */}
      {corruption > 0 && (
        <div 
          className="absolute inset-0 pointer-events-none"
          style={{
            background: `radial-gradient(circle at 50% 50%, rgba(139, 0, 0, ${corruption / 400}) 0%, transparent 70%)`
          }}
        />
      )}
    </div>
  );
};

export default GamePanel;

