import { Link } from "react-router-dom";
import "./AdminNavbar.css";

export default function AdminNavbar() {
  return (
    <nav className="admin-navbar">
      <div className="admin-logo-container">
        <h1 className="admin-logo-text">Admin Panel</h1>
      </div>

      <div className="admin-nav-tabs">
        <Link to="/admin/dashboard" className="admin-nav-tab">Match</Link>
        <Link to="/admin/events" className="admin-nav-tab">Event Management</Link>
        <Link to="/admin/volunteers" className="admin-nav-tab">Volunteers</Link>
        <Link to="/admin/history" className="admin-nav-tab">Participation History</Link>
      </div>

      <div className="admin-auth-buttons">
        <Link to="/logout" className="admin-nav-btn">Logout</Link>
      </div>
    </nav>
  );
}
