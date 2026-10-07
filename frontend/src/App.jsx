import React, { useState } from 'react';
import SplashScreen from './components/SplashScreen';
import Navbar from './components/Navbar';
import Home from './pages/Home';
import Analysis from './pages/Analysis';
import './index.css';

function App() {
  const [showSplash, setShowSplash] = useState(true);
  const [activeTab, setActiveTab] = useState('home');

  return (
    <div style={{ minHeight: '100vh', display: 'flex', flexDirection: 'column' }}>
      {/* Animated Splash Screen on Initial Load */}
      {showSplash && <SplashScreen onFinish={() => setShowSplash(false)} />}

      {/* Sticky Header Navigation */}
      <Navbar activeTab={activeTab} setActiveTab={setActiveTab} />

      {/* Main Content Body */}
      <main className="container flex-1 py-8">
        {activeTab === 'home' && <Home />}
        {activeTab === 'analysis' && <Analysis />}
        {activeTab === 'jobs' && <Analysis />}
      </main>

      {/* Footer */}
      <footer 
        style={{
          borderTop: '1px solid var(--border-card)',
          background: 'rgba(255, 255, 255, 0.95)',
          backdropFilter: 'blur(10px)',
          padding: '24px 0',
          marginTop: 'auto'
        }}
      >
        <div className="container flex justify-between items-center flex-wrap gap-4 text-xs text-muted">
          <div>
            <strong className="text-primary">SmartHire Engine v1.0</strong> — Classical Machine Learning Resume Matching Platform
          </div>

          <div className="flex gap-4 font-mono text-xs text-secondary">
            <span>Model: Logistic Regression + TF-IDF</span>
            <span>Index: 148,994 Job Postings</span>
            <span>Backend: FastAPI</span>
          </div>
        </div>
      </footer>
    </div>
  );
}

export default App;
