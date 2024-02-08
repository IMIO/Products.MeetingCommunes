#!/bin/sh
/srv/archgenxml/bin/archgenxml --cfg generate.conf MeetingCommunes.zargo -o tmp

# only keep workflows
cp -rf tmp/profiles/default/workflows/* ../profiles/financesadvice/workflows
rm -rf tmp
