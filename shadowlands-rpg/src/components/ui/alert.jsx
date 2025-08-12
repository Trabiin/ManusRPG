import React from 'react';

// Alert variants for different styles
const alertVariants = {
  default: 'bg-background text-foreground border-border',
  destructive: 'border-destructive/50 text-destructive dark:border-destructive [&>svg]:text-destructive',
  warning: 'border-yellow-500/50 text-yellow-600 dark:border-yellow-500 [&>svg]:text-yellow-600',
  success: 'border-green-500/50 text-green-600 dark:border-green-500 [&>svg]:text-green-600',
  info: 'border-blue-500/50 text-blue-600 dark:border-blue-500 [&>svg]:text-blue-600'
};

export const Alert = React.forwardRef(({ 
  className = '', 
  variant = 'default', 
  children, 
  ...props 
}, ref) => {
  const baseClasses = 'relative w-full rounded-lg border p-4 [&>svg~*]:pl-7 [&>svg+div]:translate-y-[-3px] [&>svg]:absolute [&>svg]:left-4 [&>svg]:top-4 [&>svg]:text-foreground';
  
  const variantClasses = alertVariants[variant] || alertVariants.default;
  
  const combinedClasses = `${baseClasses} ${variantClasses} ${className}`.trim();
  
  return (
    <div
      ref={ref}
      role="alert"
      className={combinedClasses}
      {...props}
    >
      {children}
    </div>
  );
});

Alert.displayName = 'Alert';

export const AlertTitle = React.forwardRef(({ 
  className = '', 
  children, 
  ...props 
}, ref) => {
  const baseClasses = 'mb-1 font-medium leading-none tracking-tight';
  const combinedClasses = `${baseClasses} ${className}`.trim();
  
  return (
    <h5
      ref={ref}
      className={combinedClasses}
      {...props}
    >
      {children}
    </h5>
  );
});

AlertTitle.displayName = 'AlertTitle';

export const AlertDescription = React.forwardRef(({ 
  className = '', 
  children, 
  ...props 
}, ref) => {
  const baseClasses = 'text-sm [&_p]:leading-relaxed';
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

AlertDescription.displayName = 'AlertDescription';

