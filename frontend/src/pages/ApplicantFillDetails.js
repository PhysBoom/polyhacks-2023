import React, {useState} from "react";
import { TextInput } from "../components/Inputs";
import Navbar from "../components/Navbar";
import { ButtonSecondary } from "../components/Buttons";
import { useNavigate } from "react-router-dom";
import axios from "axios";
import Cookies from "universal-cookie";
import { toast } from "react-hot-toast";

function FormerJobInput(props) {
    
    return (
        <div className="flex flex-col space-y-4">
            <h2>Former Job {props.index + 1}</h2>
            <TextInput placeholder="Employer" onChange={val => props.setInputs({...props.inputs, employer: val})} value={props.inputs.employer} />
            <TextInput placeholder="Start Date" onChange={val => props.setInputs({...props.inputs, start_date: val})} value={props.inputs.start_date} type="date"/>
            <TextInput placeholder="End Date" onChange={val => props.setInputs({...props.inputs, end_date: val})} value={props.inputs.end_date} type="date" />
            <TextInput placeholder="Job Title" onChange={val => props.setInputs({...props.inputs, job_title: val})} value={props.inputs.job_title} />
        </div>
    )
}

function ApplicantFillDetails() {
    const [inputs, setInputs] = useState({
        first_name: "",
        last_name: "",
        address: "",
        phone_number: "",
        degree: "",
        university: "",
        gpa: "",
        graduation_date: "",
        former_jobs: [], // Array of FormerJob objects
        skills: [],
    });
    const [loading, setLoading] = useState(false);
    const navigate = useNavigate();
    const cookies = new Cookies();

    async function updateApplicant() {
        setLoading(true);
        console.log(inputs)
        try {
            await axios({
                method: "PATCH",
                url: `${process.env.REACT_APP_API_URL}/applicant`,
                data: {
                    first_name: inputs.first_name,
                    last_name: inputs.last_name,
                    address: inputs.address,
                    phone_number: inputs.phone_number,
                    resume: {
                        degree_type: inputs.degree,
                        university: inputs.university,
                        gpa: parseFloat(inputs.gpa),
                        grad_date: new Date(inputs.graduation_date) / 1000,
                        skills: inputs.skills,
                        employment_history: inputs.former_jobs.map((job) => {
                            return {
                                employer: job.employer,
                                start_date: new Date(job.start_date) / 1000,
                                end_date: job.end_date ? new Date(job.end_date) / 1000 : -1,
                                job_title: job.job_title,
                            }
                        })
                    }
                },
                headers: {
                    "Authorization": cookies.get("token")
                }
            })
            toast.success("Successfully updated applicant information.");
            navigate("/dashboard");
        } catch (err) {
            console.error(err);
            toast.error("Failed to update applicant information.");
        }
        setLoading(false);
    }

    return (
        <div className="flex flex-col items-center justify-center w-full h-full bg-white space-y-[64px]">
            <Navbar />
            <div className="flex flex-row w-full px-10 max-w-[1200px] justify-between space-x-20">
                <div className="flex flex-col w-1/2 space-y-6">
                    <h1>Fill Out Missing Information.</h1>
                    <small>Finding employees has never been easier.</small>
                </div>
                <div className="flex flex-col w-1/2 justify-between space-y-6">
                    <div className="flex flex-col space-y-4">
                        <h2>Personal Information</h2>
                        <small>None of this is used by employers when evaluating your qualifications.</small>
                        <TextInput placeholder="First Name" onChange={val => setInputs({...inputs, first_name: val})} value={inputs.first_name} />
                        <TextInput placeholder="Last Name" onChange={val => setInputs({...inputs, last_name: val})} value={inputs.last_name} />
                        <TextInput placeholder="Address" onChange={val => setInputs({...inputs, address: val})} value={inputs.address} />
                        <TextInput placeholder="Phone Number" onChange={val => setInputs({...inputs, phone_number: val})} value={inputs.phone_number} />
                    </div>
                    <div className="flex flex-col space-y-4">
                        <h2>Education</h2>
                        <TextInput placeholder="Degree" onChange={val => setInputs({...inputs, degree: val})} value={inputs.degree} />
                        <TextInput placeholder="University" onChange={val => setInputs({...inputs, university: val})} value={inputs.university} />
                        <TextInput placeholder="GPA" onChange={val => setInputs({...inputs, gpa: val})} value={inputs.gpa} type="number" />
                        <TextInput placeholder="Graduation Date" onChange={val => setInputs({...inputs, graduation_date: val})} value={inputs.graduation_date} type="date" />
                    </div>
                    <div className="flex flex-col space-y-4">
                        <h2>Experience</h2>
                        <small>Enter your former jobs.</small>
                        {inputs.former_jobs.map((job, index) => <FormerJobInput inputs={job} index={index} setInputs={newInputs => setInputs({...inputs, former_jobs: inputs.former_jobs.map((job, i) => i === index ? newInputs : job)})} />)}
                        <ButtonSecondary onClick={() => setInputs({...inputs, former_jobs: [...inputs.former_jobs, {}]})}>Add Former Job</ButtonSecondary>
                    </div>
                    <div className="flex flex-col space-y-4">
                        <h2>Skills</h2>
                        <small>Enter your skills.</small>
                        {inputs.skills.map((skill, index) => <TextInput placeholder="Skill" onChange={val => setInputs({...inputs, skills: inputs.skills.map((skill, i) => i === index ? val : skill)})} value={skill} />)}
                        <ButtonSecondary onClick={() => setInputs({...inputs, skills: [...inputs.skills, ""]})}>Add Skill</ButtonSecondary>
                    </div>
                    <ButtonSecondary onClick={updateApplicant}>{loading ? "Loading..." : "Submit"}</ButtonSecondary>
                </div>
            </div>
        </div>
     )
}

export default ApplicantFillDetails;