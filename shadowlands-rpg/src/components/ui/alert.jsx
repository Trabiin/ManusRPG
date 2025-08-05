import React from 'react';

// Simple Alert component
export function Alert({ className, variant = 'default', children, ...props }) {
  const baseStyles = {
    position: 'relative',
    width: '100%',
    borderRadius: '0.375rem',
    border: '1px solid',
    padding: '1rem',
    fontSize: '0.875rem'
  };

  const variants = {
    default: {
      backgroundColor: '#1f2937',
      borderColor: '#374151',
      color: '#ffffff'
    },
    destructive: {
      backgroundColor: '#7f1d1d',
      borderColor: '#dc2626',
      color: '#fecaca'
    },
    warning: {
      backgroundColor: '#78350f',
      borderColor: '#f59e0b',
      color: '#fde68a'
    },
    success: {
      backgroundColor: '#14532d',
      borderColor: '#22c55e',
      color: '#bbf7d0'
    }
  };

  const alertStyles = {
    ...baseStyles,
    ...variants[variant]
  };

  return (
    <div
      className={`alert ${className || ''}`}
      style={alertStyles}
      role="alert"
      {...props}
    >
      {children}
    </div>
  );
}

// Alert Title component
export function AlertTitle({ className, children, ...props }) {
  return (
    <h5
      className={`alert-title ${className || ''}`}
      style={{
        marginBottom: '0.25rem',
        fontSize: '1rem',
        fontWeight: '500',
        lineHeight: '1.25',
        margin: 0
      }}
      {...props}
    >
      {children}
    </h5>
  );
}

// Alert Description component
export function AlertDescription({ className, children, ...props }) {
  return (
    <div
      className={`alert-description ${className || ''}`}
      style={{
        fontSize: '0.875rem',
        lineHeight: '1.25'
      }}
      {...props}
    >
      {children}
    </div>
  );
}

