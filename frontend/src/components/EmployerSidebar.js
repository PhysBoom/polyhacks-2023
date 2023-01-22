import React from "react";
import { ReactComponent as Logo } from "../images/logo.svg";
import { useNavigate } from "react-router-dom";

function EmployerSidebar() {
    const navigate = useNavigate();

    return (
        <div className="flex flex-col h-screen bg-white space-y-[100px] px-10">
            <Logo width="250px" />
            <div className="flex flex-col space-y-6">
                <button onClick={() => navigate("/dashboard")} className="text-h2 hover:underline">Dashboard</button>
                <button onClick={() => navigate("/create-posting")} className="text-h2 hover:underline">New Job</button>
                <button onClick={() => navigate("/messages")} className="text-h2 text-gray-300" disabled>Messages</button>
                <button onClick={() => navigate("/account")} className="text-h2 text-gray-300" disabled>Account</button>
                <button onClick={() => navigate("/help")} className="text-h2 text-gray-300" disabled>Help</button>
            </div>
        </div>
    )
}

export default EmployerSidebar;