import React from 'react';
import logoImg from '../assets/image.png';

const SHLogoBadge = ({ size = 36, showDot = true, animate = false }) => {
  const outerSize = size;
  const innerSize = Math.round(size * 0.62);

  return (
    <div style={{ display: 'inline-flex', alignItems: 'center', gap: '8px' }}>
      {showDot && (
        <span 
          style={{
            width: '8px',
            height: '8px',
            borderRadius: '50%',
            background: '#f97316',
            boxShadow: '0 0 8px #f97316',
            display: 'inline-block',
            flexShrink: 0
          }}
        />
      )}

      {/* SH Logo with 4 Orbiting Curved Bracket Arcs ( SH ) */}
      <div 
        style={{
          position: 'relative',
          width: `${outerSize}px`,
          height: `${outerSize}px`,
          display: 'flex',
          alignItems: 'center',
          justifyContent: 'center',
          flexShrink: 0
        }}
      >
        {/* 4 Orbiting Bracket Arcs */}
        <svg 
          width={outerSize} 
          height={outerSize} 
          viewBox="0 0 44 44" 
          fill="none" 
          style={{
            position: 'absolute',
            top: 0,
            left: 0,
            width: '100%',
            height: '100%',
            animation: animate ? 'orbit-rotate 20s linear infinite' : 'none'
          }}
        >
          {/* Top Arc */}
          <path d="M 14 7 A 17 17 0 0 1 30 7" stroke="#0f172a" strokeWidth="2.5" strokeLinecap="round" />
          {/* Bottom Arc */}
          <path d="M 14 37 A 17 17 0 0 0 30 37" stroke="#0f172a" strokeWidth="2.5" strokeLinecap="round" />
          {/* Left Arc */}
          <path d="M 7 14 A 17 17 0 0 0 7 30" stroke="#0f172a" strokeWidth="2.5" strokeLinecap="round" />
          {/* Right Arc */}
          <path d="M 37 14 A 17 17 0 0 1 37 30" stroke="#0f172a" strokeWidth="2.5" strokeLinecap="round" />
        </svg>

        {/* Center Circular SH Logo */}
        <div 
          style={{
            width: `${innerSize}px`,
            height: `${innerSize}px`,
            borderRadius: '50%',
            background: '#ffffff',
            display: 'flex',
            alignItems: 'center',
            justifyContent: 'center',
            padding: '3px',
            boxShadow: '0 2px 8px rgba(15, 23, 42, 0.08)'
          }}
        >
          <img src={logoImg} alt="SH Logo" style={{ width: '100%', height: '100%', objectFit: 'contain' }} />
        </div>
      </div>
    </div>
  );
};

export default SHLogoBadge;
