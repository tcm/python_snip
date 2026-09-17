#!/usr/bin/python3

import fileinput
import sys
import re
import hashlib
import sqlite3
from datetime import datetime, timedelta
import argparse
import json
from functions import adapt_datetime_iso, sqlite_insert_arp_data, sqlite_delete_table_data


def main():
    parser = argparse.ArgumentParser(description='Process some options.')
    parser.add_argument('-f','--file', type=str, required=True, help='Filename to process.')
    parser.add_argument('-j','--json', action='store_true', required=False, help='Print JSON output.')

    args = parser.parse_args()

    con = sqlite3.connect("./database/cmdb-cleaning.db")
    cur = con.cursor()

    filename = {args.file}
    counter = 0

    try:
      for line in fileinput.input(filename):
       # Define patterns.
       m = re.search("Vlan\\d+", line)
       n = re.match("\\d+\\.\\d+\\.\\d+\\.\\d+", line)
       o = re.search("[0-9a-f]{4}\\.[0-9a-f]{4}\\.[0-9a-f]{4}", line)

       # Show matches according to pattern.
       vlan = str(m.group(0)) if m else "undefined"
       ipaddress = str(n.group(0)) if n else "undefined"
       macaddress = str(o.group(0)) if o else "undefined"

       # Generate Hash-Key
       pkey = ipaddress + macaddress
       h = hashlib.sha1()
       h.update(pkey.encode("utf-8"))

       # Insert data to SQLite.
       # Primary key is hash of ipaddress and macaddress combined.
       current_datetime = datetime.now()
       iso_timestamp = adapt_datetime_iso(current_datetime)

       sqlite_insert_arp_data(cur, h.hexdigest(), ipaddress, macaddress, vlan.lower(),iso_timestamp)
       counter = counter + 1

      if args.json == True:
       data = {
          "linecount": counter,
          "id": h.hexdigest(),
          "ipaddress": ipaddress,
          "macaddress": macaddress,
          "vlan": vlan.lower(),
          "timestamp": iso_timestamp
        }
       json_output = json.dumps(data, indent=4)
       print(json_output)
      
    except IOError:
       print("Could not find file",filename)

    con.commit()
    con.close()

if __name__ == '__main__':
    main()