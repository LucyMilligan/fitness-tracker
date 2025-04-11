export function ActivityItem({ activity }){
    return (
        <div className="py-3">
            <span className="font-bold">Activity: {activity.id} ({activity.activity})</span>
            <dl className="grid grid-cols-6 text-left">
                <dt className="text-right pr-2">USER ID: </dt>
                <dd>{activity.user_id}</dd>
                <dt className="text-right pr-2">ACTIVITY: </dt>
                <dd>{activity.activity}</dd>
                <dt className="text-right pr-2">ACTIVITY TYPE: </dt>
                <dd>{activity.activity_type}</dd>
                <dt className="text-right pr-2">DATE: </dt>
                <dd>{activity.date}</dd>
                <dt className="text-right pr-2">TIME: </dt>
                <dd>{activity.time}</dd>
                <dt className="text-right pr-2">ELEVATION: </dt>
                <dd>{activity.elevation_m} m</dd>
                <dt className="text-right pr-2">DISTANCE: </dt>
                <dd>{activity.distance_km} km</dd>
                <dt className="text-right pr-2">MOVING TIME: </dt>
                <dd>{activity.moving_time}</dd>
                <dt className="text-right pr-2">PERCEIVED EFFORT: </dt>
                <dd>{activity.perceived_effort}</dd>
            </dl>
        </div>
    )
};

// {
//     time: 'string',
//     activity: 'string',
//     date: 'string',
//     user_id: 2,
//     moving_time: 'string',
//     perceived_effort: 9,
//     id: 4,
//     activity_type: 'string',
//     distance_km: 6,
//     elevation_m: 7
//   }