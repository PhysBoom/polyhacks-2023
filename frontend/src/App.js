import logo from './logo.svg';
import { Routes, Route } from 'react-router-dom';
import Landing from './pages/Landing';
import RegisterForm from './pages/register/RegisterForm';
import Login from './pages/Login';
import SubmitResume from './pages/SubmitResume';
import ApplicantFillDetails from './pages/ApplicantFillDetails';
import Dashboard from './pages/Dashboard';
import EmployerCreatePosting from './pages/EmployerCreatePosting';
import EmployerRatingSystem from './pages/EmployerRatingSystem';
import EmployerViewPosting from './pages/EmployerViewPosting';
import {Toaster} from 'react-hot-toast';

function App() {
  return (
    <div className="bg-white p-10">
      <Routes>
        <Route path="/" element={<Landing />} />
        <Route path="/register" element={<RegisterForm />} />
        <Route path="/login" element={<Login />} />
        <Route path="/submit-resume" element={<SubmitResume />} />
        <Route path="/applicant-fill-details" element={<ApplicantFillDetails />} />
        <Route path="/dashboard" element={<Dashboard />} />
        <Route path="/create-posting" element={<EmployerCreatePosting />} />
        <Route path="/employer/rate/:jobId" element={<EmployerRatingSystem />} />
        <Route path="/employer/view-posting/:jobId" element={<EmployerViewPosting />} />
      </Routes>
      <Toaster />
    </div>
  );
}

export default App;
