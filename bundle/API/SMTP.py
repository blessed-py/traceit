from smtplib import SMTP
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import os


class MAIL_SERVER:

    def __init__(self):
        self.smtp_server = "smtp.gmail.com"
        self.smtp_port = 587
        self.sender = os.environ.get("SYS_MAIL")
        self.password = os.environ.get("SYS_MAIL_PWD")

    def _connect(self):
        server = SMTP(self.smtp_server, self.smtp_port)
        server.starttls()
        server.login(self.sender, self.password)
        return server

    def send_text(self, receiver_email, subject, message):
        try:
            msg = MIMEText(message, "plain")
            msg["From"] = self.sender
            msg["To"] = receiver_email
            msg["Subject"] = subject

            server = self._connect()
            server.sendmail(self.sender, receiver_email, msg.as_string())
            server.quit()

            return True

        except Exception as e:
            print("[MAIL ERROR]:", e)
            return False

    def send_html_email(self, receiver_email, subject, html_message, text_fallback=None):
        try:
            msg = MIMEMultipart("alternative")
            msg["From"] = self.sender
            msg["To"] = receiver_email
            msg["Subject"] = subject

            # Plain text fallback (important)
            if text_fallback:
                msg.attach(MIMEText(text_fallback, "plain"))

            msg.attach(MIMEText(html_message, "html"))

            server = self._connect()
            server.sendmail(self.sender, receiver_email, msg.as_string())
            server.quit()

            return True

        except Exception as e:
            print("[MAIL ERROR]:", e)
            return False

    def contact_thank_you_template(name):
        return f"""
        <div style="font-family: Arial, sans-serif;">
            <h3>Hello {name},</h3>

            <p>Thank you for contacting us. We’ve received your message and our team will respond shortly.</p>

            <p>If this is urgent, feel free to reply to this email.</p>

            <br>
            <p>
                Best regards,<br>
                <strong>TraceIt Team</strong>
            </p>
        </div>
        """        