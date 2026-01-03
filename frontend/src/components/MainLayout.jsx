// components/MainLayout.jsx
import { useEffect, useState } from 'react';
import { Outlet, Navigate } from 'react-router-dom';
import { CircularProgress, Box } from '@mui/material';
import api from '../api/axios';
import Navbar from './Navbar'; // The Smart Navbar we discussed

const MainLayout = () => {
    const [user, setUser] = useState(null);
    const [loading, setLoading] = useState(true);

    // 1. Fetch User Profile Globaly for all protected pages
    useEffect(() => {
        const fetchProfile = async () => {
            try {
                const response = await api.get('/api/profile');
                setUser(response.data);
            } catch (error) {
                console.error("User not authenticated");
                setUser(null);
            } finally {
                setLoading(false);
            }
        };

        fetchProfile();
    }, []);

    // 2. Show Loader while checking auth
    if (loading) {
        return (
            <Box display="flex" justifyContent="center" mt={10}>
                <CircularProgress />
            </Box>
        );
    }

    // 3. If not logged in, kick them out to Login
    if (!user) {
        return <Navigate to="/login" replace />;
    }

    // 4. If logged in, show Navbar + The specific page content (Outlet)
    return (
        <>
            <Navbar user={user} />
            <Box sx={{ p: 3 }}>
                <Outlet context={{ user }} /> 
            </Box>
        </>
    );
};

export default MainLayout;