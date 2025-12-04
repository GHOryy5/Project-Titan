import sqlite3
import datetime
import threading

class TitanDB:
    def __init__(self):
        # check_same_thread=False allows the Background Daemon to access the DB
        # while the Main Menu is also using it.
        self.conn = sqlite3.connect("titan_operations.db", check_same_thread=False)
        self.cursor = self.conn.cursor()
        self.lock = threading.Lock() # Mutex lock to prevent data corruption
        self.initialize_tables()

    def initialize_tables(self):
        with self.lock:
            self.cursor.execute("""
                CREATE TABLE IF NOT EXISTS targets (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    codename TEXT,
                    risk_level TEXT,
                    status TEXT
                )
            """)
            self.cursor.execute("""
                CREATE TABLE IF NOT EXISTS loot (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    target_id INTEGER,
                    data_type TEXT,
                    content TEXT,
                    timestamp TEXT
                )
            """)
            self.cursor.execute("""
                CREATE TABLE IF NOT EXISTS locations (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    target_id INTEGER,
                    lat REAL,
                    long REAL,
                    timestamp TEXT
                )
            """)
            # NEW: SYSTEM EVENTS TABLE (For the Daemon)
            self.cursor.execute("""
                CREATE TABLE IF NOT EXISTS system_events (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    event_type TEXT,
                    details TEXT,
                    processed INTEGER DEFAULT 0,
                    timestamp TEXT
                )
            """)
            self.conn.commit()

    def add_target(self, codename, risk):
        with self.lock:
            self.cursor.execute("INSERT INTO targets (codename, risk_level, status) VALUES (?, ?, 'ACTIVE')", (codename, risk))
            self.conn.commit()
            return self.cursor.lastrowid

    def add_location(self, target_id, lat, long):
        ts = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        with self.lock:
            self.cursor.execute("INSERT INTO locations (target_id, lat, long, timestamp) VALUES (?, ?, ?, ?)", (target_id, lat, long, ts))
            # TRIGGER: Add an event for the Daemon to see
            self.cursor.execute("INSERT INTO system_events (event_type, details, timestamp) VALUES (?, ?, ?)", 
                               ("NEW_LOCATION", f"{target_id}:{lat}:{long}", ts))
            self.conn.commit()
        print(f"\033[1;33m[DB] Location updated & Event Triggered.\033[0m")

    def get_last_location(self, target_id):
        with self.lock:
            self.cursor.execute("SELECT lat, long FROM locations WHERE target_id=? ORDER BY id DESC LIMIT 1", (target_id,))
            return self.cursor.fetchone()
    
    def get_pending_events(self):
        with self.lock:
            self.cursor.execute("SELECT id, event_type, details FROM system_events WHERE processed=0")
            return self.cursor.fetchall()

    def mark_event_processed(self, event_id):
        with self.lock:
            self.cursor.execute("UPDATE system_events SET processed=1 WHERE id=?", (event_id,))
            self.conn.commit()

    def close(self):
        self.conn.close()
