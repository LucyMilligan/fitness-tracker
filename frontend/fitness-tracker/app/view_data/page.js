import { ActivityItem } from "../components/ActivityItem"

async function getActivityData() {
    "use server"
    return fetch('http://127.0.0.1:8080/activities/')
}

export default async function Page() {
    const data = await getActivityData()
    const activities = await data.json()
    console.log(activities)
    return (
        <>
            <main>
                <p className="text-[45px] text-center py-8 font-semibold font-[family-name:var(--font-geist-mono)]">View Activity Data</p>
                <ul className="text-center">
                    {activities.map(activity => (
                        <ActivityItem key={activity.id} activity={activity} />
                    ))}
                </ul>
            </main>
        </>
    )
}
