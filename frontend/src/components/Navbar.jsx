import React, { useState } from 'react';
import logoImg from '../assets/image.png';

const Navbar = ({ activeTab, setActiveTab }) => {
  const [mobileMenuOpen, setMobileMenuOpen] = useState(false);

  const handleNavClick = (tabId, elementId) => {
    setActiveTab(tabId);
    setMobileMenuOpen(false);
    if (elementId) {
      setTimeout(() => {
        const el = document.getElementById(elementId);
        if (el) el.scrollIntoView({ behavior: 'smooth' });
      }, 100);
    }
  };

  return (
    <header 
      style={{
        borderBottom: '1px solid rgba(15, 23, 42, 0.08)',
        background: 'rgba(255, 255, 255, 0.92)',
        backdropFilter: 'blur(20px)',
        WebkitBackdropFilter: 'blur(20px)',
        position: 'sticky',
        top: 0,
        zIndex: 100,
        boxShadow: '0 4px 20px -2px rgba(15, 23, 42, 0.04)'
      }}
    >
      <div className="container flex justify-between items-center py-3" style={{ minHeight: '70px' }}>
        {/* Left: Brand Logo & Title */}
        <div 
          onClick={() => handleNavClick('home')}
          style={{ cursor: 'pointer', display: 'flex', itemsCenter: 'center', gap: '0.75rem' }}
          className="group"
        >
          <div 
            style={{
              width: '42px',
              height: '42px',
              borderRadius: '12px',
              background: '#ffffff',
              border: '1px solid rgba(249, 115, 22, 0.3)',
              display: 'flex',
              alignItems: 'center',
              justifyContent: 'center',
              padding: '4px',
              boxShadow: '0 4px 14px rgba(249, 115, 22, 0.18)',
              transition: 'all 0.3s ease',
              flexShrink: 0
            }}
            className="group-hover:scale-105"
          >
            <img src={logoImg} alt="SH Logo" style={{ width: '100%', height: '100%', objectFit: 'contain' }} />
          </div>
          <div>
            <div style={{ fontSize: '1.35rem', fontWeight: '800', letterSpacing: '-0.025em', color: '#0f172a', lineHeight: 1.1 }}>
              Smart<span className="text-gradient-orange">Hire</span>
            </div>
            <div style={{ fontSize: '0.62rem', fontWeight: '700', color: '#64748b', letterSpacing: '0.08em', textTransform: 'uppercase' }}>
              Career Intelligence Engine
            </div>
          </div>
        </div>

        {/* Desktop Navigation */}
        <div className="hidden md:flex items-center gap-3">
          <nav className="flex items-center gap-2">
            {[
              { id: 'home', label: 'Home', scrollTo: null },
              { id: 'home', label: 'Analyze Resume', scrollTo: 'upload-section' },
              { id: 'jobs', label: 'Jobs', scrollTo: null }
            ].map((item, idx) => (
              <button
                key={idx}
                onClick={() => handleNavClick(item.id, item.scrollTo)}
                className={`btn btn-sm ${activeTab === item.id && !item.scrollTo ? 'btn-primary' : 'btn-outline'}`}
                style={{
                  padding: '8px 18px',
                  fontSize: '0.875rem',
                  fontWeight: '600',
                  borderRadius: '10px',
                  width: 'auto'
                }}
              >
                {item.label}
              </button>
            ))}
          </nav>
        </div>

        {/* Mobile Toggle Button */}
        <div className="flex md:hidden items-center">
          <button
            onClick={() => setMobileMenuOpen(!mobileMenuOpen)}
            className="btn btn-outline p-2"
            style={{ width: '40px', height: '40px', padding: 0 }}
            aria-label="Toggle Navigation"
          >
            <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="#0f172a" strokeWidth="2.5" strokeLinecap="round" strokeLinejoin="round">
              {mobileMenuOpen ? (
                <path d="M18 6L6 18M6 6l12 12" />
              ) : (
                <path d="M4 6h16M4 12h16M4 18h16" />
              )}
            </svg>
          </button>
        </div>
      </div>

      {/* Mobile Drawer Menu */}
      {mobileMenuOpen && (
        <div 
          className="md:hidden border-t p-4 flex flex-col gap-3 bg-white shadow-lg"
          style={{ borderColor: 'rgba(15, 23, 42, 0.08)' }}
        >
          {[
            { id: 'home', label: 'Home', scrollTo: null },
            { id: 'home', label: 'Analyze Resume', scrollTo: 'upload-section' },
            { id: 'jobs', label: 'Jobs', scrollTo: null }
          ].map((item, idx) => (
            <button
              key={idx}
              onClick={() => handleNavClick(item.id, item.scrollTo)}
              className={`btn ${activeTab === item.id && !item.scrollTo ? 'btn-primary' : 'btn-outline'}`}
              style={{ width: '100%', padding: '10px', fontWeight: '600', borderRadius: '10px' }}
            >
              {item.label}
            </button>
          ))}
        </div>
      )}
    </header>
  );
};

export default Navbar;
