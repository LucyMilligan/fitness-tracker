"use client";
import Link from "next/link";
import { useState } from "react";
import { createActivity } from "../server_functions/createActivity"


export default function Page() {
  const [errorMessage, setErrorMessage] = useState("")
  const [successMessage, setSuccessMessage] = useState("")
  
  async function handleSubmit(formData) {
    const result = await createActivity(formData);

    if (result.success) {
      setSuccessMessage("Activity added!");
      setErrorMessage("");
    } else {
      setErrorMessage(result.error);
      setSuccessMessage("");
    }
  }
  
  return ( 
      <>
        <main>
          <p className="text-[45px] text-center py-8 font-semibold font-[family-name:var(--font-geist-mono)]">Enter Activity Data</p>
          <p className="py-6 font-semibold text-center">Enter your latest activity data below:</p>
          <form action={handleSubmit} className="flex gap-2 flex-col">
            {/* User_id input */}  
            <div className="flex items-center gap-4">
              <label htmlFor="user_id" className="w-50 text-right">User ID:</label>          
              <input type="text" name="user_id" title="User ID number" placeholder="1" className="border border-teal-800 bg-transparent rounded outline-none focus-within:border-teal-600"></input>
            </div>

            {/* Activity input */}
            <div className="flex items-center gap-4">
              <label htmlFor="activity" className="w-50 text-right">Activity:</label>
              <input type="text" name="activity" title="Sport - run, bike" placeholder="run" className="border border-teal-800 bg-transparent rounded outline-none focus-within:border-teal-600"></input>
            </div>

            {/* Activity type input */}  
            <div className="flex items-center gap-4">
              <label htmlFor="activity_type" className="w-50 text-right">Type of activity:</label>          
              <input type="text" name="activity_type" title="Type of activity - trail, road" placeholder="road" className="border border-teal-800 bg-transparent rounded outline-none focus-within:border-teal-600"></input>
            </div>            

            {/* Date input */}  
            <div className="flex items-center gap-4">
              <label htmlFor="date" className="w-50 text-right">Date:</label>          
              <input type="text" name="date" title="format YYYY/MM/DD" placeholder="2025/01/01" className="border border-teal-800 bg-transparent rounded outline-none focus-within:border-teal-600"></input>
            </div>

            {/* Time input */}  
            <div className="flex items-center gap-4">
              <label htmlFor="time" className="w-50 text-right">Time:</label>          
              <input type="text" name="time" title="format hh:mm (24hr)" placeholder="17:30" className="border border-teal-800 bg-transparent rounded outline-none focus-within:border-teal-600"></input>
            </div> 

            {/* Elevation input */}  
            <div className="flex items-center gap-4">
              <label htmlFor="elevation_m" className="w-50 text-right">Elevation (m):</label>          
              <input type="text" name="elevation_m" title="meters" placeholder="25" className="border border-teal-800 bg-transparent rounded outline-none focus-within:border-teal-600"></input>
            </div>  

            {/* Distance input */}  
            <div className="flex items-center gap-4">
              <label htmlFor="distance_km" className="w-50 text-right">Distance (km):</label>          
              <input type="text" name="distance_km" title="km" placeholder="5.05" className="border border-teal-800 bg-transparent rounded outline-none focus-within:border-teal-600"></input>
            </div>                    

            {/* Moving time input */}  
            <div className="flex items-center gap-4">
              <label htmlFor="moving_time" className="w-50 text-right">Moving time:</label>          
              <input type="text" name="moving_time" title="format hh:mm:ss" placeholder="00:32:52" className="border border-teal-800 bg-transparent rounded outline-none focus-within:border-teal-600"></input>
            </div>  

            {/* Perceived effort input */}  
            <div className="flex items-center gap-4">
              <label htmlFor="perceived_effort" className="w-50 text-right">Perceived effort:</label>          
              <input type="text" name="perceived_effort" title="1 (very easy) to 10 (very hard)" placeholder="6" className="border border-teal-800 bg-transparent rounded outline-none focus-within:border-teal-600"></input>
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
            {successMessage && <p className="text-black text-center pl-45 pt-5">{successMessage}</p>}
          </form>
        </main>
      </>
    )
  }