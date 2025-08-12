import React, { createContext, useContext, useState } from 'react';

// Utility function to combine class names
const cn = (...classes) => classes.filter(Boolean).join(' ');

// Tabs context for managing state
const TabsContext = createContext();

export function Tabs({ 
  defaultValue, 
  value: controlledValue, 
  onValueChange, 
  className = '', 
  children, 
  ...props 
}) {
  const [internalValue, setInternalValue] = useState(defaultValue || '');
  
  const isControlled = controlledValue !== undefined;
  const value = isControlled ? controlledValue : internalValue;
  
  const handleValueChange = (newValue) => {
    if (!isControlled) {
      setInternalValue(newValue);
    }
    if (onValueChange) {
      onValueChange(newValue);
    }
  };
  
  const contextValue = {
    value,
    onValueChange: handleValueChange
  };
  
  return (
    <TabsContext.Provider value={contextValue}>
      <div
        className={cn("flex flex-col gap-2", className)}
        {...props}
      >
        {children}
      </div>
    </TabsContext.Provider>
  );
}

export function TabsList({ className = '', children, ...props }) {
  return (
    <div
      className={cn(
        "bg-muted text-muted-foreground inline-flex h-9 w-fit items-center justify-center rounded-lg p-[3px]",
        className
      )}
      role="tablist"
      {...props}
    >
      {children}
    </div>
  );
}

export function TabsTrigger({ 
  value: triggerValue, 
  className = '', 
  children, 
  disabled = false,
  ...props 
}) {
  const context = useContext(TabsContext);
  
  if (!context) {
    throw new Error('TabsTrigger must be used within a Tabs component');
  }
  
  const { value: currentValue, onValueChange } = context;
  const isActive = currentValue === triggerValue;
  
  const handleClick = () => {
    if (!disabled && triggerValue !== undefined) {
      onValueChange(triggerValue);
    }
  };
  
  const handleKeyDown = (e) => {
    if (e.key === 'Enter' || e.key === ' ') {
      e.preventDefault();
      handleClick();
    }
  };
  
  return (
    <button
      type="button"
      role="tab"
      aria-selected={isActive}
      aria-controls={`tabpanel-${triggerValue}`}
      tabIndex={isActive ? 0 : -1}
      disabled={disabled}
      onClick={handleClick}
      onKeyDown={handleKeyDown}
      className={cn(
        "inline-flex h-[calc(100%-1px)] flex-1 items-center justify-center gap-1.5 rounded-md border border-transparent px-2 py-1 text-sm font-medium whitespace-nowrap transition-[color,box-shadow] focus-visible:ring-[3px] focus-visible:outline-1 disabled:pointer-events-none disabled:opacity-50",
        isActive 
          ? "bg-background text-foreground shadow-sm" 
          : "text-foreground hover:bg-accent hover:text-accent-foreground",
        className
      )}
      {...props}
    >
      {children}
    </button>
  );
}

export function TabsContent({ 
  value: contentValue, 
  className = '', 
  children, 
  ...props 
}) {
  const context = useContext(TabsContext);
  
  if (!context) {
    throw new Error('TabsContent must be used within a Tabs component');
  }
  
  const { value: currentValue } = context;
  const isActive = currentValue === contentValue;
  
  if (!isActive) {
    return null;
  }
  
  return (
    <div
      role="tabpanel"
      id={`tabpanel-${contentValue}`}
      aria-labelledby={`tab-${contentValue}`}
      className={cn("flex-1 outline-none", className)}
      {...props}
    >
      {children}
    </div>
  );
}

