import React, {useState} from "react";
import { ButtonSecondary } from "../components/Buttons";
import { TextInput } from "../components/Inputs";
import { useNavigate } from "react-router-dom";
import axios from "axios";
import {toast} from "react-hot-toast"
import Cookies from "universal-cookie";
import Navbar from "../components/Navbar";

function Login(props) {
    const [loading, setLoading] = useState(false);
    const [email, setEmail] = useState(undefined);
    const [password, setPassword] = useState(undefined);
    const navigate = useNavigate();
    const cookies = new Cookies();

    async function handleLogin() {
        setLoading(true);
        try {
            const resp = await axios({
                method: "POST",
                url: `${process.env.REACT_APP_API_URL}/auth/login`,
                data: {
                    email,
                    password
                }
            })
            cookies.set("token", resp.data.token, {path: "/"});
            navigate("/dashboard");
        } catch (err) {
            console.error(err);
            toast.error(err.response.data.message);
        }
        setLoading(false);
    }

    return (
        <div className="flex flex-col w-full px-10 justify-center space-y-6 items-center">
            <Navbar />
            <div className="flex flex-col max-w-[1200px] w-full space-y-6">
                <h1>Login</h1>
                <TextInput placeholder="Email Address" onChange={(val) => setEmail(val)} />
                <TextInput type="password" placeholder="Password" onChange={(val) => setPassword(val)} />
                <ButtonSecondary style={{width: "100%", borderRadius: "5px", height: "45px"}} onClick={handleLogin}>{loading ? "Loading..." : "Login"}</ButtonSecondary>
            </div>
        </div>
    )
}

export default Login;