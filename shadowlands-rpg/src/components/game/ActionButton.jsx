import React from 'react';

const ActionButton = ({
  children,
  variant = 'primary',
  size = 'md',
  disabled = false,
  onClick = () => {},
  icon = null,
  corruption = 0,
  className = ''
}) => {
  const corruptionClass = `corruption-level-${Math.floor(corruption / 25)}`;
  
  const sizeClasses = {
    sm: 'px-3 py-1.5 text-sm',
    md: 'px-4 py-2 text-base',
    lg: 'px-6 py-3 text-lg'
  };

  const variantClasses = {
    primary: 'bg-gradient-to-br from-gray-600 to-gray-700 border-gray-500 text-gray-200 hover:from-gray-500 hover:to-gray-600',
    pure: 'bg-gradient-to-br from-yellow-600 to-yellow-700 border-yellow-500 text-gray-900 hover:from-yellow-500 hover:to-yellow-600',
    corrupted: 'bg-gradient-to-br from-red-800 to-red-900 border-red-700 text-gray-200 hover:from-red-700 hover:to-red-800',
    danger: 'bg-gradient-to-br from-red-600 to-red-700 border-red-500 text-gray-200 hover:from-red-500 hover:to-red-600'
  };

  return (
    <button
      className={`
        shadowlands-button
        ${sizeClasses[size]}
        ${variantClasses[variant]}
        ${corruptionClass}
        ${className}
        border-2 rounded-md font-semibold font-secondary
        transition-all duration-200 ease-out
        disabled:opacity-50 disabled:cursor-not-allowed
        flex items-center justify-center gap-2
        relative overflow-hidden
        ${!disabled ? 'hover:shadow-lg active:scale-95' : ''}
      `}
      disabled={disabled}
      onClick={onClick}
    >
      {icon && <span className="flex-shrink-0">{icon}</span>}
      <span>{children}</span>
      
      {/* Corrupted button effect */}
      {variant === 'corrupted' && (
        <div className="absolute inset-0 bg-gradient-to-r from-transparent via-white/10 to-transparent -translate-x-full hover:translate-x-full transition-transform duration-700" />
      )}
    </button>
  );
};

export default ActionButton;

