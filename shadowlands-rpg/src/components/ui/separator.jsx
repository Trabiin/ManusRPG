import React from 'react';

export const Separator = React.forwardRef(({ 
  className = '', 
  orientation = 'horizontal',
  decorative = true,
  ...props 
}, ref) => {
  const baseClasses = 'shrink-0 bg-border';
  
  const orientationClasses = {
    horizontal: 'h-[1px] w-full',
    vertical: 'h-full w-[1px]'
  };
  
  const combinedClasses = `${baseClasses} ${orientationClasses[orientation]} ${className}`.trim();
  
  return (
    <div
      ref={ref}
      role={decorative ? 'none' : 'separator'}
      aria-orientation={orientation}
      className={combinedClasses}
      {...props}
    />
  );
});

Separator.displayName = 'Separator';

