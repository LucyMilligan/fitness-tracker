"use client";
import Link from "next/link";
import { useState } from "react";
import { createUser } from "../server_functions/createUser"


export default function Page() {
  const [errorMessage, setErrorMessage] = useState("")
  const [successMessage, setSuccessMessage] = useState("")
  
  async function handleSubmit(formData) {
    const result = await createUser(formData);
    const user_id = result.data.user_id

    if (result.success) {
      setSuccessMessage(`User added! Your user_id is ${user_id}`);
      setErrorMessage("");
    } else {
      setErrorMessage(result.error);
      setSuccessMessage("");
    }
  }
  
  return ( 
      <>
        <main>
          <p className="text-[45px] text-center py-8 font-semibold font-[family-name:var(--font-geist-mono)]">Create new user</p>
          <p className="py-6 font-semibold text-center">Enter your details below to create a new user:</p>
          <form action={handleSubmit} className="flex gap-2 flex-col">
            {/* Name input */}  
            <div className="flex items-center gap-4">
              <label htmlFor="name" className="w-37 text-right">Name:</label>          
              <input type="text" name="name" title="Name or nickname" placeholder="Bob" className="border border-teal-800 bg-transparent rounded outline-none focus-within:border-teal-600"></input>
            </div>

            {/* Email input */}
            <div className="flex items-center gap-4">
              <label htmlFor="email" className="w-37 text-right">Email address:</label>
              <input type="text" name="email" title="Valid email address" placeholder="bob@gmail.com" className="border border-teal-800 bg-transparent rounded outline-none focus-within:border-teal-600"></input>
            </div>

            {/* Buttons */}
            <div className="flex gap-1 pt-6 pl-38 justify-center items-center">
              <Link
                href=".."
                className="text-center border rounded-full border-solid border-transparent focus-within:border-teal-600 w-18 hover:bg-teal-600 bg-slate-700 text-white"
              >
                Cancel
              </Link>
              <button 
                type="submit"
                className="text-center border rounded-full border-solid border-transparent focus-within:border-teal-600 w-17 hover:bg-teal-600 bg-slate-700 text-white"
              >
                Create
              </button>
            </div>

            {/* if message exists (ie not null/""/false) - render <p> element. Otherwise render nothing. */}            
            {errorMessage && <p className="text-red-600 text-center pt-5">{errorMessage}</p>}
            {successMessage && <p className="text-black text-center pt-5 pl-20">{successMessage}</p>}
          </form>
        </main>
      </>
    )
  }