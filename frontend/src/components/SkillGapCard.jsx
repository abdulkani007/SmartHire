import React from 'react';
import { IconCheck, IconArrowRight } from './Icons';

const SkillGapCard = ({ skillGapData }) => {
  if (!skillGapData) {
    return (
      <div className="glass-panel text-center py-6 text-muted">
        No skill gap analysis data available.
      </div>
    );
  }

  const {
    target_category = 'Target Domain',
    matched_skills = [],
    missing_skills = [],
    recommended_skills = [],
    match_percentage = 0,
    total_target_skills = 0
  } = skillGapData;

  const formattedPercentage = typeof match_percentage === 'number' 
    ? match_percentage.toFixed(1) 
    : parseFloat(match_percentage || 0).toFixed(1);

  const skillsToDevelop = recommended_skills.length > 0 ? recommended_skills : missing_skills;

  return (
    <div className="glass-panel mb-8">
      {/* Section Header */}
      <div className="flex justify-between items-center flex-wrap gap-4 mb-6 pb-4" style={{ borderBottom: '1px solid rgba(15, 23, 42, 0.08)' }}>
        <div>
          <span className="badge badge-dark mb-1">Phase 3C Skill Engine</span>
          <h2 className="text-2xl font-bold text-primary">Your Skill Gap Roadmap</h2>
          <p className="text-xs text-secondary mt-1">
            Target skill benchmarks extracted from 148,000+ job postings for <strong className="text-orange">{target_category}</strong>
          </p>
        </div>

        {/* Clean Frameless Circular Progress Indicator (No Inner Box Border) */}
        <div className="flex items-center gap-4">
          <div 
            style={{
              position: 'relative',
              width: '56px',
              height: '56px',
              borderRadius: '50%',
              background: `conic-gradient(var(--accent-orange) ${formattedPercentage}%, rgba(15,23,42,0.08) 0%)`,
              display: 'flex',
              alignItems: 'center',
              justifyContent: 'center',
              boxShadow: '0 0 16px rgba(249, 115, 22, 0.18)',
              flexShrink: 0
            }}
          >
            <div 
              style={{
                width: '44px',
                height: '44px',
                borderRadius: '50%',
                background: '#ffffff',
                display: 'flex',
                alignItems: 'center',
                justifyContent: 'center',
                fontWeight: '800',
                fontSize: '12px',
                color: '#0f172a'
              }}
            >
              {formattedPercentage}%
            </div>
          </div>
          <div>
            <div className="text-xs text-muted uppercase tracking-wider font-semibold">Skill Fit</div>
            <div className="text-sm font-bold text-orange">
              {matched_skills.length} of {total_target_skills || (matched_skills.length + missing_skills.length)} Skills Matched
            </div>
            <div className="text-xs text-amber font-semibold mt-0.5">
              {skillsToDevelop.length} skills to develop
            </div>
          </div>
        </div>
      </div>

      {/* Two Column Layout: YOU HAVE vs DEVELOP NEXT */}
      <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
        {/* Column 1: YOU HAVE (Green Checkmarks) */}
        <div className="p-4 rounded-xl" style={{ background: 'rgba(16, 185, 129, 0.04)', border: '1px solid rgba(16, 185, 129, 0.18)' }}>
          <div className="flex items-center justify-between mb-3.5 pb-2" style={{ borderBottom: '1px solid rgba(16, 185, 129, 0.15)' }}>
            <span className="text-xs font-bold text-emerald tracking-wider uppercase flex items-center gap-1.5">
              <IconCheck size={14} color="#059669" /> YOU HAVE ({matched_skills.length})
            </span>
            <span className="badge badge-green" style={{ fontSize: '10px' }}>Matched</span>
          </div>

          {matched_skills.length === 0 ? (
            <p className="text-xs text-muted py-4 text-center">No exact skill matches detected in resume text.</p>
          ) : (
            <div className="flex flex-wrap gap-2">
              {matched_skills.map((skill, idx) => (
                <span
                  key={idx}
                  style={{
                    display: 'inline-flex',
                    alignItems: 'center',
                    gap: '6px',
                    padding: '6px 14px',
                    borderRadius: '20px',
                    fontSize: '12.5px',
                    fontWeight: '600',
                    background: '#ffffff',
                    color: '#059669',
                    border: '1px solid rgba(16, 185, 129, 0.3)',
                    boxShadow: '0 2px 8px rgba(16, 185, 129, 0.08)'
                  }}
                >
                  <IconCheck size={12} color="#059669" /> {skill}
                </span>
              ))}
            </div>
          )}
        </div>

        {/* Column 2: DEVELOP NEXT (Amber Arrows) */}
        <div className="p-4 rounded-xl" style={{ background: 'rgba(245, 158, 11, 0.04)', border: '1px solid rgba(245, 158, 11, 0.18)' }}>
          <div className="flex items-center justify-between mb-3.5 pb-2" style={{ borderBottom: '1px solid rgba(245, 158, 11, 0.15)' }}>
            <span className="text-xs font-bold text-amber tracking-wider uppercase flex items-center gap-1.5">
              <IconArrowRight size={14} color="#d97706" /> DEVELOP NEXT ({skillsToDevelop.length})
            </span>
            <span className="badge badge-amber" style={{ fontSize: '10px' }}>Skills to Develop</span>
          </div>

          {skillsToDevelop.length === 0 ? (
            <p className="text-xs text-emerald py-4 text-center flex items-center justify-center gap-1.5">
              <IconCheck size={16} color="#10b981" /> Great job! You match all benchmark skills for this category.
            </p>
          ) : (
            <div className="flex flex-wrap gap-2">
              {skillsToDevelop.map((skill, idx) => (
                <span
                  key={idx}
                  style={{
                    display: 'inline-flex',
                    alignItems: 'center',
                    gap: '6px',
                    padding: '6px 14px',
                    borderRadius: '20px',
                    fontSize: '12.5px',
                    fontWeight: '600',
                    background: '#ffffff',
                    color: '#d97706',
                    border: '1px solid rgba(245, 158, 11, 0.3)',
                    boxShadow: '0 2px 8px rgba(245, 158, 11, 0.08)'
                  }}
                >
                  <IconArrowRight size={12} color="#d97706" /> {skill}
                </span>
              ))}
            </div>
          )}
        </div>
      </div>
    </div>
  );
};

export default SkillGapCard;
