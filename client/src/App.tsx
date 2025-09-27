import { Routes, Route } from 'react-router-dom';
import HomePage from './Homepage';
import Login from './Auth/Login';
import Signup from './Auth/Signup';
import EventListingPage from './pages/EventListing';
import HistoryListing from './pages/HistoryListing.tsx';

function App() {
  return (
    <Routes>
      <Route path="/" element={<HomePage />} />
      <Route path="/login" element={<Login />} />
      <Route path="/signup" element={<Signup />} />
      <Route path="/events" element={<EventListingPage />} />
      <Route path="/history" element={<HistoryListing />} />
    </Routes>
  );
}

export default App;
