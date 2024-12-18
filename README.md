Add the following external libraries
* ftc
* ftrobopy-master
* QtCore
* QtGui
* QtWidgets

Putty:
ssh: 192.168.178.84
user: ftc
"OK" on TXT
export PYTHONPATH=/opt/ftc
cd /opt/ftc/apps/user/191fe5a6-313b-4083-af65-d1ad7fd6d281/
python3 start.py

Update File:
Windows CMD:
scp start.py ftc@192.168.178.84:/opt/ftc/apps/user/191fe5a6-313b-4083-af65-d1ad7fd6d281/
(FT: Confirm!)
