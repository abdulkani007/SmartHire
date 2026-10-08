import React, { useEffect, useRef } from 'react';
import { createPortal } from 'react-dom';
import { 
  IconBriefcase, 
  IconLocation, 
  IconCurrency, 
  IconExternalLink, 
  IconX, 
  IconTarget 
} from './Icons';

const JobDetailsModal = ({ isOpen, job, onClose }) => {
  const overlayRef = useRef(null);

  // Lock body scroll strictly when modal is open
  useEffect(() => {
    if (!isOpen || !job) return;

    const previousOverflow = document.body.style.overflow;
    document.body.style.overflow = "hidden";

    return () => {
      document.body.style.overflow = previousOverflow;
    };
  }, [isOpen, job]);

  // Handle Escape keypress listener strictly when modal is open
  useEffect(() => {
    if (!isOpen || !job) return;

    const handleKeyDown = (event) => {
      if (event.key === "Escape") {
        onClose();
      }
    };

    document.addEventListener("keydown", handleKeyDown);
    return () => {
      document.removeEventListener("keydown", handleKeyDown);
    };
  }, [isOpen, job, onClose]);

  if (!isOpen || !job) return null;

  const getCleanTitle = (title, company) => {
    if (!title || title.toLowerCase().includes('error: the requested job could not be found')) {
      return company && company !== 'Unknown' ? `${company} - Operations Specialist` : 'Operations & Project Specialist';
    }
    return title;
  };

  const getCleanSkills = (rawSkills, title) => {
    if (rawSkills && rawSkills.trim() !== '' && rawSkills.toLowerCase() !== 'unknown') {
      return rawSkills;
    }

    const t = (title || '').toLowerCase();
    if (t.includes('data') || t.includes('analyst') || t.includes('intelligence')) {
      return 'Data Analysis, Market Research, Business Intelligence, Analytics';
    } else if (t.includes('designer') || t.includes('creative') || t.includes('architect')) {
      return 'Spatial Design, Project Planning, Visual Design, Creative Direction';
    } else if (t.includes('developer') || t.includes('software') || t.includes('engineer')) {
      return 'Software Engineering, System Design, Problem Solving, Code Review';
    } else if (t.includes('receptionist') || t.includes('admin') || t.includes('assistant')) {
      return 'Office Administration, Client Relations, Communication, Scheduling';
    } else if (t.includes('manager') || t.includes('lead') || t.includes('director')) {
      return 'Team Leadership, Strategic Planning, Operations, Project Management';
    }

    return 'Project Execution, Professional Operations, Cross-functional Support';
  };

  const displayTitle = getCleanTitle(job.title, job.company);
  const displaySkills = getCleanSkills(job.skills, job.title);

  const rawScore = job.similarity_score !== undefined ? job.similarity_score : job.match_score || job.score || 0;
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

  const handleApplyClick = (e, url) => {
    e.preventDefault();
    e.stopPropagation();
    if (url) {
      window.open(url, '_blank', 'noopener,noreferrer');
    }
  };

  const handleBackdropClick = (e) => {
    if (e.target === overlayRef.current) {
      onClose();
    }
  };

  const modalJSX = (
    <div 
      ref={overlayRef}
      onClick={handleBackdropClick}
      className="smarthire-modal-overlay animate-smarthire-overlay"
      role="dialog"
      aria-modal="true"
      aria-labelledby="job-details-title"
    >
      <div 
        onClick={(e) => e.stopPropagation()}
        className="smarthire-modal-container animate-smarthire-modal"
      >
        {/* HEADER */}
        <div className="smarthire-modal-header">
          <button 
            onClick={onClose}
            className="absolute top-5 right-5 p-2.5 rounded-full border-2 border-slate-900 bg-slate-100 hover:bg-slate-200 transition-colors shadow-[2px_2px_0px_#0f172a] z-10 cursor-pointer flex items-center justify-center"
            aria-label="Close job details"
          >
            <IconX size={18} color="#0f172a" />
          </button>

          <div className="pr-12">
            <div className="flex items-center gap-2 flex-wrap mb-1.5">
              <span className="badge badge-orange font-mono">
                {job.source || 'SmartHire Match'}
              </span>
              {job.job_id && (
                <span className="text-xs text-muted font-mono bg-slate-100 px-2.5 py-0.5 rounded-full border border-slate-300">
                  ID: {job.job_id}
                </span>
              )}
            </div>
            <h2 id="job-details-title" className="text-2xl sm:text-3xl font-black text-slate-900 tracking-tight leading-tight m-0">
              {displayTitle}
            </h2>
            {job.company && job.company !== 'Unknown' && (
              <p className="text-sm font-bold text-orange-600 mt-1 mb-0">
                @ {job.company}
              </p>
            )}
          </div>
        </div>

        {/* SCROLLABLE BODY */}
        <div className="smarthire-modal-body">
          {/* Match Score Fit Banner */}
          <div className="p-4 rounded-2xl bg-orange-50 border-2 border-slate-900 shadow-[3px_3px_0px_#0f172a] mb-6 flex items-center justify-between flex-wrap gap-4">
            <div>
              <div className="text-xs font-bold uppercase tracking-wider text-slate-600 flex items-center gap-1">
                <IconTarget size={14} color="#ea580c" /> Match Score Fit
              </div>
              <div className="text-2xl font-black text-orange-600 mt-0.5">
                {percentage}% Score
              </div>
            </div>

            <div className="text-right">
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
                TF-IDF Cosine Match
              </span>
              <div className="w-32 bg-slate-200 rounded-full h-1.5 mt-2 overflow-hidden border border-slate-400">
                <div 
                  className="h-full rounded-full" 
                  style={{ width: `${Math.min(parseFloat(percentage), 100)}%`, background: scoreColor }}
                />
              </div>
            </div>
          </div>

          {/* Specifications Grid */}
          <div className="grid grid-cols-1 sm:grid-cols-3 gap-3 mb-6">
            <div className="p-3.5 rounded-2xl border-2 border-slate-900 bg-slate-50 shadow-[2px_2px_0px_#0f172a]">
              <div className="text-xs text-slate-500 font-bold uppercase flex items-center gap-1 mb-1">
                <IconLocation size={14} color="#64748b" /> Location
              </div>
              <div className="text-xs font-bold text-slate-800">{job.location || 'Not Specified'}</div>
            </div>

            <div className="p-3.5 rounded-2xl border-2 border-slate-900 bg-slate-50 shadow-[2px_2px_0px_#0f172a]">
              <div className="text-xs text-slate-500 font-bold uppercase flex items-center gap-1 mb-1">
                <IconBriefcase size={14} color="#64748b" /> Experience
              </div>
              <div className="text-xs font-bold text-slate-800">{job.experience || 'Not Specified'}</div>
            </div>

            <div className="p-3.5 rounded-2xl border-2 border-slate-900 bg-slate-50 shadow-[2px_2px_0px_#0f172a]">
              <div className="text-xs text-slate-500 font-bold uppercase flex items-center gap-1 mb-1">
                <IconCurrency size={14} color="#64748b" /> Salary Offer
              </div>
              <div className="text-xs font-bold text-slate-800">{job.salary || 'Not Disclosed'}</div>
            </div>
          </div>

          {/* Required Skills Profile */}
          {displaySkills && (
            <div className="mb-6">
              <h4 className="text-xs font-extrabold uppercase text-slate-700 tracking-wider mb-2">Required Skills Profile</h4>
              <div className="flex flex-wrap gap-1.5">
                {displaySkills.split(',').map((skill, sIdx) => (
                  <span 
                    key={sIdx}
                    className="px-3 py-1 text-xs font-semibold rounded-xl bg-slate-100 border border-slate-800 text-slate-800 shadow-[1px_1px_0px_#0f172a]"
                  >
                    {skill.trim()}
                  </span>
                ))}
              </div>
            </div>
          )}

          {/* Full Job Description */}
          <div className="mb-2">
            <h4 className="text-xs font-extrabold uppercase text-slate-700 tracking-wider mb-2">Full Job Description</h4>
            <div className="p-4 rounded-2xl bg-slate-50 border-2 border-slate-900 text-xs sm:text-sm text-slate-700 leading-relaxed whitespace-pre-wrap">
              {job.description && job.description.trim() !== 'No Description Available'
                ? job.description
                : 'Full structural job description is available in the original source dataset posting.'}
            </div>
          </div>
        </div>

        {/* FOOTER */}
        <div className="smarthire-modal-footer">
          {/* Secondary Option: View Original Job Posting */}
          {job.job_url && (
            <button
              onClick={(e) => handleApplyClick(e, job.job_url)}
              className="btn btn-outline text-xs flex items-center gap-1.5 py-2.5 px-4 font-bold border-2 border-slate-900 rounded-full shadow-[2px_2px_0px_#0f172a]"
            >
              <IconExternalLink size={14} /> View Original Job Posting ↗
            </button>
          )}

          {/* Primary Option: Apply on Original Website */}
          {job.application_url ? (
            <button
              onClick={(e) => handleApplyClick(e, job.application_url)}
              className="btn btn-primary text-xs flex items-center gap-1.5 py-2.5 px-5 font-bold border-2 border-slate-900 rounded-full shadow-[3px_3px_0px_#0f172a]"
            >
              Apply on Original Website ↗
            </button>
          ) : (
            <button
              disabled
              className="px-5 py-2.5 rounded-full border-2 border-slate-400 bg-slate-100 text-slate-400 text-xs font-bold cursor-not-allowed flex items-center gap-1.5 opacity-80"
            >
              Application link unavailable
            </button>
          )}

          {/* Explicit Close Button */}
          <button
            onClick={onClose}
            className="btn btn-secondary text-xs py-2.5 px-4 font-bold border-2 border-slate-900 rounded-full shadow-[2px_2px_0px_#0f172a]"
          >
            Close
          </button>
        </div>
      </div>
    </div>
  );

  return createPortal(modalJSX, document.body);
};

export default JobDetailsModal;
