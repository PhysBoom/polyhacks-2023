import logo from './logo.svg';
import { Routes, Route } from 'react-router-dom';
import Landing from './pages/Landing';
import RegisterForm from './pages/register/RegisterForm';
import Login from './pages/Login';
import SubmitResume from './pages/SubmitResume';
import ApplicantFillDetails from './pages/ApplicantFillDetails';
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
      </Routes>
      <Toaster />
    </div>
  );
}

export default App;
