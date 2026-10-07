import React, { useState } from 'react';
import Hero from '../components/Hero';
import HowItWorks from '../components/HowItWorks';
import ResumeUploader from '../components/ResumeUploader';
import LoadingAnalysis from '../components/LoadingAnalysis';
import ResultsDashboard from '../components/ResultsDashboard';
import { analyzeResume } from '../services/api';
import { IconAlertTriangle } from '../components/Icons';

const Home = () => {
  const [appState, setAppState] = useState('idle'); // 'idle' | 'loading' | 'results' | 'error'
  const [analysisResult, setAnalysisResult] = useState(null);
  const [errorMessage, setErrorMessage] = useState('');
  const [currentFile, setCurrentFile] = useState(null);

  const handleUpload = async (file) => {
    setCurrentFile(file);
    setAppState('loading');
    setErrorMessage('');

    try {
      const data = await analyzeResume(file);

      if (data && data.success) {
        setAnalysisResult(data);
        setAppState('results');
      } else {
        throw new Error(data.message || 'Analysis did not complete successfully.');
      }
    } catch (err) {
      console.error('Resume Analysis Error:', err);
      setErrorMessage(err.message || 'Failed to process resume. Please ensure backend server is active.');
      setAppState('error');
    }
  };

  const handleReset = () => {
    setAppState('idle');
    setAnalysisResult(null);
    setErrorMessage('');
    setCurrentFile(null);
  };

  const scrollToSection = (id) => {
    const element = document.getElementById(id);
    if (element) {
      element.scrollIntoView({ behavior: 'smooth' });
    }
  };

  return (
    <div className="w-full">
      {/* Idle State: Hero + How It Works + Upload Area */}
      {appState === 'idle' && (
        <>
          <Hero 
            onAnalyzeClick={() => scrollToSection('upload-section')}
            onHowItWorksClick={() => scrollToSection('how-it-works-section')}
          />
          <ResumeUploader onAnalyze={handleUpload} onUpload={handleUpload} isLoading={false} />
          <HowItWorks />
        </>
      )}

      {/* Loading State */}
      {appState === 'loading' && (
        <LoadingAnalysis filename={currentFile?.name || 'Resume Document'} />
      )}

      {/* Polished Error State */}
      {appState === 'error' && (
        <div className="glass-panel max-w-xl mx-auto my-12 text-center relative" style={{ borderColor: 'rgba(239, 68, 68, 0.4)' }}>
          <div 
            style={{
              width: '60px',
              height: '60px',
              borderRadius: '50%',
              background: 'rgba(239, 68, 68, 0.15)',
              border: '1px solid rgba(239, 68, 68, 0.3)',
              color: '#f87171',
              display: 'flex',
              alignItems: 'center',
              justifyContent: 'center',
              margin: '0 auto 1.25rem auto'
            }}
          >
            <IconAlertTriangle size={28} color="#ef4444" />
          </div>

          <h3 className="text-2xl font-extrabold text-primary mb-2">Something went wrong</h3>
          <p className="text-sm text-secondary max-w-md mx-auto mb-6">
            Please check your resume and try again. Ensure the FastAPI backend server is active.
          </p>

          <div 
            className="p-4 text-left rounded-xl text-xs text-muted mb-6"
            style={{ background: 'rgba(7, 9, 14, 0.6)', border: '1px solid rgba(255, 255, 255, 0.05)' }}
          >
            <strong className="text-secondary block mb-1">Troubleshooting Checklist:</strong>
            <ul className="list-disc pl-5 space-y-1">
              <li>Ensure the FastAPI server is running: <code>python -m uvicorn app:app --reload</code> in <code>backend/</code>.</li>
              <li>Verify the document contains readable text (PDF, DOCX, or TXT).</li>
            </ul>
          </div>

          <button
            onClick={handleReset}
            className="btn btn-primary"
            style={{ padding: '0.85rem 2rem' }}
          >
            Try Again
          </button>
        </div>
      )}

      {/* Results Dashboard State */}
      {appState === 'results' && analysisResult && (
        <ResultsDashboard analysisResult={analysisResult} onReset={handleReset} />
      )}
    </div>
  );
};

export default Home;
