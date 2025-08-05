import React from 'react';

// Simple Card component
export function Card({ className, children, ...props }) {
  return (
    <div 
      className={`card ${className || ''}`}
      style={{
        backgroundColor: '#1f2937',
        border: '1px solid #374151',
        borderRadius: '0.5rem',
        padding: '1rem',
        ...props.style
      }}
      {...props}
    >
      {children}
    </div>
  );
}

// Card Header component
export function CardHeader({ className, children, ...props }) {
  return (
    <div 
      className={`card-header ${className || ''}`}
      style={{
        marginBottom: '1rem',
        paddingBottom: '0.5rem',
        borderBottom: '1px solid #374151'
      }}
      {...props}
    >
      {children}
    </div>
  );
}

// Card Title component
export function CardTitle({ className, children, ...props }) {
  return (
    <h3 
      className={`card-title ${className || ''}`}
      style={{
        fontSize: '1.25rem',
        fontWeight: '600',
        color: '#ffffff',
        margin: 0
      }}
      {...props}
    >
      {children}
    </h3>
  );
}

// Card Content component
export function CardContent({ className, children, ...props }) {
  return (
    <div 
      className={`card-content ${className || ''}`}
      {...props}
    >
      {children}
    </div>
  );
}

