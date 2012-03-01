
import sys

ADMINS = (
        ("Mike", "michael.bryant@kcl.ac.uk"),
)

EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

if "test" in sys.argv:
    DATABASES = {
        "default": {
            "ENGINE": "django.db.backends.sqlite3",
            "NAME": "test.db",                   
        }
    }


