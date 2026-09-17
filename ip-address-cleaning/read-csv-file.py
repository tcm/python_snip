#!/usr/bin/python3

import sys
import sqlite3
import hashlib
import csv
from datetime import datetime, timedelta
import argparse
from functions import adapt_datetime_iso

def sqlite_insert_data(p_cursor, p_id, p_ipaddress, p_status, p_vlan, ts):
   try:
     p_cursor.execute("INSERT INTO sharp values (?, ?, ?, ?, ? )", (p_id, p_ipaddress, p_status, p_vlan, ts ))
   except sqlite3.Error as er:
     print("sqlite_insert_data:")
     print(str(er.sqlite_errorcode) + ": " + str(er.sqlite_errorname)) 
     print (er) 

def main():
    parser = argparse.ArgumentParser(description='Process some options.')
    parser.add_argument('-f', type=str, required=True, help='Filename to process.')

    args = parser.parse_args()

    con = sqlite3.connect("./database/cmdb-cleaning.db")
    cur = con.cursor()

    filename = str(args.f) 
    try:
        with open(filename, newline='') as csvfile:
          sharpreader = csv.DictReader(csvfile)
          for row in sharpreader:
             ipaddress = row['ip_address']
             status = row['install_status']
             vlan = row['u_vlan']
             print(row['ip_address'], row['install_status'], row['u_vlan'])

        # Generate Hash-Key
        pkey = ipaddress
        h = hashlib.sha1()
        h.update(pkey.encode("utf-8"))

        # Insert data to SQLite.
        # Primary key is hash of ipaddress. 
        current_datetime = datetime.now()
        iso_timestamp = adapt_datetime_iso(current_datetime)
     
        sqlite_insert_data(cur, h.hexdigest(), ipaddress, status, vlan, iso_timestamp)
    except IOError:
       print("Could not find file",filename)

    con.commit()
    con.close()

if __name__ == '__main__':
   main()