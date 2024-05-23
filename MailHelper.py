import smtplib
# from smtplib import SMTP_SSL as SMTP
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from dotenv import load_dotenv
import os


class MailConnector():
    def __init__(self):

        load_dotenv()
        
        self.smtp_server = os.getenv('SMPT_HOST')
        self.smtp_port = os.getenv('SMPT_PORT')
        self.login = os.getenv('SMPT_MAIL')
        self.password = os.getenv('SMPT_PASSWORD')
        self.adminMail = os.getenv('SMPT_ADMIN')

    def send_email(self, subject, body):
        # Create a multipart message
        msg = MIMEMultipart()
        msg['From'] = self.login
        msg['To'] = self.adminMail
        msg['Subject'] = "Wandering Wisdom Reach Outs - " + subject

        # Attach the body with the msg instance
        msg.attach(MIMEText(body, 'plain'))

        try:
            # Setup the SMTP server
            print('Before obj')
            server = smtplib.SMTP(self.smtp_server, self.smtp_port)
            server.set_debuglevel(False)
            print('Before connect')
            server.connect(self.smtp_server, self.smtp_port)
            # server.starttls()  # Enable security
            
            # Log in to the server
            print('Before login')
            server.login(self.login, self.password)
            
            # Send the email
            print('Before send')
            server.sendmail(self.login, self.adminMail, msg.as_string())
            
            # Disconnect from the server
            print('Before quit')
            server.quit()

            print("Email sent successfully!")
            return True
        except Exception as e:
            print(f"Failed to send email. Error: {str(e)}")
            return False

    def send_confirmation(self, username, mailID):

        body = f"""Hi {username},

        Thanks for reaching out to us. We have recieved your inputs will get back to at the earliest possible.

        Thanks & Regards,
        Wnadering Wisdom.
        """

        # Create a multipart message
        msg = MIMEMultipart()
        msg['From'] = self.login
        msg['To'] = mailID
        msg['Subject'] = "Wandering Wisdom - Mail Confirmation"

        # Attach the body with the msg instance
        msg.attach(MIMEText(body, 'plain'))

        try:
            # Setup the SMTP server
            server = smtplib.SMTP(self.smtp_server, self.smtp_port)
            server.connect(self.smtp_server, self.smtp_port)
            server.starttls()  # Enable security
            
            # Log in to the server
            server.login(self.login, self.password)
            
            # Send the email
            server.sendmail(self.login, mailID, msg.as_string())
            
            # Disconnect from the server
            server.quit()

            print("Confirmation sent successfully!")
            return True
        except Exception as e:
            print(f"Failed to send cpnfirmation. Error: {str(e)}")
            return False