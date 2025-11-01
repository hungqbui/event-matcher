import React, { useState } from "react";
import { useNavigate } from "react-router-dom";
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

const SKILLS = [
  "Tree Planting","Disaster Relief","Youth Mentorship","Food Drives","Blood Drives",
  "Gardening","Organizing","First Aid","Teaching","Teamwork","Environmental Awareness"
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
  const [form, setForm] = useState<FormState>({
    name: "",
    email: "",
    password: "",
    state: "",
    skills: []
  });
  const [msg, setMsg] = useState<string>("");
  const [submitting, setSubmitting] = useState(false);

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
    if (!form.name || !form.email || !form.password || !form.state || form.skills.length === 0) {
      setMsg("All fields are required (including at least one skill).");
      return;
    }
    if (!isValidEmail(form.email)) {
      setMsg("Please enter a valid email.");
      return;
    }
    if (form.password.length < 6) {
      setMsg("Password must be at least 6 characters long.");
      return;
    }

    try {
      setSubmitting(true);
      const res = await fetch(`/api/signup`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(form),
      });
      const data = await res.json().catch(() => ({}));

      if (res.ok) {
        // Optionally stash a name for a welcome toast on the homepage
        localStorage.setItem("pp_user_name", data?.user?.name ?? form.name);
        localStorage.setItem("pp_user_id", data?.user?.id ?? "");
        // Redirect to homepage
        navigate("/");
        return;
      }

      setMsg(data?.message || "Signup failed.");
    } catch {
      setMsg("Server error. Check that the backend is running and CORS is enabled.");
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
            <h2 className="signup-title">Volunteer Sign Up</h2>

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

              <label htmlFor="skills">Skills * (hold Ctrl/Cmd to select multiple)</label>
              <select
                id="skills"
                name="skills"
                multiple
                value={form.skills}
                onChange={handleSkillsChange}
                disabled={submitting}
              >
                {SKILLS.map((skill) => (
                  <option key={skill} value={skill}>{skill}</option>
                ))}
              </select>

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
              />

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
