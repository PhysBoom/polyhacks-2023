import React from "react";

export function ButtonPrimary(props) {
  return (
    <button
      className="bg-secondary text-primary text-center h-[40px] w-[140px] rounded-full font-serif"
      {...props}
    >
      {props.children}
    </button>
  );
}