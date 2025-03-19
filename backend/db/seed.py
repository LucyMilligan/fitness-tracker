from connection import connect_to_db
import json

def seed_db(env="test"):
    print("Seeding Database....")
    db = connect_to_db()
    db.run("DROP TABLE if exists activities")
    db.run("DROP TABLE if exists users")

    db.run(
        'CREATE TABLE users (\
        user_id SERIAL PRIMARY KEY, \
        name VARCHAR(20), \
        email VARCHAR(50))' \
    )

    db.run(
        'CREATE TABLE activities (\
        id SERIAL PRIMARY KEY, \
        user_id INT REFERENCES users(user_id), \
        date VARCHAR(10), \
        time VARCHAR(5), \
        activity VARCHAR (25), \
        activity_type VARCHAR(25), \
        moving_time VARCHAR(8), \
        distance_km FLOAT, \
        perceived_effort INT, \
        elevation_m INT, \
        date_updated DATETIME)' \
    )

    with open(f'data/{env}-data/users.json', 'r') as file:
        users_data = json.load(file)
        row_count = 0
        for user in users_data:
            db.run(
                'INSERT INTO users (name, email)\
                VALUES (:name, :email)',
                name=user["name"],
                email=user["email"]
            )
            row_count += 1

        print(f"Successfully seeded {row_count} rows to 'users' table in the database")

    users = db.run('SELECT * FROM users')
    user_ids = {user[1]: user[0] for user in users} #dict of "name": user_id

    with open(f'data/{env}-data/activities.json', 'r') as file:
        activities_data = json.load(file)
        row_count = 0
        for activity in activities_data:
            activity_values = {
                "user_id": user_ids[activity["name"]] if "name" in activity else None,
                "date": activity["date"] if "date" in activity else None,
                "time": activity["time"] if "time" in activity else None,
                "activity": activity["activity"] if "activity" in activity else None,
                "activity_type": activity["activity_type"] if "activity_type" in activity else None,
                "moving_time": activity["moving_time"] if "moving_time" in activity else None,
                "distance_km": activity["distance_km"] if "distance_km" in activity else None,
                "perceived_effort": activity["perceived_effort"] if "perceived_effort" in activity else None,
                "elevation_m": activity["elevation_m"] if "elevation_m" in activity else None,
                "date_updated": activity["date_updated"] if "date_updated" in activity else None
            }
            db.run(
                'INSERT INTO activities (user_id, date, time \
                activity, activity_type, moving_time, distance_km \
                perceived_effort, elevation_m, date_updated) \
                VALUES (:user_id, :date, :time \
                :activity, :activity_type, :moving_time, :distance_km \
                :perceived_effort, :elevation_m, :date_updated)',
                **activity_values
            )
            row_count += 1
        print(f"Successfully seeded {row_count} rows to 'users' table in the database")