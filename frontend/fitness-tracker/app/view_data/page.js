// export default function Page() {
//     return <p>View Activity Data Page</p>;
// }

export default async function Page() {
    const data = await fetch('http://127.0.0.1:8080/activities/')
    const activities = await data.json()
    return (
        <ul>
            {activities.map((activity) => (
                <li key={activity.id}>{activity.moving_time}</li>
            ))}
        </ul>
    )
}