import React, { useState, useEffect } from 'react';
import logoImg from '../assets/image.png';

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
        {/* Prominent "SH" Logo Card */}
        <div
          style={{
            width: '160px',
            height: '160px',
            margin: '0 auto 2.5rem auto',
            borderRadius: '28px',
            background: '#ffffff',
            padding: '16px',
            boxShadow: '0 25px 50px rgba(249, 115, 22, 0.18)',
            border: '1px solid rgba(249, 115, 22, 0.25)',
            display: 'flex',
            alignItems: 'center',
            justifyContent: 'center',
            animation: 'pulseGlow 2s infinite ease-in-out'
          }}
        >
          <img
            src={logoImg}
            alt="SH Logo"
            style={{ width: '100%', height: '100%', objectFit: 'contain' }}
          />
        </div>

        {/* Loading Progress Bar Container */}
        <div
          style={{
            width: '240px',
            height: '6px',
            background: 'rgba(15, 23, 42, 0.08)',
            borderRadius: '10px',
            margin: '0 auto 1.25rem auto',
            overflow: 'hidden',
            position: 'relative'
          }}
        >
          <div
            style={{
              width: `${progress}%`,
              height: '100%',
              background: 'linear-gradient(90deg, #f97316, #ea580c)',
              borderRadius: '10px',
              transition: 'width 0.1s ease-out'
            }}
          />
        </div>

        <div style={{ fontSize: '0.825rem', color: '#64748b', fontWeight: '600', letterSpacing: '0.04em' }}>
          Loading Engine... {progress}%
        </div>
      </div>
    </div>
  );
};

export default SplashScreen;
