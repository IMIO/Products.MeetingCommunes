#!/bin/sh
/srv/archgenxml/bin/archgenxml --cfg generate.conf MeetingCommunes.zargo -o tmp

# only keep workflows
cp -rf tmp/profiles/default/workflows/meetingcommunes_workflow ../profiles/default/workflows
cp -rf tmp/profiles/default/workflows/meetingitemcommunes_workflow ../profiles/default/workflows
cp -rf tmp/profiles/default/workflows/meetingadvicefinances_workflow ../profiles/financesadvice/workflows
cp -rf tmp/profiles/default/workflows/meetingadvicefinanceseditor_workflow ../profiles/financesadvice/workflows
cp -rf tmp/profiles/default/workflows/meetingadvicefinancesmanager_workflow ../profiles/financesadvice/workflows
rm -rf tmp
