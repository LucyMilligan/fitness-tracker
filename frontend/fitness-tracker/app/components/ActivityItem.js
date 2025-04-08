export function ActivityItem({ activity }){
    return (
        <div className="py-3">
            <span className="font-bold">Activity: {activity.id} ({activity.activity})</span>
            <dl className="grid grid-cols-6 text-left">
                <dt>USER ID: </dt>
                <dd>{activity.user_id}</dd>
                <dt>ACTIVITY: </dt>
                <dd>{activity.activity}</dd>
                <dt>DATE: </dt>
                <dd>{activity.date}</dd>
                <dt>TIME: </dt>
                <dd>{activity.time}</dd>
                <dt>DISTANCE: </dt>
                <dd>{activity.distance_km} km</dd>
                <dt>ACTIVITY TYPE: </dt>
                <dd>{activity.activity_type}</dd>
                <dt>ELEVATION: </dt>
                <dd>{activity.elevation_m} m</dd>
                <dt>PERCEIVED EFFORT: </dt>
                <dd>{activity.perceived_effort}</dd>
                <dt>MOVING TIME: </dt>
                <dd>{activity.moving_time}</dd>
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