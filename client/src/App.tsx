import { Routes, Route } from 'react-router-dom';
import HomePage from './Homepage';
import Login from './Auth/Login';
import Signup from './Auth/Signup';

function App() {
  return (
    <Routes>
      <Route path="/" element={<HomePage />} />
      <Route path="/login" element={<Login />} />
      <Route path="/signup" element={<Signup />} />

    </Routes>
  );
}

export default App;
