import React from 'react';

// Simple Button component
export function Button({ 
  className, 
  variant = 'default', 
  size = 'default', 
  children, 
  disabled,
  onClick,
  ...props 
}) {
  const baseStyles = {
    display: 'inline-flex',
    alignItems: 'center',
    justifyContent: 'center',
    borderRadius: '0.375rem',
    fontSize: '0.875rem',
    fontWeight: '500',
    border: 'none',
    cursor: disabled ? 'not-allowed' : 'pointer',
    transition: 'all 0.2s',
    textDecoration: 'none'
  };

  const variants = {
    default: {
      backgroundColor: '#3b82f6',
      color: '#ffffff',
      ':hover': {
        backgroundColor: '#2563eb'
      }
    },
    destructive: {
      backgroundColor: '#ef4444',
      color: '#ffffff',
      ':hover': {
        backgroundColor: '#dc2626'
      }
    },
    outline: {
      backgroundColor: 'transparent',
      color: '#ffffff',
      border: '1px solid #374151',
      ':hover': {
        backgroundColor: '#374151'
      }
    },
    secondary: {
      backgroundColor: '#374151',
      color: '#ffffff',
      ':hover': {
        backgroundColor: '#4b5563'
      }
    },
    ghost: {
      backgroundColor: 'transparent',
      color: '#ffffff',
      ':hover': {
        backgroundColor: '#374151'
      }
    }
  };

  const sizes = {
    default: {
      height: '2.5rem',
      padding: '0 1rem'
    },
    sm: {
      height: '2rem',
      padding: '0 0.75rem',
      fontSize: '0.75rem'
    },
    lg: {
      height: '3rem',
      padding: '0 2rem'
    }
  };

  const buttonStyles = {
    ...baseStyles,
    ...variants[variant],
    ...sizes[size],
    opacity: disabled ? 0.5 : 1
  };

  return (
    <button
      className={`button ${className || ''}`}
      style={buttonStyles}
      disabled={disabled}
      onClick={onClick}
      {...props}
    >
      {children}
    </button>
  );
}

