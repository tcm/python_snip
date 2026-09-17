#!/usr/bin/python3

import sys
import sqlite3
from datetime import datetime, timedelta
from functions import adapt_datetime_iso, sqlite_insert_arp_data, sqlite_delete_table_data
import argparse

# Create all my tables
def sqlite_create_tables(p_cursor):
   try:
     p_cursor.execute("CREATE TABLE arp(id TEXT PRIMARY KEY, ipaddress TEXT, macaddress TEXT, vlan TEXT, ts TIMESTAMP)")
     p_cursor.execute("CREATE TABLE sharp(id TEXT PRIMARY KEY, ipaddress TEXT, status TEXT, vlan TEXT,  ts TIMESTAMP)")
   except sqlite3.Error as er:
    print("sqlite_create_tables:")
    print(str(er.sqlite_errorcode) + ": " + str(er.sqlite_errorname)) 
    print (er)   
            
def main():

    parser = argparse.ArgumentParser(
        description="Process database actions"
    )

    parser.add_argument(
        "-d", "--delete",
        action="store_true",
        help="Delete rows in table."
    )

    parser.add_argument(
        "-c", "--create",
        action="store_true",
        help="Create tables."
    )

    parser.add_argument(
        "-i", "--init",
        action="store_true",
        help="Initialise tables with test data."
    )

    args = parser.parse_args()

    con = sqlite3.connect("./database/cmdb-cleaning.db")
    cur = con.cursor()

    if args.create:
        sqlite_create_tables(cur)

    if args.delete:
        sqlite_delete_table_data(cur,"ARP")

    if args.init:
        current_datetime = datetime.now()

        iso_timestamp = adapt_datetime_iso(current_datetime)
        sqlite_insert_arp_data(cur, "A", "192,168.0.1", "abc41.abc92.abc22", "Vlan3401", iso_timestamp )
        sqlite_insert_arp_data(cur, "B", "192,168.0.2", "abc41.abc97.abc27", "Vlan3401", iso_timestamp)
        sqlite_insert_arp_data(cur, "C", "192,168.0.3", "abc41.abc91.abc23", "Vlan3401", iso_timestamp )

        one_day_ago = current_datetime - timedelta(days=1)
        iso_timestamp = adapt_datetime_iso(one_day_ago)
        sqlite_insert_arp_data(cur, "F", "192,168.0.5", "abc42.abc52.abc62", "Vlan3401", iso_timestamp )
        sqlite_insert_arp_data(cur, "G", "192,168.0.6", "abc47.abc57.abc67", "Vlan3401", iso_timestamp)
        sqlite_insert_arp_data(cur, "H", "192,168.0.7", "abc43.abc53.abc63", "Vlan3401", iso_timestamp )

        two_days_ago = current_datetime - timedelta(days=2)
        iso_timestamp = adapt_datetime_iso(two_days_ago)
        sqlite_insert_arp_data(cur, "I", "192,168.0.15", "abc41.abc51.abc61", "Vlan3402", iso_timestamp )
        sqlite_insert_arp_data(cur, "J", "192,168.0.16", "abc42.abc52.abc62", "Vlan3402", iso_timestamp)
        sqlite_insert_arp_data(cur, "K", "192,168.0.17", "abc42.abc52.abc62", "Vlan3402", iso_timestamp )

    con.commit()
    con.close()

if __name__ == '__main__':
    main()