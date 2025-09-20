import React, { useState } from "react";
import "./Signup.css";
import PinePalLogo from "../assets/pineLogo.webp";
import Home from "../assets/Volunteer_home.jpg";
import Footer from "../components/Footer";
import Navbar from "../components/Navbar";
const states = ["AL","AK","AZ","AR","CA","CO","CT","DE","FL","GA","HI","ID","IL","IN","IA","KS","KY","LA","ME","MD","MA","MI","MN","MS","MO","MT","NE","NV","NH","NJ","NM","NY","NC","ND","OH","OK","OR","PA","RI","SC","SD","TN","TX","UT","VT","VA","WA","WV","WI","WY"];
const skillsOptions = ["Tree Planting", "Disaster Relief", "Youth Mentorship", "Food Drives", "Blood Drives"];

const Signup: React.FC = () => {
  const [skills, setSkills] = useState<string[]>([]);

  const handleSkillsChange = (e: React.ChangeEvent<HTMLSelectElement>) => {
    const selected = Array.from(e.target.selectedOptions, option => option.value);
    setSkills(selected);
  };

  return (
    <>
    <Navbar />
    <div className="signup-page" style={{ backgroundImage: `url(${Home})` }}>
      <div className="signup-overlay">
        <div className="signup-card">
          <img src={PinePalLogo} alt="Pine Pals Logo" className="signup-logo" />
          <h2 className="signup-title">Volunteer Sign Up</h2>
          <form className="signup-form">
            <label>Full Name *</label>
            <input type="text" placeholder="Enter your full name" maxLength={50} required />

            <label>Address 1 *</label>
            <input type="text" placeholder="Street Address" maxLength={100} required />

            <label>Address 2</label>
            <input type="text" placeholder="Apt, Suite, etc. (Optional)" maxLength={100} />

            <label>City *</label>
            <input type="text" placeholder="City" maxLength={100} required />

            <label>State *</label>
            <select required>
              <option value="">Select State</option>
              {states.map(state => (
                <option key={state} value={state}>{state}</option>
              ))}
            </select>

            <label>Zip Code *</label>
            <input type="text" placeholder="Zip Code" maxLength={9} required />

            <label>Skills *</label>
            <select multiple required value={skills} onChange={handleSkillsChange} className="skills-select">
              {skillsOptions.map(skill => (
                <option key={skill} value={skill}>{skill}</option>
              ))}
            </select>

            <label>Preferences</label>
            <textarea placeholder="Any preferences or notes (Optional)"></textarea>

            <label>Availability *</label>
            <input type="date" required />

            <label>Email *</label>
            <input type="email" placeholder="Enter your email" required />

            <label>Password *</label>
            <input type="password" placeholder="Enter a password" required />

            <button type="submit" className="signup-btn">Create Account</button>
          </form>
        </div>
      </div>
    </div>
    <Footer />
    </>
  );
};

export default Signup;
