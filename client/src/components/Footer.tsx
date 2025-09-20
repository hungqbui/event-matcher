// Footer.jsx
import "./Footer.css";

const Footer = () => {
  return (
    <footer className="footer">
      <div className="footer-content">
        <div className="footer-section about">
          <h3>About Us</h3>
          <p>
            Connecting volunteers with meaningful opportunities to create lasting change in our community.
          </p>
        </div>

        <div className="footer-section links">
          <h3>Quick Links</h3>
          <ul>
            <li><a href="/">Home</a></li>
            <li><a href="/mission">Our Mission</a></li>
            <li><a href="/programs">Volunteer Programs</a></li>
            <li><a href="/contact">Contact</a></li>
          </ul>
        </div>

        <div className="footer-section contact">
          <h3>Contact</h3>
          <p>Email: PinePals@volunteer.org</p>
          <p>Phone: +1 555 123 4567</p>
          <p>Address: 123 Pinepal St, City, State</p>
        </div>
      </div>

      <div className="footer-bottom">
        <p>&copy; {new Date().getFullYear()} PinePals Organization. All rights reserved.</p>
      </div>
    </footer>
  );
};

export default Footer;
