import { useState } from 'react';
import api from '../api/axios'; // Your axios instance
import { useNavigate } from 'react-router-dom';
import { 
    Container, 
    TextField, 
    Button, 
    Typography, 
    Box, 
    Paper, 
    Alert, 
    Link,
    CircularProgress
} from '@mui/material';

const Register = () => {
    const navigate = useNavigate();
    
    // State for form fields
    const [formData, setFormData] = useState({
        email: '',
        password: '',
        confirmPassword: ''
    });

    const [error, setError] = useState('');
    const [success, setSuccess] = useState('');
    const [loading, setLoading] = useState(false);

    // Handle input changes
    const handleChange = (e) => {
        setFormData({
            ...formData,
            [e.target.name]: e.target.value
        });
    };

    const handleRegister = async (e) => {
        e.preventDefault();
        setError('');
        setSuccess('');

        // 1. Client-side Validation: Check if passwords match
        if (formData.password !== formData.confirmPassword) {
            setError("Passwords do not match.");
            return;
        }

        setLoading(true);

        try {
            // 2. Send Data to your Flask API
            // Note: We only send email and password, not confirmPassword
            const response = await api.post('/api/register', {
                email: formData.email,
                password: formData.password
            });

            // 3. Handle Success (HTTP 201)
            setSuccess(response.data.msg || "Registration successful!");
            
            // Redirect to login after 2 seconds so user sees the success message
            setTimeout(() => {
                navigate('/login');
            }, 2000);

        } catch (err) {
            // 4. Handle Errors (HTTP 400)
            console.error("Registration Error:", err);
            
            if (err.response && err.response.data) {
                const data = err.response.data;

                // Case A: Simple "User already exists" message
                if (data.msg) {
                    setError(data.msg);
                } 
                // Case B: Validation Schema errors (e.g. { password: ["Too short"], email: ["Invalid"] })
                else if (typeof data === 'object') {
                    // Grab the first error message from the object to display
                    const firstErrorKey = Object.keys(data)[0];
                    const firstErrorMessage = data[firstErrorKey]; // This might be an array or string
                    // Flatten it if it's an array
                    setError(Array.isArray(firstErrorMessage) ? firstErrorMessage[0] : firstErrorMessage);
                } else {
                    setError("Registration failed. Please try again.");
                }
            } else {
                setError("Server error. Please try again later.");
            }
        } finally {
            setLoading(false);
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
                        Patient Registration
                    </Typography>
                    
                    <Typography variant="body2" align="center" color="text.secondary" sx={{ mb: 3 }}>
                        Create your account to access hospital services
                    </Typography>

                    {/* Feedback Messages */}
                    {error && <Alert severity="error" sx={{ mb: 2 }}>{error}</Alert>}
                    {success && <Alert severity="success" sx={{ mb: 2 }}>{success}</Alert>}

                    <form onSubmit={handleRegister}>
                        <TextField
                            label="Email Address"
                            name="email"
                            type="email"
                            variant="outlined"
                            fullWidth
                            margin="normal"
                            value={formData.email}
                            onChange={handleChange}
                            required
                            disabled={loading}
                        />
                        <TextField
                            label="Password"
                            name="password"
                            type="password"
                            variant="outlined"
                            fullWidth
                            margin="normal"
                            value={formData.password}
                            onChange={handleChange}
                            required
                            disabled={loading}
                        />
                        <TextField
                            label="Confirm Password"
                            name="confirmPassword"
                            type="password"
                            variant="outlined"
                            fullWidth
                            margin="normal"
                            value={formData.confirmPassword}
                            onChange={handleChange}
                            required
                            disabled={loading}
                            error={formData.password !== formData.confirmPassword && formData.confirmPassword !== ''}
                        />
                        
                        <Button 
                            type="submit" 
                            variant="contained" 
                            color="primary" 
                            fullWidth 
                            size="large"
                            sx={{ mt: 2 }}
                            disabled={loading}
                        >
                            {loading ? <CircularProgress size={24} /> : "Register"}
                        </Button>
                    </form>

                    {/* Link back to Login */}
                    <Box sx={{ mt: 3, textAlign: 'center' }}>
                        <Typography variant="body2" color="text.secondary">
                            Already have an account? {' '}
                            <Link 
                                component="button" 
                                variant="body2" 
                                onClick={() => navigate('/login')}
                                sx={{ 
                                    fontWeight: 'bold', 
                                    cursor: 'pointer',
                                    textDecoration: 'none',
                                    '&:hover': { textDecoration: 'underline' } 
                                }}
                            >
                                Log In
                            </Link>
                        </Typography>
                    </Box>

                </Paper>
            </Box>
        </Container>
    );
};

export default Register;