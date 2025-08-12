import React from 'react';

// Card component with dark theme styling for Shadowlands RPG
export const Card = React.forwardRef(({ className = '', children, ...props }, ref) => {
  const baseClasses = 'rounded-lg border shadow-sm bg-gray-800 border-gray-700 text-white';
  const combinedClasses = `${baseClasses} ${className}`.trim();
  
  return (
    <div
      ref={ref}
      className={combinedClasses}
      {...props}
    >
      {children}
    </div>
  );
});

Card.displayName = 'Card';

export const CardHeader = React.forwardRef(({ className = '', children, ...props }, ref) => {
  const baseClasses = 'flex flex-col space-y-1.5 p-6';
  const combinedClasses = `${baseClasses} ${className}`.trim();
  
  return (
    <div
      ref={ref}
      className={combinedClasses}
      {...props}
    >
      {children}
    </div>
  );
});

CardHeader.displayName = 'CardHeader';

export const CardTitle = React.forwardRef(({ className = '', children, ...props }, ref) => {
  const baseClasses = 'text-2xl font-semibold leading-none tracking-tight';
  const combinedClasses = `${baseClasses} ${className}`.trim();
  
  return (
    <h3
      ref={ref}
      className={combinedClasses}
      {...props}
    >
      {children}
    </h3>
  );
});

CardTitle.displayName = 'CardTitle';

export const CardDescription = React.forwardRef(({ className = '', children, ...props }, ref) => {
  const baseClasses = 'text-sm text-gray-400';
  const combinedClasses = `${baseClasses} ${className}`.trim();
  
  return (
    <p
      ref={ref}
      className={combinedClasses}
      {...props}
    >
      {children}
    </p>
  );
});

CardDescription.displayName = 'CardDescription';

export const CardContent = React.forwardRef(({ className = '', children, ...props }, ref) => {
  const baseClasses = 'p-6 pt-0';
  const combinedClasses = `${baseClasses} ${className}`.trim();
  
  return (
    <div
      ref={ref}
      className={combinedClasses}
      {...props}
    >
      {children}
    </div>
  );
});

CardContent.displayName = 'CardContent';

export const CardFooter = React.forwardRef(({ className = '', children, ...props }, ref) => {
  const baseClasses = 'flex items-center p-6 pt-0';
  const combinedClasses = `${baseClasses} ${className}`.trim();
  
  return (
    <div
      ref={ref}
      className={combinedClasses}
      {...props}
    >
      {children}
    </div>
  );
});

CardFooter.displayName = 'CardFooter';

