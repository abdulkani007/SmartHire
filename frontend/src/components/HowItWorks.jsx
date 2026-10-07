import React from 'react';
import { IconFile, IconCpu, IconTarget } from './Icons';

const HowItWorks = () => {
  const steps = [
    {
      step: '01',
      title: 'UPLOAD RESUME',
      icon: <IconFile size={24} color="#f97316" />,
      description: 'Upload your PDF or DOCX resume document. SmartHire securely extracts structural text, skills, and experience tokens.',
      badge: 'Parsing'
    },
    {
      step: '02',
      title: 'ML CLASSIFICATION',
      icon: <IconCpu size={24} color="#f97316" />,
      description: 'SmartHire vectorizes your profile using TF-IDF unigram & bigrams and predicts your category across 25 career domains.',
      badge: 'Phase 3 ML'
    },
    {
      step: '03',
      title: 'CAREER ROADMAP',
      icon: <IconTarget size={24} color="#f97316" />,
      description: 'Discover top job matches from 148,000+ postings via cosine similarity and receive targeted skill gap recommendations.',
      badge: 'Intelligence'
    }
  ];

  return (
    <div id="how-it-works-section" className="w-full my-16">
      <div className="text-center mb-12">
        <span className="badge badge-orange mb-2">3-STEP INTELLIGENCE PIPELINE</span>
        <h2 className="text-3xl font-extrabold text-primary">How SmartHire Works</h2>
        <p className="text-secondary text-sm max-w-xl mx-auto mt-2 leading-relaxed">
          From raw document parsing to vector space matching — classical machine learning engineered for career growth.
        </p>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-3 gap-6 relative">
        {steps.map((item, idx) => (
          <div 
            key={idx} 
            className="glass-panel flex flex-col justify-between relative glow-card-orange group hover:-translate-y-1 transition-all duration-300" 
            style={{ padding: '2rem 1.75rem' }}
          >
            <div>
              <div className="flex justify-between items-center mb-5">
                <span className="text-3xl font-black text-gradient-orange tracking-tight">{item.step}</span>
                <span className="badge badge-dark" style={{ fontSize: '10px' }}>{item.badge}</span>
              </div>

              <div 
                style={{
                  width: '52px',
                  height: '52px',
                  borderRadius: '14px',
                  background: 'rgba(249, 115, 22, 0.1)',
                  border: '1px solid rgba(249, 115, 22, 0.25)',
                  display: 'flex',
                  alignItems: 'center',
                  justifyContent: 'center',
                  marginBottom: '1.25rem',
                  boxShadow: '0 4px 15px rgba(249, 115, 22, 0.1)'
                }}
              >
                {item.icon}
              </div>

              <h3 className="text-lg font-extrabold text-primary mb-2 tracking-wide">
                {item.title}
              </h3>

              <p className="text-sm text-secondary leading-relaxed">
                {item.description}
              </p>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
};

export default HowItWorks;
