# Final task
# Create a tool which will calculate straight-line distance between different cities based on coordinates:
#  1. User will provide two city names by console interface
#  2. If tool do not know about city coordinates, it will ask user for input and store it in SQLite DB for future use
#  3. Return distance between cities in kilometers
# Do not forgot that Earth is a sphere, so length of one degree is different.


import pyodbc
import math
import os
import re

DRIVER = "SQLite3 ODBC Driver"


class CityDB:
    """
    Handles all DB operations:
    - Create cities.db and table for storing city coordinates
    - Connect to DB
    - Insert new city coordinates
    - Get city coordinates
    """
    def __init__(self, db_path=None, driver=DRIVER):
        # Default to current directory if no path provided
        self.db_path = db_path or os.path.join(os.getcwd(), "cities.db")
        self.driver = driver

        # Open connection and create cursor
        self.conn = pyodbc.connect(f"DRIVER={self.driver};Database={self.db_path};")
        self.cursor = self.conn.cursor()

        # Create DB table if it doesn't exist
        self._create_table()

    def _create_table(self):
        # Create DB table if it doesn't exist
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS cities (
                city_name TEXT PRIMARY KEY,
                latitude REAL NOT NULL,
                longitude REAL NOT NULL
            )
        """)
        self.conn.commit()

    def insert_coordinates(self, city_name, lat, lon):
        # Insert city coordinates
        self.cursor.execute(
            "INSERT INTO cities (city_name, latitude, longitude) VALUES (?, ?, ?)",
            (city_name, lat, lon)
        )
        self.conn.commit()

    def get_coordinates(self, city_name):
        # Fetch coordinates form DB for a given city name
        self.cursor.execute(
            "SELECT latitude, longitude FROM cities WHERE city_name = ?",
            (city_name,)
        )
        row = self.cursor.fetchone()
        return row if row else None

    def close(self):
        # Close connection
        self.conn.close()


class DistanceCalculator:
    """Calculates distance using the Haversine formula
    (the standard way to calculate the shortest distance between two points on the Earth’s surface)
    Haversine Formula (Great-Circle Distance):
    Given two points on Earth specified by latitude/longitude:
    φ1, λ1 = latitude and longitude of point 1 (in radians)
    φ2, λ2 = latitude and longitude of point 2 (in radians)
    Steps:
    Δφ = φ2 - φ1          # difference in latitude
    Δλ = λ2 - λ1          # difference in longitude
    a = sin²(Δφ/2) + cos(φ1) * cos(φ2) * sin²(Δλ/2)
    c = 2 * atan2( √a, √(1−a) )
    d = R * c
    Where:
    R = Earth’s radius (mean ≈ 6371 km)
    d = distance between the two points along the sphere’s surface
    Notes:
        - Input lat/lon must be converted from degrees to radians.
        - Output d is in kilometers if R is set to 6371.
    """
    @staticmethod
    def haversine(lat1, lon1, lat2, lon2):
        R = 6371.0  # Earth radius in km

        # Convert degrees to radians
        phi1, phi2 = math.radians(lat1), math.radians(lat2)
        dphi = math.radians(lat2 - lat1)  # difference in latitude
        dlambda = math.radians(lon2 - lon1)  # difference in longitude

        # Apply Haversine formula
        a = math.sin(dphi / 2) ** 2 + math.cos(phi1) * math.cos(phi2) * math.sin(dlambda / 2) ** 2
        c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))

        return R * c  # Distance in kilometers


class UserInterface:
    """Handles user input and output"""
    def get_city_name(self, city_prompt):
        # Ask user for a city name
        return input(city_prompt).strip().title()

    def get_or_fetch_coordinates(self, city_name, db):
        # Try to get coordinates from DB
        city_coordinates = db.get_coordinates(city_name)
        # If found, return coordinates
        if city_coordinates:
            return city_coordinates
        # If not found, ask user for coordinates and save them to DB
        else:
            print(f"Coordinates for '{city_name}' not found.")
            lat_str = input(f"Enter latitude for {city_name}: ")
            lon_str = input(f"Enter longitude for {city_name}: ")

            # Parse and normalize coordinates input
            lat = InputCoordinateValidator.normalize(InputCoordinateValidator.parse_coordinate(lat_str))
            lon = InputCoordinateValidator.normalize(InputCoordinateValidator.parse_coordinate(lon_str))

            # Validate coordinates input
            InputCoordinateValidator.validate(lat, lon)

            # Insert normalized coordinates to DB
            db.insert_coordinates(city_name, lat, lon)
            return lat, lon

    def show_distance(self, city1, city2, distance):
        # Display the calculated distance
        print(f"Straight-line distance between {city1} and {city2}: {distance:.2f} km")


class InputCoordinateValidator:
    """
    Handles geographic coordinate input:
    - Normalize coordinates: rounds decimal degree values to a fixed precision
      (default: 6 decimal places, ~11 cm accuracy).
    - Validate coordinates: ensures latitude is within -90 - +90 and longitude within -180 - +180 degrees.
    - Convert DMS (Degrees, Minutes, Seconds) format to decimal degrees
    - Parse user input: detects whether a coordinate is provided in decimal degrees or DMS format,
      and converts it to a normalized decimal degree value.
    """
    @staticmethod
    def normalize(value, decimals=6):
        # Use 6 decimal places (0.11 m) for precision, more looks redundant
        return round(float(value), decimals)

    @staticmethod
    def validate(lat, lon):
        # Basic coordinates validation for user input
        if not (-90 <= lat <= 90):
            raise ValueError("Latitude must be between -90 and 90.")
        if not (-180 <= lon <= 180):
            raise ValueError("Longitude must be between -180 and 180.")
        return True

    @staticmethod
    def dms_to_decimal(degrees, minutes, seconds, direction):
        # Convert coordinates in DMS format (degrees, minutes, seconds) to decimal degrees
        decimal = degrees + minutes/60 + seconds/3600
        if direction in ['S', 'W']:
            decimal *= -1
        return decimal

    @staticmethod
    def parse_coordinate(coord_str):
        """Detects coordinates format, converts it to a normalized decimal degree value"""

        coord_str = coord_str.strip()

        # Case 1: Decimal degrees (e.g.53.900556)
        try:
            return float(coord_str)
        except ValueError:
            pass

        # Case 2: DMS format (e.g. 53°54′02″N)
        dms_pattern = r"(\d+)[°\s]+(\d+)[′'\s]+(\d+)[″\"\s]*([NSEW])"
        match = re.match(dms_pattern, coord_str, re.IGNORECASE)
        if match:
            deg, min_, sec, direction = match.groups()
            return InputCoordinateValidator.dms_to_decimal(int(deg), int(min_), int(sec), direction.upper())

        raise ValueError("Invalid coordinate format. Use decimal degrees or DMS (e.g. 53°54′02″N).")


def main():
    # Create database object
    db = CityDB()
    # Create calculator object
    calculator = DistanceCalculator()
    # Create user interface object
    ui = UserInterface()

    # Ask user for two city names
    city1 = ui.get_city_name("Enter first city name: ")
    city2 = ui.get_city_name("Enter second city name: ")

    # Get coordinates for cities (from DB or user)
    lat1, lon1 = ui.get_or_fetch_coordinates(city1, db)
    lat2, lon2 = ui.get_or_fetch_coordinates(city2, db)

    # Calculate distance using Haversine formula
    distance = calculator.haversine(lat1, lon1, lat2, lon2)

    # Show result to user
    ui.show_distance(city1, city2, distance)

    # Close DB connection
    db.close()


# Run main program if script is executed directly
if __name__ == "__main__":
    main()

