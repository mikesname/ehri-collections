
import sys

ADMINS = (
        ("Mike", "michael.bryant@kcl.ac.uk"),
)

EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

YAHOO_APP_ID = "33_udMTV34GnWuHaUYyuZXH.wkBvwNDroY74jndgzW0lNtePUNMb7GBk91hYdxAc"

if "test" in sys.argv:
    DATABASES = {
        "default": {
            "ENGINE": "django.db.backends.sqlite3",
            "NAME": "test.sqlite",                       # Or path to database file if using sqlite3.
        }
    }
