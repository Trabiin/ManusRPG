import React, { useState, useEffect } from 'react';
import GameInterface from './GameInterface';
import MobileGameInterface from './MobileGameInterface';

const ResponsiveGameWrapper = () => {
  const [isMobile, setIsMobile] = useState(false);

  useEffect(() => {
    const checkScreenSize = () => {
      setIsMobile(window.innerWidth < 1024);
    };

    checkScreenSize();
    window.addEventListener('resize', checkScreenSize);

    return () => window.removeEventListener('resize', checkScreenSize);
  }, []);

  return (
    <div className="w-full h-screen">
      {isMobile ? <MobileGameInterface /> : <GameInterface />}
    </div>
  );
};

export default ResponsiveGameWrapper;

