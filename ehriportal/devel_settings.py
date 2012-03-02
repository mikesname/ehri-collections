
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

YAHOO_APP_ID = "33_udMTV34GnWuHaUYyuZXH.wkBvwNDroY74jndgzW0lNtePUNMb7GBk91hYdxAc"
