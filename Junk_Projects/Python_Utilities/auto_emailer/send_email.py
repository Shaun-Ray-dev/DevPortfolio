import smtplib
from email.message import EmailMessage
import os

smtp_server = "smtp.gmail.com"
smtp_port = 587
sender_email = "youremail@gmail.com"
password = os.getenv("EMAIL_PASS")
recipient_email = "recipient@example.com"

msg = EmailMessage()
msg['From'] = sender_email
msg['To'] = recipient_email
msg['Subject'] = "Test Email"
msg.set_content("This is a test email from Python.")

file_path = "test.txt"
if os.path.exists(file_path):
    with open(file_path, 'rb') as f:
        msg.add_attachment(f.read(), maintype='application', subtype='octet-stream', filename=f.name)
else:
    print("No attachment found, sending email without it.")

try:
    with smtplib.SMTP(smtp_server, smtp_port) as server:
        server.starttls()
        server.login(sender_email, password)
        server.send_message(msg)
    print("Email sent successfully!")
except Exception as e:
    print(f"Failed to send email: {e}")
