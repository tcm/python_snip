#!/usr/bin/python3

import csv
import sqlite3
from pathlib import Path
from typing import List, Tuple, Any
from datetime import datetime

class ReportData:
    """
    Data layer that encapsulates all DB access.
    """

    def __init__(self, db_path: str | Path):
        self.db_path = Path(db_path)

    def _get_connection(self) -> sqlite3.Connection:
        return sqlite3.connect(self.db_path)

    def get_vlans(self) -> List[str]:
        """
        Returns a sorted list of distinct VLAN IDs.
        """
        with self._get_connection() as conn:
            cur = conn.cursor()
            cur.execute("SELECT DISTINCT vlan FROM arp ORDER BY vlan")
            return [row[0] for row in cur.fetchall()]

    def get_vlan_entries(self, vlan: str) -> List[Tuple[Any, ...]]:
        """
        Returns all ARP entries for a given VLAN.
        """
        query = """
            SELECT ipaddress, macaddress, ts
            FROM arp
            WHERE vlan = ?
            ORDER BY ipaddress
        """
        with self._get_connection() as conn:
            cur = conn.cursor()
            cur.execute(query, (vlan,))
            return cur.fetchall()


class ReportExporter:
    """
    Handles exporting data to CSV files.
    """

    def __init__(self, repo: ReportData, output_dir: str | Path = "reports-"):
        self.repo = repo
        
        # Get current month (change format as needed)
        month_suffix = datetime.now().strftime("%Y-%m")  # e.g. "2026-03"
        
        # Ensure Path, then append month
        base_path = Path(output_dir)
        self.output_dir = base_path.with_name(base_path.name + month_suffix)

        self.output_dir.mkdir(parents=True, exist_ok=True)

    def export_vlan_to_csv(self, vlan: str) -> Path:
        """
        Exports fields for a VLAN into a CSV file.
        Returns the path to the written file.
        """
        rows = self.repo.get_vlan_entries(vlan)
        out_file = self.output_dir / f"{vlan}.csv"

        # Define the CSV columns in a fixed order.
        # Data fields are defined via query.
        # See method: get_vlan_entries
        headers = ["ipaddress", "macaddress", "ts"]

        with out_file.open("w", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow(headers)
            writer.writerows(rows)

        print(f"[INFO] Written CSV for VLAN {vlan}: {out_file}")
        return out_file

    def export_all_vlans_to_csv(self) -> None:
        """
        Exports one CSV file per VLAN.
        """
        vlans = self.repo.get_vlans()
        if not vlans:
            print("[INFO] No VLANs found in database.")
            return

        for vlan in vlans:
            self.export_vlan_to_csv(vlan)


def main():
    repo = ReportData("database/cmdb-cleaning.db")
    exporter = ReportExporter(repo, output_dir="vlan-reports-")
    exporter.export_all_vlans_to_csv()


if __name__ == "__main__":
    main()
