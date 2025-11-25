import React, { useState, useEffect } from "react";
import { useNavigate } from "react-router-dom";
import { useAuth } from "../contexts/AuthContext";
import "./Signup.css";
import PinePalLogo from "../assets/pineLogo.webp";
import Home from "../assets/Volunteer_home.jpg";
import Footer from "../components/Footer";
import Navbar from "../components/Navbar";


const STATES = [
  "AL","AK","AZ","AR","CA","CO","CT","DE","DC","FL","GA","HI","ID","IL","IN","IA","KS","KY","LA",
  "ME","MD","MA","MI","MN","MS","MO","MT","NE","NV","NH","NJ","NM","NY","NC","ND","OH","OK","OR",
  "PA","RI","SC","SD","TN","TX","UT","VT","VA","WA","WV","WI","WY"
];

type FormState = {
  name: string;
  email: string;
  password: string;
  state: string;
  skills: string[];
};

const Signup: React.FC = () => {
  const navigate = useNavigate();
  const { signup } = useAuth();
  const [isAdminSignup, setIsAdminSignup] = useState(false);
  const [form, setForm] = useState<FormState>({
    name: "",
    email: "",
    password: "",
    state: "",
    skills: []
  });
  const [msg, setMsg] = useState<string>("");
  const [submitting, setSubmitting] = useState(false);
  const [availableSkills, setAvailableSkills] = useState<string[]>([]);
  const [loadingSkills, setLoadingSkills] = useState(true);

  useEffect(() => {
    // Fetch skills from the database
    const fetchSkills = async () => {
      try {
        const response = await fetch("/api/skills");
        if (response.ok) {
          const skills = await response.json();
          setAvailableSkills(skills);
        } else {
          setMsg("Failed to load skills. Please refresh the page.");
        }
      } catch (err) {
        setMsg("Error loading skills. Please check your connection.");
      } finally {
        setLoadingSkills(false);
      }
    };

    fetchSkills();
  }, []);

  const handleChange = (
    e: React.ChangeEvent<HTMLInputElement | HTMLSelectElement>
  ) => {
    const { name, value } = e.target;
    setForm((f) => ({ ...f, [name]: value }));
  };

  const handleSkillsChange = (e: React.ChangeEvent<HTMLSelectElement>) => {
    const selected = Array.from(e.target.selectedOptions, (opt) => opt.value);
    setForm((f) => ({ ...f, skills: selected }));
  };

  const isValidEmail = (em: string) => /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(em);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setMsg("");

    // match backend validations
    if (!form.name || !form.email || !form.password || !form.state) {
      setMsg("All fields are required.");
      return;
    }
    if (!isAdminSignup && form.skills.length === 0) {
      setMsg("Please select at least one skill.");
      return;
    }
    if (!isValidEmail(form.email)) {
      setMsg("Please enter a valid email.");
      return;
    }
    if (isAdminSignup && !form.email.endsWith("@pine.edu")) {
      setMsg("Admin registration requires a @pine.edu email address.");
      return;
    }
    if (form.password.length < 6) {
      setMsg("Password must be at least 6 characters long.");
      return;
    }

    try {
      setSubmitting(true);
      await signup(form);
      
      // Store legacy fields for backward compatibility
      const userData = JSON.parse(localStorage.getItem('user') || '{}');
      localStorage.setItem("pp_user_name", userData.name || form.name);
      localStorage.setItem("pp_user_id", userData.id || "");
      
      // Redirect to homepage
      navigate("/");
    } catch (err) {
      setMsg(err instanceof Error ? err.message : "Signup failed.");
    } finally {
      setSubmitting(false);
    }
  };

  return (
    <>
      <Navbar />
      <div className="signup-page" style={{ backgroundImage: `url(${Home})` }}>
        <div className="signup-overlay">
          <div className="signup-card">
            <img src={PinePalLogo} alt="Pine Pals Logo" className="signup-logo" />
            
            <div className="signup-type-toggle">
              <button
                type="button"
                className={`toggle-btn ${!isAdminSignup ? "active" : ""}`}
                onClick={() => setIsAdminSignup(false)}
              >
                Volunteer
              </button>
              <button
                type="button"
                className={`toggle-btn ${isAdminSignup ? "active" : ""}`}
                onClick={() => setIsAdminSignup(true)}
              >
                Admin
              </button>
            </div>

            <h2 className="signup-title">
              {isAdminSignup ? "Admin Registration" : "Volunteer Sign Up"}
            </h2>

            {isAdminSignup && (
              <p className="admin-note">
                ℹ️ Admin accounts require a @pine.edu email address
              </p>
            )}

            <form className="signup-form" onSubmit={handleSubmit} noValidate>
              <label htmlFor="name">Full Name *</label>
              <input
                id="name"
                name="name"
                value={form.name}
                onChange={handleChange}
                required
                disabled={submitting}
              />

              <label htmlFor="state">State *</label>
              <select
                id="state"
                name="state"
                value={form.state}
                onChange={handleChange}
                required
                disabled={submitting}
              >
                <option value="">Select State</option>
                {STATES.map((s) => (
                  <option key={s} value={s}>{s}</option>
                ))}
              </select>

              {!isAdminSignup && (
                <>
                  <label htmlFor="skills">Skills * (hold Ctrl/Cmd to select multiple)</label>
                  <select
                    id="skills"
                    name="skills"
                    multiple
                    value={form.skills}
                    onChange={handleSkillsChange}
                    disabled={submitting || loadingSkills}
                  >
                    {loadingSkills ? (
                      <option disabled>Loading skills...</option>
                    ) : (
                      availableSkills.map((skill) => (
                        <option key={skill} value={skill}>{skill}</option>
                      ))
                    )}
                  </select>
                </>
              )}

              <label htmlFor="email">Email *</label>
              <input
                id="email"
                name="email"
                type="email"
                value={form.email}
                onChange={handleChange}
                required
                autoComplete="email"
                disabled={submitting}
                placeholder={isAdminSignup ? "your.name@pine.edu" : ""}
              />
              {isAdminSignup && !form.email.endsWith("@pine.edu") && form.email.length > 0 && (
                <p className="email-warning">⚠️ Admin email must end with @pine.edu</p>
              )}

              <label htmlFor="password">Password *</label>
              <input
                id="password"
                name="password"
                type="password"
                value={form.password}
                onChange={handleChange}
                required
                autoComplete="new-password"
                disabled={submitting}
                minLength={6}
              />

              <button type="submit" className="signup-btn" disabled={submitting}>
                {submitting ? "Creating..." : "Create Account"}
              </button>

              {msg && <p className="form-message" role="alert">{msg}</p>}
            </form>
          </div>
        </div>
      </div>
      <Footer />
    </>
  );
};

export default Signup;
