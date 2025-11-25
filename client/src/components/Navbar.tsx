import { Link, useNavigate } from "react-router-dom";
import { useState, useRef, useEffect } from "react";
import "./Navbar.css";
import PinePal from "../assets/pineLogo.webp";
import NotificationSystem from "./NotificationSystem";
import { useAuth } from "../contexts/AuthContext";
import AdminNavbar from "../admin/adminnavbar";

const Navbar = () => {
  const { isAuthenticated, user, isAdmin, logout } = useAuth();
  const navigate = useNavigate();
  const [dropdownOpen, setDropdownOpen] = useState(false);
  const dropdownRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    const handleClickOutside = (event: MouseEvent) => {
      if (dropdownRef.current && !dropdownRef.current.contains(event.target as Node)) {
        setDropdownOpen(false);
      }
    };

    document.addEventListener("mousedown", handleClickOutside);
    return () => document.removeEventListener("mousedown", handleClickOutside);
  }, []);

  const handleLogout = () => {
    logout();
    setDropdownOpen(false);
    navigate("/");
  };

  if (isAuthenticated && isAdmin) {
    return <nav>
        <AdminNavbar />
        { isAuthenticated && <NotificationSystem />}
    </nav>;
  }

  return (
    <nav className="navbar">
      <Link to="/" className="logo-container">
        <img src={PinePal} alt="Pine Pals Logo" />
        <h1 className="logo-text">Pine Pals</h1>
      </Link>

      <div className="nav-tabs">
        <Link to="/events" className="nav-tab">
          Browse Events
        </Link>
      </div>

      <div className="navbar-right">
        {
          !isAuthenticated ?
          <div className="auth-buttons">
            <Link to="/login" className="nav-btn">
              Login
            </Link>
            <Link to="/signup" className="nav-btn primary">
              Sign Up
            </Link>
          </div>
          : 
          <div className="user-menu" ref={dropdownRef}>
            <button 
              className="user-menu-button" 
              onClick={() => setDropdownOpen(!dropdownOpen)}
              aria-expanded={dropdownOpen}
              aria-haspopup="true"
            >
              <span className="user-avatar">{user?.name?.charAt(0).toUpperCase()}</span>
              <span className="user-name">{user?.name}</span>
              <span className={`dropdown-arrow ${dropdownOpen ? 'open' : ''}`}>▼</span>
            </button>
            {dropdownOpen && (
              <div className="user-dropdown">
                <Link 
                  to="/profile" 
                  className="dropdown-item"
                  onClick={() => setDropdownOpen(false)}
                >
                  <span className="dropdown-icon">👤</span>
                  View Profile
                </Link>
                <Link 
                  to="/history" 
                  className="dropdown-item"
                  onClick={() => setDropdownOpen(false)}
                >
                  <span className="dropdown-icon">📋</span>
                  Volunteer History
                </Link>
                <button 
                  className="dropdown-item logout-item"
                  onClick={handleLogout}
                >
                  <span className="dropdown-icon">🚪</span>
                  Log Out
                </button>
              </div>
            )}
          </div>
        }
        { isAuthenticated && <NotificationSystem />}
      </div>
    </nav>
  );

};

export default Navbar;
