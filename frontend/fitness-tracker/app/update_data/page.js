"use client";
import Link from "next/link";
import { useState } from "react";
import { updateActivity } from "../server_functions/updateActivity"

// TODO: update the below function
    // needs to fetch activity data for the given activity ID
    // set this info as the placeholders/defaultValues in the form
    // user input for the updated fields
    // update database

export default function Page() {
  const [errorMessage, setErrorMessage] = useState("")
  const [successMessage, setSuccessMessage] = useState("")
  const [activityId, setActivityId] = useState("")
  
  // TODO: update the below function
  async function handleSubmit(formData) {
    const result = await updateActivity(formData);

    if (result.success) {
      setSuccessMessage("Activity updated!");
      setErrorMessage("");
    } else {
      setErrorMessage(result.error);
      setSuccessMessage("");
    }
  }

  // TODO: update with fetched activity data
  function placeholders(attribute) {
    const placeholderValues = {
        userId: 3,
        activity: "Run",
        activity_type: "Road",
        date: "2025-05-01",
        time: "17:00",
        elevation_m: 200,
        distance_km: 5.00,
        moving_time: "00:30:00",
        perceived_effort: 5
    }
    const placeholderValue = placeholderValues[attribute]
    return placeholderValue
  }
  
  return ( 
      <>
        <main>
          <p className="text-[45px] text-center py-8 font-semibold font-[family-name:var(--font-geist-mono)]">Update Activity Data</p>
          {/* TODO: Add action={something} to form */}
          <form className="flex gap-2 flex-col">
            {/* Activity_id input */}  
            <div className="flex items-center gap-4">
              <label htmlFor="id" className="w-80 text-right">Which Activity ID would you like to update?</label>          
              <input 
                type="text" 
                name="id" 
                title="Activity ID number" 
                placeholder="1" 
                className="w-10 border border-teal-800 bg-transparent rounded outline-none focus-within:border-teal-600"></input>
              <Link
                href=".."
                className="text-center border rounded-full border-solid border-transparent focus-within:border-teal-600 w-18 hover:bg-teal-600 bg-slate-700 text-white"
              >
                Enter
              </Link>
            </div>
            </form>
          
          <p className="py-10 font-semibold text-center">Update your activity below:</p>
          
          {/* TODO: Add action={handleSubmit} to form */}
          <form action={handleSubmit} className="flex gap-2 flex-col">
            {/* User_id input */}  
            <div className="flex items-center gap-4">
              <label htmlFor="user_id" className="w-50 text-right">User ID:</label>          
              <input 
                type="text" 
                name="user_id" 
                title="User ID number" 
                placeholder={placeholders("userId")} 
                defaultValue={placeholders("userId")} 
                className="border border-teal-800 bg-transparent rounded outline-none focus-within:border-teal-600"></input>
            </div>

            {/* Activity input */}
            <div className="flex items-center gap-4">
              <label htmlFor="activity" className="w-50 text-right">Activity:</label>
              <select 
                name="activity"
                className="w-45 border border-teal-800 bg-transparent rounded outline-none focus-within:border-teal-600"
                defaultValue={placeholders("activity")} 
                >
                <option value="run">Run</option>
              </select>
            </div>

            {/* Activity type input */}  
            <div className="flex items-center gap-4">
              <label htmlFor="activity_type" className="w-50 text-right">Type of activity:</label>          
              <select 
                name="activity_type"
                className="w-45 border border-teal-800 bg-transparent rounded outline-none focus-within:border-teal-600"
                defaultValue={placeholders("activity_type")} 
                >
                <option value="" disabled selected hidden></option>
                <option value="road">Road</option>
                <option value="trail">Trail</option>
              </select>
            </div>            

            {/* Date input */}  
            <div className="flex items-center gap-4">
              <label htmlFor="date" className="w-50 text-right">Date:</label>          
              <input 
                type="date" 
                name="date" 
                min="1981-01-01"
                max="2081-01-01"
                defaultValue={placeholders("date")}
                className="w-45 border border-teal-800 bg-transparent rounded outline-none focus-within:border-teal-600"></input>
            </div>

            {/* Time input */}  
            <div className="flex items-center gap-4">
              <label htmlFor="time" className="w-50 text-right">Time:</label>          
              <input 
                type="time" 
                name="time"
                title="hh:mm"
                defaultValue={placeholders("time")} 
                className="w-45 border border-teal-800 bg-transparent rounded outline-none focus-within:border-teal-600"></input>
            </div> 

            {/* Elevation input */}  
            <div className="flex items-center gap-4">
              <label htmlFor="elevation_m" className="w-50 text-right">Elevation (m):</label>          
              <input 
                type="text" 
                name="elevation_m" 
                title="meters" 
                placeholder="25"
                defaultValue={placeholders("elevation_m")} 
                className="border border-teal-800 bg-transparent rounded outline-none focus-within:border-teal-600"></input>
            </div>  

            {/* Distance input */}  
            <div className="flex items-center gap-4">
              <label htmlFor="distance_km" className="w-50 text-right">Distance (km):</label>          
              <input 
                type="text" 
                name="distance_km" 
                title="km" 
                placeholder="5.05"
                defaultValue={placeholders("distance_km")}  
                className="border border-teal-800 bg-transparent rounded outline-none focus-within:border-teal-600"></input>
            </div>                    

            {/* Moving time input */}  
            <div className="flex items-center gap-4">
              <label htmlFor="moving_time" className="w-50 text-right">Moving time:</label>          
              <input 
                type="time" 
                name="moving_time" 
                title="hh:mm:ss" 
                step="1" //steps in increments of 1 second
                defaultValue={placeholders("moving_time")}
                className="w-45 border border-teal-800 bg-transparent rounded outline-none focus-within:border-teal-600">
              </input>
            </div>  

            {/* Perceived effort input */}  
            <div className="flex items-center gap-4">
              <label htmlFor="perceived_effort" className="w-50 text-right">Perceived effort:</label>
              <select
                name="perceived_effort"
                title="1 (very easy) to 10 (very hard)" 
                className="w-45 border border-teal-800 bg-transparent rounded outline-none focus-within:border-teal-600"
                defaultValue={placeholders("perceived_effort")}
                >
                <option value="" disabled selected hidden></option>
                <option value="1">1 (extremely easy)</option>
                <option value="2">2 (very easy)</option>
                <option value="3">3 (easy)</option>
                <option value="4">4 (moderately easy)</option>
                <option value="5">5 (moderate)</option>
                <option value="6">6 (moderately hard)</option>
                <option value="7">7 (hard)</option>
                <option value="8">8 (very hard)</option>
                <option value="9">9 (very very hard)</option>
                <option value="10">10 (maximum effort)</option>
              </select>
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
                Update
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