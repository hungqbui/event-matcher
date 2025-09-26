import { Link } from "react-router-dom";
import "./Navbar.css";
import PinePal from "../assets/pineLogo.webp";

const Navbar = () => {
  return (
    <nav className="navbar">
        <Link to="/" className="logo-container">
        <img src={PinePal} alt="Pine Pals Logo" />
        <h1 className="logo-text">Pine Pals</h1>
      </Link>

      <div className="nav-tabs">
        <Link to="/mission" className="nav-tab">Our Mission</Link>
        <Link to="/about" className="nav-tab">About Us</Link>
        <Link to="/faq" className="nav-tab">FAQ</Link>
        <Link to="/programs" className="nav-tab">Volunteer Programs</Link>
        <Link to="/get-involved" className="nav-tab">Get Involved</Link>
      </div>

      <div className="auth-buttons">
        <Link to="/login" className="nav-btn">Login</Link>
        <Link to="/signup" className="nav-btn primary">Sign Up</Link>
      </div>
    </nav>
  );
};

export default Navbar;