"use client";
import Link from "next/link";
import { useEffect, useState } from "react";
import { updateActivity } from "../server_functions/updateActivity"

// TODO: update the below function
    // needs to fetch activity data for the given activity ID (done)
    // set this info as the placeholders/defaultValues in the form (semi-done)
    // user input for the updated fields (done)
    // update database

export default function Page() {
  const [errorMessageId, setErrorMessageId] = useState("")
  const [errorMessageUpdate, setErrorMessageUpdate] = useState("")
  const [successMessageUpdate, setSuccessMessageUpdate] = useState("")
  const [activityId, setActivityId] = useState("")
  const [activityData, setActivityData] = useState("")
  // const [formData, setFormData] = useState({
  //   user_id: "",
  //   activity: "",
  //   activity_type: "",
  //   date: "",
  //   time: "",
  //   elevation_m: "",
  //   distance_km: "",
  //   moving_time: "",
  //   perceived_effort: ""
  // })
  
  async function fetchActivities(activityId) {
    try {
      const url = `http://localhost:8080/activities/${activityId}`
      
      const response = await fetch(url)
      
      if (!response.ok) {
        throw new Error(`HTTP error! Status: ${response.status}`)
      } 
      
      const data = await response.json()
      
      setActivityData(data)
      // setFormData({
      //   user_id: data.user_id,
      //   activity: data.activity,
      //   activity_type: data.activity_type,
      //   date: data.date,
      //   time: data.time,
      //   elevation_m: data.elevation_m,
      //   distance_km: data.distance_km,
      //   moving_time: data.moving_time,
      //   perceived_effort: data.perceived_effort
      // })
      
      return {success: true}
      
    } catch (error) {
      console.error("API Error", error)
      setActivityData([])
      return {success: false, error: `Activity ID ${activityId} does not exist. Please try again.`}
    }
  }
  
  
  // useEffect (React hook) runs side effect after component renders. 
  // Second arg [activityId] - dependancy array (tell it to only run effect when the value changes)
  // useEffect(() => {
  //   if (activityId) {
  //     fetchActivities(activityId)
  //   }
  // }, [activityId])


  async function handleActivityIdSubmit() {
    const result = await fetchActivities(activityId)

    if (result.success) {
      setErrorMessageId("")
    } else {
      setErrorMessageId(result.error)
    }
  }

  // TODO: write updateActivity function
  async function handleUpdateSubmit(formData) {
    const result = await updateActivity(formData);

    if (result.success) {
      setSuccessMessageUpdate("Activity updated!");
      setErrorMessageUpdate("");
    } else {
      setErrorMessageUpdate(result.error);
      setSuccessMessageUpdate("");
    }
  }


  function defaultActivityValues(attribute) {
    const activityValues = activityData
    const activityValue = activityValues[attribute]
    return activityValue
  }
  
  // {/* Bug: default values don't update if previously edited (because defaultValue is only used in the first render) */}
  // {/* Bug: drop downs don't change to default values */}
  // {/* Bug: "update activity ID X below" - would rather the number change when Enter is clicked */}
  return ( 
      <>
        <main>
          <p className="text-[45px] text-center py-8 font-semibold font-[family-name:var(--font-geist-mono)]">Update Activity Data</p>
          <form action={handleActivityIdSubmit} className="flex gap-2 flex-col">
            {/* Activity_id input */}  
            <div className="flex items-center gap-4">
              <label htmlFor="id" className="w-80 text-right">Which Activity ID would you like to update?</label>          
              <input 
                type="text" 
                name="id" 
                title="Activity ID number" 
                placeholder="1" 
                defaultValue={activityId}
                onChange={(formData) => setActivityId(formData.target.value)}
                className="w-10 border border-teal-800 bg-transparent rounded outline-none focus-within:border-teal-600"></input>
              <button 
                type="submit"
                className="text-center border rounded-full border-solid border-transparent focus-within:border-teal-600 w-17 hover:bg-teal-600 bg-slate-700 text-white"
              >
                Enter
              </button>
            </div>
            {/* if message exists (ie not null/""/false) - render <p> element. Otherwise render nothing. */}            
            {errorMessageId && <p className="text-red-600 text-center pt-5">{errorMessageId}</p>}
          </form>
          
          <p className="py-10 font-semibold text-center">Update Activity ID {activityId} below:</p>
          
          <form action={handleUpdateSubmit} className="flex gap-2 flex-col">
            {/* User_id input */}  
            <div className="flex items-center gap-4">
              <label htmlFor="user_id" className="w-50 text-right">User ID:</label>          
              <input 
                type="text" 
                name="user_id" 
                title="User ID number" 
                placeholder={defaultActivityValues("user_id")} 
                defaultValue={defaultActivityValues("user_id")} 
                className="border border-teal-800 bg-transparent rounded outline-none focus-within:border-teal-600"></input>
            </div>

            {/* Activity input */}
            <div className="flex items-center gap-4">
              <label htmlFor="activity" className="w-50 text-right">Activity:</label>
              <select 
                name="activity"
                className="w-45 border border-teal-800 bg-transparent rounded outline-none focus-within:border-teal-600"
                defaultValue={defaultActivityValues("activity")} 
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
                defaultValue={defaultActivityValues("activity_type")} 
                >
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
                defaultValue={defaultActivityValues("date")}
                className="w-45 border border-teal-800 bg-transparent rounded outline-none focus-within:border-teal-600"></input>
            </div>

            {/* Time input */}  
            <div className="flex items-center gap-4">
              <label htmlFor="time" className="w-50 text-right">Time:</label>          
              <input 
                type="time" 
                name="time"
                title="hh:mm"
                defaultValue={defaultActivityValues("time")} 
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
                defaultValue={defaultActivityValues("elevation_m")} 
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
                defaultValue={defaultActivityValues("distance_km")}  
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
                defaultValue={defaultActivityValues("moving_time")}
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
                defaultValue={defaultActivityValues("perceived_effort")}
                >
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
            {errorMessageUpdate && <p className="text-red-600 text-center pt-5">{errorMessageUpdate}</p>}
            {successMessageUpdate && <p className="text-black text-center pl-45 pt-5">{successMessageUpdate}</p>}
          </form>
        </main>
      </>
    )
  }