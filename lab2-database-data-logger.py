import sqlite3
import time
from datetime import datetime
from sense_hat import SenseHat

# Initialize SenseHAT
sense = SenseHat()

# Database name
DATABASE_NAME = "sensorDB.db"

def create_database():
    """Create SQLite database and sensordata table."""
    conn = sqlite3.connect(DATABASE_NAME)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS sensordata (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            datetime TEXT NOT NULL,
            temperature REAL NOT NULL,
            humidity REAL NOT NULL,
            pressure REAL NOT NULL
        )
    ''')
    conn.commit()
    conn.close()

def insert_sensor_data(temperature, humidity, pressure):
    """Insert a row of sensor data into the sensordata table."""
    conn = sqlite3.connect(DATABASE_NAME)
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO sensordata (datetime, temperature, humidity, pressure) VALUES (?, ?, ?, ?)",
        (datetime.now().strftime('%Y-%m-%d %H:%M:%S'), temperature, humidity, pressure)
    )
    conn.commit()
    conn.close()

def main():
    """Main function to log data to the database."""
    create_database()
    print("Database initialized. Logging sensor data... Press Ctrl+C to stop.")

    try:
        for _ in range(20):
            # Read data from SenseHAT sensors
            temperature = sense.get_temperature()
            humidity = sense.get_humidity()
            pressure = sense.get_pressure()

            # Insert data into the database
            insert_sensor_data(temperature, humidity, pressure)

            # Print logged data for verification
            print(f"Logged: Temp={temperature:.2f}C, Humidity={humidity:.2f}%, Pressure={pressure:.2f}hPa")

            # Wait for 1 second
            time.sleep(1)
    except KeyboardInterrupt:
        print("\nData logging stopped.")

if __name__ == "__main__":
    main()
