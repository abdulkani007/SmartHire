import React, { useState } from 'react';
import { IconSparkles, IconCheck, IconArrowRight, IconZap } from './Icons';
import logoImg from '../assets/image.png';

const Hero = ({ onAnalyzeClick, onHowItWorksClick }) => {
  const [activeNode, setActiveNode] = useState(null);

  // 6 skill nodes placed around R=150px circle centered at (220, 220)
  const skillNodes = [
    { id: 'aws', name: 'AWS & Kubernetes', x: 220, y: 70, score: '91.0%', target: 'DevOps Lead' },
    { id: 'ml', name: 'Machine Learning', x: 350, y: 145, score: '96.2%', target: 'AI Engineer' },
    { id: 'react', name: 'React & TypeScript', x: 350, y: 295, score: '94.8%', target: 'Frontend Lead' },
    { id: 'nlp', name: 'NLP & LLM Tuning', x: 220, y: 370, score: '95.6%', target: 'AI Researcher' },
    { id: 'sql', name: 'SQL & Data Lakes', x: 90, y: 295, score: '92.5%', target: 'Data Engineer' },
    { id: 'python', name: 'Python & PyTorch', x: 90, y: 145, score: '98.4%', target: 'Data Science' }
  ];

  return (
    <div className="w-full my-6 md:my-14">
      <div className="grid grid-cols-1 md:grid-cols-2 gap-8 md:gap-10 items-center">
        {/* Left Column: Headline & Call To Action */}
        <div>
          <div className="inline-flex items-center gap-2 mb-4">
            <span className="badge badge-orange flex items-center gap-1.5 shadow-sm">
              <IconSparkles size={14} color="#ea580c" />
              <span>AI CAREER INTELLIGENCE ENGINE 2.0</span>
            </span>
          </div>

          <h1 className="text-3xl sm:text-4xl md:text-5xl font-extrabold text-primary mb-4 md:mb-5" style={{ lineHeight: 1.15, letterSpacing: '-0.025em' }}>
            Turn Your Resume Into Your{' '}
            <span className="text-gradient-orange">Career Roadmap.</span>
          </h1>

          <p className="text-secondary text-sm md:text-lg mb-6 md:mb-8 max-w-xl leading-relaxed">
            Upload your resume to instantly extract structural skill vectors, predict your career category, and discover matching opportunities across 148,000+ postings.
          </p>

          {/* Action Buttons */}
          <div className="flex flex-col sm:flex-row flex-wrap gap-3 sm:gap-4 items-center mb-8 md:mb-10">
            <button
              onClick={onAnalyzeClick}
              className="btn btn-primary w-full sm:w-auto"
              style={{ padding: '0.9rem 2.2rem', fontSize: '1rem' }}
            >
              <span>Analyze My Resume</span>
              <IconArrowRight size={18} />
            </button>
            <button
              onClick={onHowItWorksClick}
              className="btn btn-secondary w-full sm:w-auto"
              style={{ padding: '0.9rem 1.8rem', fontSize: '1rem' }}
            >
              Explore How It Works
            </button>
          </div>

          {/* Feature Highlights Grid */}
          <div className="grid grid-cols-1 sm:grid-cols-3 gap-3 sm:gap-4 pt-6" style={{ borderTop: '1px solid rgba(15, 23, 42, 0.08)' }}>
            <div className="flex items-center gap-2 text-xs text-secondary font-semibold">
              <div className="w-5 h-5 rounded-full flex items-center justify-center text-orange flex-shrink-0" style={{ background: 'rgba(249,115,22,0.12)' }}>
                <IconCheck size={12} color="#f97316" />
              </div>
              <span>Classical ML Models</span>
            </div>

            <div className="flex items-center gap-2 text-xs text-secondary font-semibold">
              <div className="w-5 h-5 rounded-full flex items-center justify-center text-dark flex-shrink-0" style={{ background: 'rgba(15,23,42,0.08)' }}>
                <IconCheck size={12} color="#0f172a" />
              </div>
              <span>148K+ Job Index</span>
            </div>

            <div className="flex items-center gap-2 text-xs text-secondary font-semibold">
              <div className="w-5 h-5 rounded-full flex items-center justify-center text-emerald flex-shrink-0" style={{ background: 'rgba(16,185,129,0.12)' }}>
                <IconCheck size={12} color="#10b981" />
              </div>
              <span>Exact Vector Matches</span>
            </div>
          </div>
        </div>

        {/* Right Column: Mobile Responsive Orbital Constellation */}
        <div className="flex justify-center items-center w-full overflow-hidden">
          <div className="constellation-wrapper">
            <div 
              style={{
                position: 'relative',
                width: '440px',
                height: '440px',
                margin: '0 auto',
                userSelect: 'none'
              }}
            >
              {/* Ambient Center Glow */}
              <div 
                style={{
                  position: 'absolute',
                  top: '50%',
                  left: '50%',
                  transform: 'translate(-50%, -50%)',
                  width: '280px',
                  height: '280px',
                  background: 'radial-gradient(circle, rgba(249, 115, 22, 0.22) 0%, rgba(249, 115, 22, 0.04) 60%, transparent 75%)',
                  borderRadius: '50%',
                  pointerEvents: 'none',
                  zIndex: 1
                }}
              />

              {/* Central Stationary SH Engine Node - Z-Index 25 (Direct Center) */}
              <div
                style={{
                  position: 'absolute',
                  top: '50%',
                  left: '50%',
                  transform: 'translate(-50%, -50%)',
                  zIndex: 25,
                  pointerEvents: 'none'
                }}
                className="flex flex-col items-center justify-center"
              >
                <div 
                  style={{
                    width: '74px',
                    height: '74px',
                    borderRadius: '22px',
                    background: '#ffffff',
                    border: '2px solid rgba(249, 115, 22, 0.45)',
                    display: 'flex',
                    alignItems: 'center',
                    justifyContent: 'center',
                    padding: '6px',
                    boxShadow: '0 0 35px rgba(249, 115, 22, 0.38)',
                    animation: 'pulseGlow 3s infinite ease-in-out'
                  }}
                >
                  <img src={logoImg} alt="SH Engine" style={{ width: '100%', height: '100%', objectFit: 'contain' }} />
                </div>
                <span className="badge badge-dark mt-2 shadow-sm" style={{ fontSize: '9px', padding: '2px 8px', letterSpacing: '0.08em' }}>
                  SH CORE
                </span>
              </div>

              {/* Orbit Container Rotating Exactly Around Center (220px, 220px) */}
              <div 
                className="animate-orbit-rotate"
                style={{
                  position: 'absolute',
                  top: 0,
                  left: 0,
                  width: '440px',
                  height: '440px',
                  transformOrigin: '220px 220px',
                  zIndex: 10
                }}
              >
                {/* SVG Vector Signal Lines & Dashed Radar Rings */}
                <svg 
                  width="440" 
                  height="440" 
                  viewBox="0 0 440 440"
                  style={{ position: 'absolute', top: 0, left: 0, pointerEvents: 'none', overflow: 'visible' }}
                >
                  {/* Dashed Radar Orbit Rings Centered at (220, 220) */}
                  <circle cx="220" cy="220" r="75" fill="none" stroke="rgba(249, 115, 22, 0.2)" strokeWidth="1.5" strokeDasharray="4 4" />
                  <circle cx="220" cy="220" r="150" fill="none" stroke="rgba(15, 23, 42, 0.1)" strokeWidth="1.5" strokeDasharray="6 6" />

                  {/* Vector Lines Connecting Center (220, 220) to Node Positions */}
                  {skillNodes.map((node) => {
                    const isActive = activeNode === node.id;
                    return (
                      <line 
                        key={node.id}
                        x1="220" 
                        y1="220" 
                        x2={node.x} 
                        y2={node.y} 
                        stroke={isActive ? '#f97316' : 'rgba(15, 23, 42, 0.14)'} 
                        strokeWidth={isActive ? '3' : '1.5'} 
                        className={isActive ? '' : 'animate-dash-flow'}
                        style={{ filter: isActive ? 'drop-shadow(0 0 6px #f97316)' : 'none' }}
                      />
                    );
                  })}
                </svg>

                {/* Orbiting Skill Node Chips */}
                {skillNodes.map((node) => {
                  const isActive = activeNode === node.id;
                  return (
                    <div
                      key={node.id}
                      onMouseEnter={() => setActiveNode(node.id)}
                      onMouseLeave={() => setActiveNode(null)}
                      style={{
                        position: 'absolute',
                        left: `${node.x}px`,
                        top: `${node.y}px`,
                        transform: 'translate(-50%, -50%)',
                        zIndex: 20,
                        cursor: 'pointer'
                      }}
                    >
                      {/* Counter-Rotating Label Badge (keeps text level & readable as orbit spins) */}
                      <div className="animate-orbit-counter transition-all duration-300">
                        <div
                          style={{
                            padding: '6px 12px',
                            borderRadius: '12px',
                            background: isActive ? '#ffffff' : 'rgba(255, 255, 255, 0.95)',
                            border: `1.5px solid ${isActive ? '#f97316' : 'rgba(15, 23, 42, 0.14)'}`,
                            color: isActive ? '#ea580c' : '#0f172a',
                            fontWeight: '700',
                            fontSize: '11px',
                            display: 'flex',
                            alignItems: 'center',
                            gap: '6px',
                            boxShadow: isActive ? '0 8px 24px rgba(249, 115, 22, 0.32)' : '0 4px 14px rgba(15, 23, 42, 0.08)',
                            transform: isActive ? 'scale(1.15)' : 'scale(1)',
                            whiteSpace: 'nowrap'
                          }}
                        >
                          <span 
                            style={{ 
                              width: '6px', 
                              height: '6px', 
                              borderRadius: '50%', 
                              background: isActive ? '#f97316' : '#10b981' 
                            }} 
                          />
                          {node.name}
                        </div>

                        {/* Vector Match Popover Tooltip */}
                        {isActive && (
                          <div
                            style={{
                              position: 'absolute',
                              bottom: '125%',
                              left: '50%',
                              transform: 'translateX(-50%)',
                              background: '#0f172a',
                              color: '#ffffff',
                              padding: '6px 12px',
                              borderRadius: '8px',
                              fontSize: '10px',
                              whiteSpace: 'nowrap',
                              boxShadow: '0 8px 20px rgba(0, 0, 0, 0.3)',
                              pointerEvents: 'none',
                              zIndex: 40
                            }}
                          >
                            <div className="font-bold text-orange flex items-center gap-1">
                              <IconZap size={10} color="#f97316" /> {node.target} Fit
                            </div>
                            <div className="text-slate-300 font-mono" style={{ fontSize: '9px' }}>Vector Fit: {node.score}</div>
                          </div>
                        )}
                      </div>
                    </div>
                  );
                })}
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default Hero;
