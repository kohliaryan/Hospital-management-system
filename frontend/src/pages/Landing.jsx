import React from 'react';
import { useNavigate } from 'react-router-dom';
import { AppBar, Toolbar, Typography, Button, Box, Container } from '@mui/material';
import LocalHospitalIcon from '@mui/icons-material/LocalHospital'; // Optional icon

const Landing = () => {
    const navigate = useNavigate();

    return (
        <Box sx={{ minHeight: '100vh', display: 'flex', flexDirection: 'column' }}>
            
            {/* --- 1. Top Navigation Bar --- */}
            <AppBar position="static" color="transparent" elevation={0} sx={{ paddingY: 1 }}>
                <Toolbar>
                    {/* Logo Area */}
                    <LocalHospitalIcon color="primary" sx={{ mr: 1, fontSize: 32 }} />
                    <Typography 
                        variant="h6" 
                        component="div" 
                        sx={{ flexGrow: 1, fontWeight: 'bold', color: '#1976d2' }}
                    >
                        AKHS
                    </Typography>

                    {/* Login Button (Upper Right) */}
                    <Button 
                        variant="outlined" 
                        color="primary" 
                        onClick={() => navigate('/login')}
                        sx={{ borderRadius: '20px', px: 3 }}
                    >
                        Log In
                    </Button>
                </Toolbar>
            </AppBar>

            {/* --- 2. Main Hero Section --- */}
            <Box 
                sx={{ 
                    flexGrow: 1,
                    display: 'flex', 
                    alignItems: 'center', 
                    justifyContent: 'center',
                    background: 'linear-gradient(135deg, #e3f2fd 0%, #f5f5f5 100%)', // Soft medical blue gradient
                }}
            >
                <Container maxWidth="md" sx={{ textAlign: 'center' }}>
                    
                    {/* Main Headline */}
                    <Typography 
                        variant="h2" 
                        component="h1" 
                        sx={{ 
                            fontWeight: '800', 
                            color: '#0d47a1', 
                            mb: 2,
                            fontSize: { xs: '2.5rem', md: '4rem' } // Responsive font size
                        }}
                    >
                        Welcome to <br />
                        Aryan Kohli Hospital Services
                    </Typography>

                    {/* Subtitle */}
                    <Typography 
                        variant="h5" 
                        color="text.secondary" 
                        sx={{ mb: 6, fontWeight: 'light' }}
                    >
                        Compassionate care, advanced medicine, and a commitment to your well-being.
                    </Typography>

                    {/* Register Now Button (In Between) */}
                    <Button 
                        variant="contained" 
                        color="primary" 
                        size="large"
                        onClick={() => navigate('/register')}
                        sx={{ 
                            padding: '15px 50px', 
                            fontSize: '1.2rem', 
                            borderRadius: '50px',
                            boxShadow: '0px 10px 20px rgba(25, 118, 210, 0.3)',
                            '&:hover': {
                                transform: 'scale(1.05)',
                                transition: 'all 0.2s ease-in-out'
                            }
                        }}
                    >
                        Register Now
                    </Button>

                </Container>
            </Box>
        </Box>
    );
}

export default Landing;