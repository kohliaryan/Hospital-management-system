// pages/Dashboard.js
import { useOutletContext } from 'react-router-dom';
import PatientDashboard from './dashboards/PatientDashboard';
// ... other imports

const Dashboard = () => {
    // Receive the user data passed down from MainLayout
    const { user } = useOutletContext(); 
    const role = user.roles ? user.roles[0] : null;

    return (
        <div>
            {role === 'Patient' && <PatientDashboard user={user} />}
            {/* ... other roles */}
        </div>
    );
};

export default Dashboard;