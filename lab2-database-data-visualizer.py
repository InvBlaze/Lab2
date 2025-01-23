import sqlite3
import pandas as pd
import matplotlib.pyplot as plt

# Database name
DATABASE_NAME = "sensorDB.db"

def connect_database():

    return sqlite3.connect(DATABASE_NAME)

def load_sensor_data():

    conn = connect_database()
    query = "SELECT * FROM sensordata"
    df = pd.read_sql_query(query, conn)
    conn.close()
    return df

def plot_sensor_data(df):

    plt.figure(figsize=(10, 6))
    plt.plot(df['datetime'], df['temperature'], label='Temperature (°C)', color='red')
    plt.plot(df['datetime'], df['humidity'], label='Humidity (%)', color='blue')
    plt.plot(df['datetime'], df['pressure'], label='Pressure (hPa)', color='green')
    
    plt.xlabel('Date and Time')
    plt.ylabel('Sensor Readings')
    plt.title('Sensor Data Over Time')
    plt.legend()
    plt.grid(True)
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.show()

def main():

    df = load_sensor_data()
    if not df.empty:
        plot_sensor_data(df)
    else:
        print("No data available to plot.")

if __name__ == "__main__":
    main()
