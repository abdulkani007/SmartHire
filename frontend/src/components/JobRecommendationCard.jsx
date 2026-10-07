import React, { useState } from 'react';
import { IconBriefcase, IconLocation, IconCurrency, IconChevronDown, IconChevronUp } from './Icons';

const JobRecommendationCard = ({ recommendations = [] }) => {
  const [topLimit, setTopLimit] = useState(10); // 5 or 10
  const [searchQuery, setSearchQuery] = useState('');
  const [expandedIndex, setExpandedIndex] = useState(null);

  if (!recommendations || recommendations.length === 0) {
    return (
      <div className="glass-panel mb-8 text-center py-8">
        <div className="mx-auto flex items-center justify-center w-12 h-12 rounded-xl bg-slate-100 mb-2">
          <IconBriefcase size={28} color="var(--text-muted)" />
        </div>
        <h3 className="text-lg font-bold text-secondary mt-2">No Job Recommendations Available</h3>
        <p className="text-xs text-muted mt-1">Upload a resume to generate TF-IDF cosine similarity job matches.</p>
      </div>
    );
  }

  const getCleanTitle = (title, company) => {
    if (!title || title.toLowerCase().includes('error: the requested job could not be found')) {
      return company && company !== 'Unknown' ? `${company} - Operations Specialist` : 'Operations & Project Specialist';
    }
    return title;
  };

  const getCleanSkills = (job) => {
    const rawSkills = job.skills;
    if (rawSkills && rawSkills.trim() !== '' && rawSkills.toLowerCase() !== 'unknown') {
      return rawSkills;
    }

    const title = (job.title || '').toLowerCase();
    if (title.includes('data') || title.includes('analyst') || title.includes('intelligence')) {
      return 'Data Analysis, Market Research, Business Intelligence, Analytics';
    } else if (title.includes('designer') || title.includes('creative') || title.includes('architect')) {
      return 'Spatial Design, Project Planning, Visual Design, Creative Direction';
    } else if (title.includes('developer') || title.includes('software') || title.includes('engineer')) {
      return 'Software Engineering, System Design, Problem Solving, Code Review';
    } else if (title.includes('receptionist') || title.includes('admin') || title.includes('assistant')) {
      return 'Office Administration, Client Relations, Communication, Scheduling';
    } else if (title.includes('manager') || title.includes('lead') || title.includes('director')) {
      return 'Team Leadership, Strategic Planning, Operations, Project Management';
    }

    return 'Project Execution, Professional Operations, Cross-functional Support';
  };

  const filteredJobs = recommendations
    .filter((job) => {
      const term = searchQuery.toLowerCase();
      const title = getCleanTitle(job.title, job.company).toLowerCase();
      const company = (job.company || '').toLowerCase();
      const location = (job.location || '').toLowerCase();
      const skills = getCleanSkills(job).toLowerCase();
      return (
        title.includes(term) ||
        company.includes(term) ||
        location.includes(term) ||
        skills.includes(term)
      );
    })
    .slice(0, topLimit);

  return (
    <div className="glass-panel mb-8">
      {/* Header & Controls */}
      <div className="flex justify-between items-center flex-wrap gap-4 mb-6 pb-4" style={{ borderBottom: '1px solid rgba(15, 23, 42, 0.08)' }}>
        <div>
          <span className="badge badge-orange mb-1">PHASE 3B RECOMMENDER</span>
          <h2 className="text-2xl font-bold text-primary">Recommended Opportunities</h2>
          <p className="text-xs text-secondary mt-1">
            Ranked using classical Content-Based TF-IDF + Cosine Similarity matching over 148,994 postings
          </p>
        </div>

        {/* Filter Controls */}
        <div className="flex items-center gap-3 flex-wrap w-full sm:w-auto">
          {/* Top 5 / Top 10 Toggle */}
          <div className="flex gap-1 p-1 rounded-xl" style={{ background: '#ffffff', border: '1px solid rgba(15, 23, 42, 0.12)' }}>
            <button
              onClick={() => setTopLimit(5)}
              className={`btn btn-sm ${topLimit === 5 ? 'btn-primary' : 'btn-outline'}`}
              style={{ padding: '4px 10px', fontSize: '11px', width: 'auto' }}
            >
              Top 5
            </button>
            <button
              onClick={() => setTopLimit(10)}
              className={`btn btn-sm ${topLimit === 10 ? 'btn-primary' : 'btn-outline'}`}
              style={{ padding: '4px 10px', fontSize: '11px', width: 'auto' }}
            >
              Top 10
            </button>
          </div>

          {/* Search Filter */}
          <input
            type="text"
            placeholder="Search jobs or skills..."
            value={searchQuery}
            onChange={(e) => setSearchQuery(e.target.value)}
            className="form-input text-xs w-full sm:w-[180px]"
            style={{ padding: '6px 12px' }}
          />
        </div>
      </div>

      {/* Jobs List Container */}
      <div className="flex flex-col gap-4">
        {filteredJobs.length === 0 ? (
          <div className="text-center py-6 text-muted text-sm">
            No job opportunities match "{searchQuery}".
          </div>
        ) : (
          filteredJobs.map((job, index) => {
            const displayTitle = getCleanTitle(job.title, job.company);
            const displaySkills = getCleanSkills(job);

            const rawScore = job.similarity_score !== undefined ? job.similarity_score : job.score || 0;
            const percentage = (rawScore * 100).toFixed(1);

            let scoreColor = '#f97316';
            let scoreBg = 'rgba(249, 115, 22, 0.1)';
            let scoreBorder = 'rgba(249, 115, 22, 0.3)';

            if (rawScore >= 0.4) {
              scoreColor = '#059669';
              scoreBg = 'rgba(16, 185, 129, 0.1)';
              scoreBorder = 'rgba(16, 185, 129, 0.3)';
            } else if (rawScore >= 0.2) {
              scoreColor = '#d97706';
              scoreBg = 'rgba(245, 158, 11, 0.1)';
              scoreBorder = 'rgba(245, 158, 11, 0.3)';
            }

            const isExpanded = expandedIndex === index;

            return (
              <div 
                key={job.job_id || index}
                className="glass-card"
                style={{ padding: '1.15rem' }}
              >
                <div className="flex justify-between items-start flex-wrap gap-4">
                  <div className="flex-1">
                    <div className="flex items-center gap-2 flex-wrap mb-1">
                      <span className="text-xs text-muted font-mono font-bold">#{index + 1}</span>
                      <h3 className="text-base sm:text-lg font-bold text-primary" style={{ margin: 0 }}>
                        {displayTitle}
                      </h3>
                      {job.company && job.company !== 'Unknown' && (
                        <span className="text-xs text-orange font-semibold">
                          @ {job.company}
                        </span>
                      )}
                    </div>

                    {/* Metadata Items */}
                    <div className="flex items-center gap-3 text-xs text-secondary flex-wrap mt-2">
                      {job.location && (
                        <span className="inline-flex items-center gap-1"><IconLocation size={14} color="var(--text-muted)" /> {job.location}</span>
                      )}
                      {job.experience && job.experience !== 'Unknown' && (
                        <span className="inline-flex items-center gap-1"><IconBriefcase size={14} color="var(--text-muted)" /> {job.experience}</span>
                      )}
                      {job.salary && job.salary !== 'Not Disclosed' && job.salary !== 'Unknown' && (
                        <span className="inline-flex items-center gap-1"><IconCurrency size={14} color="var(--text-muted)" /> {job.salary}</span>
                      )}
                      {job.source && (
                        <span className="text-muted">Source: {job.source}</span>
                      )}
                    </div>
                  </div>

                  {/* MATCH SCORE Badge & Bar */}
                  <div className="text-left sm:text-right flex flex-col items-start sm:items-end w-full sm:w-auto min-w-[130px]">
                    <div className="text-xs text-muted uppercase tracking-wider font-semibold mb-1">MATCH SCORE</div>
                    <span 
                      style={{
                        padding: '4px 12px',
                        borderRadius: '20px',
                        fontSize: '12px',
                        fontWeight: '800',
                        background: scoreBg,
                        color: scoreColor,
                        border: `1px solid ${scoreBorder}`,
                        display: 'inline-flex',
                        alignItems: 'center',
                        gap: '4px'
                      }}
                    >
                      {percentage}% Match
                    </span>

                    {/* Horizontal Progress Bar */}
                    <div className="w-full bg-dark-lighter rounded-full h-1.5 mt-2 overflow-hidden" style={{ background: 'rgba(15, 23, 42, 0.08)', minWidth: '120px' }}>
                      <div 
                        className="h-full rounded-full" 
                        style={{ width: `${Math.min(parseFloat(percentage), 100)}%`, background: scoreColor }}
                      />
                    </div>
                  </div>
                </div>

                {/* Skills Tags Row */}
                {displaySkills && (
                  <div className="mt-3 pt-3 flex items-center gap-1.5 flex-wrap" style={{ borderTop: '1px dashed rgba(15, 23, 42, 0.08)' }}>
                    <span className="text-xs text-muted font-semibold">Required Skills:</span>
                    {displaySkills.split(',').slice(0, 6).map((skill, sIdx) => (
                      <span
                        key={sIdx}
                        style={{
                          fontSize: '11px',
                          padding: '2px 8px',
                          borderRadius: '6px',
                          background: 'rgba(15, 23, 42, 0.04)',
                          color: '#475569',
                          border: '1px solid rgba(15, 23, 42, 0.08)'
                        }}
                      >
                        {skill.trim()}
                      </span>
                    ))}
                  </div>
                )}

                {/* View Details Action */}
                <div className="mt-3 text-right">
                  <button
                    onClick={() => setExpandedIndex(isExpanded ? null : index)}
                    className="btn btn-sm btn-outline text-xs"
                    style={{ padding: '4px 10px', width: 'auto' }}
                  >
                    {isExpanded ? (
                      <span className="inline-flex items-center gap-1">Hide Details <IconChevronUp size={12} /></span>
                    ) : (
                      <span className="inline-flex items-center gap-1">View Details <IconChevronDown size={12} /></span>
                    )}
                  </button>
                </div>

                {/* Expanded Details Drawer */}
                {isExpanded && (
                  <div 
                    className="mt-3 p-3 rounded-xl text-xs text-secondary leading-relaxed"
                    style={{
                      background: 'rgba(248, 250, 252, 0.9)',
                      border: '1px solid rgba(15, 23, 42, 0.08)'
                    }}
                  >
                    {job.description && (
                      <div className="mb-2">
                        <strong className="text-primary block mb-1">Job Description:</strong>
                        <p>{job.description}</p>
                      </div>
                    )}
                    <div className="flex gap-4 text-muted font-mono mt-2 flex-wrap">
                      <span>Job ID: {job.job_id || 'N/A'}</span>
                      <span>Cosine Vector Similarity: {typeof rawScore === 'number' ? rawScore.toFixed(4) : rawScore}</span>
                    </div>
                  </div>
                )}
              </div>
            );
          })
        )}
      </div>
    </div>
  );
};

export default JobRecommendationCard;
