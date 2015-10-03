#!/bin/sh
echo 'FROM .sh script:'
echo $1 $2 $3 $4 $5
echo '<br>'

/usr/bin/python event_notification.py $1 $2 $3 $4 $5

exit 0
