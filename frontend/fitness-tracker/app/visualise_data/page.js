"use client"

import { useState } from "react";
import { Plot } from "../plots/scatter_plot"
import { ActivityItem } from "../components/ActivityItem"
import getXYData from "../client_functions/getXYData"

//TODO:
  //make plot scale according to the size of the page

export default function Page() {
  
  const [activities, setActivities] = useState([])
  const [startDate, setStartDate] = useState("")
  const [endDate, setEndDate] = useState("")
  const [userId, setUserId] = useState("")
  const [yAxis, setyAxis] = useState("pace_float_mps")
  const [xAxis, setxAxis] = useState("distance_km")
  const [errorMessage, setErrorMessage] = useState("")
  const [plotData, setPlotData] = useState(null)
  const [plotYAxis, setPlotYAxis] = useState("")
  const [plotXAxis, setPlotXAxis] = useState("")
  const [plotTitle, setPlotTitle] = useState("")


  async function fetchActivities() {
    try {
      let url = `http://localhost:8080/users/${userId}/activities-to-plot/`
    
      if (startDate.trim() && endDate.trim()) {
        url += `?start_date=${startDate}&end_date=${endDate}`
      }

      if (startDate > endDate) {
        return { success: false, error: `No activity data to plot. Please enter correct start and end dates.`}
      }
      
      if (!userId) {
        return { success: false, error: `Please enter a User ID.`}
      }

      const response = await fetch(url)
      const data = await response.json()

      if (!response.ok) {
        return { success: false, error: `No activity data to plot for User ID ${userId} between the given dates. Please try again.`}
      }
      
      setActivities(data)
      return { success: true, data }

    } catch (error) {
      console.error("API Error", error)
      return { success: false, error: `Oops, something went wrong on our end. Not able to plot activity data right now.`}
    }
  }

  async function handleSubmit(formData) {
    formData.preventDefault()
    const result = await fetchActivities()

    if (result.success) {
      const newActities = result.data
      setErrorMessage("")

      setPlotData(getXYData(newActities, yAxis, xAxis))
      setPlotYAxis(await getPlotYAxis())
      setPlotXAxis(await getPlotXAxis())
      setPlotTitle(await getPlotTitle())
    } else {
      setErrorMessage(result.error)
    }
  }

  async function getPlotYAxis() {
    let yAxisTitle = ""
    switch(yAxis) {
      case "pace_float_mps":
        yAxisTitle = "Pace (min/km)"
        break
      case "speed_kmphr":
        yAxisTitle = "Speed (km/hr)"
        break
    }
    return yAxisTitle
  }

  async function getPlotXAxis() {
    let xAxisTitle = ""
    switch(xAxis) {
      case "distance_km":
        xAxisTitle = "Distance (km)"
        break
      case "elevation_m":
        xAxisTitle = "Elevation (m)"
        break
      case "perceived_effort":
        xAxisTitle = "Perceived Effort (1 [very easy] - 10 [maximum effort])"
        break
      case "date":
        xAxisTitle = "Date"
        break
    }
    return xAxisTitle
  }

  async function getPlotTitle() {
    const xAxisTitle = await getPlotXAxis()
    const yAxisTitle = await getPlotYAxis()
    const plotTitle = `${yAxisTitle} vs ${xAxisTitle}`
    return plotTitle
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
                min="1981-01-01"
                max="2081-01-01"
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
                min="1981-01-01"
                max="2081-01-01"
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
                <option value="pace_float_mps">Pace (min/km)</option>
                <option value="speed_kmphr">Speed (km/hr)</option>
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
                <option value="distance_km">Distance (km)</option>
                <option value="elevation_m">Elevation (m)</option>
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
            <Plot chartTitle={plotTitle} yAxisTitle={plotYAxis} xAxisTitle={plotXAxis} chartData={plotData}/>
          </div>

          {/* sense check that data correctly fetched */}
          {/* <ul className="text-center">
              {activities.map(activity => (
                  <ActivityItem key={activity.id} activity={activity} />
              ))}
          </ul> */}
        </main>
      </>
    )
  }