import { Routes, Route } from 'react-router-dom';
import HomePage from './Homepage';
import Login from './Auth/Login';
import Signup from './Auth/Signup';
import EventListingPage from './pages/EventListing';
import ProfileForm from './profile/profile';
import VolunteerHistory from "./admin/volunteerhistory";


function App() {
  return (
    <Routes>
      <Route path="/" element={<HomePage />} />
      <Route path="/login" element={<Login />} />
      <Route path="/signup" element={<Signup />} />
      <Route path="/events" element={<EventListingPage />} />
      <Route path="/profile" element={<ProfileForm user={{name: '', email: ''}} onSave={() => {}} />} />
      <Route path="/admin/volunteers" element={<VolunteerHistory />} />
    </Routes>
  );
}

export default App;
