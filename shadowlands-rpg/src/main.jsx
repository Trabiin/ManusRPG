import React from 'react'
import ReactDOM from 'react-dom/client'
import App from './App.jsx'
import './App.css'

// Error boundary component for better error handling
class ErrorBoundary extends React.Component {
  constructor(props) {
    super(props);
    this.state = { hasError: false, error: null, errorInfo: null };
  }

  static getDerivedStateFromError(error) {
    return { hasError: true };
  }

  componentDidCatch(error, errorInfo) {
    this.setState({
      error: error,
      errorInfo: errorInfo
    });
    
    // Log error for debugging
    console.error('Shadowlands RPG Error:', error, errorInfo);
  }

  render() {
    if (this.state.hasError) {
      return (
        <div style={{
          minHeight: '100vh',
          display: 'flex',
          alignItems: 'center',
          justifyContent: 'center',
          background: 'linear-gradient(135deg, #1a1a2e 0%, #16213e 50%, #1a1a2e 100%)',
          color: '#9333ea',
          fontFamily: 'Arial, sans-serif',
          textAlign: 'center',
          padding: '20px'
        }}>
          <div>
            <h2 style={{ marginBottom: '20px', fontSize: '24px' }}>
              Something went wrong in Shadowlands
            </h2>
            <p style={{ marginBottom: '20px', color: '#ccc' }}>
              The application encountered an unexpected error.
            </p>
            <button
              onClick={() => window.location.reload()}
              style={{
                background: '#9333ea',
                color: 'white',
                border: 'none',
                padding: '12px 24px',
                borderRadius: '6px',
                cursor: 'pointer',
                fontSize: '16px',
                fontWeight: '600'
              }}
            >
              Reload Game
            </button>
            {process.env.NODE_ENV === 'development' && (
              <details style={{ marginTop: '20px', textAlign: 'left', maxWidth: '600px' }}>
                <summary style={{ cursor: 'pointer', color: '#9333ea' }}>
                  Error Details (Development)
                </summary>
                <pre style={{ 
                  background: '#000', 
                  padding: '10px', 
                  borderRadius: '4px', 
                  overflow: 'auto',
                  fontSize: '12px',
                  color: '#ff6b6b'
                }}>
                  {this.state.error && this.state.error.toString()}
                  {this.state.errorInfo.componentStack}
                </pre>
              </details>
            )}
          </div>
        </div>
      );
    }

    return this.props.children;
  }
}

// Performance monitoring (development only)
if (process.env.NODE_ENV === 'development') {
  // Log render performance
  const observer = new PerformanceObserver((list) => {
    for (const entry of list.getEntries()) {
      if (entry.entryType === 'measure') {
        console.log(`Shadowlands Performance: ${entry.name} took ${entry.duration.toFixed(2)}ms`);
      }
    }
  });
  observer.observe({ entryTypes: ['measure'] });
}

// Initialize React application
const root = ReactDOM.createRoot(document.getElementById('root'));

// Render the app with error boundary
root.render(
  <React.StrictMode>
    <ErrorBoundary>
      <App />
    </ErrorBoundary>
  </React.StrictMode>
);

// Service worker registration for PWA capabilities (optional)
if ('serviceWorker' in navigator && process.env.NODE_ENV === 'production') {
  window.addEventListener('load', () => {
    navigator.serviceWorker.register('/sw.js')
      .then((registration) => {
        console.log('SW registered: ', registration);
      })
      .catch((registrationError) => {
        console.log('SW registration failed: ', registrationError);
      });
  });
}

// Hot module replacement for development
if (import.meta.hot) {
  import.meta.hot.accept('./App.jsx', () => {
    // Re-render the app when App.jsx changes
    root.render(
      <React.StrictMode>
        <ErrorBoundary>
          <App />
        </ErrorBoundary>
      </React.StrictMode>
    );
  });
}

