import React, { useState } from "react";
import "./Signup.css";
import PinePalLogo from "../assets/pineLogo.webp";
import Home from "../assets/Volunteer_home.jpg";
import Footer from "../components/Footer";
import Navbar from "../components/Navbar";

const states = ["TX", "CA", "NY"];
const skillsOptions = ["Tree Planting", "Disaster Relief", "Youth Mentorship", "Food Drives", "Blood Drives"];

const Signup: React.FC = () => {
  const [form, setForm] = useState({ name: "", email: "", password: "", state: "", skills: [] as string[] });
  const [message, setMessage] = useState("");

  const handleChange = (e: React.ChangeEvent<HTMLInputElement | HTMLSelectElement>) => {
    setForm({ ...form, [e.target.name]: e.target.value });
  };

  const handleSkillsChange = (e: React.ChangeEvent<HTMLSelectElement>) => {
    const selected = Array.from(e.target.selectedOptions, opt => opt.value);
    setForm({ ...form, skills: selected });
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    try {
      const res = await fetch("http://127.0.0.1:5000/api/signup", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(form),
      });
      const data = await res.json();
      if (res.ok) setMessage("Signup successful! You can now log in.");
      else setMessage(data.message);
    } catch {
      setMessage("Server error");
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
            <form className="signup-form" onSubmit={handleSubmit}>
              <label>Full Name *</label>
              <input name="name" value={form.name} onChange={handleChange} required />

              <label>State *</label>
              <select name="state" value={form.state} onChange={handleChange} required>
                <option value="">Select State</option>
                {states.map(s => <option key={s}>{s}</option>)}
              </select>

              <label>Skills *</label>
              <select multiple name="skills" value={form.skills} onChange={handleSkillsChange}>
                {skillsOptions.map(skill => <option key={skill}>{skill}</option>)}
              </select>

              <label>Email *</label>
              <input name="email" type="email" value={form.email} onChange={handleChange} required />

              <label>Password *</label>
              <input name="password" type="password" value={form.password} onChange={handleChange} required />

              <button type="submit" className="signup-btn">Create Account</button>
            </form>
            {message && <p>{message}</p>}
          </div>
        </div>
      </div>
      <Footer />
    </>
  );
};

export default Signup;
