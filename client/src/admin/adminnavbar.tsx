import { Link } from "react-router-dom";
import "./AdminNavbar.css";
import { useAuth } from "../contexts/AuthContext";
import { useNavigate } from "react-router-dom";

export default function AdminNavbar() {
  const { logout } = useAuth();
  const navigate = useNavigate();
  return (
    <nav className="admin-navbar">
      <div className="admin-logo-container">
        <h1 className="admin-logo-text" onClick={() => navigate("/")}>Admin Panel</h1>
      </div>

      <div className="admin-nav-tabs">
        <Link to="/admin/matching" className="admin-nav-tab">
          Match
        </Link>
        <Link to="/admin/events" className="admin-nav-tab">
          Event Management
        </Link>
        <Link to="/admin/volunteers" className="admin-nav-tab">
          Volunteers
        </Link>

      </div>

      <div className="admin-auth-buttons" onClick={logout}>
        Logout
      </div>
    </nav>
  );
}
