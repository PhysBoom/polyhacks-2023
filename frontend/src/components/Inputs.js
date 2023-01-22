import React from 'react';

/**
 * Text input box with label
 * @param {string} label - Label for the input box
 * @param {string} value - Value of the input box
 * @param {function} onChange - Function to call when the input box changes
 * @param {string} type - Type of the input box
 * @param {string} placeholder - Placeholder text for the input box
 */
export function TextInput(props) {
    function handleChange(e) {
        e.preventDefault();
        props.onChange(e.target.value);
    }

    return (
        <input className="border border-black border-2 rounded-sm p-3 text-black placeholder-black" type={props.type} value={props.value} onChange={handleChange} placeholder={props.placeholder}/>
    );
}
