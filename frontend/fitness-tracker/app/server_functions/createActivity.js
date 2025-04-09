"use server";

export async function createActivity(formData) {
  //create activity response body - json
  const activity_data = {
    "user_id": formData.get("user_id")?.valueOf(),
    "date": formData.get("date")?.valueOf(),
    "time": formData.get("time")?.valueOf(),
    "activity": formData.get("activity")?.valueOf(),
    "activity_type": formData.get("activity_type")?.valueOf(),
    "moving_time": formData.get("moving_time")?.valueOf(),
    "distance_km": formData.get("distance_km")?.valueOf(),
    "perceived_effort": formData.get("perceived_effort")?.valueOf(),
    "elevation_m": formData.get("elevation_m")?.valueOf()
  };
  const jsonData = JSON.stringify(activity_data);

  //try to post activity data to the API
  //if response not okay (i.e. not 200 status code), throw an error
  //error handled in the catch block
  try {
    const response = await fetch("http://127.0.0.1:8080/activities/", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: jsonData
    });

    if (!response.ok) {
      throw new Error(`HTTP error! Status: ${response.status}`);
    }

    const result = await response.json();
    console.log("Success:", result);
    return { success: true, data: result };

    } catch (error) {
      console.error("API Error:", error);
      return { success: false, error: "Something went wrong. Please try again."};
    }
}