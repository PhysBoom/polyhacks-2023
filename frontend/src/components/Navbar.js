import React from 'react';
import { ReactComponent as Logo } from '../images/logo.svg';
import { ButtonPrimary } from './Buttons';
import { useNavigate } from 'react-router-dom';

function Navbar() {
    const navigate = useNavigate();

    return (
        <div className="flex w-full h-[85px] px-4 items-center justify-between bg-white">
            <Logo width="250px"/>
            <ButtonPrimary onClick={() => navigate('/register')}>Get Started</ButtonPrimary>
        </div>
    )
}

export default Navbar;