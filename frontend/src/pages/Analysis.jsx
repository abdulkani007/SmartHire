import React, { useState } from 'react';
import { predictCategory, recommendJobs, generateSkillGap } from '../services/api';
import CareerCategoryCard from '../components/CareerCategoryCard';
import SkillGapCard from '../components/SkillGapCard';
import JobRecommendationCard from '../components/JobRecommendationCard';
import { IconSparkles, IconAlertTriangle } from '../components/Icons';

const Analysis = () => {
  const [resumeText, setResumeText] = useState('');
  const [targetCategory, setTargetCategory] = useState('');
  const [loading, setLoading] = useState(false);
  const [activeSubTab, setActiveSubTab] = useState('all');
  const [results, setResults] = useState(null);
  const [error, setError] = useState('');

  const handleTextAnalysis = async (e) => {
    e.preventDefault();
    if (!resumeText.trim()) {
      setError('Please paste your resume text before running analysis.');
      return;
    }

    setLoading(true);
    setError('');
    setResults(null);

    try {
      // Execute 3 classical ML calls in parallel
      const [catRes, recRes, gapRes] = await Promise.all([
        predictCategory(resumeText),
        recommendJobs(resumeText, 10),
        generateSkillGap(resumeText, targetCategory.trim() || null, 20)
      ]);

      setResults({
        category: catRes.category,
        recommendations: recRes.recommendations || [],
        skillGap: gapRes
      });
    } catch (err) {
      console.error('Direct Text Analysis Error:', err);
      setError(err.message || 'Failed to complete analysis. Please verify FastAPI backend status.');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="w-full">
      <div className="mb-6">
        <h1 className="text-3xl font-bold text-gradient">Direct Text & Custom Analysis</h1>
        <p className="text-secondary text-sm mt-1">
          Paste plain resume text or override the target career category to test the Phase 3 ML models interactively.
        </p>
      </div>

      {/* Input Form Card */}
      <div className="glass-card mb-8">
        <form onSubmit={handleTextAnalysis}>
          <div className="mb-4">
            <label className="block text-sm font-semibold text-secondary mb-2">
              Candidate Resume Text:
            </label>
            <textarea
              rows={6}
              placeholder="Paste raw resume text here (e.g. Work experience, skills, education, projects...)"
              value={resumeText}
              onChange={(e) => setResumeText(e.target.value)}
              className="form-input font-mono text-xs"
              style={{ width: '100%', resize: 'vertical' }}
            />
          </div>

          <div className="flex justify-between items-center flex-wrap gap-4">
            <div style={{ flex: '1', minWidth: '220px' }}>
              <label className="block text-xs text-muted mb-1 font-semibold">
                Target Category (Optional Override):
              </label>
              <input
                type="text"
                placeholder="e.g. Data Science, Java Developer, Sales"
                value={targetCategory}
                onChange={(e) => setTargetCategory(e.target.value)}
                className="form-input text-xs"
                style={{ width: '100%', padding: '8px 12px' }}
              />
            </div>

            <div className="flex items-center gap-3">
              <button
                type="button"
                onClick={() => {
                  setResumeText('');
                  setTargetCategory('');
                  setResults(null);
                  setError('');
                }}
                className="btn btn-outline btn-sm text-muted"
              >
                Clear
              </button>
              <button
                type="submit"
                disabled={loading || !resumeText.trim()}
                className="btn btn-primary"
                style={{ padding: '10px 24px' }}
              >
                {loading ? 'Running ML Models...' : (
                  <span className="inline-flex items-center gap-1.5">
                    <IconSparkles size={16} /> Analyze Text
                  </span>
                )}
              </button>
            </div>
          </div>
        </form>

        {error && (
          <div className="mt-4 p-3 rounded-lg bg-red-50 border border-red-200 text-red-600 text-xs flex items-center gap-2">
            <IconAlertTriangle size={16} color="#ef4444" />
            <span>{error}</span>
          </div>
        )}
      </div>

      {/* Results Rendering */}
      {results && (
        <div className="mt-6">
          <div className="flex gap-2 mb-6">
            <button
              onClick={() => setActiveSubTab('all')}
              className={`btn btn-sm ${activeSubTab === 'all' ? 'btn-primary' : 'btn-outline'}`}
            >
              All Results
            </button>
            <button
              onClick={() => setActiveSubTab('category')}
              className={`btn btn-sm ${activeSubTab === 'category' ? 'btn-primary' : 'btn-outline'}`}
            >
              Category ({results.category})
            </button>
            <button
              onClick={() => setActiveSubTab('jobs')}
              className={`btn btn-sm ${activeSubTab === 'jobs' ? 'btn-primary' : 'btn-outline'}`}
            >
              Jobs ({results.recommendations.length})
            </button>
            <button
              onClick={() => setActiveSubTab('skills')}
              className={`btn btn-sm ${activeSubTab === 'skills' ? 'btn-primary' : 'btn-outline'}`}
            >
              Skill Gap
            </button>
          </div>

          {(activeSubTab === 'all' || activeSubTab === 'category') && (
            <CareerCategoryCard category={results.category} filename="Direct Text Query" />
          )}

          {(activeSubTab === 'all' || activeSubTab === 'skills') && (
            <SkillGapCard skillGapData={results.skillGap} />
          )}

          {(activeSubTab === 'all' || activeSubTab === 'jobs') && (
            <JobRecommendationCard recommendations={results.recommendations} />
          )}
        </div>
      )}
    </div>
  );
};

export default Analysis;
