import React, { useState, useEffect } from 'react';
import { IconFile, IconCheck } from './Icons';

const LoadingAnalysis = ({ filename }) => {
  const [activeStep, setActiveStep] = useState(0);

  const steps = [
    { label: 'Reading resume text & parsing content', sub: 'Extracting raw structural tokens' },
    { label: 'Identifying candidate skills & domain features', sub: 'Vectorizing TF-IDF unigram & bigrams' },
    { label: 'Finding matching job opportunities', sub: 'Computing cosine similarity over 148,994 postings' },
    { label: 'Building your career intelligence report', sub: 'Synthesizing skill gap recommendations' }
  ];

  useEffect(() => {
    const timer = setInterval(() => {
      setActiveStep((prev) => (prev < steps.length - 1 ? prev + 1 : prev));
    }, 1200);

    return () => clearInterval(timer);
  }, [steps.length]);

  return (
    <div className="glass-panel max-w-xl mx-auto my-12 text-center relative" style={{ padding: '3rem 2rem' }}>
      <div className="spinner mx-auto mb-6" />

      <h3 className="text-2xl font-extrabold text-primary mb-1">
        Analyzing your resume...
      </h3>
      {filename && (
        <p className="text-xs text-orange font-mono mb-8 font-semibold flex items-center justify-center gap-1.5">
          <IconFile size={14} color="var(--accent-orange)" /> Processing: {filename}
        </p>
      )}

      {/* Sequential Steps List */}
      <div className="space-y-3 text-left max-w-md mx-auto flex flex-col gap-2">
        {steps.map((step, idx) => {
          const isDone = idx < activeStep;
          const isCurrent = idx === activeStep;

          return (
            <div 
              key={idx}
              className="flex items-center gap-3 p-3 rounded-xl transition-all duration-300"
              style={{
                background: isCurrent ? 'rgba(249, 115, 22, 0.08)' : isDone ? 'rgba(16, 185, 129, 0.05)' : 'rgba(15, 23, 42, 0.02)',
                border: `1px solid ${isCurrent ? 'rgba(249, 115, 22, 0.3)' : isDone ? 'rgba(16, 185, 129, 0.25)' : 'rgba(15, 23, 42, 0.06)'}`
              }}
            >
              <div 
                style={{
                  width: '24px',
                  height: '24px',
                  borderRadius: '50%',
                  display: 'flex',
                  alignItems: 'center',
                  justifyContent: 'center',
                  fontSize: '12px',
                  fontWeight: 'bold',
                  background: isDone ? '#10b981' : isCurrent ? '#f97316' : 'rgba(15,23,42,0.1)',
                  color: isDone || isCurrent ? '#ffffff' : 'var(--text-muted)'
                }}
              >
                {isDone ? <IconCheck size={14} color="#ffffff" /> : idx + 1}
              </div>

              <div>
                <div className={`text-sm font-semibold ${isCurrent ? 'text-orange' : isDone ? 'text-emerald' : 'text-muted'}`}>
                  {step.label}
                </div>
                <div className="text-xs text-muted">
                  {step.sub}
                </div>
              </div>
            </div>
          );
        })}
      </div>
    </div>
  );
};

export default LoadingAnalysis;
