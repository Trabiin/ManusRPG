import React from 'react';

// Simple Badge component
export function Badge({ className, variant = 'default', children, ...props }) {
  const baseStyles = {
    display: 'inline-flex',
    alignItems: 'center',
    borderRadius: '9999px',
    padding: '0.125rem 0.625rem',
    fontSize: '0.75rem',
    fontWeight: '600',
    lineHeight: '1',
    border: '1px solid transparent',
    transition: 'all 0.2s'
  };

  const variants = {
    default: {
      backgroundColor: '#374151',
      color: '#ffffff'
    },
    secondary: {
      backgroundColor: '#1f2937',
      color: '#d1d5db',
      border: '1px solid #374151'
    },
    destructive: {
      backgroundColor: '#dc2626',
      color: '#ffffff'
    },
    outline: {
      backgroundColor: 'transparent',
      color: '#ffffff',
      border: '1px solid #374151'
    },
    success: {
      backgroundColor: '#16a34a',
      color: '#ffffff'
    },
    warning: {
      backgroundColor: '#ca8a04',
      color: '#ffffff'
    }
  };

  const badgeStyles = {
    ...baseStyles,
    ...variants[variant]
  };

  return (
    <div
      className={`badge ${className || ''}`}
      style={badgeStyles}
      {...props}
    >
      {children}
    </div>
  );
}

