import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import Login from './pages/Login';

function App() {
  return (
    <Router>
      <Routes>
        {/* Set Login as the default page */}
        <Route path="/" element={<Login />} />
        
        {/* We will build this next */}
        <Route path="/dashboard" element={<h1>Dashboard Coming Soon</h1>} />
      </Routes>
    </Router>
  );
}

export default App;