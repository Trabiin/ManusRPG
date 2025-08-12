import React, { createContext, useContext, useState } from 'react';

// Select context for managing state
const SelectContext = createContext();

export function Select({ 
  defaultValue, 
  value: controlledValue, 
  onValueChange, 
  children, 
  ...props 
}) {
  const [internalValue, setInternalValue] = useState(defaultValue || '');
  const [isOpen, setIsOpen] = useState(false);
  
  const isControlled = controlledValue !== undefined;
  const value = isControlled ? controlledValue : internalValue;
  
  const handleValueChange = (newValue) => {
    if (!isControlled) {
      setInternalValue(newValue);
    }
    if (onValueChange) {
      onValueChange(newValue);
    }
    setIsOpen(false);
  };
  
  const contextValue = {
    value,
    onValueChange: handleValueChange,
    isOpen,
    setIsOpen
  };
  
  return (
    <SelectContext.Provider value={contextValue}>
      <div className="relative" {...props}>
        {children}
      </div>
    </SelectContext.Provider>
  );
}

export function SelectTrigger({ 
  className = '', 
  children, 
  ...props 
}) {
  const context = useContext(SelectContext);
  
  if (!context) {
    throw new Error('SelectTrigger must be used within a Select component');
  }
  
  const { isOpen, setIsOpen } = context;
  
  const handleClick = () => {
    setIsOpen(!isOpen);
  };
  
  const baseClasses = 'flex h-10 w-full items-center justify-between rounded-md border border-input bg-background px-3 py-2 text-sm ring-offset-background placeholder:text-muted-foreground focus:outline-none focus:ring-2 focus:ring-ring focus:ring-offset-2 disabled:cursor-not-allowed disabled:opacity-50';
  const combinedClasses = `${baseClasses} ${className}`.trim();
  
  return (
    <button
      type="button"
      role="combobox"
      aria-expanded={isOpen}
      className={combinedClasses}
      onClick={handleClick}
      {...props}
    >
      {children}
      <svg
        className="h-4 w-4 opacity-50"
        fill="none"
        stroke="currentColor"
        viewBox="0 0 24 24"
      >
        <path
          strokeLinecap="round"
          strokeLinejoin="round"
          strokeWidth={2}
          d="M19 9l-7 7-7-7"
        />
      </svg>
    </button>
  );
}

export function SelectValue({ 
  placeholder = 'Select an option...', 
  className = '',
  ...props 
}) {
  const context = useContext(SelectContext);
  
  if (!context) {
    throw new Error('SelectValue must be used within a Select component');
  }
  
  const { value } = context;
  
  return (
    <span className={className} {...props}>
      {value || placeholder}
    </span>
  );
}

export function SelectContent({ 
  className = '', 
  children, 
  ...props 
}) {
  const context = useContext(SelectContext);
  
  if (!context) {
    throw new Error('SelectContent must be used within a Select component');
  }
  
  const { isOpen } = context;
  
  if (!isOpen) {
    return null;
  }
  
  const baseClasses = 'absolute top-full left-0 z-50 w-full mt-1 rounded-md border bg-popover text-popover-foreground shadow-md';
  const combinedClasses = `${baseClasses} ${className}`.trim();
  
  return (
    <div className={combinedClasses} {...props}>
      {children}
    </div>
  );
}

export function SelectItem({ 
  value: itemValue, 
  className = '', 
  children, 
  ...props 
}) {
  const context = useContext(SelectContext);
  
  if (!context) {
    throw new Error('SelectItem must be used within a Select component');
  }
  
  const { value: selectedValue, onValueChange } = context;
  const isSelected = selectedValue === itemValue;
  
  const handleClick = () => {
    if (itemValue !== undefined) {
      onValueChange(itemValue);
    }
  };
  
  const baseClasses = 'relative flex w-full cursor-default select-none items-center rounded-sm py-1.5 pl-8 pr-2 text-sm outline-none hover:bg-accent hover:text-accent-foreground focus:bg-accent focus:text-accent-foreground';
  const selectedClasses = isSelected ? 'bg-accent text-accent-foreground' : '';
  const combinedClasses = `${baseClasses} ${selectedClasses} ${className}`.trim();
  
  return (
    <div
      className={combinedClasses}
      onClick={handleClick}
      {...props}
    >
      {isSelected && (
        <span className="absolute left-2 flex h-3.5 w-3.5 items-center justify-center">
          <svg
            className="h-4 w-4"
            fill="none"
            stroke="currentColor"
            viewBox="0 0 24 24"
          >
            <path
              strokeLinecap="round"
              strokeLinejoin="round"
              strokeWidth={2}
              d="M5 13l4 4L19 7"
            />
          </svg>
        </span>
      )}
      {children}
    </div>
  );
}

