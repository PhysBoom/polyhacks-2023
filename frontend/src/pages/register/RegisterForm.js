import React, {useState} from 'react';
import * as steps from './steps';
import Navbar from '../../components/Navbar';

function RegisterForm() {
    const [step, setStep] = useState(1);

    function renderStep(){
        switch(step){
            case 1:
                return <steps.Step1 setStep={setStep} />
            case 2:
                return <steps.Step2 setStep={setStep} /> // Bad practice but this is individual
            case 3:
                return <steps.Step3 setStep={setStep} /> // And this is corporation
            default:
                return <steps.Step1 />
        }
    }

    return (
        <div className="flex flex-col items-center justify-center w-full h-full bg-white space-y-[64px]">
            <Navbar />
            {renderStep()}
        </div>
    )
}

export default RegisterForm;