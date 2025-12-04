import hashlib
import time
import itertools
import string

class TitanBreaker:
    def __init__(self, db_handle):
        self.db = db_handle
        print("[*] TITAN BREAKER: CRYPTANALYSIS ENGINE LOADED")

    def crack_hash(self, target_hash, hash_type="MD5"):
        """
        Simulates a Dictionary/Brute-Force Attack on a captured hash.
        """
        print(f"\n[*] INITIATING BRUTE-FORCE ATTACK ON: {target_hash}")
        print(f"    > ALGORITHM: {hash_type}")
        print(f"    > THREADS:   8 (Simulated)")
        time.sleep(1)

        # A small dictionary of common terrorist passwords
        wordlist = ["123456", "password", "jihad", "freedom", "eagle", "admin", "toor", "786", "kaboom", "martyr"]
        
        print("[*] Running Dictionary Attack...")
        for word in wordlist:
            # Hash the word to see if it matches
            if hash_type == "MD5":
                attempt = hashlib.md5(word.encode()).hexdigest()
            elif hash_type == "SHA256":
                attempt = hashlib.sha256(word.encode()).hexdigest()
            
            if attempt == target_hash:
                print(f"\033[1;32m[+] PASSWORD CRACKED: '{word}'\033[0m")
                return word
            
            time.sleep(0.05) # Visual effect

        print("[-] Dictionary exhausted. Switching to Incremental Brute Force (3 chars)...")
        
        # Brute force 3 character combinations (a-z)
        chars = string.ascii_lowercase
        for combo in itertools.product(chars, repeat=3):
            word = "".join(combo)
            if hash_type == "MD5":
                attempt = hashlib.md5(word.encode()).hexdigest()
            
            if attempt == target_hash:
                print(f"\033[1;32m[+] PASSWORD CRACKED: '{word}'\033[0m")
                return word

        print("\033[1;31m[-] CRACKING FAILED. HASH TOO COMPLEX.\033[0m")
        return None

    def decrypt_loot(self, target_id):
        """
        Checks the 'Loot' table for encrypted files and tries to crack them.
        """
        print(f"[*] Scanning seized artifacts for Target #{target_id}...")
        
        # 1. Fetch data that looks encrypted (We simulate finding a hash)
        # We assume we found a 'SIGNAL_DB' in the loot earlier which is locked
        self.db.cursor.execute("SELECT id, content FROM loot WHERE target_id=? AND data_type='SIGNAL_DB'", (target_id,))
        rows = self.db.cursor.fetchall()
        
        if not rows:
            print("[-] No encrypted containers found in evidence.")
            return

        for row in rows:
            loot_id = row[0]
            content = row[1]
            print(f"[*] Found Encrypted Container (ID: {loot_id})")
            
            # Simulation: The content string contains a hash in real life, 
            # here we just mock a hash for the demo
            mock_target = "eagle" 
            mock_hash = hashlib.md5(mock_target.encode()).hexdigest()
            
            print(f"    > EXTRACTED HASH: {mock_hash}")
            
            password = self.crack_hash(mock_hash, "MD5")
            
            if password:
                # Update DB with cracked content
                new_content = f"DECRYPTED_DB: (Contacts: Al-Baghdadi, The_Jackal, Courier_6)"
                self.db.cursor.execute("UPDATE loot SET content=?, data_type='DECRYPTED_INTEL' WHERE id=?", (new_content, loot_id))
                self.db.conn.commit()
                print("[+] Database Updated with Plaintext Intel.")

