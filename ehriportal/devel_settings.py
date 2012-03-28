
import sys

ADMINS = (
        ("Mike", "michael.bryant@kcl.ac.uk"),
)

EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

YAHOO_APP_ID = "33_udMTV34GnWuHaUYyuZXH.wkBvwNDroY74jndgzW0lNtePUNMb7GBk91hYdxAc"

if "test" in sys.argv:
    DATABASES = {
        "default": {
            "ENGINE": "django.contrib.gis.db.backends.spatialite",
            "NAME": "test.sqlite",                       # Or path to database file if using sqlite3.
        }
    }
    SPATIALITE_SQL = "conf/init_spatialite-2.3.sql"
