"use client"

import { useEffect, useState } from "react";
import { PaceVsElevation } from "../plots/practice_plot"

//TODO:
  //function to convert data into xy plot format [{x: 180, y: 7.2}, {x: 70, y: 6.6}]
  //Page function
    //logic for which graph is being shown (useState)

export default function Page() {
  
  const [activities, setActivities] = useState([]); //may not need
  const [startDate, setStartDate] = useState("1981-01-01");
  const [endDate, setEndDate] = useState("2081-01-01");
  const [userId, setUserId] = useState("");
  const [yAxis, setyAxis] = useState("");
  const [xAxis, setxAxis] = useState("");
  const [errorMessage, setErrorMessage] = useState("");
  //plotData = [{x: 180, y: 7.2}, {x: 70, y: 6.6}]

  async function fetchActivities() {
    try {
      const url = `http://localhost:8080/users/${userId}/activities?start_date=${startDate}&end_date=${endDate}`
    
      const response = await fetch(url)
      const data = await response.json()

      if (startDate > endDate) {
        return { success: false, error: `No activity data to plot. Please enter correct start and end dates.`}
      }

      if (!response.ok) {
        setActivities([]) 
        throw new Error(`HTTP error! Status: ${response.status}`)
      } else {
        setActivities(data)
        return { success: true }
      }

    } catch (error) {
      console.error("API Error", error)
      return { success: false, error: `No activity data to plot for user ID ${userId} between ${startDate} and ${endDate}. Please try again.`}
    }
  }

  async function handleSubmit(formData) {
    formData.preventDefault()
    const result = await fetchActivities()

    if (result.success) {
      setErrorMessage("")
    } else {
      setErrorMessage(result.error)
    }
  }

  return ( 
      <>
        <main>
          <p className="text-[45px] text-center py-8 font-semibold font-[family-name:var(--font-geist-mono)]">Visualise Activity Data</p>  
          <form onSubmit={handleSubmit} className="flex gap-2 flex-col justify-end">
            {/* User ID - add value and onChange to input*/}
            <div className="flex justify-end items-center gap-4">
              <label htmlFor="user_id" className="w-37 text-right font-12">User ID:</label> 
              <input 
                type="text"
                name="user_id"
                title="User ID number"
                placeholder="1"
                value={userId}
                onChange={(formData) => setUserId(formData.target.value)}
                className="w-40 border border-teal-800 bg-transparent rounded outline-none focus-within:border-teal-600"
                >
              </input>
            </div>

            {/* start date */}
            <div className="flex justify-end items-center gap-4">
              <label htmlFor="start_date" className="w-37 text-right font-12">Start date:</label> 
              <input 
                type="date"
                id="start_date"
                name="start_date"
                min="2020-01-01"
                max="2030-01-01"
                value={startDate} //does the date have a value??
                onChange={(formData) => setStartDate(formData.target.value)} //does the date have a value??
                className="w-40 border border-teal-800 bg-transparent rounded outline-none focus-within:border-teal-600"
                >
              </input>
            </div>

            {/* end date */}
            <div className="flex justify-end items-center gap-4">
              <label htmlFor="end_date" className="w-37 text-right font-12">End date:</label> 
              <input 
                type="date"
                id="end_date"
                name="end_date"
                min="2020-01-01"
                max="2030-01-01"
                value={endDate} //does the date have a value??
                onChange={(formData) => setEndDate(formData.target.value)} //does the date have a value??
                className="w-40 border border-teal-800 bg-transparent rounded outline-none focus-within:border-teal-600"
                >
              </input>
            </div>

            {/* plot y axis */}
            <div className="flex justify-end items-center gap-4">
              <label htmlFor="plot_type" className="w-80 text-right font-12">What would you like to plot on the y axis?</label> 
              <select
                id="y_axis"
                name="y_axis"
                value={yAxis}
                onChange={(formData) => setyAxis(formData.target.value)}
                className="w-40 border border-teal-800 bg-transparent rounded outline-none focus-within:border-teal-600"
                >
                <option value="pace">Pace (min/km)</option>
                <option value="speed">Speed (km/hr)</option>
              </select>
            </div>

            {/* plot x axis */}
            <div className="flex justify-end items-center gap-4">
              <label htmlFor="plot_type" className="w-80 text-right font-12">What would you like to plot on the x axis?</label> 
              <select
                id="x_axis"
                name="x_axis"
                value={xAxis}
                onChange={(formData) => setxAxis(formData.target.value)}
                className="w-40 border border-teal-800 bg-transparent rounded outline-none focus-within:border-teal-600"
                >
                <option value="distance">Distance (km)</option>
                <option value="elevation">Elevation (m)</option>
                <option value="perceived_effort">Perceived effort</option>
                <option value="date">Date</option>
              </select>
            </div>

            {/* button */}
            <div className="flex gap-1 pl-38 justify-end items-center">
              <button
                type="submit"
                className="text-center border rounded-full border-solid border-transparent focus-within:border-teal-600 w-17 hover:bg-teal-600 bg-slate-700 text-white"
              >
                Plot
              </button>
            </div>
            {/* if message exists (ie not null/""/false) - render <p> element. Otherwise render nothing. */}            
            {errorMessage && <p className="text-red-600 text-center pt-5">{errorMessage}</p>}
          </form>

          <div className="pt-15">
            <PaceVsElevation />
          </div>
        </main>
      </>
    )
  }