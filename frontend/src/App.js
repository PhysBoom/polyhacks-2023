import logo from './logo.svg';
import { Routes, Route } from 'react-router-dom';
import Landing from './pages/Landing';
import RegisterForm from './pages/register/RegisterForm';
import {Toaster} from 'react-hot-toast';

function App() {
  return (
    <div className="bg-white p-10">
      <Routes>
        <Route path="/" element={<Landing />} />
        <Route path="/register" element={<RegisterForm />} />
      </Routes>
      <Toaster />
    </div>
  );
}

export default App;
