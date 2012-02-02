#!/bin/sh

OUT=$HOME/Dropbox/EHRI/portal_test_db.sql.gz
PASS=changeme
USER=portaltest
DB=portaltest

echo "Dumping to $OUT"
mysqldump -u$USER -p$PASS $DB|gzip > $OUT
