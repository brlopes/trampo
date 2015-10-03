#!/usr/bin/python
#
# STATIC script trigger on event, quick check database and write:
#
#         JSON
#          ^
#          |
#          v
# PHP -> PYTHON
#          ^
#          |
#          v
#          DB

import smtplib
from email.MIMEMultipart import MIMEMultipart
from email.MIMEText import MIMEText
import sys
import sqlite3
import csv
import datetime
import json
import time

DBNAME = 'notifications.db'
DBTABLE = "notifications"
JSONFILE = "Loco.json"

# FILENAME = argv[0]
EMAILTO = str(sys.argv[1]).lower().strip()
LOCOMOTIVE = str(sys.argv[2]).strip()
DEVICE = str(sys.argv[3]).lower().strip()
STATUS = str(sys.argv[4]).lower().strip()
RECUR = str(sys.argv[5]).lower().strip()

# quick printout test to verify if .py script is called
print "<hr>"
print "FROM .py (argv[s]): "
print EMAILTO, LOCOMOTIVE, DEVICE, STATUS, RECUR
print "<hr>"

# json_current = json.loads(JSONFILE)
with open('Loco.json', 'r') as file:
    event = eval(file.read())
# > datab['data'][0][0]


# ############################################################################
def quick_check_current_json(event, EMAILTO, LOCOMOTIVE, STATUS, RECUR, DEVICE):
    """ compares input to JSON event data: LOCOMOTIVE + STATUS + DEVICE
        True: online
        False: offline
    """
    req_match = None
    if STATUS == "online":
        req_status = True
    elif STATUS == "offline":
        req_status = False

    # for each event, check current json data:
    for row in event['data']:
        json_loco_id = str(row[0])
        json_loco_datetime = row[4].lower()

        if row[1].lower() != "none":
            json_loco_radio = True
        elif row[1].lower() == "none":
            json_loco_radio = False

        if row[2] == "True":
            json_loco_wifi = True
        else:
            json_loco_wifi = False

        if row[3] == "True":
            json_loco_cell = True
        else:
            json_loco_cell = False

        # 3 device types, each one with 2 states:
        if LOCOMOTIVE == json_loco_id:
            if DEVICE == "radio":
                if json_loco_radio == req_status:
                    req_match = True
                else:
                    req_match = False

            if DEVICE == "wifi":
                if json_loco_wifi == req_status:
                    req_match = True
                else:
                    req_match = False

            if DEVICE == "cell":
                if json_loco_cell == req_status:
                    req_match = True
                else:
                    req_match = False

            if req_match:
                print "MATCH ALREADY FOUND!"
                return True
            else:
                print "CURRENT MATCH NOT FOUND!"
                return False
# ############################################################################


# ############################################################################
def check_db_for_already_present_notifications(EMAILTO, LOCOMOTIVE, STATUS, RECUR, DEVICE):
    """ when quick_json_check returs False, then check the db before writting to it
        (dups) if same record found(EMAILTO,LOCOMOTIVE,STATUS,DEVICE): count++
        else: write_new_notification_to_db(**)
    """

    con = None  # connection
    try:
        con = sqlite3.connect(DBNAME)
        cur = con.cursor()

        locoEMAILTO = EMAILTO  # *@*.com
        locoID = LOCOMOTIVE  # 4010
        locoDEVICE = DEVICE  # radio/cell/wifi
        locoSTATUS = STATUS  # online/offline
        locoNOTIFY = RECUR  # single/repeat
        row_requested = (locoEMAILTO, locoID, locoDEVICE, locoSTATUS, locoNOTIFY)

        # 1st: read row ONLY with matching data:
        cur.execute("SELECT locoEMAILTO, locoID, locoDEVICE, locoSTATUS, locoNOTIFY \
        FROM "+DBTABLE+" \
        WHERE locoEMAILTO=? and locoID=? and locoDEVICE=? and locoSTATUS=? and locoNOTIFY=?",
                    (locoEMAILTO, locoID, locoDEVICE, locoSTATUS, locoNOTIFY,))
        matched_row = cur.fetchall()

        # for values already stored on db, update count of notifications made:
        if row_requested in matched_row:
            cur.execute("SELECT locoCount FROM "+DBTABLE+" \
            WHERE locoID=? and locoEMAILTO=? and locoSTATUS=? and locoNOTIFY=? and locoDEVICE=?",
                        (locoID, locoEMAILTO, locoSTATUS, locoNOTIFY, locoDEVICE,))
            stored_count = cur.fetchone()  # picks just one, if repeated should be count++

            increment = stored_count[0] + 1  # repeated notifications

            cur.execute("UPDATE notifications SET locoCOUNT=? WHERE locoID=? and locoEMAILTO=? and locoSTATUS=? and locoNOTIFY=? and locoDEVICE=?",
                        (increment, locoID, locoEMAILTO, locoSTATUS, locoNOTIFY, locoDEVICE,))
            con.commit()  # CARALHO NAO ESQUECE
            # print "notification already present, count increased"
            print " | count++ | "
            return True

        # if values are not found on db then create a new row with the new notification
        else:
            write_new_notification_to_db(EMAILTO, LOCOMOTIVE, STATUS, RECUR, DEVICE)
            print " | new notification row added | "
            return False

    except sqlite3.Error, e:
        print "Error %s:" % e.args[0]
        print "oops, something went wrong when checking the db"

    finally:
        if con:
            con.close()
# ############################################################################


# ############################################################################
def write_new_notification_to_db(EMAILTO, LOCOMOTIVE, STATUS, RECUR, DEVICE):
    """ after checking, if loco is not on json data already write new
        notification request to db, starts with count 0"""

    con = None  # connection
    try:
        con = sqlite3.connect(DBNAME)   # tba just add row to an existing db?
        cur = con.cursor()

        locoEMAILTO = EMAILTO  # *@*.com
        locoID = LOCOMOTIVE  # 4010
        locoDEVICE = DEVICE  # radio/cell/wifi
        locoSTATUS = STATUS  # online/offline
        locoNOTIFY = RECUR  # single/repeat
        TIMESTAMP = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        # every new notification count starts at 0
        if RECUR == 'single':
            locoCOUNT = 1
        elif RECUR == 'repeat':
            locoCOUNT = 10

        dbrow = (locoEMAILTO, locoID, locoDEVICE, locoSTATUS, locoNOTIFY, locoCOUNT, TIMESTAMP)

        cur.execute("CREATE TABLE IF NOT EXISTS notifications\
        (locoEMAILTO TEXT, locoID TEXT, locoDEVICE TEXT, locoSTATUS TEXT, locoNOTIFY TEXT, locoCOUNT INT, locoTIME TEXT)")

        cur.execute("INSERT INTO notifications VALUES (?,?,?,?,?,?,?)", dbrow)

    except sqlite3.Error, e:
        print "Error %s:" % e.args[0]
        print "oops, soething went wrong with SQL when INSERTING row"

    finally:
        if con:
            con.commit()  # CARALHO NAO ESQUECE
            print "New notification ROW successfully written on DB"
            con.close()
# ############################################################################


if __name__ == "__main__":
    if quick_check_current_json(event, EMAILTO, LOCOMOTIVE, STATUS, RECUR, DEVICE):
        print "DATA ALREADY FOUND ON JSON TABLE, NO NEED FOR new NOTIFICATIONs <br>"
        sys.exit(0)
    if check_db_for_already_present_notifications(EMAILTO, LOCOMOTIVE, STATUS, RECUR, DEVICE):
        print "Notification already present on DB, notification count++ <br>"
        sys.exit(0)
    else:
        print "Notification not found, new row added!"
        # print "write to a file for PHP to read and WARN user that
        # locomotive is already online/offline"
