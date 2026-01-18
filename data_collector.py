import RPi.GPIO as GPIO
import adafruit_dht
import time
import pandas as pd
from datetime import datetime

# Project3 Hardware Configuration (BCM Mode)
GPIO.setmode(GPIO.BCM)
SOIL_SENSOR_A0 = 2  # FC-28 A0 pin → GPIO2
DHT11_DATA_PIN = 4  # DHT11 DATA pin → GPIO4
dht_device = adafruit_dht.DHT11(DHT11_DATA_PIN)

# Data Collection Settings
data = []
collection_duration = 48  # Collect data for 48 hours
interval = 30  # Collect data every 30 minutes
total_readings = (collection_duration * 60) // interval

# Read soil moisture (analog value via voltage division)
def read_soil_moisture():
    # Use Raspberry Pi as analog-to-digital converter (simplified)
    GPIO.setup(SOIL_SENSOR_A0, GPIO.IN)
    time.sleep(0.1)
    # Convert digital signal to analog-like value (0-1023)
    moisture_value = sum([GPIO.input(SOIL_SENSOR_A0) for _ in range(10)]) * 102.3
    return round(moisture_value, 2)

# Read temperature and air humidity from DHT11
def read_temperature_humidity():
    try:
        temperature = dht_device.temperature
        humidity = dht_device.humidity
        return round(temperature, 2) if temperature else None, round(humidity, 2) if humidity else None
    except RuntimeError as e:
        print(f"DHT11 Error: {e}")
        return None, None

# Core Data Collection Loop
print(f"Project3: Starting data collection for {collection_duration} hours (interval: {interval} mins)")
for i in range(total_readings):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    soil_moisture = read_soil_moisture()
    temp, air_humidity = read_temperature_humidity()
    
    if temp and air_humidity:
        data.append([timestamp, soil_moisture, temp, air_humidity])
        print(f"Reading {i+1}/{total_readings}: {timestamp} - Soil Moisture: {soil_moisture}, Temp: {temp}°C, Air Humidity: {air_humidity}%")
    
    time.sleep(interval * 60)

# Save Data to CSV
df = pd.DataFrame(data, columns=["Timestamp", "Soil_Moisture", "Temperature", "Air_Humidity"])
df.to_csv("sensor_data.csv", index=False)
print("Project3: Data collection complete. Saved to sensor_data.csv")

# Clean Up Resources
GPIO.cleanup()
dht_device.exit()
