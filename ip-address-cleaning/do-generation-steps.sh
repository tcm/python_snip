#!/usr/bin/bash



echo "Clear database."
./init-sqlite-database.py --delete


for file in ./cifs_download/device?/arp_table*.*; do
    echo "Processing file: $file"
    ./parse-nxos-output.py -f $file 
    sleep 3
done


echo "Generate reports."
./generate-report.py

exit 0
