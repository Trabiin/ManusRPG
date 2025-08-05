import React from 'react';

// Simple Input component
export function Input({ 
  className, 
  type = 'text',
  disabled,
  ...props 
}) {
  const baseStyles = {
    display: 'flex',
    height: '2.5rem',
    width: '100%',
    borderRadius: '0.375rem',
    border: '1px solid #374151',
    backgroundColor: '#1f2937',
    padding: '0.5rem 0.75rem',
    fontSize: '0.875rem',
    color: '#ffffff',
    outline: 'none',
    transition: 'all 0.2s'
  };

  const focusStyles = {
    ':focus': {
      borderColor: '#3b82f6',
      boxShadow: '0 0 0 2px rgba(59, 130, 246, 0.1)'
    }
  };

  const disabledStyles = disabled ? {
    cursor: 'not-allowed',
    opacity: 0.5
  } : {};

  const inputStyles = {
    ...baseStyles,
    ...disabledStyles
  };

  return (
    <input
      type={type}
      className={`input ${className || ''}`}
      style={inputStyles}
      disabled={disabled}
      {...props}
    />
  );
}

