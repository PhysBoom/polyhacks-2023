import React, {useEffect, useState} from "react";
import axios from "axios";
import { useParams, useNavigate } from "react-router-dom";
import { ReactComponent as ApplicantInfoIcon } from "../images/view_posting_images/applicant-info.svg";
import { ReactComponent as MessageApplicantIcon } from "../images/view_posting_images/message-applicant.svg";
import { ReactComponent as RemoveApplicantIcon } from "../images/view_posting_images/remove-applicant.svg";
import { toast } from "react-hot-toast";
import Cookies from "universal-cookie";
import EmployerSidebar from "../components/EmployerSidebar";
import { ButtonSecondary } from "../components/Buttons";


function ApplicantView() {
    // TODO: interactive
    return (
        <div className="flex flex-row w-full justify-between py-6 px-8 items-center">
            <p className="font-semibold">Applicant</p>
            <button onClick={() => toast.error("Sorry! This is not yet implemented.")}><ApplicantInfoIcon /></button>
            <button onClick={() => toast.error("Sorry! This is not yet implemented.")}><MessageApplicantIcon /></button>
            <button onClick={() => toast.error("Sorry! This is not yet implemented.")}><RemoveApplicantIcon /></button>
        </div>
    )
}

function EmployerViewPosting() {
    const [loading, setLoading] = useState(true);
    const [user, setUser] = useState({});
    const cookies = new Cookies();
    const navigate = useNavigate();
    const { jobId } = useParams();
    const [numOfEachLikelihoodCategory, setNumOfEachLikelihoodCategory] = useState({
        "unlikely": 0,
        "undecided": 0,
        "likely": 0,
    });

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
            countNumOfEachLikelihood(resp.data.job_postings[jobId]);
        } catch (err) {
            console.error(err);
            navigate("/login");
        }
        setLoading(false);
    }

    function countNumOfEachLikelihood(job) {
        const numOfEachLikelihoodCategory = {
            "unlikely": 0,
            "undecided": 0,
            "likely": 0,
        }
        for (const [key, value] of Object.entries(job.resume_selection_history)) {
            if (value === -1) {
                numOfEachLikelihoodCategory["unlikely"] += 1;
            } else if (value === 0) {
                numOfEachLikelihoodCategory["undecided"] += 1;
            } else if (value === 1) {
                numOfEachLikelihoodCategory["likely"] += 1;
            }
        }
        setNumOfEachLikelihoodCategory(numOfEachLikelihoodCategory);
    }

    useEffect(() => {
        loadUser();
    }, [])

    return (
        <>
            {loading && <h1>Loading...</h1>}
            {!loading && 
                <div className="flex flex-row w-full divide-x divide-gray-300">
                    <EmployerSidebar />
                    <div className="flex flex-col w-full px-[30px] space-y-20">
                        <h1>{`${user.job_postings[jobId].title} Applicants`}</h1>
                        <div className="flex flex-row space-x-[20px]">
                            <div className="flex flex-col space-y-10 w-full">
                                <div className="flex flex-col space-y-4">
                                    <h2>Likely</h2>
                                    <div className="flex flex-col rounded-md border border-black divide-gray-300 divide-y">
                                        {numOfEachLikelihoodCategory["likely"] === 0 && <p className="text-center py-6">No applicants</p>}
                                        {numOfEachLikelihoodCategory["likely"] !== 0 && <>{[...Array(numOfEachLikelihoodCategory["likely"])].map((e, i) => <ApplicantView />)}</>}
                                    </div>
                                </div>
                                <div className="flex flex-col space-y-4">
                                    <h2>Unlikely</h2>
                                    <div className="flex flex-col rounded-md border border-black divide-gray-300 divide-y">
                                        {numOfEachLikelihoodCategory["unlikely"] === 0 && <p className="text-center py-6">No applicants</p>}
                                        {numOfEachLikelihoodCategory["unlikely"] !== 0 && <>{[...Array(numOfEachLikelihoodCategory["unlikely"])].map((e, i) => <ApplicantView />)}</>}
                                    </div>
                                </div>
                            </div>
                            <div className="flex flex-col space-y-4 w-full">
                                <h2>Undecided</h2>
                                <div className="flex flex-col rounded-md border border-black divide-gray-300 divide-y">
                                    {numOfEachLikelihoodCategory["undecided"] === 0 && <p className="text-center py-6">No applicants</p>}
                                    {numOfEachLikelihoodCategory["undecided"] !== 0 && <>{[...Array(numOfEachLikelihoodCategory["undecided"])].map((e, i) => <ApplicantView />)}</>}
                                </div>
                            </div>
                        </div>
                        <div className="flex flex-row justify-center"><ButtonSecondary style={{height: "50px", width: "200px", borderRadius: "20px"}} onClick={() => navigate(`/employer/rate/${jobId}`)}>Rate More Applicants</ButtonSecondary></div>
                    </div>
                </div>
            }
        </>
    )
}

export default EmployerViewPosting;