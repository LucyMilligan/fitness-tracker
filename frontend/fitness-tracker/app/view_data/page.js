"use client"

import { useEffect, useState } from "react";
import { ActivityItem } from "../components/ActivityItem"


export default function Page() {

    const [activities, setActivities] = useState([]);
    const [sortBy, setSortBy] = useState("id");
    const [orderBy, setOrderBy] = useState("ASC");
    const [userId, setUserId] = useState("");
    const [errorMessage, setErrorMessage] = useState("");

    // fetch activities when form is submitted
    async function fetchActivities() {
        try {
            let url = "http://localhost:8080"

            // if a user_id is specified, use a different endpoint
            if (userId.trim()) {
                url += `/users/${userId}/activities`
            } else {
                url += `/activities`
            };

            // add query parameters
            url += `/?sort_by=${sortBy}&order_by=${orderBy}`

            const response = await fetch(url)
            const data = await response.json()

            // raise and handle errors. Add data to activities
            if (!response.ok) {
                setActivities([]) 
                throw new Error(`HTTP error! Status: ${response.status}`)
            } else {
                setActivities(data)
                return { success: true }
            }
        } catch (error) {
            console.error("API Error", error)
            return { success: false, error: `No activity data for User ID ${userId}. Please try again.`}
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

    // fetch on first load with default sorting ([] means its only run once)
    useEffect(() => {fetchActivities()}, [])

    return (
        <>
            <main>
                <p className="text-[45px] text-center py-8 font-semibold font-[family-name:var(--font-geist-mono)]">View Activity Data</p>
                <form onSubmit={handleSubmit} className="flex gap-2 flex-col justify-end">
                    {/* sort by */}  
                    <div className="flex justify-end items-center gap-4">
                        <label htmlFor="sort_by" className="w-37 text-right font-12">Sort by:</label>          
                        <select 
                            id="sort_by" 
                            name="sort_by"
                            value={sortBy}
                            onChange={(formData) => setSortBy(formData.target.value)}
                            className="border border-teal-800 bg-transparent rounded outline-none focus-within:border-teal-600 w-45 "
                        >
                            <option value="id">ID</option>
                            <option value="user_id">User ID</option>
                            <option value="date">Date</option>
                            <option value="time">Time</option>
                            <option value="activity">Activity</option>
                            <option value="activity_type">Activity type</option>
                            <option value="moving_time">Moving time</option>
                            <option value="distance_km">Distance</option>
                            <option value="perceived_effort">Perceived effort</option>
                            <option value="elevation_m">Elevation</option>
                        </select>
                    </div>

                    {/* order by */}
                    <div className="flex justify-end items-center gap-4">
                        <label htmlFor="order_by" className="w-37 text-right">Order by:</label>
                        <select 
                            id="order_by" 
                            name="order_by" 
                            value={orderBy}
                            onChange={(formData) => setOrderBy(formData.target.value)}
                            className="border border-teal-800 bg-transparent rounded outline-none focus-within:border-teal-600 w-45"
                        >
                            <option value="ASC">Ascending</option>
                            <option value="DESC">Descending</option>
                        </select>                    
                    </div>

                    {/* user_id input */}  
                    <div className="flex justify-end items-center gap-4">
                        <label htmlFor="user_id" className="w-37 text-right">Filter by User ID (optional):</label>          
                        <input 
                            type="text" 
                            name="user_id"
                            title="User ID number, optional"
                            value={userId}
                            onChange={(formData) => setUserId(formData.target.value)}
                            placeholder="1" 
                            className="border border-teal-800 bg-transparent rounded outline-none focus-within:border-teal-600">
                        </input>
                    </div>

                    {/* Button */}
                    <div className="flex gap-1 pl-38 justify-end items-center">
                        <button 
                            type="submit"
                            className="text-center border rounded-full border-solid border-transparent focus-within:border-teal-600 w-17 hover:bg-teal-600 bg-slate-700 text-white"
                        >
                        Apply
                        </button>
                    </div>
                    {/* if message exists (ie not null/""/false) - render <p> element. Otherwise render nothing. */}            
                    {errorMessage && <p className="text-red-600 text-center pt-5">{errorMessage}</p>}
                </form>
                <ul className="text-center">
                    {activities.map(activity => (
                        <ActivityItem key={activity.id} activity={activity} />
                    ))}
                </ul>
            </main>
        </>
    )
}
