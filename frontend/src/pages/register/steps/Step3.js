import React, {useState} from "react";
import { ButtonSecondary } from "../../../components/Buttons";
import { TextInput } from "../../../components/Inputs";
import { useNavigate } from "react-router-dom";
import axios from "axios";
import {toast} from "react-hot-toast"

function Step3(props) {
    const [loading, setLoading] = useState(false);
    const [email, setEmail] = useState(undefined);
    const [password, setPassword] = useState(undefined);
    const [name, setName] = useState(undefined);
    const [phone, setPhone] = useState(undefined);
    const navigate = useNavigate();

    async function handleRegister() {
        setLoading(true);
        try {
            await axios({
                method: "POST",
                url: `${process.env.REACT_APP_API_URL}/auth/register`,
                data: {
                    email,
                    password,
                    type: "employer",
                    name,
                    phone_number: phone
                }
            })
            navigate("/login");
        } catch (err) {
            console.error(err);
            toast.error(err.response.data.message);
        }
        setLoading(false);
    }

    return (
        <div className="flex flex-row w-full px-10 max-w-[1200px] justify-between space-x-20">
            <div className="flex flex-col w-1/2 space-y-6">
                <h1>I'm Looking to Hire.</h1>
                <p>Lorem ipsum dolor sit amet consectetur. Malesuada penatibus vulputate dictumst non. Porta cras sodales quis tellus commodo sit aliquet orci quisque. Porttitor morbi diam mattis at etiam et semper id morbi. Elit suscipit id porttitor pellentesque vel posuere vel mollis. </p>
            </div>
            <div className="flex flex-col w-1/2 space-y-6 text-center">
                <h1>Create an account</h1>
                <small>Finding employees has never been easier</small>
                <TextInput placeholder="Email Address" onChange={(val) => setEmail(val)} value={email} />
                <TextInput type="password" placeholder="Password" onChange={(val) => setPassword(val)} value={password} />
                <TextInput placeholder="Full Name" onChange={(val) => setName(val)} value={name} />
                <TextInput placeholder="Phone Number" onChange={(val) => setPhone(val)} value={phone} />
                <ButtonSecondary style={{width: "100%", borderRadius: "5px", height: "45px"}} onClick={handleRegister}>{loading ? "Loading..." : "Create Account"}</ButtonSecondary>
                <small className="underline cursor-pointer" onClick={() => navigate("/login")}>Already have an account?</small>
            </div>
        </div>
    )
}

export default Step3;