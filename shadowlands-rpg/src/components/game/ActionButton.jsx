import React from 'react';

const ActionButton = ({ 
  children, 
  onClick, 
  variant = 'default',
  size = 'default',
  disabled = false,
  className = '',
  icon: Icon,
  ...props 
}) => {
  const baseClasses = 'inline-flex items-center justify-center rounded-md font-medium transition-colors focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring focus-visible:ring-offset-2 disabled:pointer-events-none disabled:opacity-50';
  
  const variantClasses = {
    default: 'bg-purple-600 text-white hover:bg-purple-700 focus:bg-purple-700',
    secondary: 'bg-gray-600 text-white hover:bg-gray-700 focus:bg-gray-700',
    outline: 'border border-purple-400 text-purple-300 hover:bg-purple-600 hover:text-white',
    ghost: 'text-purple-300 hover:bg-purple-600/20',
    destructive: 'bg-red-600 text-white hover:bg-red-700 focus:bg-red-700'
  };
  
  const sizeClasses = {
    default: 'h-10 px-4 py-2 text-sm',
    sm: 'h-8 px-3 py-1 text-xs',
    lg: 'h-12 px-6 py-3 text-base',
    icon: 'h-10 w-10'
  };
  
  const combinedClasses = `${baseClasses} ${variantClasses[variant] || variantClasses.default} ${sizeClasses[size] || sizeClasses.default} ${className}`.trim();
  
  return (
    <button
      type="button"
      className={combinedClasses}
      onClick={onClick}
      disabled={disabled}
      {...props}
    >
      {Icon && <Icon className="w-4 h-4 mr-2" />}
      {children}
    </button>
  );
};

export default ActionButton;

