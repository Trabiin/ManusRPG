import React, { createContext, useContext } from 'react';

// Create context for tabs
const TabsContext = createContext();

// Main Tabs component
export function Tabs({ value, onValueChange, className, children, ...props }) {
  return (
    <TabsContext.Provider value={{ value, onValueChange }}>
      <div className={className} {...props}>
        {children}
      </div>
    </TabsContext.Provider>
  );
}

// TabsList component
export function TabsList({ className, children, ...props }) {
  return (
    <div className={className} role="tablist" {...props}>
      {children}
    </div>
  );
}

// TabsTrigger component
export function TabsTrigger({ value, className, children, ...props }) {
  const { value: activeValue, onValueChange } = useContext(TabsContext);
  const isActive = activeValue === value;
  
  return (
    <button
      className={className}
      role="tab"
      aria-selected={isActive}
      data-state={isActive ? 'active' : 'inactive'}
      onClick={() => onValueChange(value)}
      {...props}
    >
      {children}
    </button>
  );
}

// TabsContent component
export function TabsContent({ value, className, children, ...props }) {
  const { value: activeValue } = useContext(TabsContext);
  const isActive = activeValue === value;
  
  if (!isActive) return null;
  
  return (
    <div className={className} role="tabpanel" {...props}>
      {children}
    </div>
  );
}

