import Link from "next/link";

async function createActivity(data) {
  "use server"
  //how to handle API errors?? 
  //use API to post the activity to the db
  // const activity = data.get("activity")?.valueOf();
  const activity_data = {
    "user_id": data.get("user_id")?.valueOf(),
    "date": data.get("date")?.valueOf(),
    "time": data.get("time")?.valueOf(),
    "activity": data.get("activity")?.valueOf(),
    "activity_type": data.get("activity_type")?.valueOf(),
    "moving_time": data.get("moving_time")?.valueOf(),
    "distance_km": data.get("distance_km")?.valueOf(),
    "perceived_effort": data.get("perceived_effort")?.valueOf(),
    "elevation_m": data.get("elevation_m")?.valueOf()
  };
  const jsonData = JSON.stringify(activity_data);

  fetch("http://127.0.0.1:8080/activities/", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: jsonData
  })
  .then(response => {
    if (!response.ok) {
      throw new Error(`HTTP error! Status: ${response.status}`);
    }
    return response.json();
  })
  .then(data => console.log("Success:", data))
  .catch(error => console.log("Error:", error));
}

export default function Page() {
    return ( 
      <>
        <main>
          <p className="text-[45px] text-center py-8 font-semibold font-[family-name:var(--font-geist-mono)]">Enter Activity Data</p>
          <p className="py-6 font-semibold text-center">Enter your latest activity data below:</p>
          <form action={createActivity} className="flex gap-2 flex-col">
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
            <div className="flex gap-1 pt-8 pl-40 justify-center items-center">
              <Link
                href=".."
                className="text-center border rounded-full border-solid border-transparent focus-within:border-teal-600 w-15 hover:bg-teal-600 bg-slate-700 text-white"
              >
                Cancel
              </Link>
              <button 
                type="submit"
                className="text-center border rounded-full border-solid border-transparent focus-within:border-teal-600 w-15 hover:bg-teal-600 bg-slate-700 text-white"
              >
                Create
              </button>
            </div>          
          </form>
        </main>
      </>
    )
  }