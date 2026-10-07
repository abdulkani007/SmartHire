import React, { useState, useEffect } from 'react';
import SHLogoBadge from './SHLogoBadge';

const Navbar = ({ activeTab, setActiveTab }) => {
  const [mobileMenuOpen, setMobileMenuOpen] = useState(false);
  const [scrolled, setScrolled] = useState(false);
  const [isMobile, setIsMobile] = useState(false);

  useEffect(() => {
    const handleScroll = () => {
      setScrolled(window.scrollY > 15);
    };
    const handleResize = () => {
      setIsMobile(window.innerWidth < 768);
    };

    handleResize();
    window.addEventListener('scroll', handleScroll);
    window.addEventListener('resize', handleResize);
    return () => {
      window.removeEventListener('scroll', handleScroll);
      window.removeEventListener('resize', handleResize);
    };
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
        padding: isMobile ? '0 8px' : '0 16px',
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
          boxShadow: scrolled ? '5px 5px 0px #0f172a' : '3px 3px 0px #0f172a',
          padding: isMobile ? '6px 12px' : '8px 18px',
          display: 'flex',
          justifyContent: 'space-between',
          alignItems: 'center',
          transition: 'all 0.3s cubic-bezier(0.16, 1, 0.3, 1)',
          backdropFilter: 'blur(12px)',
          WebkitBackdropFilter: 'blur(12px)'
        }}
      >
        {/* Left: SH Logo Badge with 4 Orbiting Curved Arcs + Brand Title */}
        <div 
          onClick={() => handleNavClick('home')}
          style={{ cursor: 'pointer', display: 'flex', alignItems: 'center', gap: '0.6rem' }}
          className="group"
        >
          <SHLogoBadge size={isMobile ? 32 : 38} showDot={true} animate={false} />

          <div>
            <div style={{ fontSize: isMobile ? '1.05rem' : '1.15rem', fontWeight: '800', letterSpacing: '-0.025em', color: '#0f172a', lineHeight: 1.1 }}>
              Smart<span style={{ color: '#f97316' }}>Hire</span>
            </div>
            {!isMobile && (
              <div style={{ fontSize: '0.58rem', fontWeight: '800', color: '#64748b', letterSpacing: '0.08em', textTransform: 'uppercase' }}>
                Career Intelligence Engine
              </div>
            )}
          </div>
        </div>

        {/* Desktop Only Navigation Links */}
        {!isMobile && (
          <nav style={{ display: 'flex', alignItems: 'center', gap: '1.5rem' }}>
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
                  padding: '4px 8px',
                  borderRadius: '9999px',
                  transition: 'all 0.2s ease'
                }}
              >
                {item.label}
              </button>
            ))}
          </nav>
        )}

        {/* Desktop Only Action Pill Button */}
        {!isMobile && (
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
          >
            <span>ANALYZE AI</span>
            <span style={{ fontSize: '0.9rem' }}>↗</span>
          </button>
        )}

        {/* Mobile Only Hamburger Menu Toggle */}
        {isMobile && (
          <button
            onClick={() => setMobileMenuOpen(!mobileMenuOpen)}
            style={{
              background: '#ffffff',
              border: '2px solid #0f172a',
              borderRadius: '9999px',
              width: '34px',
              height: '34px',
              display: 'flex',
              alignItems: 'center',
              justifyContent: 'center',
              cursor: 'pointer',
              boxShadow: '1.5px 1.5px 0px #0f172a',
              padding: 0
            }}
            aria-label="Toggle Navigation"
          >
            <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="#0f172a" strokeWidth="2.5" strokeLinecap="round" strokeLinejoin="round">
              {mobileMenuOpen ? (
                <path d="M18 6L6 18M6 6l12 12" />
              ) : (
                <path d="M4 6h16M4 12h16M4 18h16" />
              )}
            </svg>
          </button>
        )}
      </header>

      {/* Mobile Floating Drawer Card */}
      {isMobile && mobileMenuOpen && (
        <div 
          style={{
            width: '100%',
            maxWidth: '1180px',
            marginTop: '8px',
            background: '#ffffff',
            border: '2px solid #0f172a',
            borderRadius: '20px',
            boxShadow: '4px 4px 0px #0f172a',
            padding: '12px',
            display: 'flex',
            flexDirection: 'column',
            gap: '8px'
          }}
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
                padding: '10px 14px',
                fontSize: '0.85rem',
                fontWeight: '800',
                letterSpacing: '0.05em',
                borderRadius: '9999px',
                border: '1.5px solid #0f172a',
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

          <button
            onClick={() => handleNavClick('home', 'upload-section')}
            style={{
              width: '100%',
              padding: '10px 14px',
              fontSize: '0.85rem',
              fontWeight: '800',
              letterSpacing: '0.05em',
              borderRadius: '9999px',
              border: '2px solid #0f172a',
              background: '#f97316',
              color: '#ffffff',
              boxShadow: '2px 2px 0px #0f172a',
              cursor: 'pointer',
              textAlign: 'center',
              display: 'flex',
              alignItems: 'center',
              justifyContent: 'center',
              gap: '6px'
            }}
          >
            <span>ANALYZE AI</span>
            <span>↗</span>
          </button>
        </div>
      )}
    </div>
  );
};

export default Navbar;
