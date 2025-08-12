// Utility function to combine class names
export function cn(...classes) {
  return classes.filter(Boolean).join(' ');
}

// Utility function to merge class names with conditional logic
export function clsx(...classes) {
  const result = [];
  
  for (const cls of classes) {
    if (!cls) continue;
    
    if (typeof cls === 'string') {
      result.push(cls);
    } else if (typeof cls === 'object') {
      for (const [key, value] of Object.entries(cls)) {
        if (value) {
          result.push(key);
        }
      }
    }
  }
  
  return result.join(' ');
}

