// components/Navbar.js
import { AppBar, Toolbar, Typography, Button, Box } from '@mui/material';
import { useNavigate } from 'react-router-dom';

const Navbar = ({ user, onLogout }) => {
    const navigate = useNavigate();
    const role = user?.roles?.[0]; // Assuming roles is an array like ["Patient"]

    return (
        <AppBar position="static">
            <Toolbar>
                <Typography variant="h6" sx={{ flexGrow: 1 }}>
                    AKHS - {role || 'Guest'}
                </Typography>

                {/* --- COMMON LINKS (Everyone sees these) --- */}
                <Button color="inherit" onClick={() => navigate('/dashboard')}>
                    Home
                </Button>

                {/* --- PATIENT ONLY LINKS --- */}
                {role === 'Patient' && (
                    <>
                        <Button color="inherit" onClick={() => navigate('/book-appointment')}>
                            Book Appointment
                        </Button>
                        <Button color="inherit" onClick={() => navigate('/history')}>
                            Medical History
                        </Button>
                    </>
                )}

                {/* --- DOCTOR ONLY LINKS --- */}
                {role === 'Doctor' && (
                    <>
                        <Button color="inherit" onClick={() => navigate('/doctor/schedule')}>
                            My Schedule
                        </Button>
                        <Button color="inherit" onClick={() => navigate('/doctor/patients')}>
                            My Patients
                        </Button>
                    </>
                )}

                {/* --- ADMIN ONLY LINKS --- */}
                {role === 'Admin' && (
                    <Button color="inherit" onClick={() => navigate('/admin/users')}>
                        Manage Users
                    </Button>
                )}

                <Button color="inherit" onClick={onLogout} sx={{ ml: 2, bgcolor: 'error.main' }}>
                    Logout
                </Button>
            </Toolbar>
        </AppBar>
    );
};

export default Navbar;