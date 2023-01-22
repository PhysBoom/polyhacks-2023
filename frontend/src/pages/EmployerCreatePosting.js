import React, {useState} from "react";
import EmployerSidebar from "../components/EmployerSidebar";
import axios from "axios";
import { TextInput, TextArea } from "../components/Inputs";
import { ButtonSecondary } from "../components/Buttons";
import { ReactComponent as DotSeparator } from "../images/dot-separator.svg";
import { toast } from "react-hot-toast";
import Cookies from "universal-cookie";
import { useNavigate } from "react-router-dom";

function EmployerCreatePosting() {
  const [loading, setLoading] = useState(false);
  const [inputs, setInputs] = useState({
    title: "",
    description: "",
    salary: "",
    job_type: "",
    desired_skills: []
  });
  const cookies = new Cookies();
  const navigate = useNavigate();

  async function submitPosting() {
    setLoading(true);
    try {
      await axios({
        method: "POST",
        url: `${process.env.REACT_APP_API_URL}/employer/job`,
        data: {
          title: inputs.title,
          description: inputs.description,
          salary: inputs.salary,
          job_type: inputs.job_type,
          desired_skills: inputs.desired_skills
        },
        headers: {
            Authorization: cookies.get("token")
        }
      });
      toast.success("Successfully created posting.");
      navigate("/dashboard");
    } catch (err) {
      console.log(err);
      toast.error("Failed to create posting.");
    }
    setLoading(false);
  }


  return (
    <div className="flex flex-row w-full divide-x divide-gray-300">
        <EmployerSidebar />
        <div className="flex flex-row w-full justify-center items-center px-4 text-center">
            <div className="flex flex-col w-full h-full items-center justify-center space-y-6">
                <h1>Create Your Posting.</h1>
                <p>Input all necessary information that will be used by Applicants to find your posting.</p>
                <div className="flex flex-col space-y-2">
                    <h2>Job Information</h2>
                    <TextInput placeholder="Job Title (eg Software Engineer)" onChange={val => setInputs({...inputs, title: val})} value={inputs.title} />
                    <TextArea placeholder="Job Description" onChange={val => setInputs({...inputs, description: val})} value={inputs.description} />
                    <TextInput placeholder="Salary" onChange={val => setInputs({...inputs, salary: val})} value={inputs.salary} type="number" />
                    <TextInput placeholder="Job Type (e.g. Full Time)" onChange={val => setInputs({...inputs, job_type: val})} value={inputs.job_type} />
                    <h3 className="text-body font-semibold font-serif">Desired Skills</h3>
                    {inputs.desired_skills.map((skill, index) => {
                        return (
                            <TextInput placeholder="Leadership" key={index} onChange={val => {
                                const newSkills = inputs.desired_skills;
                                newSkills[index] = val;
                                setInputs({...inputs, desired_skills: newSkills});
                            }} value={skill} />
                        )
                    })}
                    <div className="flex flex-col w-full justify-center items-center space-y-6">
                        <ButtonSecondary onClick={() => setInputs({...inputs, desired_skills: [...inputs.desired_skills, ""]})}>Add Skill</ButtonSecondary>
                        <DotSeparator />
                        <ButtonSecondary onClick={submitPosting}>{loading ? "Loading..." : "Submit Posting"}</ButtonSecondary>
                    </div>
                </div>
            </div>
        </div>
    </div>
  )
}

export default EmployerCreatePosting;