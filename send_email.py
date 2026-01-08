import smtplib
from email.message import EmailMessage


FROM_EMAIL = "13615115272@163.com"  
AUTH_CODE = "AZbqXyDJzbRxXH5a"  
TO_EMAIL = "1707977630@qq.com" 


msg = EmailMessage()
msg['From'] = FROM_EMAIL
msg['To'] = TO_EMAIL
msg['Subject'] = "Plant Moisture Test Email"
msg.set_content("This is a test email from Raspberry Pi (NetEase Email).")

try:
 
    server = smtplib.SMTP('smtp.163.com', 25)
    server.starttls() 
    server.login(FROM_EMAIL, AUTH_CODE)
    server.send_message(msg)
    server.quit()
    print("Email sent successfully! Check your inbox.")
except Exception as e:
    print(f"Failed to send email: {e}")
