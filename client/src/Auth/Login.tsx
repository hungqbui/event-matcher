import React from "react";
import "./Login.css";
import VolunteerHome from "../assets/Volunteer_home.jpg"; 
import PinePal from "../assets/pineLogo.webp"; 
import Navbar from "../components/Navbar";
import Footer from "../components/Footer";
const Login: React.FC = () => {
  return (
    <>
    <Navbar />
    <div
      className="login-page"
      style={{ backgroundImage: `url(${VolunteerHome})` }}
    >
      <div className="login-overlay">
        <div className="login-card">
           <div className="login-header">
          <img src={PinePal} alt="Pine Pals Logo" className="login-logo" />
          <h1 className="login-name">Pine Pals</h1>
        </div>
          <h2 className="login-title">Welcome Back</h2>
          <form className="login-form">
            <input type="email" placeholder="Email" required />
            <input type="password" placeholder="Password" required />
            <button type="submit" className="login-btn">Login</button>
          </form>
          <p className="signup-link">
            Don’t have an account? <a href="/signup">Sign up</a>
          </p>
        </div>
      </div>
    </div>
    <Footer />
    </>
  );
};

export default Login;
