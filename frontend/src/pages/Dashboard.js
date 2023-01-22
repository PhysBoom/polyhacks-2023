import React, {useState, useEffect} from "react";
import axios from "axios";
import Cookies from "universal-cookie";
import { useNavigate } from "react-router-dom";
import EmployerSidebar from "../components/EmployerSidebar";

function Dashboard() {
    const [loading, setLoading] = useState(true);
    const [user, setUser] = useState({});
    const cookies = new Cookies();
    const navigate = useNavigate();

    async function loadUser() {
        try { 
            const resp =  await axios({
                method: "GET",
                url: `${process.env.REACT_APP_API_URL}/auth/user`,
                headers: {
                    "Authorization": cookies.get("token")
                }
            })
            setUser(resp.data);
        } catch (err) {
            console.error(err);
            navigate("/login");
        }
        setLoading(false);
    }

    useEffect(() => {
        loadUser();
        
    }, [])

    return (
        <>
            {loading && <h1>Loading...</h1>}
            {!loading && (user.user_type === "employer" ? (
                    <div className="flex flex-row w-full divide-x divide-gray-300">
                        <EmployerSidebar />
                        <div className="flex flex-col w-full px-[30px] space-y-10">
                            <h1>Employer Dashboard</h1>
                        </div>
                    </div>
                ) : (
                    <h1>Applicant Dashboard</h1>
                ))
            }
        </>
        
    )
}

export default Dashboard;
