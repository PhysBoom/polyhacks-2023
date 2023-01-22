import React, {useState, useRef} from "react";
import {ReactComponent as FileUploadIcon} from "../images/file-upload.svg";
import { useNavigate } from "react-router-dom";
import axios from "axios";
import {toast} from "react-hot-toast"
import Navbar from "../components/Navbar";
import Cookies from "universal-cookie";

function SubmitResume() {
    const hiddenFileInput = useRef(null);
    const navigate = useNavigate();
    const cookies = new Cookies();

    async function handleSubmitResume(event) {
        const file = event.target.files[0];
        if (!file) return;
        const formData = new FormData();
        formData.append("resume", file);
        try {
            await axios({
                method: "POST",
                url: `${process.env.REACT_APP_API_URL}/applicant/upload-resume`,
                data: formData,
                headers: {
                    "Content-Type": "multipart/form-data",
                    "Authorization": cookies.get("token")
                }
            })
            toast.success("Resume uploaded successfully!");
            navigate("/dashboard");
        } catch (err) {
            console.error(err);
            toast.error(err.response.data.message);
        }
    }

    return (
        <div className="flex flex-col w-full px-10 justify-center space-y-10 items-center">
            <Navbar />
            <div className="flex flex-row w-full px-10 max-w-[1200px] justify-between space-x-20">
                <div className="flex flex-col w-1/2 space-y-6">
                    <h1>Submit your Resume.</h1>
                    <p>Lorem ipsum dolor sit amet consectetur. Malesuada penatibus vulputate dictumst non. Porta cras sodales quis tellus commodo sit aliquet orci quisque. Porttitor morbi diam mattis at etiam et semper id morbi. Elit suscipit id porttitor pellentesque vel posuere vel mollis. </p>
                </div>
                <div className="flex flex-col w-1/2 space-y-6 text-center">
                    <h2>Upload Files</h2>
                    <small>Please upload your resume below.</small>
                    <label className="flex flex-col bg-secondary h-[300px] items-center justify-center rounded-md" onClick={handleSubmitResume}>
                        <FileUploadIcon />
                        <p>Drag and drop file.</p>
                        <small>PNG or JPG</small>
                        <input type="file" ref={hiddenFileInput} onChange={handleSubmitResume} style={{display: "none"}} />
                    </label>
                </div>
            </div>
        </div>
    )
}

export default SubmitResume;