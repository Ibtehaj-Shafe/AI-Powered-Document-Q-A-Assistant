import smtplib
from email.message import EmailMessage
import os

SMTP_EMAIL = os.getenv("SMTP_EMAIL")
SMTP_PASSWORD = os.getenv("SMTP_PASSWORD")
SMTP_HOST = os.getenv("SMTP_HOST", "smtp.gmail.com")
SMTP_PORT = int(os.getenv("SMTP_PORT", 587))


def send_otp_email(to_email: str, otp: str) -> None:
    """
    Send OTP email from official email to user email.
    """

    msg = EmailMessage()
    msg["Subject"] = "Password Reset OTP"
    msg["From"] = SMTP_EMAIL
    msg["To"] = to_email

    msg.set_content(
        f"""
Hello,

Your One-Time Password (OTP) for password reset is:

{otp}

This OTP is valid for 5 minutes.
If you did not request this, please ignore this email.

Thanks,
Support Team
"""
    )

    try:
        with smtplib.SMTP(SMTP_HOST, SMTP_PORT) as server:
            server.starttls()               # Secure connection
            server.login(SMTP_EMAIL, SMTP_PASSWORD)
            server.send_message(msg)
    except Exception as e:
        # Do NOT expose SMTP error details to user
        raise RuntimeError("Failed to send OTP email")
