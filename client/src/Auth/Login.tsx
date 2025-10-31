import React, { useState } from "react";
import { useNavigate } from "react-router-dom";
import "./Login.css";
import VolunteerHome from "../assets/Volunteer_home.jpg";
import PinePal from "../assets/pineLogo.webp";
import Navbar from "../components/Navbar";
import Footer from "../components/Footer";
import { login } from "../utils/auth";

const Login: React.FC = () => {
  const nav = useNavigate();
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [submitting, setSubmitting] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [showPassword, setShowPassword] = useState(false);

  const onSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (submitting) return;

    setError(null);
    const payload = {
      email: email.trim().toLowerCase(),
      password,
    };

    if (!payload.email || !payload.password) {
      setError("Please enter both email and password.");
      return;
    }

    setSubmitting(true);
    try {
      // Use the auth utility to handle JWT tokens
      const data = await login(payload.email, payload.password);
      
      // Store user name for backward compatibility
      localStorage.setItem("pp_user_name", data.user.name);
      
      // Redirect to homepage or admin panel based on role
      if (data.user.role === 'admin') {
        nav("/event-listing"); // or admin dashboard
      } else {
        nav("/");
      }
    } catch (err: any) {
      setError(err.message || "Login failed. Please try again.");
    } finally {
      setSubmitting(false);
    }
  };

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

            <form className="login-form" onSubmit={onSubmit} noValidate>
              <label className="sr-only" htmlFor="email">Email</label>
              <input
                id="email"
                type="email"
                placeholder="Email"
                autoComplete="email"
                required
                value={email}
                onChange={(e) => setEmail(e.target.value)}
                disabled={submitting}
              />

              <label className="sr-only" htmlFor="password">Password</label>
              <div className="password-field">
                <input
                  id="password"
                  type={showPassword ? "text" : "password"}
                  placeholder="Password"
                  autoComplete="current-password"
                  required
                  value={password}
                  onChange={(e) => setPassword(e.target.value)}
                  disabled={submitting}
                />
                <button
                  type="button"
                  className="toggle-password"
                  onClick={() => setShowPassword((v) => !v)}
                  disabled={submitting}
                  aria-label={showPassword ? "Hide password" : "Show password"}
                >
                  {showPassword ? "Hide" : "Show"}
                </button>
              </div>

              <button type="submit" className="login-btn" disabled={submitting}>
                {submitting ? "Logging in..." : "Login"}
              </button>

              {error && (
                <div className="form-error" role="alert" aria-live="assertive">
                  {error}
                </div>
              )}
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
