import React from "react";
import { ButtonSecondary } from "../../../components/Buttons";

function Step1(props){
    return (
        <div className="flex flex-row w-full px-10 max-w-[1200px] justify-between space-x-20">
            <div className="flex flex-col w-1/2 space-y-6">
                {/* Placeholder rectangle */}
                <div className="bg-gray-200 h-[200px] w-full"></div>
                <h1>I'm an individual looking for a job.</h1>
                <p>Lorem ipsum dolor sit amet, consectetur adipiscing</p>
                <ButtonSecondary onClick={() => props.setStep(2)}>Sign Up.</ButtonSecondary>
            </div>
            <div className="flex flex-col w-1/2 justify-between">
                {/* Placeholder rectangle */}
                <div className="bg-gray-200 h-[200px] w-full"></div>
                <h1>I'm a company looking to hire.</h1>
                <p>Lorem ipsum dolor sit amet, consectetur adipiscing</p>
                <ButtonSecondary onClick={() => props.setStep(3)}>Sign Up.</ButtonSecondary>
            </div>
        </div>
    )
}

export default Step1;