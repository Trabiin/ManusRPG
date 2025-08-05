import React, { createContext, useContext, useState } from 'react';

// Create context for select
const SelectContext = createContext();

// Main Select component
export function Select({ value, onValueChange, children, ...props }) {
  const [isOpen, setIsOpen] = useState(false);
  
  return (
    <SelectContext.Provider value={{ 
      value, 
      onValueChange, 
      isOpen, 
      setIsOpen 
    }}>
      <div className="select-container" style={{ position: 'relative' }} {...props}>
        {children}
      </div>
    </SelectContext.Provider>
  );
}

// SelectTrigger component
export function SelectTrigger({ className, children, ...props }) {
  const { isOpen, setIsOpen } = useContext(SelectContext);
  
  const triggerStyles = {
    display: 'flex',
    height: '2.5rem',
    width: '100%',
    alignItems: 'center',
    justifyContent: 'space-between',
    borderRadius: '0.375rem',
    border: '1px solid #374151',
    backgroundColor: '#1f2937',
    padding: '0.5rem 0.75rem',
    fontSize: '0.875rem',
    color: '#ffffff',
    cursor: 'pointer',
    outline: 'none'
  };

  return (
    <button
      type="button"
      className={`select-trigger ${className || ''}`}
      style={triggerStyles}
      onClick={() => setIsOpen(!isOpen)}
      {...props}
    >
      {children}
      <span style={{ marginLeft: '0.5rem' }}>
        {isOpen ? '▲' : '▼'}
      </span>
    </button>
  );
}

// SelectValue component
export function SelectValue({ placeholder, className, ...props }) {
  const { value } = useContext(SelectContext);
  
  return (
    <span className={`select-value ${className || ''}`} {...props}>
      {value || placeholder}
    </span>
  );
}

// SelectContent component
export function SelectContent({ className, children, ...props }) {
  const { isOpen } = useContext(SelectContext);
  
  if (!isOpen) return null;
  
  const contentStyles = {
    position: 'absolute',
    top: '100%',
    left: 0,
    right: 0,
    zIndex: 50,
    marginTop: '0.25rem',
    backgroundColor: '#1f2937',
    border: '1px solid #374151',
    borderRadius: '0.375rem',
    boxShadow: '0 10px 15px -3px rgba(0, 0, 0, 0.1)',
    maxHeight: '200px',
    overflowY: 'auto'
  };
  
  return (
    <div
      className={`select-content ${className || ''}`}
      style={contentStyles}
      {...props}
    >
      {children}
    </div>
  );
}

// SelectItem component
export function SelectItem({ value, className, children, ...props }) {
  const { onValueChange, setIsOpen } = useContext(SelectContext);
  
  const itemStyles = {
    display: 'flex',
    width: '100%',
    alignItems: 'center',
    padding: '0.5rem 0.75rem',
    fontSize: '0.875rem',
    color: '#ffffff',
    cursor: 'pointer',
    backgroundColor: 'transparent',
    border: 'none',
    textAlign: 'left'
  };
  
  const handleClick = () => {
    onValueChange(value);
    setIsOpen(false);
  };
  
  return (
    <button
      type="button"
      className={`select-item ${className || ''}`}
      style={itemStyles}
      onClick={handleClick}
      onMouseEnter={(e) => e.target.style.backgroundColor = '#374151'}
      onMouseLeave={(e) => e.target.style.backgroundColor = 'transparent'}
      {...props}
    >
      {children}
    </button>
  );
}

