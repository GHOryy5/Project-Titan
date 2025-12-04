import sys
import time
from titan_core.config.settings import Config

# Infrastructure Imports
from titan_core.infrastructure.event_bus import bus
from titan_core.infrastructure.database import TitanDB
from titan_core.infrastructure.logger import TitanLogger
from titan_core.infrastructure.daemon import TitanDaemon 

# Domain Imports (New Paths)
from titan_core.domains.signals.hunter import TitanHunter
from titan_core.domains.signals.telecom import TitanSignaling
from titan_core.domains.signals.satcom import TitanSatcom
from titan_core.domains.signals.guardian import TitanGuardian

from titan_core.domains.cyber.strike import TitanStrike
from titan_core.domains.cyber.breaker import TitanBreaker
from titan_core.domains.cyber.vision import TitanVision
from titan_core.domains.cyber.recon.core import TitanReconCore

from titan_core.domains.kinetic.ballistics import TitanBallistics
from titan_core.domains.kinetic.seismic import TitanTunnel
from titan_core.domains.kinetic.drone import TitanSentinel
from titan_core.domains.kinetic.defense.core import TitanDefenseCore

from titan_core.domains.intel.analysis.core import TitanIntelCore
from titan_core.domains.intel.reporting import TitanReporter

def clear_screen():
    print("\033[2J\033[H", end="")

def banner():
    print(f"""
\033[1;36m
   ████████╗██╗████████╗ █████╗ ███╗   ██╗
   ╚══██╔══╝██║╚══██╔══╝██╔══██╗████╗  ██║
      ██║   ██║   ██║   ███████║██╔██╗ ██║
      ██║   ██║   ██║   ██╔══██║██║╚██╗██║
      ██║   ██║   ██║   ██║  ██║██║ ╚████║
      ╚═╝   ╚═╝   ╚═╝   ╚═╝  ╚═╝╚═╝  ╚═══╝
   [ TITAN ARCHITECTURE | v17.0 DISTRIBUTED ]
   [ DOMAINS: SIGNALS | CYBER | KINETIC | INTEL ]
\033[0m""")

def main_menu():
    try:
        # 1. Boot Infrastructure
        logger = TitanLogger()
        db = TitanDB()
        
        # 2. Hook up the Nervous System (Event Bus)
        # Example: When 'TARGET_LOCATED' event fires, log it automatically
        def log_event_listener(data):
            logger.log_op("BUS_EVENT", str(data))
        bus.subscribe("TARGET_LOCATED", log_event_listener)
        
        daemon = TitanDaemon(db, logger)
        daemon.start()
        
        # 3. Initialize Domains
        hunter = TitanHunter()
        telecom = TitanSignaling(db)
        satcom = TitanSatcom(db)
        guardian = TitanGuardian(db)
        
        strike = TitanStrike(db)
        breaker = TitanBreaker(db)
        vision = TitanVision()
        recon = TitanReconCore()
        
        kinetic = TitanBallistics()
        tunnel = TitanTunnel()
        sentinel = TitanSentinel(db)
        defense = TitanDefenseCore()
        
        intel = TitanIntelCore()
        reporter = TitanReporter(db)
        
        active_target_id = None
        
        while True:
            clear_screen()
            banner()
            if active_target_id:
                db.cursor.execute("SELECT codename FROM targets WHERE id=?", (active_target_id,))
                res = db.cursor.fetchone()
                name = res[0] if res else "UNKNOWN"
                print(f"\033[1;33m[!] ACTIVE MISSION: {name} (ID: #{active_target_id})\033[0m")
                
                db.cursor.execute("SELECT content FROM loot WHERE target_id=? AND data_type='DAEMON_ALERT' ORDER BY id DESC LIMIT 1", (active_target_id,))
                alert = db.cursor.fetchone()
                if alert: print(f"\033[1;31m[!] {alert[0]}\033[0m")
            else:
                print("\033[1;30m[!] STATUS: IDLE (Select Option 1)\033[0m")

            print("-" * 60)
            print("--- SIGNALS DOMAIN ---")
            print("1.  [INTEL]    Create NEW Case or LOAD Existing")
            print("2.  [TELECOM]  SS7 HLR Lookup & Tracking")
            print("3.  [SATCOM]   Orbital Satellite Interception")
            print("4.  [HUNTER]   Geolocation (TDoA Tracking)")
            print("5.  [GUARDIAN] C-IED Jamming")
            print("\n--- KINETIC DOMAIN ---")
            print("6.  [SENTINEL] AI Video Surveillance")
            print("7.  [TUNNEL]   Subterranean Sensors")
            print("8.  [DEFENSE]  Airspace Defense Grid")
            print("9.  [KINETIC]  Calculate Fire Solution")
            print("\n--- CYBER DOMAIN ---")
            print("10. [RECON]    Network Vulnerability Grid")
            print("11. [STRIKE]   Launch Zero-Click Exploit")
            print("12. [BREAKER]  Decrypt Captured Intel")
            print("\n--- INTEL DOMAIN ---")
            print("13. [ANALYSIS] Run Graph & NLP Analytics")
            print("14. [REPORT]   Generate Mission Dossier")
            print("15. [SYSTEM]   Exit")
            print("-" * 60)
            
            try:
                choice = input("TITAN-C2 > ")
            except EOFError:
                break
            
            if choice == "1":
                print("\n[1] Create New Target")
                print("[2] Load Existing Target")
                sub = input("Select > ")
                if sub == "1":
                    name = input("Enter Target Codename: ")
                    risk = input("Enter Risk Level (LOW/MED/HIGH): ")
                    active_target_id = db.add_target(name, risk)
                    logger.log_op("INTEL", f"Created Case {name}")
                elif sub == "2":
                    db.cursor.execute("SELECT id, codename, risk_level FROM targets")
                    rows = db.cursor.fetchall()
                    print("\nID | CODENAME       | RISK")
                    print("---|----------------|-----")
                    for r in rows:
                        print(f"{r[0]:<2} | {r[1]:<14} | {r[2]}")
                    tid = input("\nEnter Target ID to Load: ")
                    db.cursor.execute("SELECT id FROM targets WHERE id=?", (tid,))
                    if db.cursor.fetchone(): 
                        active_target_id = int(tid)
                        logger.log_op("INTEL", f"Loaded Case #{tid}")
                time.sleep(1)

            elif choice == "2":
                if not active_target_id: print("[-] No active target."); time.sleep(1); continue
                phone = input("Enter Target MSISDN: ")
                imsi, msc = telecom.resolve_msisdn_to_imsi(phone)
                telecom.send_silent_sms(imsi)
                lat, long = telecom.get_cell_id_location(imsi, msc)
                db.add_location(active_target_id, lat, long)
                # EVENT BUS PUBLISH
                bus.publish("TARGET_LOCATED", {"id": active_target_id, "lat": lat, "long": long, "source": "SS7"})
                input("\nPress Enter...")

            elif choice == "3":
                if not active_target_id: print("[-] No active target."); time.sleep(1); continue
                success = satcom.track_pass()
                if success: satcom.decode_downlink(active_target_id)
                input("\nPress Enter...")

            elif choice == "4":
                if not active_target_id: print("[-] No active target."); time.sleep(1); continue
                x, y = hunter.track_target("LIVE_SIGNAL")
                db.add_location(active_target_id, x, y)
                bus.publish("TARGET_LOCATED", {"id": active_target_id, "lat": x, "long": y, "source": "TDoA"})
                input("\nPress Enter...")

            elif choice == "5":
                if not active_target_id: print("[-] No active target."); time.sleep(1); continue
                freq, power = guardian.scan_rf_environment()
                if freq:
                    success = guardian.engage_jammer(freq, power)
                    if success:
                        db.cursor.execute("INSERT INTO loot (target_id, data_type, content, timestamp) VALUES (?, ?, ?, datetime('now'))", 
                                         (active_target_id, "IED_NEUTRALIZED", f"Freq: {freq}MHz"))
                        db.conn.commit()
                input("\nPress Enter...")

            elif choice == "6":
                if not active_target_id: print("[-] No active target."); time.sleep(1); continue
                feed = input("Enter Drone Feed Source: ")
                lat, long, obj_type = sentinel.analyze_video_feed(feed)
                if lat: db.add_location(active_target_id, lat, long)
                input("\nPress Enter...")

            elif choice == "7":
                if not active_target_id: print("[-] No active target."); time.sleep(1); continue
                is_threat, depth = tunnel.listen_ground()
                if is_threat: db.add_location(active_target_id, 0, 0)
                input("\nPress Enter...")

            elif choice == "8":
                if not active_target_id: print("[-] No active target."); time.sleep(1); continue
                loc = db.get_last_location(active_target_id)
                if loc: defense.scan_airspace(loc[0], loc[1])
                else: print("[-] No location data.")
                input("\nPress Enter...")

            elif choice == "9":
                if not active_target_id: print("[-] No active target."); time.sleep(1); continue
                loc = db.get_last_location(active_target_id)
                if loc: kinetic.calculate_drop(500, loc[0], loc[1])
                else: print("[-] No location data.")
                input("\nPress Enter...")

            elif choice == "10":
                target_ip = input("Enter Target IP: ")
                recon.run_full_scan(target_ip)
                input("\nPress Enter...")

            elif choice == "11":
                if not active_target_id: print("[-] No active target."); time.sleep(1); continue
                confirm = input("AUTHORIZE INTRUSIVE CYBER OPERATION? (Y/N): ")
                if confirm.upper() == "Y":
                    success = strike.launch_exploit(active_target_id)
                    if success: strike.exfiltrate_data(active_target_id)
                input("\nPress Enter...")

            elif choice == "12":
                if not active_target_id: print("[-] No active target."); time.sleep(1); continue
                breaker.decrypt_loot(active_target_id)
                input("\nPress Enter...")

            elif choice == "13":
                if not active_target_id: print("[-] No active target."); time.sleep(1); continue
                intel.analyze_target_network("TARGET_ALPHA")
                intel.scan_intercepts("The package arrives at midnight via eagle courier.")
                input("\nPress Enter...")

            elif choice == "14":
                if not active_target_id: print("[-] No active target."); time.sleep(1); continue
                reporter.generate_intsum(active_target_id)
                input("\nPress Enter...")

            elif choice == "15":
                daemon.stop()
                db.close()
                sys.exit()

    except KeyboardInterrupt:
        print("\n\033[1;31m[!] SYSTEM HALTED.\033[0m")
        sys.exit()

if __name__ == "__main__":
    main_menu()
