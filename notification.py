import smtplib
from email.message import EmailMessage
import pandas as pd
from datetime import datetime

# Project3 Email Configuration - NetEase 163 SMTP (SSL Encryption)
FROM_EMAIL = "13615115272@163.com"
AUTH_CODE = "AZbqXyDJzbRxXH5a"
TO_EMAIL = "1707977630@qq.com"
SMTP_SERVER = "smtp.163.com"
SMTP_PORT = 465

def send_project3_alert():
    # Load latest preprocessed sensor data
    try:
        df = pd.read_csv("preprocessed_data.csv")
        latest = df.iloc[-1]
        ts = latest["Timestamp"]
        moisture = latest["Soil_Moisture_Denoised"]
        temp = latest["Temperature_Denoised"]
        air_hum = latest["Air_Humidity_Denoised"]
        sensor_info = f"Latest Sensor Data (Time: {ts})\n- Soil Moisture: {moisture:.2f}\n- Temperature: {temp:.2f}°C\n- Air Humidity: {air_hum:.2f}%\n"
    except Exception as e:
        sensor_info = f"Sensor Data Load Error: {str(e)}\n"

    # Load model performance metrics
    try:
        with open("model_performance.txt", "r") as f:
            model_metrics = f.read()
    except Exception as e:
        model_metrics = f"Model Metrics Load Error: {str(e)}\n"

    # Compose Project3 Email
    subject = f"Project3 - Soil Moisture Prediction Report | {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
    body = f"""============================================================
Project3: Raspberry Pi Soil Moisture Trend Modeling & Prediction System
============================================================

{sensor_info}

{model_metrics}

This is an automatic notification from Project3 Intelligent Monitoring System.
All data is collected and processed for academic project use only.
============================================================
"""
    # Send Email via SMTP SSL
    msg = EmailMessage()
    msg['From'] = FROM_EMAIL
    msg['To'] = TO_EMAIL
    msg['Subject'] = subject
    msg.set_content(body)

    try:
        with smtplib.SMTP_SSL(SMTP_SERVER, SMTP_PORT) as server:
            server.login(FROM_EMAIL, AUTH_CODE)
            server.send_message(msg)
        print(f"Project3: Alert Email sent successfully to {TO_EMAIL}")
    except Exception as e:
        print(f"Project3: Email Sending Failed - {str(e)}")

if __name__ == "__main__":
    send_project3_alert()
