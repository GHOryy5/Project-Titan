import time
import random
import uuid
from collections import deque

# --- THREAT INTEL CONFIGURATION ---
# Keywords that trigger the "Listening" transcription algorithms
WATCHLIST_KEYWORDS = ["package", "delivery", "tunnel", "eagle", "payload", "midnight"]

# Known Hostile Nodes (The starting point of our investigation)
KNOWN_TARGETS = ["555-0199", "555-0100"] 

class TitanPrism:
    def __init__(self):
        print("\033[1;34m[*] TITAN PRISM: MASS SURVEILLANCE & LINK ANALYSIS SYSTEM\033[0m")
        # Graph Database: Stores who calls whom (Adjacency List)
        self.network_graph = {}
        # Metadata Store: Stores the details of the nodes (IMSI, Name, Risk Score)
        self.metadata_store = {}
        # Transcription Store: Simulated audio-to-text logs
        self.transcripts = {}

    def add_citizen(self, phone_number, name, risk_level="LOW"):
        """
        Registers a citizen in the tracking database.
        """
        self.metadata_store[phone_number] = {
            "name": name,
            "imsi": f"310-{random.randint(100,999)}-{random.randint(100000,999999)}",
            "risk": risk_level,
            "geo_history": []
        }
        if phone_number not in self.network_graph:
            self.network_graph[phone_number] = []

    def simulate_call(self, caller, receiver, duration, content_snippet):
        """
        Ingests a CDR (Call Data Record).
        This connects two nodes in our graph.
        """
        # 1. Update Graph Connections (Undirected for this demo)
        if receiver not in self.network_graph[caller]:
            self.network_graph[caller].append(receiver)
        if caller not in self.network_graph[receiver]:
            self.network_graph[receiver].append(caller)
            
        # 2. Store Transcript
        call_id = str(uuid.uuid4())[:8]
        self.transcripts[call_id] = {
            "from": caller,
            "to": receiver,
            "text": content_snippet,
            "flagged": False
        }
        
        # 3. Real-Time Keyword Spotting (The "Listening" Part)
        for word in WATCHLIST_KEYWORDS:
            if word in content_snippet.lower():
                self.transcripts[call_id]["flagged"] = True
                print(f"\033[1;31m[!] KEYWORD ALERT: '{word}' detected in call {caller} -> {receiver}\033[0m")
                # Escalate Risk of both parties
                self.metadata_store[caller]["risk"] = "HIGH"
                self.metadata_store[receiver]["risk"] = "ELEVATED"

    def generate_population(self):
        print("[*] Ingesting Population Registry...")
        # 1. Create Innocent Citizens
        for i in range(20):
            num = f"555-02{i:02d}"
            self.add_citizen(num, f"Citizen_{i}")

        # 2. Create The Terror Cell (Hidden among citizens)
        self.add_citizen("555-0199", "TARGET_ALPHA (Leader)", "CRITICAL")
        self.add_citizen("555-0100", "TARGET_BRAVO (Logistics)", "CRITICAL")
        self.add_citizen("555-0150", "Unknown_Courier", "LOW") # We don't know him yet
        
        # 3. Simulate Traffic (Building the Haystack)
        print("[*] Ingesting 5,000 Call Data Records (CDRs)...")
        time.sleep(1)
        
        # Innocent chatter
        self.simulate_call("555-0201", "555-0202", 120, "Hey mom, coming home for dinner.")
        self.simulate_call("555-0205", "555-0209", 45, "Did you see the game last night?")
        
        # SUSPICIOUS TRAFFIC (The Hidden Network)
        # Leader calls Logistics
        self.simulate_call("555-0199", "555-0100", 15, "The eagle has landed.") 
        # Logistics calls Unknown Courier (The Link)
        self.simulate_call("555-0100", "555-0150", 300, "Package delivery at midnight.")
        # Courier calls Innocent Pizza Guy (Noise)
        self.simulate_call("555-0150", "555-0205", 20, "Two pepperoni pizzas please.")

    def run_link_analysis(self, start_node, max_depth=2):
        """
        The Core Algo: Breadth-First Search (BFS) to find 
        2nd and 3rd degree connections to the target.
        """
        print(f"\n[ANALYSIS] Running Link Analysis on Target: {start_node} ({self.metadata_store[start_node]['name']})")
        print(f"[*] Scanning for associations within {max_depth} hops...")
        
        visited = set()
        queue = deque([(start_node, 0)]) # (PhoneNumber, Degree)
        visited.add(start_node)
        
        while queue:
            current_node, degree = queue.popleft()
            
            if degree > 0:
                # Visualize the Link
                indent = "    " * degree
                meta = self.metadata_store[current_node]
                
                # Color code based on Risk
                color = "\033[0m"
                if meta['risk'] == "CRITICAL": color = "\033[1;31m" # Red
                elif meta['risk'] == "HIGH":     color = "\033[1;33m" # Yellow
                elif meta['risk'] == "ELEVATED": color = "\033[1;35m" # Magenta
                
                print(f"{indent}└── [Tier {degree}] {color}{current_node} ({meta['name']}) - Risk: {meta['risk']}\033[0m")

            if degree < max_depth:
                for neighbor in self.network_graph[current_node]:
                    if neighbor not in visited:
                        visited.add(neighbor)
                        queue.append((neighbor, degree + 1))
        
        print("\n[RESULT] Analysis Complete. Network graph mapping finished.")

if __name__ == "__main__":
    system = TitanPrism()
    system.generate_population()
    
    # Run the Link Analysis starting from the Known Terrorist Leader
    # We want to see who he is connected to, and who THEY are connected to.
    time.sleep(1)
    system.run_link_analysis("555-0199", max_depth=3)
