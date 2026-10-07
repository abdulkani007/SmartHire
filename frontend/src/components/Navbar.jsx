import React, { useState, useEffect } from 'react';
import logoImg from '../assets/image.png';

const Navbar = ({ activeTab, setActiveTab }) => {
  const [mobileMenuOpen, setMobileMenuOpen] = useState(false);
  const [scrolled, setScrolled] = useState(false);

  useEffect(() => {
    const handleScroll = () => {
      setScrolled(window.scrollY > 20);
    };
    window.addEventListener('scroll', handleScroll);
    return () => window.removeEventListener('scroll', handleScroll);
  }, []);

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
    <div 
      style={{
        position: 'sticky',
        top: '10px',
        zIndex: 100,
        width: '100%',
        display: 'flex',
        flexDirection: 'column',
        alignItems: 'center',
        padding: '0 12px',
        transition: 'all 0.3s ease'
      }}
    >
      {/* Floating Pill Capsule Header Container */}
      <header 
        style={{
          width: '100%',
          maxWidth: '1180px',
          background: '#ffffff',
          border: '2px solid #0f172a',
          borderRadius: '9999px',
          boxShadow: scrolled ? '6px 6px 0px #0f172a' : '4px 4px 0px #0f172a',
          padding: '8px 16px',
          display: 'flex',
          justifyContent: 'space-between',
          alignItems: 'center',
          transition: 'all 0.3s cubic-bezier(0.16, 1, 0.3, 1)',
          backdropFilter: 'blur(10px)',
          WebkitBackdropFilter: 'blur(10px)'
        }}
      >
        {/* Left: Active Dot + Logo + Brand Title */}
        <div 
          onClick={() => handleNavClick('home')}
          style={{ cursor: 'pointer', display: 'flex', alignItems: 'center', gap: '0.6rem' }}
          className="group"
        >
          {/* Red/Orange Active Status Indicator Dot */}
          <span 
            style={{
              width: '10px',
              height: '10px',
              borderRadius: '50%',
              background: '#f97316',
              boxShadow: '0 0 8px #f97316',
              display: 'inline-block',
              flexShrink: 0
            }}
          />

          <div 
            style={{
              width: '34px',
              height: '34px',
              borderRadius: '50%',
              background: '#ffffff',
              border: '1.5px solid #0f172a',
              display: 'flex',
              alignItems: 'center',
              justifyContent: 'center',
              padding: '2px',
              boxShadow: '2px 2px 0px #0f172a',
              transition: 'all 0.25s ease',
              flexShrink: 0
            }}
            className="group-hover:scale-105"
          >
            <img src={logoImg} alt="SH Logo" style={{ width: '100%', height: '100%', objectFit: 'contain' }} />
          </div>

          <div>
            <div style={{ fontSize: '1.15rem', fontWeight: '800', letterSpacing: '-0.025em', color: '#0f172a', lineHeight: 1.1 }}>
              Smart<span style={{ color: '#f97316' }}>Hire</span>
            </div>
            <div className="hidden sm:block" style={{ fontSize: '0.58rem', fontWeight: '800', color: '#64748b', letterSpacing: '0.08em', textTransform: 'uppercase' }}>
              Career Intelligence Engine
            </div>
          </div>
        </div>

        {/* Desktop Navigation Links */}
        <nav className="hidden md:flex items-center gap-6">
          {[
            { id: 'home', label: 'HOME', scrollTo: null },
            { id: 'home', label: 'ANALYZE RESUME', scrollTo: 'upload-section' },
            { id: 'jobs', label: 'JOBS', scrollTo: null }
          ].map((item, idx) => (
            <button
              key={idx}
              onClick={() => handleNavClick(item.id, item.scrollTo)}
              style={{
                background: 'transparent',
                border: 'none',
                color: activeTab === item.id && !item.scrollTo ? '#f97316' : '#0f172a',
                fontSize: '0.8rem',
                fontWeight: '800',
                letterSpacing: '0.06em',
                cursor: 'pointer',
                padding: '6px 12px',
                borderRadius: '9999px',
                transition: 'all 0.2s ease'
              }}
              className="hover:text-orange-500"
            >
              {item.label}
            </button>
          ))}
        </nav>

        {/* Right: Highlighted Action Pill Button */}
        <div className="hidden md:flex items-center gap-2">
          <button
            onClick={() => handleNavClick('home', 'upload-section')}
            style={{
              background: '#f97316',
              color: '#ffffff',
              border: '2px solid #0f172a',
              borderRadius: '9999px',
              padding: '6px 16px',
              fontSize: '0.825rem',
              fontWeight: '800',
              cursor: 'pointer',
              boxShadow: '2px 2px 0px #0f172a',
              display: 'flex',
              alignItems: 'center',
              gap: '6px',
              transition: 'all 0.2s ease'
            }}
            className="hover:translate-x-0.5 hover:translate-y-0.5"
          >
            <span>ANALYZE AI</span>
            <span style={{ fontSize: '0.9rem' }}>↗</span>
          </button>
        </div>

        {/* Mobile Hamburger Menu Toggle */}
        <div className="flex md:hidden items-center">
          <button
            onClick={() => setMobileMenuOpen(!mobileMenuOpen)}
            style={{
              background: '#ffffff',
              border: '2px solid #0f172a',
              borderRadius: '9999px',
              width: '38px',
              height: '38px',
              display: 'flex',
              alignItems: 'center',
              justifyContent: 'center',
              cursor: 'pointer',
              boxShadow: '2px 2px 0px #0f172a',
              padding: 0
            }}
            aria-label="Toggle Navigation"
          >
            <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="#0f172a" strokeWidth="2.5" strokeLinecap="round" strokeLinejoin="round">
              {mobileMenuOpen ? (
                <path d="M18 6L6 18M6 6l12 12" />
              ) : (
                <path d="M4 6h16M4 12h16M4 18h16" />
              )}
            </svg>
          </button>
        </div>
      </header>

      {/* Mobile Floating Drawer Card */}
      {mobileMenuOpen && (
        <div 
          style={{
            width: '100%',
            maxWidth: '1180px',
            marginTop: '8px',
            background: '#ffffff',
            border: '2px solid #0f172a',
            borderRadius: '24px',
            boxShadow: '4px 4px 0px #0f172a',
            padding: '16px',
            display: 'flex',
            flexDirection: 'column',
            gap: '10px'
          }}
          className="md:hidden"
        >
          {[
            { id: 'home', label: 'HOME', scrollTo: null },
            { id: 'home', label: 'ANALYZE RESUME', scrollTo: 'upload-section' },
            { id: 'jobs', label: 'JOBS', scrollTo: null }
          ].map((item, idx) => (
            <button
              key={idx}
              onClick={() => handleNavClick(item.id, item.scrollTo)}
              style={{
                width: '100%',
                padding: '12px 16px',
                fontSize: '0.875rem',
                fontWeight: '800',
                letterSpacing: '0.05em',
                borderRadius: '9999px',
                border: '2px solid #0f172a',
                background: activeTab === item.id && !item.scrollTo ? '#f97316' : '#ffffff',
                color: activeTab === item.id && !item.scrollTo ? '#ffffff' : '#0f172a',
                boxShadow: '2px 2px 0px #0f172a',
                cursor: 'pointer',
                textAlign: 'center'
              }}
            >
              {item.label}
            </button>
          ))}
        </div>
      )}
    </div>
  );
};

export default Navbar;
