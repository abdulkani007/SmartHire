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
          borderTop: '2px solid #0f172a',
          background: '#ffffff',
          padding: '20px 0',
          marginTop: 'auto'
        }}
      >
        <div className="container flex justify-between items-center flex-wrap gap-4 text-xs font-bold text-slate-700">
          <div className="flex items-center gap-2">
            <span className="badge badge-orange font-mono">SMARTHIRE CORE v1.0</span>
            <span className="hidden md:inline text-slate-500">• Classical ML Resume Matching Platform</span>
          </div>

          <div className="flex flex-wrap gap-2 font-mono text-xs">
            <span className="px-3 py-1 rounded-full border-2 border-slate-900 bg-slate-100 text-slate-800 shadow-[2px_2px_0px_#0f172a]">
              Model: Logistic Regression + TF-IDF
            </span>
            <span className="px-3 py-1 rounded-full border-2 border-slate-900 bg-orange-100 text-orange-900 shadow-[2px_2px_0px_#0f172a]">
              Index: 148,994 Postings
            </span>
            <span className="px-3 py-1 rounded-full border-2 border-slate-900 bg-slate-900 text-white shadow-[2px_2px_0px_#0f172a]">
              FastAPI + Atlas
            </span>
          </div>
        </div>
      </footer>
    </div>
  );
}

export default App;
