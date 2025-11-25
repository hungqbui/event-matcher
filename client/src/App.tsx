import { Routes, Route } from "react-router-dom";
import { AuthProvider } from "./contexts/AuthContext";
import { ProtectedRoute } from "./components/ProtectedRoute";
import HomePage from "./Homepage";
import Login from "./Auth/Login";
import Signup from "./Auth/Signup";
import EventListingPage from "./pages/EventListing";
import EventView from "./pages/EventView";
import ProfileForm from "./profile/profile";
import VolunteerHistory from "./admin/volunteerhistory";
import VolunteerMatchingForm from "./admin/VolunteerMatchingForm";
import HistoryListing from './pages/HistoryListing.tsx';
import Leaderboard from './pages/Leaderboard.tsx';

function App() {
  return (
    <AuthProvider>
      <Routes>
        <Route path="/" element={<HomePage />} />
        <Route path="/login" element={<Login />} />
        <Route path="/signup" element={<Signup />} />
        <Route 
          path="/admin/events" 
          element={
            <ProtectedRoute requireAdmin>
              <EventListingPage />
            </ProtectedRoute>
          } 
        />
        <Route 
          path="/events" 
          element={
            <EventView />
          } 
        />
        <Route
          path="/profile"
          element={
            <ProtectedRoute>
              <ProfileForm />
            </ProtectedRoute>
          }
        />
        <Route 
          path="/admin/volunteers" 
          element={
            <ProtectedRoute requireAdmin>
              <VolunteerHistory />
            </ProtectedRoute>
          } 
        />
        <Route 
          path="/admin/matching" 
          element={
            <ProtectedRoute requireAdmin>
              <VolunteerMatchingForm />
            </ProtectedRoute>
          } 
        />
        <Route 
          path="/history" 
          element={
            <ProtectedRoute>
              <HistoryListing />
            </ProtectedRoute>
          } 
        />
        <Route 
          path="/leaderboard" 
          element={<Leaderboard />} 
        />
      </Routes>
    </AuthProvider>
  );
}

export default App;
