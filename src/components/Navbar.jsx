import { useState } from 'react';
import { Link, useLocation } from 'react-router-dom';
import { ScanEye, Menu, X } from 'lucide-react';
import { isInMockMode } from '../services/inspectionApi.js';

/**
 * VEERA Navigation Bar
 *
 * Displays the VEERA wordmark, navigation links, and a mock-mode indicator.
 * Responsive: collapses to hamburger menu on mobile.
 */
export default function Navbar() {
  const [mobileOpen, setMobileOpen] = useState(false);
  const location = useLocation();
  const mockMode = isInMockMode();

  const isActive = (path) => location.pathname === path;

  return (
    <nav className="navbar" role="navigation" aria-label="Main navigation">
      <div className="container">
        <Link to="/" className="navbar__brand" aria-label="VEERA — Home">
          <ScanEye size={22} className="navbar__brand-icon" aria-hidden="true" />
          VEERA
        </Link>

        <button
          className="navbar__toggle"
          onClick={() => setMobileOpen(!mobileOpen)}
          aria-expanded={mobileOpen}
          aria-label={mobileOpen ? 'Close navigation menu' : 'Open navigation menu'}
        >
          {mobileOpen ? <X size={22} /> : <Menu size={22} />}
        </button>

        <ul className={`navbar__links ${mobileOpen ? 'navbar__links--open' : ''}`}>
          <li>
            <Link
              to="/"
              className={`navbar__link ${isActive('/') ? 'navbar__link--active' : ''}`}
              onClick={() => setMobileOpen(false)}
            >
              Inspection
            </Link>
          </li>
          <li>
            <Link
              to="/about"
              className={`navbar__link ${isActive('/about') ? 'navbar__link--active' : ''}`}
              onClick={() => setMobileOpen(false)}
            >
              Methodology
            </Link>
          </li>
          {mockMode && (
            <li>
              <span className="navbar__mock-badge" title="Using demonstration data — no backend connected">
                Mock Mode
              </span>
            </li>
          )}
        </ul>
      </div>
    </nav>
  );
}
