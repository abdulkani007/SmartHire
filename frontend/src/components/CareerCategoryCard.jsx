import React from 'react';
import { IconTarget, IconFile, IconCpu } from './Icons';

const CareerCategoryCard = ({ category, filename }) => {
  return (
    <div className="glass-panel mb-8 relative overflow-hidden glow-card-orange">
      {/* Subtle Corner Orange Glow */}
      <div 
        style={{
          position: 'absolute',
          top: '-40px',
          right: '-40px',
          width: '240px',
          height: '240px',
          background: 'radial-gradient(circle, rgba(249, 115, 22, 0.14) 0%, transparent 70%)',
          borderRadius: '50%',
          pointerEvents: 'none'
        }}
      />

      <div className="flex justify-between items-center flex-wrap gap-6 relative" style={{ zIndex: 1 }}>
        <div>
          <div className="flex items-center gap-2 mb-2 flex-wrap">
            <span className="badge badge-orange flex items-center gap-1.5">
              <IconCpu size={12} color="#ea580c" /> FEATURE EXTRACTION & CLASSIFICATION
            </span>
            {filename && (
              <span className="text-xs text-muted font-mono flex items-center gap-1">
                <IconFile size={12} color="var(--accent-orange)" /> {filename}
              </span>
            )}
          </div>

          <h3 className="text-xl font-bold text-primary mb-1">
            Model Classification Insight
          </h3>
          <p className="text-xs text-secondary max-w-xl leading-relaxed">
            Target domain predicted as <strong className="text-orange">{category || 'General Technical Role'}</strong> using TF-IDF n-gram vectorization and Logistic Regression.
          </p>
        </div>

        {/* Clean Frameless Spec Display (No Inner Box Border) */}
        <div className="flex items-center gap-3">
          <div 
            style={{
              width: '46px',
              height: '46px',
              borderRadius: '14px',
              background: 'rgba(249, 115, 22, 0.1)',
              border: '1px solid rgba(249, 115, 22, 0.25)',
              display: 'flex',
              alignItems: 'center',
              justifyContent: 'center',
              flexShrink: 0
            }}
          >
            <IconTarget size={22} color="#f97316" />
          </div>
          <div>
            <div className="text-xs text-muted uppercase tracking-wider font-bold">CLASSIFIER MODEL</div>
            <div className="text-sm text-orange font-mono font-bold">TF-IDF + Logistic Regression</div>
            <div className="text-xs text-emerald font-semibold flex items-center gap-1 mt-0.5">
              <span>●</span> Vector Feature Extraction Active
            </div>
          </div>
        </div>
      </div>

      <div className="mt-4 pt-3 text-secondary text-xs flex items-center justify-between flex-wrap gap-2" style={{ borderTop: '1px solid rgba(15, 23, 42, 0.08)' }}>
        <span>Extracted structural tokens, technical skills, and domain experience from your document.</span>
        <span className="text-xs text-muted font-mono">25 Domain Categories Index</span>
      </div>
    </div>
  );
};

export default CareerCategoryCard;
