"use server";

export async function createUser(formData) {
  //create user response body - json
  const user_data = {
    "name": formData.get("name")?.valueOf(),
    "email": formData.get("email")?.valueOf()
  };
  const jsonData = JSON.stringify(user_data);

  //try to post user data to the API
  //if response not okay (i.e. not 200 status code), throw an error
  //error handled in the catch block
  try {
    const response = await fetch("http://127.0.0.1:8080/users/", {
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