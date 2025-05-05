from flask import Flask, render_template, jsonify
from db_config import get_connection
import warnings
import requests
warnings.filterwarnings("ignore", category=UserWarning, message="resource_tracker")


app = Flask(__name__)

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/analysis")
def analysis():
    return render_template("analysis.html")

@app.route("/api/season-champions")
def season_champions():
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)

    query = """
        SELECT R.year, D.forename, D.surname, DS.points
        FROM DriverStandings DS
        JOIN Races R ON DS.raceId = R.raceId
        JOIN Drivers D ON DS.driverId = D.driverId
        WHERE (R.raceId, DS.points) IN (
            SELECT raceId, MAX(points)
            FROM DriverStandings
            GROUP BY raceId
        )
        AND R.raceId IN (
            SELECT MAX(raceId)
            FROM Races
            GROUP BY year
        )
        ORDER BY R.year;
    """

    cursor.execute(query)
    results = cursor.fetchall()
    return jsonify(results)

@app.route("/api/top-constructors")
def top_constructors():
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("""
        SELECT C.name, SUM(CS.points) AS points
        FROM ConstructorStandings CS
        JOIN Constructors C ON CS.constructorId = C.constructorId
        GROUP BY CS.constructorId
        ORDER BY points DESC
        LIMIT 10;
    """)
    return jsonify(cursor.fetchall())

@app.route("/api/fastest-pitstops")
def fastest_pitstops():
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("""
        SELECT D.forename, D.surname, MIN(P.milliseconds) AS milliseconds
        FROM PitStops P
        JOIN Drivers D ON P.driverId = D.driverId
        GROUP BY P.driverId
        ORDER BY milliseconds ASC
        LIMIT 10;
    """)
    return jsonify(cursor.fetchall())

@app.route("/api/top-constructors/<int:year>")
def top_constructors_by_year(year):
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)

    query = """
        SELECT C.name, CS.points
        FROM ConstructorStandings CS
        JOIN Constructors C ON CS.constructorId = C.constructorId
        JOIN Races R ON CS.raceId = R.raceId
        WHERE R.year = %s
          AND R.raceId = (
              SELECT MAX(raceId)
              FROM Races
              WHERE year = %s
          )
        ORDER BY CS.points DESC
        LIMIT 10;
    """

    cursor.execute(query, (year, year))
    results = cursor.fetchall()
    return jsonify(results)


@app.route("/api/seasons")
def get_seasons():
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT DISTINCT year FROM Races ORDER BY year DESC;")
    return jsonify([row['year'] for row in cursor.fetchall()])

@app.route("/teams")
def teams():
    return render_template("teams.html")

@app.route("/circuits")
def circuits():
    return render_template("circuits.html")

@app.route("/drivers")
def drivers():
    return render_template("drivers.html")

@app.route("/api/teams-drivers")
def teams_drivers():
    import json
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("""
        SELECT R.constructorId, R.driverId, SUM(R.points) AS points
        FROM Results R
        GROUP BY R.constructorId, R.driverId
    """)
    points_data = cursor.fetchall()

    # Now get constructor and driver names
    cursor.execute("SELECT constructorId, name FROM Constructors")
    constructors = {row["constructorId"]: row["name"] for row in cursor.fetchall()}

    cursor.execute("SELECT driverId, forename, surname FROM Drivers")
    drivers = {
        row["driverId"]: f"{row['forename']} {row['surname']}" for row in cursor.fetchall()
    }

    team_data = {}
    for row in points_data:
        team = constructors.get(row["constructorId"], "Unknown")
        driver = drivers.get(row["driverId"], "Unknown")
        if team not in team_data:
            team_data[team] = []
        team_data[team].append({
            "name": driver,
            "points": row["points"]
        })

    return json.dumps([
        {"team": team, "drivers": sorted(dlist, key=lambda x: -x["points"])}
        for team, dlist in team_data.items()
    ])

@app.route("/api/circuits-fastest-laps")
def circuits_fastest_laps():
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("""
        SELECT C.name AS circuit, C.country, D.forename, D.surname, R.fastestLapTime
        FROM Results R
        JOIN Races Ra ON R.raceId = Ra.raceId
        JOIN Circuits C ON Ra.circuitId = C.circuitId
        JOIN Drivers D ON R.driverId = D.driverId
        WHERE R.fastestLapTime IS NOT NULL
    """)
    all_laps = cursor.fetchall()

    best_laps = {}
    for row in all_laps:
        key = row["circuit"]
        current_best = best_laps.get(key)
        if not current_best or row["fastestLapTime"] < current_best["lap_time"]:
            best_laps[key] = {
                "circuit": key,
                "country": row["country"],
                "driver": f"{row['forename']} {row['surname']}",
                "lap_time": row["fastestLapTime"]
            }

    return list(best_laps.values())

@app.route("/drivers")
def drivers_page():
    return render_template("drivers.html")

@app.route("/api/drivers")
def get_all_drivers():
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM Drivers ORDER BY surname ASC")
    return cursor.fetchall()

@app.route("/api/add-driver", methods=["POST"])
def add_driver():
    from flask import request
    data = request.json
    conn = get_connection()
    cursor = conn.cursor()

    # Safely handle empty number field
    number = data.get("number")
    number = int(number) if number and number.strip() != "" else None

    cursor.execute("SELECT MAX(driverId) FROM Drivers")
    max_id = cursor.fetchone()[0] or 0
    next_id = max_id + 1

    cursor.execute("""
        INSERT INTO Drivers (driverId, driverRef, number, code, forename, surname, dob, nationality, url)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
    """, (
        next_id,
        data["driverRef"],
        number,
        data.get("code"),
        data["forename"],
        data["surname"],
        data["dob"],
        data["nationality"],
        data["url"]
    ))
    conn.commit()
    return {"message": "Driver added successfully!"}, 201

@app.route("/api/update-driver/<int:driverId>", methods=["PUT"])
def update_driver(driverId):
    from flask import request
    data = request.json
    conn = get_connection()
    cursor = conn.cursor()

    # Convert '' to None for nullable fields
    number = data.get("number")
    number = int(number) if number and number.strip() != "" else None
    code = data.get("code") or None
    url = data.get("url") or None

    cursor.execute("""
        UPDATE Drivers
        SET driverRef=%s, number=%s, code=%s, forename=%s, surname=%s,
            dob=%s, nationality=%s, url=%s
        WHERE driverId=%s
    """, (
        data["driverRef"], number, code,
        data["forename"], data["surname"],
        data["dob"], data["nationality"], url,
        driverId
    ))
    conn.commit()
    return {"message": "Driver updated!"}, 200

@app.route("/api/delete-driver/<int:driverId>", methods=["DELETE"])
def delete_driver(driverId):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM Drivers WHERE driverId = %s", (driverId,))
    conn.commit()
    return {"message": "Driver deleted"}, 200

@app.route("/schedule")
def schedule_page():
    return render_template("schedule.html")

@app.route("/api/schedule")
def get_schedule():
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM F1_2025_Schedule ORDER BY date;")
    return jsonify(cursor.fetchall())


@app.route('/api/f1-news')
def get_f1_news():
      url = "https://f1-latest-news.p.rapidapi.com/news"
      headers = {
          "X-RapidAPI-Key": "15c6438a9fmsh1ff533fe115fd39p148f30jsnfe4f580121d4",
          "X-RapidAPI-Host": "f1-latest-news.p.rapidapi.com"
      }
      response = requests.get(url, headers=headers)
      return jsonify(response.json())
    
@app.route("/api/most-poles")
def most_poles():
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)

    query = """
        SELECT D.forename, D.surname, COUNT(*) AS pole_count
        FROM Qualifying Q
        JOIN Drivers D ON Q.driverId = D.driverId
        WHERE Q.position = 1
        GROUP BY Q.driverId
        ORDER BY pole_count DESC
        LIMIT 10;
    """
    cursor.execute(query)
    return jsonify(cursor.fetchall())


@app.route("/api/points-over-season/<int:driver_id>/<int:year>")
def points_over_season(driver_id, year):
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)

    query = """
        SELECT R.round, DS.points
        FROM DriverStandings DS
        JOIN Races R ON DS.raceId = R.raceId
        WHERE DS.driverId = %s AND R.year = %s
        ORDER BY R.round
    """
    cursor.execute(query, (driver_id, year))
    return jsonify(cursor.fetchall())


if __name__ == "__main__":
    app.run(debug=True, port=5099)

# if __name__ == "__main__":
#     import os
#     port = int(os.environ.get("PORT", 5000))
#     app.run(debug=True, host="0.0.0.0", port=port)
# minor update for redeploy