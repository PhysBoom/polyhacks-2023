import React, {useEffect, useState} from "react";
import axios from "axios";
import { useParams, useNavigate } from "react-router-dom";
import { ButtonSecondary, ButtonPrimary } from "../components/Buttons";
import { toast } from "react-hot-toast";
import EmployerSidebar from "../components/EmployerSidebar";
import Cookies from "universal-cookie";
import { ReactComponent as CheckmarkBox} from "../images/checkmark-page.svg";

function EmployerRatingSystem() {
    const [loading, setLoading] = useState(true);
    const [user, setUser] = useState({});
    const [curApplicant, setCurApplicant] = useState({});
    const cookies = new Cookies();
    const navigate = useNavigate();
    const { jobId } = useParams();

    function toTitleCase(str) {
        return str.replace(
            /\w\S*/g,
            (txt) => {
                return txt.charAt(0).toUpperCase() + txt.substr(1).toLowerCase();
            }
        );
    }

    async function loadUser() {
        setLoading(true);
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

    async function submitRating(rating) {
        try{
            await axios({
                method: "POST",
                url: `${process.env.REACT_APP_API_URL}/employer/job/${jobId}/resume/${curApplicant.resume.id}/rating`,
                headers: {
                    "Authorization": cookies.get("token")
                },
                data: {
                    rating: rating
                }
            })
            await loadNextApplicant();
            toast.success("Rating submitted!");
        } catch (err) {
            console.error(err);
            toast.error("Error submitting rating!");
        }
    }

    async function sendMessageToApplicant() {
        toast.success("Message sent!");
    }

    async function loadNextApplicant() {
        setLoading(true);
        try {
            const resp = await axios({
                method: "GET",
                url: `${process.env.REACT_APP_API_URL}/employer/job/${jobId}/next-applicant`,
                headers: {
                    "Authorization": cookies.get("token")
                }
            })
            console.log(resp);
            setCurApplicant(resp.data);
        } catch (err) {
            console.error(err);
            navigate("/login");
        }
        setLoading(false);
    }

    async function initialize() {
        await loadUser();
        await loadNextApplicant();
    }

    useEffect(() => {
        initialize();
    }, [])
    
    return (
            <>
                {loading && <h1>Loading...</h1>}
                {!loading && 
                    <div className="flex flex-row w-full divide-x divide-gray-300">
                        <EmployerSidebar />
                        <div className="flex flex-col w-full text-center space-y-6">
                            <h1>Applicant Information</h1>
                            <span className="flex flex-row w-full justify-center">
                                <ButtonPrimary onClick={sendMessageToApplicant}>Send Message</ButtonPrimary>
                            </span>
                            <div className="flex flex-row w-full h-full items-center space-x-6 text-left pl-10">
                                <div className="flex flex-row w-1/3 h-full items-center space-x-6 text-left pl-10">
                                    <div className="flex flex-col justify-center space-y-10">
                                        <h2>Rating for the <span className="text-quaternary underline">{user.job_postings[jobId].title}</span> position</h2>
                                        <span>After reviewing the application, choose whether your company is likely to hire, unlikely to hire, or undecided about this application. Seekworks will begin to show you applicants who are more likely to fit your job posting once you have rated enough applications.</span>
                                    </div>
                                </div>
                                <div className="flex flex-col space-y-6">
                                    <div className="flex flex-col p-4 border border-black rounded-lg space-y-6 w-full">
                                        <div className="flex flex-col space-y-4">
                                            <h2>Education</h2>
                                            <div className="flex flex-col">
                                                <small>{`University: ${curApplicant.resume.university}`}</small>
                                                <small>{`Degree: ${curApplicant.resume.degree_type}`}</small>
                                                <small>{`Graduation Date: ${new Date(new Date(curApplicant.resume.grad_date).setHours(0,0,0,0) * 1000).toLocaleString(`en-US`, {month: `long`, year: `numeric`})}`}</small>
                                                <small>{`GPA: ${curApplicant.resume.gpa.toFixed(2)}`}</small>
                                            </div>
                                        </div>
                                        <div className="flex flex-col space-y-4">
                                            <h2>Work Experience</h2>
                                            <div className="flex flex-col space-y-2">
                                                {curApplicant.resume.employment_history.map((workExp, index) => (
                                                    <div className="flex flex-col" key={index}>
                                                        <small>{`Company: ${workExp.employer}`}</small>
                                                        <small>{`Job Title: ${workExp.job_title}`}</small>
                                                        <small>{`Start Date: ${new Date(new Date(workExp.start_date).setHours(0,0,0,0) * 1000).toLocaleString(`en-US`, {month: `long`, year: `numeric`})}`}</small>
                                                        <small>{`End Date: ${workExp.end_date != -1 ? new Date(new Date(workExp.end_date).setHours(0,0,0,0) * 1000).toLocaleString(`en-US`, {month: `long`, year: `numeric`}) : "Present" }`}</small>
                                                    </div>
                                                ))}
                                            </div>
                                        </div>
                                        <div className="flex flex-col space-y-4">
                                            <h2>Skills</h2>
                                            <div className="flex flex-col">
                                                {curApplicant.resume.skills.map((skill, index) => (
                                                    <small key={index}>{toTitleCase(skill)}</small>
                                                ))}
                                            </div>
                                        </div>
                                        
                                    </div>
                                    <div className="flex flex-row w-full justify-center space-x-10">
                                        <ButtonSecondary onClick={() => submitRating(-1)} style={{width: "230px", height: "100px", borderRadius: "20px"}}>Unlikely to Hire</ButtonSecondary>
                                        <ButtonSecondary onClick={() => submitRating(0)} style={{width: "230px", height: "100px", borderRadius: "20px"}}>Undecided</ButtonSecondary>
                                        <ButtonSecondary onClick={() => submitRating(1)} style={{width: "230px", height: "100px", borderRadius: "20px"}}><div className="flex flex-row space-x-4 justify-center items-center"><CheckmarkBox />Likely to Hire</div></ButtonSecondary>
                                    </div>
                                </div>
                            </div>
                        </div>
                        
                    </div>
                }
            </>
    )
}

export default EmployerRatingSystem;