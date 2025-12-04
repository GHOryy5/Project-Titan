import datetime
import os

class TitanReporter:
    def __init__(self, db_handle):
        self.db = db_handle

    def generate_intsum(self, target_id):
        """
        Generates an Intelligence Summary (INTSUM) text file.
        This allows the user to export their findings.
        """
        if not target_id:
            print("[-] Error: No target selected for report.")
            return

        # Fetch Target Info
        self.db.cursor.execute("SELECT codename, risk_level, status FROM targets WHERE id=?", (target_id,))
        target = self.db.cursor.fetchone()
        
        if not target:
            print("[-] Target not found.")
            return

        filename = f"INTSUM_{target[0]}_{datetime.datetime.now().strftime('%Y%m%d')}.txt"
        
        print(f"[*] Compiling Dossier for {target[0]}...")
        
        with open(filename, "w") as f:
            f.write("TOP SECRET // NOFORN\n")
            f.write("TITAN OPERATIONS - INTELLIGENCE SUMMARY\n")
            f.write("="*50 + "\n")
            f.write(f"TARGET ID:   {target_id}\n")
            f.write(f"CODENAME:    {target[0]}\n")
            f.write(f"RISK LEVEL:  {target[1]}\n")
            f.write(f"STATUS:      {target[2]}\n")
            f.write(f"GENERATED:   {datetime.datetime.now()}\n")
            f.write("="*50 + "\n\n")
            
            # SECTION 1: LOCATION HISTORY
            f.write("[1.0] GEOSPATIAL INTELLIGENCE (GEOINT)\n")
            f.write("-" * 40 + "\n")
            self.db.cursor.execute("SELECT timestamp, lat, long FROM locations WHERE target_id=?", (target_id,))
            locs = self.db.cursor.fetchall()
            if locs:
                for loc in locs:
                    f.write(f"   [{loc[0]}] GRID: {loc[1]}, {loc[2]}\n")
            else:
                f.write("   No geospatial data recorded.\n")
            f.write("\n")

            # SECTION 2: EXFILTRATED DATA
            f.write("[2.0] SIGNALS INTELLIGENCE (SIGINT/CYBER)\n")
            f.write("-" * 40 + "\n")
            self.db.cursor.execute("SELECT timestamp, data_type, content FROM loot WHERE target_id=?", (target_id,))
            loot = self.db.cursor.fetchall()
            if loot:
                for item in loot:
                    f.write(f"   [{item[0]}] TYPE: {item[1]}\n")
                    f.write(f"       CONTENT: {item[2]}\n")
            else:
                f.write("   No data exfiltrated.\n")
            f.write("\n")
            
            f.write("="*50 + "\n")
            f.write("END OF REPORT\n")
            
        print(f"\033[1;32m[+] SUCCESS: Report generated at {os.getcwd()}/{filename}\033[0m")
