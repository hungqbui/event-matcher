import Navbar from "./components/Navbar";
import Footer from "./components/Footer";
import "./HomePage.css";
import VolunteerHome from "./assets/Volunteer_home.jpg";
import MissionCarousel from "./components/MissionCarousel";
import VCleanUp from "./assets/VCleanupHome.webp";
import FoodDrive from "./assets/FoodDrive.jpg";
import TreePlant from "./assets/TreePlant.jpg";
import DisasterRelief from "./assets/DisasterRelief.jpg";
import BloodDrive from "./assets/BloodDrive.webp";
import YouthMentor from "./assets/YouthMentor.jpg";
const HomePage = () => {
  return (
    <>
      <Navbar />
      <div className="home">

        <section
          className="hero"
          style={{ backgroundImage: `url(${VolunteerHome})` }}
        >
          <div className="hero-overlay">
            <h1>Volunteer With Us</h1>
            <p>
              Thank you for caring about our community. Your time and skills
              make all the difference — now more than ever!
            </p>
            <button className="primary-btn">Find Opportunities</button>
          </div>
        </section>


        <section className="mission-section">
          <h2 className="section-header">Our Mission</h2>
          <MissionCarousel />
        </section>


        <section className="programs">
          <h2 className="section-header">Volunteer Programs</h2>
          <div className="program-cards">
            <div className="card">
              <img src={VCleanUp} alt="Community Clean-Up" />
              <div className="overlay">
                <h3>Community Clean-Up</h3>
              </div>
            </div>
            <div className="card">
              <img src={DisasterRelief} alt="Disaster Relief" />
              <div className="overlay">
                <h3>Disaster Relief</h3>
              </div>
            </div>
            <div className="card">
              <img src={YouthMentor} alt="Youth Mentor" />
              <div className="overlay">
                <h3>Youth Mentorship</h3>
              </div>
            </div>
            <div className="card">
              <img src={BloodDrive} alt="Blood Drive" />
              <div className="overlay">
                <h3>Blood Drive</h3>
              </div>
            </div>
            <div className="card">
              <img src={TreePlant} alt="Tree Planting" />
              <div className="overlay">
                <h3>Tree Planting</h3>
              </div>
            </div>
            <div className="card">
              <img src={FoodDrive} alt="Food Drive" />
              <div className="overlay">
                <h3>Food Drives</h3>
              </div>
            </div>



          </div>
        </section>
      </div>
      <Footer />
    </>
  );
};

export default HomePage;
