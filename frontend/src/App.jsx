import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import Login from './pages/Login';
import Landing from './pages/Landing';
import Register from './pages/Register';
import Dashboard from './pages/Dashboard';
import MainLayout from './components/MainLayout'; // Import the wrapper

function App() {
  return (
    <Router>
      <Routes>
        {/* --- PUBLIC ROUTES (No Navbar, No Auth Check) --- */}
        <Route path="/" element={<Landing />} />
        <Route path="/login" element={<Login />} />
        <Route path="/register" element={<Register />} />
        
        {/* --- PROTECTED ROUTES (Has Navbar + Auth Check) --- */}
        {/* Everything inside this Route tag gets wrapped by MainLayout */}
        <Route element={<MainLayout />}>
            
            {/* The Dashboard will now appear INSIDE the MainLayout */}
            <Route path="/dashboard" element={<Dashboard />} />
            
            {/* Future routes go here too */}
            {/* <Route path="/appointments" element={<Appointments />} /> */}
            {/* <Route path="/profile" element={<Profile />} /> */}
            
        </Route>

      </Routes>
    </Router>
  );
}

export default App;