import React, { useState } from "react";
import { useNavigate } from "react-router-dom";
import "./Login.css";
import VolunteerHome from "../assets/Volunteer_home.jpg";
import PinePal from "../assets/pineLogo.webp";
import Navbar from "../components/Navbar";
import Footer from "../components/Footer";

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
      // Login.tsx - in fetch options
        const res = await fetch(`/api/login`, {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          // credentials: "include", // ← remove this
          body: JSON.stringify(payload),
        });


      const data = await res.json().catch(() => ({}));

      if (!res.ok) {
        setError(data?.message || "Invalid email or password.");
        return;
      }

      // Backend returns: { message, id, name, email, state }
      localStorage.setItem("pp_user_name", data?.user.name ?? "");
      localStorage.setItem("pp_user_id", data?.user.id ?? "");

      nav("/"); // redirect to homepage
    } catch {
      setError("Network error. Ensure the server is running and CORS is enabled.");
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
