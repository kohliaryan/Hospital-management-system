import { useState } from 'react';
import api from '../api/axios';
import { useNavigate } from 'react-router-dom';
// Added 'Link' to the imports
import { Container, TextField, Button, Typography, Box, Paper, Alert, Link } from '@mui/material';

const Login = () => {
    const [email, setEmail] = useState('');
    const [password, setPassword] = useState('');
    const [error, setError] = useState('');
    const navigate = useNavigate();

    const handleLogin = async (e) => {
        e.preventDefault();
        setError('');

        try {
            const response = await api.post('/login', {
                email: email,
                password: password
            });

            console.log("Login Successful:", response.data);
            navigate('/dashboard');

        } catch (err) {
            console.error(err);
            setError('Invalid email or password');
        }
    };

    return (
        <Container maxWidth="xs">
            <Box 
                display="flex" 
                flexDirection="column" 
                alignItems="center" 
                justifyContent="center" 
                minHeight="100vh"
            >
                <Paper elevation={3} sx={{ padding: 4, borderRadius: 2, width: '100%' }}>
                    <Typography variant="h4" component="h1" align="center" gutterBottom color="primary">
                        Hospital Login
                    </Typography>
                    
                    {error && <Alert severity="error" sx={{ mb: 2 }}>{error}</Alert>}

                    <form onSubmit={handleLogin}>
                        <TextField
                            label="Email Address"
                            variant="outlined"
                            fullWidth
                            margin="normal"
                            value={email}
                            onChange={(e) => setEmail(e.target.value)}
                            required
                        />
                        <TextField
                            label="Password"
                            type="password"
                            variant="outlined"
                            fullWidth
                            margin="normal"
                            value={password}
                            onChange={(e) => setPassword(e.target.value)}
                            required
                        />
                        
                        <Button 
                            type="submit" 
                            variant="contained" 
                            color="primary" 
                            fullWidth 
                            size="large"
                            sx={{ mt: 2 }}
                        >
                            Sign In
                        </Button>
                    </form>

                    {/* --- NEW SECTION: Register Link --- */}
                    <Box sx={{ mt: 3, textAlign: 'center' }}>
                        <Typography variant="body2" color="text.secondary">
                            New to AKHS? {' '}
                            <Link 
                                component="button" 
                                variant="body2" 
                                onClick={() => navigate('/register')}
                                sx={{ 
                                    fontWeight: 'bold', 
                                    cursor: 'pointer',
                                    textDecoration: 'none',
                                    '&:hover': { textDecoration: 'underline' } 
                                }}
                            >
                                Register Here
                            </Link>
                        </Typography>
                    </Box>
                    {/* ---------------------------------- */}

                </Paper>
            </Box>
        </Container>
    );
};

export default Login;