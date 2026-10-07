import React from 'react';

const LoadingState = () => {
  return (
    <div className="glass-card" style={{ padding: '3.5rem 2rem', textAlign: 'center', maxWidth: '550px', margin: '2rem auto' }}>
      <div style={{ display: 'flex', justifyContent: 'center', marginBottom: '1.5rem' }}>
        <div className="spinner"></div>
      </div>

      <h3 style={{ fontSize: '1.3rem', fontWeight: '600', color: '#fff', marginBottom: '0.75rem' }}>
        Analyzing your resume...
      </h3>

      <p style={{ color: 'var(--text-muted)', fontSize: '0.95rem', maxWidth: '400px', margin: '0 auto 1.5rem auto' }}>
        Extracting skills, classifying your career domain, and searching 148,000+ job postings for optimal recommendations.
      </p>

      <div style={{
        height: '4px',
        width: '100%',
        background: 'rgba(255, 255, 255, 0.1)',
        borderRadius: '2px',
        overflow: 'hidden',
        position: 'relative'
      }}>
        <div style={{
          position: 'absolute',
          height: '100%',
          width: '50%',
          background: 'linear-gradient(90deg, var(--accent-cyan), var(--accent-purple))',
          borderRadius: '2px',
          animation: 'progressAnim 1.5s ease-in-out infinite'
        }}></div>
      </div>

      <style>{`
        @keyframes progressAnim {
          0% { left: -50%; }
          100% { left: 100%; }
        }
      `}</style>
    </div>
  );
};

export default LoadingState;
