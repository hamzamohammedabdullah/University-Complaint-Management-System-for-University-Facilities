"""Notification delivery helpers.

This module provides two simple helpers used by the app to deliver
notifications via email and SMS. Email delivery uses Django's
email backend (so configure EMAIL_BACKEND / DEFAULT_FROM_EMAIL in
settings). SMS delivery supports Twilio when the Twilio settings
are present; otherwise it logs the message so you can integrate a
real gateway later.

Usage: import send_email_notification, send_sms_notification

Note: This module avoids making network calls unless the relevant
settings are configured. It logs failures and returns boolean
success flags.
"""
import logging
from django.conf import settings

logger = logging.getLogger(__name__)


def send_email_notification(recipient_email: str, subject: str, message: str) -> bool:
    """Send an email using Django's configured email backend.

    Returns True on success, False on failure or when recipient_email
    is falsy.
    """
    if not recipient_email:
        return False
    try:
        from django.core.mail import send_mail

        from_email = getattr(settings, 'DEFAULT_FROM_EMAIL', 'no-reply@localhost')
        send_mail(subject, message, from_email, [recipient_email], fail_silently=False)
        logger.info("Notification email sent to %s", recipient_email)
        return True
    except Exception:
        logger.exception("Failed to send notification email to %s", recipient_email)
        return False


def send_sms_notification(phone: str, message: str) -> bool:
    """Send an SMS using Twilio if configured; otherwise log the SMS.

    Returns True if a send was attempted (or succeeded in the case of
    Twilio), False if phone is falsy.
    """
    if not phone:
        return False
    try:
        # If Twilio settings are present, attempt a real send
        account_sid = getattr(settings, 'TWILIO_ACCOUNT_SID', None)
        auth_token = getattr(settings, 'TWILIO_AUTH_TOKEN', None)
        from_number = getattr(settings, 'TWILIO_FROM_NUMBER', None)
        if account_sid and auth_token and from_number:
            try:
                from twilio.rest import Client
            except Exception:
                logger.exception("Twilio client not available; please install twilio package")
                return False
            client = Client(account_sid, auth_token)
            client.messages.create(body=message, from_=from_number, to=phone)
            logger.info("SMS sent to %s via Twilio", phone)
            return True

        # Fallback: log the message so developers can inspect it
        logger.info("SMS (mock) to %s: %s", phone, message)
        return True
    except Exception:
        logger.exception("Failed to send SMS to %s", phone)
        return False
