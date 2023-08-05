from .base_settings import *

# ======================
# django-smsish settings
# ======================

# Add `smsish` to your INSTALLED_APPS
INSTALLED_APPS += (
    'smsish',
)

# Set `SMS_BACKEND` in your settings.
SMS_BACKEND_CONSOLE = 'smsish.sms.backends.console.SMSBackend'
SMS_BACKEND_DUMMY = 'smsish.sms.backends.dummy.SMSBackend'
SMS_BACKEND_RQ = 'smsish.sms.backends.rq.SMSBackend'
SMS_BACKEND_TWILIO = 'smsish.sms.backends.twilio.SMSBackend'
SMS_BACKEND = SMS_BACKEND_DUMMY

# Set Twilio settings if needed.
# Note: `pip install twilio` to use the Twilio backend.
TWILIO_ACCOUNT_SID = os.getenv("TWILIO_ACCOUNT_SID", None)
TWILIO_AUTH_TOKEN = os.getenv("TWILIO_AUTH_TOKEN", None)
TWILIO_MAGIC_FROM_NUMBER = "+15005550006"  # This number passes all validation.
TWILIO_FROM_NUMBER = os.getenv("TWILIO_FROM_NUMBER", TWILIO_MAGIC_FROM_NUMBER)

RQ_QUEUES = {
    'default': {
        'URL': os.getenv("REDIS_URL", None),
    },
}
