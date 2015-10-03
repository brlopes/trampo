#!/usr/bin/python
#
# recursive script, auto refresh every 15s searching DB for JSON match:
#
#         JSON
#          ^
#          |
#          v
#     -> PYTHON -> EMAIL
#          ^
#          |
#          v
#          DB

import smtplib
from email.MIMEMultipart import MIMEMultipart
from email.MIMEText import MIMEText
import sys
import sqlite3
import datetime
import json
import time

import recursive_notification_check

DBNAME = 'notifications.db'
DBTABLE = "notifications"
JSONFILE = "Loco.json"


# ############################################################################
def send_notification_email(EMAILTO, LOCOMOTIVE, message):
    """ Sends email notifications for matches found on db"""

    fromaddr = "loco_watcher_son@akrr.com"
    msg = MIMEMultipart()
    msg['From'] = fromaddr
    msg['To'] = EMAILTO
    msg['Subject'] = "loco_watcher notification message from locomotive {0}".format(str(LOCOMOTIVE))

    # last name: (#struggle)
    lastname = EMAILTO.split('@')
    lastname = lastname[0]
    lastName = lastname[:-1]
    fullname = lastName[0].upper() + lastName[1:]  # booya

    # import pdb; pdb.set_trace()

    body = "Hello " + lastName + ", \n "
    body += '\n'
    body += 'This is an automated message from the PTC_LAB locomotive notification system'
    body += '\n\n'
    body += 'The Locomotive {0}'.format(str(message))
    body += ' on '
    body += datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    body += '\n'

    msg.attach(MIMEText(body, 'plain'))

    server = smtplib.SMTP()
    server.connect('smtp.akrr.com', 25)

    text = msg.as_string()
    server.sendmail(fromaddr, EMAILTO, text)
    # print "EMAIL SENT"
# ############################################################################


# ############################################################################
def recursive_check():
    """Checks db on every check_time intervals, if DB matches JSON data, then
        send_notification_email() with message found"""

    con = None
    try:
        # open JSON and use it as a dict
        with open(JSONFILE, 'r') as file:
            event = eval(file.read())

        con = sqlite3.connect(DBNAME)
        cur = con.cursor()

        for entry in event['data']:
            json_loco_id = entry[0]
            json_loco_radio = str(entry[1]).lower()
            json_loco_wifi = str(entry[2]).lower()
            json_loco_cell = str(entry[3]).lower()
            json_loco_stamp = str(entry[4]).lower()

            # Status
            if json_loco_radio != 'none':
                json_statusR = 'online'
            else:
                json_statusR = 'offline'

            if json_loco_wifi == 'true':
                json_statusW = 'online'
            else:
                json_statusW = 'offline'

            if json_loco_cell == 'true':
                json_statusC = 'online'
            else:
                json_statusC = 'offline'

            cur.execute("SELECT * FROM "+DBTABLE+" \
            WHERE locoID=?", (json_loco_id,))
            matched_row = cur.fetchone()

            if matched_row is not None:
                print "inside row matched on db"
                EMAILTO = str(matched_row[0])
                LOCOMOTIVE = str(matched_row[1])
                DEVICE = str(matched_row[2])
                STATUS = str(matched_row[3])
                NOTIFY = str(matched_row[4])
                COUNT = int(matched_row[5])


                if DEVICE == 'radio' and LOCOMOTIVE == json_loco_id and STATUS == json_statusR:
                    if COUNT >= 1:
                        message = str(LOCOMOTIVE) + " was found " + STATUS + " using " + str(DEVICE) + " " + json_loco_radio
                        send_notification_email(EMAILTO, LOCOMOTIVE, message)
                        COUNT -= 1
                        cur.execute("UPDATE notifications SET locoCOUNT=? WHERE locoID=? and locoEMAILTO=? and locoSTATUS=? and locoNOTIFY=? and locoDEVICE=?",
                                    (COUNT, LOCOMOTIVE, EMAILTO, STATUS, NOTIFY, DEVICE,))
                    else:
                        cur.execute("DELETE FROM "+DBTABLE+" WHERE locoEMAILTO=? AND locoID=? AND locoDEVICE=? AND locoSTATUS=?", (EMAILTO, LOCOMOTIVE, DEVICE, STATUS))
                        break

                if DEVICE == 'wifi' and LOCOMOTIVE == json_loco_id and STATUS == json_statusW:
                    if COUNT >= 1:
                        message = str(LOCOMOTIVE) + " was found " + STATUS + " using " + str(DEVICE) + " " + json_loco_wifi
                        send_notification_email(EMAILTO, LOCOMOTIVE, message)
                        COUNT -= 1
                        cur.execute("UPDATE notifications SET locoCOUNT=? WHERE locoID=? and locoEMAILTO=? and locoSTATUS=? and locoNOTIFY=? and locoDEVICE=?",
                                    (COUNT, LOCOMOTIVE, EMAILTO, STATUS, NOTIFY, DEVICE,))
                    else:
                        cur.execute("DELETE FROM "+DBTABLE+" WHERE locoEMAILTO=? AND locoID=? AND locoDEVICE=? AND locoSTATUS=?", (EMAILTO, LOCOMOTIVE, DEVICE, STATUS))
                        break

                if DEVICE == 'cell' and LOCOMOTIVE == json_loco_id and STATUS == json_statusC:
                    if COUNT >= 1:
                        message = str(LOCOMOTIVE) + " was found " + STATUS + " using " + str(DEVICE) + " " + json_loco_cell
                        send_notification_email(EMAILTO, LOCOMOTIVE, message)
                        COUNT -= 1
                        cur.execute("UPDATE notifications SET locoCOUNT=? WHERE locoID=? and locoEMAILTO=? and locoSTATUS=? and locoNOTIFY=? and locoDEVICE=?",
                                    (COUNT, LOCOMOTIVE, EMAILTO, STATUS, NOTIFY, DEVICE,))
                    else:
                        cur.execute("DELETE FROM "+DBTABLE+" WHERE locoEMAILTO=? AND locoID=? AND locoDEVICE=? AND locoSTATUS=?", (EMAILTO, LOCOMOTIVE, DEVICE, STATUS))
                        break

            else:
                print "* * * searching the db for a match * * *"

    except sqlite3.Error, e:
        print "Error %s:" % e.args[0]
        print "oops, soething super bad happened with SQL"
    finally:
        if con:
            con.commit()
            con.close()
            file.close()
# ############################################################################


if __name__ == "__main__":
    while True:
        print "checking db for json match"
        recursive_check()
        time.sleep(5)
