import React, { useState, useEffect } from 'react';
import SHLogoBadge from './SHLogoBadge';

const SplashScreen = ({ onFinish }) => {
  const [progress, setProgress] = useState(0);
  const [fadeOut, setFadeOut] = useState(false);

  useEffect(() => {
    // Animate progress bar over 1.8 seconds
    const interval = setInterval(() => {
      setProgress((prev) => {
        if (prev >= 100) {
          clearInterval(interval);
          return 100;
        }
        return prev + 5;
      });
    }, 75);

    // Trigger fade out transition at 2.0 seconds
    const timeoutFade = setTimeout(() => {
      setFadeOut(true);
    }, 2000);

    // Complete splash screen at 2.5 seconds
    const timeoutFinish = setTimeout(() => {
      if (onFinish) onFinish();
    }, 2500);

    return () => {
      clearInterval(interval);
      clearTimeout(timeoutFade);
      clearTimeout(timeoutFinish);
    };
  }, [onFinish]);

  return (
    <div
      style={{
        position: 'fixed',
        top: 0,
        left: 0,
        width: '100vw',
        height: '100vh',
        zIndex: 9999,
        background: '#ffffff',
        display: 'flex',
        flexDirection: 'column',
        alignItems: 'center',
        justifyContent: 'center',
        opacity: fadeOut ? 0 : 1,
        transition: 'opacity 0.5s ease-in-out',
        pointerEvents: fadeOut ? 'none' : 'auto'
      }}
    >
      {/* Background Radial Glow */}
      <div
        style={{
          position: 'absolute',
          inset: 0,
          background: 'radial-gradient(circle at 50% 45%, rgba(249, 115, 22, 0.1) 0%, transparent 60%)',
          pointerEvents: 'none'
        }}
      />

      <div className="relative text-center px-4 flex flex-col items-center" style={{ zIndex: 1 }}>
        {/* Prominent "SH" Logo Badge with 4 Orbiting Curved Arcs */}
        <div style={{ marginBottom: '2rem' }}>
          <SHLogoBadge size={90} showDot={true} animate={true} />
        </div>

        <div style={{ fontSize: '1.5rem', fontWeight: '800', color: '#0f172a', marginBottom: '1.5rem' }}>
          Smart<span style={{ color: '#f97316' }}>Hire</span>
        </div>

        {/* Loading Progress Bar Container */}
        <div
          style={{
            width: '240px',
            height: '8px',
            background: '#ffffff',
            border: '2px solid #0f172a',
            borderRadius: '9999px',
            boxShadow: '2px 2px 0px #0f172a',
            margin: '0 auto 1.25rem auto',
            overflow: 'hidden',
            padding: '1px'
          }}
        >
          <div
            style={{
              width: `${progress}%`,
              height: '100%',
              background: '#f97316',
              borderRadius: '9999px',
              transition: 'width 0.1s ease-out'
            }}
          />
        </div>

        <div style={{ fontSize: '0.85rem', color: '#0f172a', fontWeight: '800', letterSpacing: '0.04em' }}>
          Loading Intelligence Engine... {progress}%
        </div>
      </div>
    </div>
  );
};

export default SplashScreen;
