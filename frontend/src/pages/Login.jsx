import { useState } from 'react';
import api from '../api/axios';
import { useNavigate } from 'react-router-dom';
import { Container, TextField, Button, Typography, Box, Paper, Alert } from '@mui/material';

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

            // 1. Log the response to verify (Optional)
            console.log("Login Successful:", response.data);

            // 2. YOU DO NOT NEED TO SAVE A TOKEN.
            // The browser has already saved the session cookie because
            // you set 'supports_credentials=True' in Flask.
            
            // 3. Just Redirect
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
                </Paper>
            </Box>
        </Container>
    );
};

export default Login;