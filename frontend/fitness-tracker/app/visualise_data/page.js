"use client"
import { PaceVsElevation } from "../plots/practice_plot"

//TODO:
  //create a new API which returns:
    //original data, plus pace (min/km) and speed (km/hr) - will need util functions
    //dates in a format that can easily be converted to datetime in JS (YYYY-MM-DDT00:00:00.000Z)
    //data between given dates (all if no dates specified)
    //data for a given user
  //function to fetch activities when form is submitted (similar to view)
  //handleSubmit function
  //Page function
    //logic for which graph is being shown (useState)
    //add onSubmit={handleSubmit} to form - create function for handleSubmit
    //add value and onChange to each form item

export default function Page() {
    return ( 
      <>
        <main>
          <p className="text-[45px] text-center py-8 font-semibold font-[family-name:var(--font-geist-mono)]">Visualise Activity Data</p>  
          <form className="flex gap-2 flex-col justify-end">
            {/* User ID - add value and onChange to input*/}
            <div className="flex justify-end items-center gap-4">
              <label htmlFor="user_id" className="w-37 text-right font-12">User ID:</label> 
              <input 
                type="text"
                name="user_id"
                title="User ID number"
                placeholder="1" 
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
                className="w-40 border border-teal-800 bg-transparent rounded outline-none focus-within:border-teal-600"
                >
              </input>
            </div>

            {/* plot type */}
            <div className="flex justify-end items-center gap-4">
              <label htmlFor="plot_type" className="w-70 text-right font-12">What would you like to plot?</label> 
              <select
                id="plot_type"
                name="plot_type"
                className="w-40 border border-teal-800 bg-transparent rounded outline-none focus-within:border-teal-600"
                >
                <option value="paceVsElev">Pace vs Elevation</option>
                <option value="paceVsElev">Pace vs Perceived effort</option>
                <option value="paceVsElev">Pace vs Distance</option>
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
          </form>
          <div className="pt-15">
            <PaceVsElevation />
          </div>
        </main>
      </>
    )
  }