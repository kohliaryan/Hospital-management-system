import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import Login from './pages/Login';
import Landing from './pages/Landing';
import Register from './pages/Register';

function App() {
  return (
    <Router>
      <Routes>
        {/* Set Login as the default page */}
        <Route path="/login" element={<Login />} />
        <Route path="/" element={<Landing />} />
        <Route path="/register" element={<Register />} />
        
        {/* We will build this next */}
        <Route path="/dashboard" element={<h1>Dashboard Coming Soon</h1>} />
      </Routes>
    </Router>
  );
}

export default App;