import sqlite3

# cmdb-cleaning functions
##########################

def adapt_datetime_iso(val):
   """adapt datetime.datetime""" 
   return val.isoformat()

# Database access functions

def sqlite_insert_arp_data(p_cursor, id, ipaddress, macaddress, vlan, ts):
   try:
     # Insert data normally. Take ISO Timestamp. 
     p_cursor.execute("INSERT INTO arp values (?, ?, ?, ?, ?) ", (id, ipaddress, macaddress, vlan, ts))
     # print("New record:{}".format(id))

   except sqlite3.Error as er:
          # If a primary key violation occurs update timestamp only.
          # SQLITE_CONSTRAINT_PRIMARYKEY error (1555)
          if hasattr(er, 'sqlite_errorcode') and er.sqlite_errorcode == 1555:
            # print("Duplicate primary key: {} -> New timestamp: {}".format(id, ts))
            sql = "UPDATE arp SET ts = ?  WHERE id = ?"
            values = (ts, id )
            p_cursor.execute(sql, values)
          else:
            print("sqlite_insert_data:")
            print(str(er.sqlite_errorcode) + ": " + str(er.sqlite_errorname)) 
            print(er)

def sqlite_delete_table_data(p_cursor, tablename):
   try:
     # Delete all data from table.
     print("Delete all data from {}".format(tablename))
     sql = f"DELETE FROM {tablename}"
     p_cursor.execute(sql)

   except sqlite3.Error as er:
            print("sqlite_delete_table_data:")
            print(str(er.sqlite_errorcode) + ": " + str(er.sqlite_errorname)) 
            print(er)
