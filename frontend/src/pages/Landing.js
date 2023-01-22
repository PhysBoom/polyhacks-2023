import React from "react";
import { ButtonPrimary } from "../components/Buttons";
import Navbar from "../components/Navbar";
import { useNavigate } from "react-router-dom";

function Landing(){
    const navigate = useNavigate();

    return (
        <div className="flex flex-col items-center justify-between bg-white min-h-screen">
            <Navbar />
            <div className="flex flex-col items-center justify-center max-w-[1000px] space-y-4 text-center">
                <h1 className="mb-4">The Best Way For Small Businesses to Find New Employees</h1>
                <p>Lorem ipsum dolor sit amet consectetur. Malesuada penatibus vulputate dictumst non. Porta cras sodales quis tellus commodo sit aliquet orci quisque. Porttitor morbi diam mattis at etiam et semper id morbi. Elit suscipit id porttitor pellentesque vel posuere vel mollis.</p>
                <ButtonPrimary onClick={() => navigate("/register")}>Get Started</ButtonPrimary>
            </div>
            <div>
                TODO: Images and stuff
            </div>
        </div>
    )
}

export default Landing;