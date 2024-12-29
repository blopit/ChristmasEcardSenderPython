import smtplib
import os
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.image import MIMEImage
from datetime import datetime
from config import SMTP_EMAIL, SMTP_PASSWORD, SMTP_SERVER, SMTP_PORT

class ChristmasCardSender:
    def __init__(self, sender_email, sender_password):
        self.sender_email = sender_email
        self.sender_password = sender_password
        self.smtp_server = SMTP_SERVER
        self.smtp_port = SMTP_PORT

    def create_html_message(self, recipient_name):
        current_year = datetime.now().year
        
        html = f"""
        <html>
            <body style="background-color: #f8f8f8; font-family: Arial, sans-serif;">
                <div style="max-width: 600px; margin: 0 auto; padding: 20px; background-color: white; border-radius: 10px; box-shadow: 0 0 10px rgba(0,0,0,0.1);">
                    <h1 style="color: #c41e3a; text-align: center;">Merry Christmas & Happy New Year!</h1>
                    <div style="text-align: center;">
                        <img src="cid:lion_motel_image" style="max-width: 100%; height: auto; border-radius: 8px; margin: 20px 0;">
                    </div>
                    <p style="color: #333; font-size: 16px; line-height: 1.6;">
                        Dear {recipient_name},
                    </p>
                    <p style="color: #333; font-size: 16px; line-height: 1.6;">
                        Wishing you a wonderful Christmas filled with joy, love, and happiness!
                        May this festive season bring you and your loved ones countless blessings.
                    </p>
                    <p style="color: #333; font-size: 16px; line-height: 1.6; text-align: right;">
                        Best wishes,<br>
                        Jina & JP @ <span style="color: #666;">The Lion Motel</span>
                    </p>
                    <div style="text-align: center; margin-top: 20px; color: #888;">
                        <small>Christmas {current_year}</small>
                    </div>
                </div>
            </body>
        </html>
        """
        return html

    def send_card(self, recipient_email, recipient_name):
        try:
            # Create message container
            msg = MIMEMultipart('related')
            msg['Subject'] = "Merry Christmas from Lion Motel! 🎄"
            msg['From'] = self.sender_email
            msg['To'] = recipient_email

            # Create the HTML content
            html_content = self.create_html_message(recipient_name)
            html_part = MIMEText(html_content, 'html')
            msg.attach(html_part)

            # Attach the image
            with open('lionmotel.jpeg', 'rb') as img_file:
                img = MIMEImage(img_file.read())
                img.add_header('Content-ID', '<lion_motel_image>')
                img.add_header('Content-Disposition', 'inline')
                msg.attach(img)

            # Create SMTP session
            with smtplib.SMTP(self.smtp_server, self.smtp_port) as server:
                server.starttls()
                server.login(self.sender_email, self.sender_password)
                server.send_message(msg)

            print(f"Successfully sent Christmas card to {recipient_name} ({recipient_email})")
            return True

        except Exception as e:
            print(f"Failed to send email to {recipient_email}. Error: {str(e)}")
            return False

def main():
    # Load credentials from config
    sender_email = SMTP_EMAIL
    sender_password = SMTP_PASSWORD

    # Create card sender instance
    card_sender = ChristmasCardSender(sender_email, sender_password)

    # Load recipients from CSV file
    from recipients import load_recipients
    recipients = load_recipients('recipients.csv')

    # Send cards to all recipients
    for recipient in recipients:
        card_sender.send_card(recipient["email"], recipient["name"])

if __name__ == "__main__":
    main() 