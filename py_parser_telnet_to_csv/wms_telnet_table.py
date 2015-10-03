""" yet another parser, fetch telnet data and append to csv """

import getpass
import sys
import telnetlib
import time
import csv
import string
import pdb

HOST = "192.168.X.X"  # :D
PORT = "10123"  # telnet
FILENAME = "wms_table.csv"
# user = raw_input("Enter your remote account: ")
# password = getpass.getpass()


def connect_to_wiu():
    """connects to wms via telnet, and extract the WIU info from the table"""
    try:
        tn = telnetlib.Telnet(HOST, PORT)

        tn.read_until("username:")
        tn.write("admin\r\n")

        tn.read_until("password:")
        tn.write("cci\r\n")

        tn.read_until("> ")
        tn.write("wsrs wsm\r\n")

        tn.read_until("Wayside")
        table = tn.read_very_eager()

        # just as a backup, can also be run on wiulist
        store_original(table)

        # pdb.set_trace()
        wiulist = []
        for wiu in table.splitlines():
            if '.wiu' in wiu:
                wiulist.append(wiu.split())
        print wiulist

        # kill the connection:
        tn.write('\x1d')    # closes OCM prompt
        tn.close()          # ends telnet
        # print table

    except:
        if tn.read_very_eager() is "":
            print "**Telnet timeout error**"
        elif tn.read_very_eager() is "Connection refused":
            print "**Telnet connection was refused**"


def store_original(table):
    with open(FILENAME, 'ab') as f:
        for rows in table:
            f.write(rows)
            # add stuff
        f.write("\n")
        f.close()

# somevar = connect_to_wiu
# extract_table(somevar)


def telnet_wiu_fetch():
    try:
        tn = telnetlib.Telnet("192.168.X.X", "10123")  # :D

        tn.read_until("username:", 5)
        tn.write("admin\r\n")

        if tn.read_until("password:", 5) is '':
            raise Exception('WOWOW')
        tn.write(":D\r\n")

        tn.read_until("> ", 5)
        tn.write(":D wsm\r\n")

        tn.read_until(":D", 5)
        table = tn.read_very_eager()

        # kill the connection:
        tn.write('\x1d')    # closes OCM prompt
        tn.close()          # ends telnet

        # format the results to a list of lists
        wiulist = []
        for wiu in table.splitlines():
            if '.wiu' in wiu:
                wdata = wiu.split()
                u = WaysideWIU('Hello I am a WIU', wdata[0])
                list_merge_update(u)
                # wiulist.append(u)
        print wiulist
        # return wiulist
    except Exception, e:
        print e
        print 'AAAAAAAAAAAAAAAAAAAAAAA'
        sys.exit(1)
        # if table is "":
        #     print "**Telnet timeout error**"
        # elif table is "Connection refused":
        #     print "**Telnet connection was refused**"

# telnet_wiu_fetch()
connect_to_wiu()
