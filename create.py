from fastapi import FastAPI
from pydantic import BaseModel
import psycopg2

app = FastAPI()


def get_connection():
    return psycopg2.connect(
        host="localhost",
        database="smartbus",
        user="postgres",
        password="postgres12345",
        port="5432"
    )


class User(BaseModel):
    name: str
    email: str
    phone: str
    password: str
    role: str = "PASSENGER"

#users
@app.post("/users")
def create_user(user: User):

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute(
        """
        INSERT INTO users
        (name, email, phone, password, role)
        VALUES (%s, %s, %s, %s, %s)
        RETURNING user_id
        """,
        (
            user.name,
            user.email,
            user.phone,
            user.password,
            user.role
        )
    )

    user_id = cursor.fetchone()[0]

    if user.role == "DRIVER":

        cursor.execute(
            """
            INSERT INTO drivers (user_id)
            VALUES (%s)
            """,
            (user_id,)
        )

    connection.commit()

    cursor.close()
    connection.close()

    return {
        "message": "User added successfully!",
        "user_id": user_id
    }
@app.get("/users")
def get_users():

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute(
        "SELECT user_id, name, email, phone, role FROM users"
    )

    data = cursor.fetchall()

    cursor.close()
    connection.close()

    users = []

    for row in data:
        users.append({
            "user_id": row[0],
            "name": row[1],
            "email": row[2],
            "phone": row[3],
            "role": row[4]
        })

    return users

#drivers

@app.get("/drivers")
def get_drivers():

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute(
        """
        SELECT
            drivers.driver_id,
            users.user_id,
            users.name,
            users.role
        FROM drivers
        JOIN users
        ON drivers.user_id = users.user_id
        """
    )

    rows = cursor.fetchall()

    cursor.close()
    connection.close()

    drivers = []

    for i in rows:
        drivers.append({
            "driver_id": i[0],
            "user_id": i[1],
            "name": i[2],
            "role": i[3]
        })

    return drivers

class Bus(BaseModel):
    bus_number: str
    driver_id: int

#buses
@app.post("/buses")
def create_bus(bus: Bus):

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute(
        """
        INSERT INTO buses (bus_number, driver_id)
        VALUES (%s, %s)
        RETURNING bus_id
        """,
        (
            bus.bus_number,
            bus.driver_id
        )
    )

    bus_id = cursor.fetchone()[0]

    connection.commit()

    cursor.close()
    connection.close()

    return {
        "message": "Bus added successfully!",
        "bus_id": bus_id
    }


@app.get("/buses")
def get_buses():

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute(
        """
        SELECT bus_id, bus_number, driver_id
        FROM buses
        """
    )

    buses = cursor.fetchall()

    cursor.close()
    connection.close()

    return buses

#routes
class Route(BaseModel):
    route_name: str
    start_location: str
    destination: str


@app.post("/routes")
def create_route(route: Route):

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute(
        """
        INSERT INTO routes
        (route_name, start_location, destination)
        VALUES (%s, %s, %s)
        RETURNING route_id
        """,
        (
            route.route_name,
            route.start_location,
            route.destination
        )
    )

    route_id = cursor.fetchone()[0]

    connection.commit()

    cursor.close()
    connection.close()

    return {
        "message": "Route added successfully!",
        "route_id": route_id
    }

@app.get("/routes")
def get_routes():

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        SELECT route_id, route_name, start_location, destination
        FROM routes
    """)

    routes = cursor.fetchall()

    cursor.close()
    connection.close()

    return routes


#stops

class Stop(BaseModel):
    route_id: int
    stop_name: str
    latitude: float
    longitude: float
    stop_order: int


@app.post("/stops")
def create_stop(stop: Stop):

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute(
        """
        INSERT INTO stops
        (route_id, stop_name, latitude, longitude, stop_order)
        VALUES (%s, %s, %s, %s, %s)
        RETURNING stop_id
        """,
        (
            stop.route_id,
            stop.stop_name,
            stop.latitude,
            stop.longitude,
            stop.stop_order
        )
    )

    stop_id = cursor.fetchone()[0]

    connection.commit()

    cursor.close()
    connection.close()

    return {
        "message": "Stop added successfully!",
        "stop_id": stop_id
    }

@app.get("/stops")
def get_stops():
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute(
        """
        SELECT stop_id, route_id, stop_name, latitude, longitude, stop_order
        FROM stops
        """
    )

    rows = cursor.fetchall()

    cursor.close()
    connection.close()

    stops = []

    for row in rows:
        stops.append({
            "stop_id": row[0],
            "route_id": row[1],
            "stop_name": row[2],
            "latitude": float(row[3]) if row[3] is not None else None,
            "longitude": float(row[4]) if row[4] is not None else None,
            "stop_order": row[5]
        })

    return stops

#bus_location

class BusLocation(BaseModel):
    bus_id: int
    latitude: float
    longitude: float


@app.post("/bus-locations")
def create_bus_location(location: BusLocation):
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute(
        """
        INSERT INTO bus_locations
        (bus_id, latitude, longitude)
        VALUES (%s, %s, %s)
        RETURNING location_id
        """,
        (
            location.bus_id,
            location.latitude,
            location.longitude
        )
    )

    location_id = cursor.fetchone()[0]

    connection.commit()

    cursor.close()
    connection.close()

    return {
        "message": "Bus location added successfully!",
        "location_id": location_id
    }


@app.get("/bus-locations")
def get_bus_locations():
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute(
        """
        SELECT location_id, bus_id, latitude, longitude, timestamp
        FROM bus_locations
        """
    )

    rows = cursor.fetchall()

    cursor.close()
    connection.close()

    locations = []

    for row in rows:
        locations.append({
            "location_id": row[0],
            "bus_id": row[1],
            "latitude": float(row[2]),
            "longitude": float(row[3]),
            "timestamp": row[4]
        })

    return locations


#stops for routes

@app.get("/routes/{route_id}/stops")
def get_route_stops(route_id: int):
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute(
        """
        SELECT stop_id, route_id, stop_name, latitude, longitude, stop_order
        FROM stops
        WHERE route_id = %s
        ORDER BY stop_order
        """,
        (route_id,)
    )

    rows = cursor.fetchall()

    cursor.close()
    connection.close()

    stops = []

    for row in rows:
        stops.append({
            "stop_id": row[0],
            "route_id": row[1],
            "stop_name": row[2],
            "latitude": float(row[3]) if row[3] is not None else None,
            "longitude": float(row[4]) if row[4] is not None else None,
            "stop_order": row[5]
        })

    return stops


#driver,bus, bus_location


@app.get("/buses/{bus_id}/details")
def get_bus_details(bus_id: int):

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute(
        """
        SELECT
            buses.bus_id,
            buses.bus_number,
            drivers.driver_id,
            users.name,
            bus_locations.latitude,
            bus_locations.longitude,
            bus_locations.timestamp
        FROM buses
        JOIN drivers
            ON buses.driver_id = drivers.driver_id
        JOIN users
            ON drivers.user_id = users.user_id
        LEFT JOIN bus_locations
            ON buses.bus_id = bus_locations.bus_id
        WHERE buses.bus_id = %s
        ORDER BY bus_locations.timestamp DESC
        LIMIT 1
        """,
        (bus_id,)
    )

    row = cursor.fetchone()

    cursor.close()
    connection.close()

    if row is None:
        return {
            "message": "Bus not found"
        }

    return {
        "bus_id": row[0],
        "bus_number": row[1],
        "driver_id": row[2],
        "driver_name": row[3],
        "latitude": float(row[4]) if row[4] is not None else None,
        "longitude": float(row[5]) if row[5] is not None else None,
        "timestamp": row[6]
    }


#finding the next stop

@app.get("/routes/{route_id}/stops")
def get_route_stops(route_id: int):

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute(
        """
        SELECT
            stop_id,
            route_id,
            stop_name,
            latitude,
            longitude,
            stop_order
        FROM stops
        WHERE route_id = %s
        ORDER BY stop_order
        """,(route_id,))

    rows = cursor.fetchall()

    cursor.close()
    connection.close()

    stops = []

    for row in rows:
        stops.append({
            "stop_id": row[0],
            "route_id": row[1],
            "stop_name": row[2],
            "latitude": float(row[3]) if row[3] is not None else None,
            "longitude": float(row[4]) if row[4] is not None else None,
            "stop_order": row[5]})

    return stops

#bus to route


@app.get("/buses/{bus_id}/route")
def get_bus_route(bus_id: int):
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute(
        """
        SELECT
            buses.bus_id,
            buses.bus_number,
            routes.route_id,
            routes.route_name,
            routes.start_location,
            routes.destination
        FROM buses
        JOIN routes
            ON buses.route_id = routes.route_id
        WHERE buses.bus_id = %s
        """,
        (bus_id,)
    )

    row = cursor.fetchone()

    cursor.close()
    connection.close()

    if row is None:
        return {
            "message": "Bus or assigned route not found"
        }

    return {
        "bus_id": row[0],
        "bus_number": row[1],
        "route_id": row[2],
        "route_name": row[3],
        "start_location": row[4],
        "destination": row[5]
    }

