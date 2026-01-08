import RPi.GPIO as GPIO
import smtplib
from email.message import EmailMessage
import time
from datetime import datetime

# ---------------------- Configuration (replace with yours!) ----------------------
FROM_EMAIL = "13615115272@163.com"  # Your NetEase email
AUTH_CODE = "AZbqXyDJzbRxXH5a"      # Your NetEase authorization code (not login password)
TO_EMAIL = "1707977630@qq.com"      # Recipient email
GPIO_CHANNEL = 4                    # Corresponding to your GPIO4 wiring

# ---------------------- Initialize GPIO ----------------------
GPIO.setmode(GPIO.BCM)
GPIO.setup(GPIO_CHANNEL, GPIO.IN)

# ---------------------- Send moisture email function ----------------------
def send_moisture_email(status):
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    msg = EmailMessage()
    msg['From'] = FROM_EMAIL
    msg['To'] = TO_EMAIL
    msg['Subject'] = f"Plant Moisture Alert - {current_time}"
    msg.set_content(f"""
Plant Moisture Detection Result:
Time: {current_time}
Status: {status}

Please take care of your plant in time!
    """)
    try:
        # Connect to NetEase SMTP server (465 port + SSL encryption)
        server = smtplib.SMTP_SSL('smtp.163.com', 465)
        server.login(FROM_EMAIL, AUTH_CODE)
        server.send_message(msg)
        server.quit()
        print(f"Alert email sent successfully: {status}")
    except Exception as e:
        print(f"Failed to send alert email: {e}")

# ---------------------- Main Program ----------------------
def main():
    print("Plant moisture monitoring system started...")
    # Record last email sending time (avoid frequent emails)
    last_send_time = 0
    while True:
        # Detect moisture
        if GPIO.input(GPIO_CHANNEL):
            status = "Soil is dry! Please water the plant immediately."
            # Send email only once every 30 minutes (1800 seconds)
            if time.time() - last_send_time > 1800:
                send_moisture_email(status)
                last_send_time = time.time()
        else:
            status = "Soil is moist, plant is in good condition."
        
        print(f"[{datetime.now().strftime('%H:%M:%S')}] {status}")
        time.sleep(60)  # Detect every 60 seconds

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        GPIO.cleanup()
        print("\nSystem stopped, GPIO cleaned up")
