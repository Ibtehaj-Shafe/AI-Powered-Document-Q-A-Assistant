import random
from datetime import datetime, timedelta, timezone
from sqlalchemy.orm import Session
from Backend.models import OTPReset
from Backend.dependencies.password import hash_password, verify_password
from Backend.services.email_service import send_otp_email


def create_otp(db: Session, email: str):
    return generate_and_store_otp(db, email)


def generate_and_store_otp(db: Session, email: str) -> dict:
    """
    Generate OTP, hash it, store in DB, and send via email.
    """

    # 1. Generate 6-digit numeric OTP
    otp = str(random.randint(100000, 999999))

    # 2. Hash OTP before storing
    otp_hash = hash_password(otp)

    # 3. Set expiry (5 minutes)
    expires_at = datetime.now(timezone.utc) + timedelta(minutes=5)

    # 4. Invalidate previous OTPs for same email
    db.query(OTPReset).filter(
        OTPReset.email == email,
        OTPReset.used == False
    ).update({"used": True})

    # 5. Store new OTP
    otp_entry = OTPReset(
        email=email,
        otp_hash=otp_hash,
        expires_at=expires_at,
        used=False
    )

    db.add(otp_entry)
    db.commit()

    # 6. Send OTP via email
    send_otp_email(email, otp)

    return {"message": "If the email exists, an OTP has been sent"}


def verify_otp(db: Session, email: str, otp: str):
    """
    Verify OTP validity.
    Raises ValueError if invalid.
    """

    otp_entry = db.query(OTPReset).filter(
        OTPReset.email == email,
        OTPReset.used == False
    ).order_by(OTPReset.expires_at.desc()).first()

    if not otp_entry:
        raise ValueError("Invalid or expired OTP")

    # Check expiry by column name
    if otp_entry.expires_at < datetime.now(timezone.utc):
        raise ValueError("OTP has expired")

    # Verify OTP hash
    if not verify_password(otp, otp_entry.otp_hash):
        raise ValueError("Invalid OTP")

    # Mark OTP as used
    otp_entry.used = True
    db.commit()
