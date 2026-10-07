import React, { useState, useRef } from 'react';
import { IconUpload, IconFile, IconLock, IconAlertTriangle, IconArrowRight, IconSparkles } from './Icons';

const ResumeUploader = ({ onAnalyze, onUpload, isLoading, error }) => {
  const [selectedFile, setSelectedFile] = useState(null);
  const [fileError, setFileError] = useState('');
  const [isDragOver, setIsDragOver] = useState(false);
  const fileInputRef = useRef(null);

  const handleCallback = onAnalyze || onUpload;

  const MAX_FILE_SIZE = 10 * 1024 * 1024; // 10 MB
  const ALLOWED_EXTENSIONS = ['.pdf', '.docx', '.doc', '.txt'];
  const ALLOWED_TYPES = [
    'application/pdf',
    'application/vnd.openxmlformats-officedocument.wordprocessingml.document',
    'application/msword',
    'text/plain'
  ];

  const validateFile = (file) => {
    setFileError('');
    if (!file) return false;

    const fileExt = '.' + file.name.split('.').pop().toLowerCase();
    if (!ALLOWED_EXTENSIONS.includes(fileExt) && !ALLOWED_TYPES.includes(file.type)) {
      setFileError('Invalid file format. Only PDF, DOCX, and TXT documents are supported.');
      return false;
    }

    if (file.size > MAX_FILE_SIZE) {
      setFileError('File size exceeds the 10 MB limit.');
      return false;
    }

    return true;
  };

  const handleFileChange = (e) => {
    const file = e.target.files[0];
    if (file && validateFile(file)) {
      setSelectedFile(file);
    }
  };

  const handleDragOver = (e) => {
    e.preventDefault();
    setIsDragOver(true);
  };

  const handleDragLeave = (e) => {
    e.preventDefault();
    setIsDragOver(false);
  };

  const handleDrop = (e) => {
    e.preventDefault();
    setIsDragOver(false);
    const file = e.dataTransfer.files[0];
    if (file && validateFile(file)) {
      setSelectedFile(file);
    }
  };

  const handleRemoveFile = (e) => {
    e.stopPropagation();
    setSelectedFile(null);
    setFileError('');
    if (fileInputRef.current) {
      fileInputRef.current.value = '';
    }
  };

  const formatFileSize = (bytes) => {
    if (bytes < 1024) return bytes + ' B';
    if (bytes < 1024 * 1024) return (bytes / 1024).toFixed(1) + ' KB';
    return (bytes / (1024 * 1024)).toFixed(2) + ' MB';
  };

  const handleAnalyzeClick = () => {
    if (selectedFile && typeof handleCallback === 'function') {
      handleCallback(selectedFile);
    }
  };

  // Sample Resume Creator for instant testing without manual file selection
  const handleLoadSampleResume = (sampleType) => {
    let textContent = "";
    let fileName = "";
    
    if (sampleType === 'datascience') {
      fileName = "Sample_Data_Scientist_Resume.txt";
      textContent = "EXPERT DATA SCIENTIST AND MACHINE LEARNING ENGINEER\nExperience with Python, PyTorch, TensorFlow, Scikit-learn, SQL, Data Pipelines, Pandas, NumPy, Predictive Modeling, NLP, Feature Engineering, Neural Networks, Computer Vision, Big Data, Spark, Docker, AWS S3, MLOps, Git, A/B Testing, Statistics.";
    } else if (sampleType === 'frontend') {
      fileName = "Sample_Frontend_Engineer_Resume.txt";
      textContent = "SENIOR FRONTEND DEVELOPER AND UI/UX ARCHITECT\nExperience with React.js, TypeScript, Next.js, HTML5, CSS3, Tailwind CSS, JavaScript ES6+, Webpack, Redux Toolkit, REST APIs, GraphQL, UI Performance Optimization, Responsive Design, Jest, Cypress, Figma, Git.";
    } else {
      fileName = "Sample_Software_Engineer_Resume.txt";
      textContent = "FULL STACK SOFTWARE ENGINEER\nExperience with Java, Spring Boot, Microservices, Python, Node.js, PostgreSQL, MongoDB, Docker, Kubernetes, AWS, RESTful Web Services, CI/CD, Git, Unit Testing, System Architecture, Agile Methodologies.";
    }

    const blob = new Blob([textContent], { type: 'text/plain' });
    const sampleFile = new File([blob], fileName, { type: 'text/plain' });

    if (validateFile(sampleFile)) {
      setSelectedFile(sampleFile);
    }
  };

  return (
    <div id="upload-section" className="w-full my-8 md:my-12">
      <div className="glass-panel max-w-2xl mx-auto text-center relative glow-card-orange p-4 sm:p-8 md:p-10">
        {/* Header */}
        <div className="mb-6 md:mb-8">
          <span className="badge badge-orange mb-2">RESUME PARSER & ANALYSIS</span>
          <h2 className="text-2xl sm:text-3xl font-extrabold text-primary">Analyze Your Resume</h2>
          <p className="text-secondary text-xs sm:text-sm mt-2 max-w-lg mx-auto leading-relaxed">
            Upload your PDF, DOCX, or TXT resume to let SmartHire predict your career role, recommend job matches, and map your skill gap.
          </p>
        </div>

        <input
          type="file"
          ref={fileInputRef}
          onChange={handleFileChange}
          accept=".pdf,.docx,.doc,.txt"
          style={{ display: 'none' }}
        />

        {/* Drag & Drop Upload Container */}
        {!selectedFile ? (
          <div>
            <div
              onDragOver={handleDragOver}
              onDragLeave={handleDragLeave}
              onDrop={handleDrop}
              onClick={() => fileInputRef.current?.click()}
              style={{
                border: `2px dashed ${isDragOver ? 'var(--accent-orange)' : 'rgba(15, 23, 42, 0.18)'}`,
                borderRadius: '20px',
                background: isDragOver ? 'rgba(249, 115, 22, 0.08)' : '#ffffff',
                cursor: 'pointer',
                transition: 'all 0.3s cubic-bezier(0.16, 1, 0.3, 1)',
                boxShadow: isDragOver ? '0 0 30px rgba(249, 115, 22, 0.22)' : '0 4px 20px rgba(15, 23, 42, 0.04)'
              }}
              className="p-6 sm:p-10 md:p-14 hover:border-orange-400 group"
            >
              <div 
                style={{
                  width: '64px',
                  height: '64px',
                  borderRadius: '50%',
                  background: 'rgba(249, 115, 22, 0.1)',
                  border: '1px solid rgba(249, 115, 22, 0.3)',
                  display: 'flex',
                  alignItems: 'center',
                  justifyContent: 'center',
                  margin: '0 auto 1rem auto',
                  boxShadow: '0 0 24px rgba(249, 115, 22, 0.16)',
                  transition: 'transform 0.3s ease'
                }}
                className="group-hover:scale-110"
              >
                <IconUpload size={28} color="#f97316" />
              </div>
              <h3 style={{ fontSize: '1.15rem', fontWeight: '800', marginBottom: '0.4rem', color: '#0f172a' }}>
                Drop your resume file here
              </h3>
              <p style={{ color: 'var(--text-muted)', fontSize: '0.875rem', marginBottom: '1rem' }}>
                or <span style={{ color: 'var(--accent-orange)', fontWeight: '700', textDecoration: 'underline' }}>browse from your computer</span>
              </p>
              
              {/* File format badges */}
              <div className="flex justify-center items-center gap-2 flex-wrap text-xs text-muted">
                <span className="badge badge-dark" style={{ fontSize: '10px' }}>PDF</span>
                <span className="badge badge-dark" style={{ fontSize: '10px' }}>DOCX</span>
                <span className="badge badge-dark" style={{ fontSize: '10px' }}>TXT</span>
                <span style={{ color: 'var(--text-muted)' }}>• Max size: 10 MB</span>
              </div>
            </div>

            {/* Quick Sample Resume Loader buttons for instant testing */}
            <div className="mt-6 pt-4" style={{ borderTop: '1px dashed rgba(15, 23, 42, 0.1)' }}>
              <div className="text-xs text-muted font-semibold mb-2.5 flex items-center justify-center gap-1">
                <IconSparkles size={12} color="#f97316" /> Or test instantly with a sample profile:
              </div>
              <div className="flex justify-center gap-2 flex-wrap">
                <button
                  type="button"
                  onClick={() => handleLoadSampleResume('datascience')}
                  className="btn btn-outline btn-sm text-xs"
                >
                  Sample Data Scientist
                </button>
                <button
                  type="button"
                  onClick={() => handleLoadSampleResume('frontend')}
                  className="btn btn-outline btn-sm text-xs"
                >
                  Sample Frontend Engineer
                </button>
                <button
                  type="button"
                  onClick={() => handleLoadSampleResume('software')}
                  className="btn btn-outline btn-sm text-xs"
                >
                  Sample Software Engineer
                </button>
              </div>
            </div>
          </div>
        ) : (
          /* File Selected Preview Card */
          <div style={{
            background: '#ffffff',
            border: '1px solid rgba(249, 115, 22, 0.35)',
            borderRadius: '20px',
            padding: '1.25rem',
            textAlign: 'left',
            boxShadow: '0 10px 30px rgba(249, 115, 22, 0.12)'
          }}>
            <div className="flex justify-between items-center flex-wrap gap-3">
              <div className="flex items-center gap-3">
                <div 
                  style={{
                    width: '48px',
                    height: '48px',
                    borderRadius: '14px',
                    background: 'rgba(249, 115, 22, 0.12)',
                    border: '1px solid rgba(249, 115, 22, 0.3)',
                    display: 'flex',
                    alignItems: 'center',
                    justifyContent: 'center',
                    flexShrink: 0
                  }}
                >
                  <IconFile size={24} color="#f97316" />
                </div>
                <div>
                  <div style={{ fontWeight: '800', color: '#0f172a', fontSize: '1rem', wordBreak: 'break-all' }}>
                    {selectedFile.name}
                  </div>
                  <div className="text-xs text-muted mt-1 flex flex-wrap gap-2 items-center">
                    <span className="badge badge-green" style={{ fontSize: '9px', padding: '1px 6px' }}>READY</span>
                    <span>{formatFileSize(selectedFile.size)}</span>
                    <span>•</span>
                    <span>{selectedFile.name.split('.').pop().toUpperCase()}</span>
                  </div>
                </div>
              </div>

              <button
                onClick={handleRemoveFile}
                className="btn-danger w-full sm:w-auto"
                disabled={isLoading}
              >
                Remove File
              </button>
            </div>
          </div>
        )}

        {/* Local Validation Error */}
        {fileError && (
          <div className="flex items-center gap-2" style={{ color: '#dc2626', fontSize: '0.85rem', marginTop: '1rem', background: 'rgba(239, 68, 68, 0.08)', border: '1px solid rgba(239, 68, 68, 0.25)', padding: '0.75rem 1rem', borderRadius: '12px', textAlign: 'left' }}>
            <IconAlertTriangle size={16} color="#dc2626" />
            <span><strong>Error:</strong> {fileError}</span>
          </div>
        )}

        {/* Backend Error */}
        {error && (
          <div className="flex items-center gap-2" style={{ color: '#dc2626', fontSize: '0.85rem', marginTop: '1rem', background: 'rgba(239, 68, 68, 0.08)', border: '1px solid rgba(239, 68, 68, 0.25)', padding: '0.75rem 1rem', borderRadius: '12px', textAlign: 'left' }}>
            <IconAlertTriangle size={16} color="#dc2626" />
            <span><strong>Server Notice:</strong> {error}</span>
          </div>
        )}

        {/* Analyze Button */}
        {selectedFile && (
          <div style={{ marginTop: '1.5rem' }}>
            <button
              onClick={handleAnalyzeClick}
              className="btn-primary w-full"
              style={{ padding: '0.95rem', fontSize: '1rem', fontWeight: '800' }}
              disabled={isLoading}
            >
              {isLoading ? 'Analyzing Resume...' : (
                <span className="flex items-center justify-center gap-2">
                  Analyze Resume <IconArrowRight size={18} />
                </span>
              )}
            </button>
          </div>
        )}

        {/* Security / Privacy Footnote */}
        <div className="flex items-center justify-center gap-1.5" style={{ marginTop: '1.5rem', fontSize: '0.75rem', color: 'var(--text-muted)' }}>
          <IconLock size={12} color="#64748b" />
          <span>Your document is processed securely. Data is analyzed locally without external storage.</span>
        </div>
      </div>
    </div>
  );
};

export default ResumeUploader;
