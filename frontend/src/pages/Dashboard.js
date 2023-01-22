import React, {useState, useEffect} from "react";
import axios from "axios";
import Cookies from "universal-cookie";
import { useNavigate } from "react-router-dom";
import EmployerSidebar from "../components/EmployerSidebar";

function EmployerPosting(props) {
    // props.job contains a field resume_selection_history {str: int}
    // Count how many times the value is -1 (unlikely), 0 (undecided), 1 (likely)
    const numOfEachLikelihoodCategory = {
        "unlikely": 0,
        "undecided": 0,
        "likely": 0,
    }
    for (const [key, value] of Object.entries(props.job.resume_selection_history)) {
        if (value === -1) {
            numOfEachLikelihoodCategory["unlikely"] += 1;
        } else if (value === 0) {
            numOfEachLikelihoodCategory["undecided"] += 1;
        } else if (value === 1) {
            numOfEachLikelihoodCategory["likely"] += 1;
        }
    }

    return (
        <div className="flex flex-row w-full justify-between py-6 px-8 items-center">
            <div className="flex flex-col w-1/4">
                <p className="font-semibold">{props.job.title}</p>
                <a href={`/employer/posting/${props.job.id}`} className="text-blue-300 hover:cursor-pointer underline">View this posting.</a>
            </div>
            <div className="flex flex-col w-1/4">
                <p className="font-semibold">Status</p>
                <span className="flex flex-col items-center justify-center bg-quaternary text-center w-[100px] h-[40px] italic rounded-full text-white font-semibold">Active</span>
            </div>
            <div className="flex flex-row justify-end items-center space-x-4">
                <div className="flex flex-col space-y-2 border border-black rounded py-4 w-[150px]">
                    <p className="text-center">Likely</p>
                    <p className="text-center">{numOfEachLikelihoodCategory["likely"]}</p>
                </div>
                <div className="flex flex-col space-y-2 border border-black rounded py-4 w-[150px]">
                    <p className="text-center">Undecided</p>
                    <p className="text-center">{numOfEachLikelihoodCategory["undecided"]}</p>
                </div>
                <div className="flex flex-col space-y-2 border border-black rounded py-4 w-[150px]">
                    <p className="text-center">Unlikely</p>
                    <p className="text-center">{numOfEachLikelihoodCategory["unlikely"]}</p>
                </div>
            </div>
        </div>
    )
}

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
                        <div className="flex flex-col w-full px-[30px] space-y-20">
                            <h1>Dashboard</h1>
                            <div className="flex flex-col space-y-6">
                                <h2>Postings</h2>
                                <div className="flex flex-col rounded-md border border-black divide-gray-300 divide-y">
                                    {Object.entries(user.job_postings).map(([job_id, job]) => (
                                        <EmployerPosting key={job_id} job={job} />
                                    ))}
                                </div>
                            </div>
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
