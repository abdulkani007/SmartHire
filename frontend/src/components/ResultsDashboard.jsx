import React from 'react';
import CareerCategoryCard from './CareerCategoryCard';
import SkillGapCard from './SkillGapCard';
import JobRecommendationCard from './JobRecommendationCard';
import { IconChart, IconRefresh, IconTarget, IconZap, IconBriefcase, IconFile } from './Icons';

const ResultsDashboard = ({ analysisResult, onReset }) => {
  if (!analysisResult) return null;

  const {
    filename = 'resume.pdf',
    predicted_category = 'General Category',
    recommendations = [],
    skill_gap = {}
  } = analysisResult;

  const matchPercentage = skill_gap.match_percentage || 0;
  const totalJobsCount = recommendations.length;

  return (
    <div className="w-full my-8">
      {/* Top Banner Header */}
      <div className="glass-panel mb-8 p-6 flex justify-between items-center flex-wrap gap-4 glow-card-orange">
        <div className="flex items-center gap-4">
          <div 
            style={{
              width: '52px',
              height: '52px',
              borderRadius: '16px',
              background: 'linear-gradient(135deg, #f97316, #ea580c)',
              display: 'flex',
              alignItems: 'center',
              justifyContent: 'center',
              boxShadow: '0 0 24px rgba(249, 115, 22, 0.35)'
            }}
          >
            <IconChart size={26} color="#ffffff" />
          </div>
          <div>
            <div className="flex items-center gap-2 mb-1">
              <span className="badge badge-orange">CAREER INTELLIGENCE REPORT</span>
              {filename && (
                <span className="text-xs text-muted font-mono flex items-center gap-1 bg-slate-100 px-2 py-0.5 rounded-md" style={{ background: 'rgba(15, 23, 42, 0.05)' }}>
                  <IconFile size={12} color="var(--accent-orange)" /> {filename}
                </span>
              )}
            </div>
            <h1 className="text-2xl md:text-3xl font-black text-primary">Your Career Intelligence Report</h1>
            <p className="text-xs text-secondary mt-0.5">
              Derived via Phase 3 Classical ML Pipeline over 148,000+ job postings index
            </p>
          </div>
        </div>

        <button
          onClick={onReset}
          className="btn btn-secondary flex items-center gap-1.5"
          style={{ padding: '0.75rem 1.4rem', fontSize: '0.9rem' }}
        >
          <IconRefresh size={16} /> Upload New Resume
        </button>
      </div>

      {/* Top Summary Metrics Cards (3-column layout) */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-6 mb-8">
        {/* Metric 1: Predicted Career */}
        <div className="glass-card flex items-center gap-4" style={{ padding: '1.35rem' }}>
          <div style={{ background: 'rgba(249, 115, 22, 0.1)', padding: '12px', borderRadius: '16px', border: '1px solid rgba(249, 115, 22, 0.25)', display: 'flex', alignItems: 'center', justifyContent: 'center' }}>
            <IconTarget size={26} color="#f97316" />
          </div>
          <div>
            <div className="text-xs text-muted uppercase tracking-wider font-bold">PREDICTED CAREER</div>
            <div className="text-xl font-black text-orange mt-0.5" style={{ wordBreak: 'break-word' }}>{predicted_category}</div>
            <div className="text-xs text-secondary mt-0.5 font-mono">TF-IDF Logistic Regression</div>
          </div>
        </div>

        {/* Metric 2: Skill Match */}
        <div className="glass-card flex items-center gap-4" style={{ padding: '1.35rem' }}>
          <div style={{ background: 'rgba(16, 185, 129, 0.1)', padding: '12px', borderRadius: '16px', border: '1px solid rgba(16, 185, 129, 0.25)', display: 'flex', alignItems: 'center', justifyContent: 'center' }}>
            <IconZap size={26} color="#10b981" />
          </div>
          <div>
            <div className="text-xs text-muted uppercase tracking-wider font-bold">SKILL MATCH FIT</div>
            <div className="text-xl font-black text-emerald mt-0.5">{matchPercentage.toFixed(1)}% Score</div>
            <div className="text-xs text-secondary mt-0.5">
              {skill_gap.matched_skills?.length || 0} matched / {skill_gap.missing_skills?.length || 0} to develop
            </div>
          </div>
        </div>

        {/* Metric 3: Jobs Found */}
        <div className="glass-card flex items-center gap-4" style={{ padding: '1.35rem' }}>
          <div style={{ background: 'rgba(15, 23, 42, 0.08)', padding: '12px', borderRadius: '16px', border: '1px solid rgba(15, 23, 42, 0.18)', display: 'flex', alignItems: 'center', justifyContent: 'center' }}>
            <IconBriefcase size={26} color="#0f172a" />
          </div>
          <div>
            <div className="text-xs text-muted uppercase tracking-wider font-bold">RECOMMENDED JOBS</div>
            <div className="text-xl font-black text-dark mt-0.5">{totalJobsCount} Opportunities</div>
            <div className="text-xs text-secondary mt-0.5 font-mono">Cosine Ranked from 148K+</div>
          </div>
        </div>
      </div>

      {/* Main Results Sections */}
      <CareerCategoryCard category={predicted_category} filename={filename} />
      <SkillGapCard skillGapData={skill_gap} />
      <JobRecommendationCard recommendations={recommendations} />
    </div>
  );
};

export default ResultsDashboard;
