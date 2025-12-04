from .sna import GraphEngine
from .nlp import SentimentEngine
import time

class TitanIntelCore:
    def __init__(self):
        print("[*] INTEL GRID: LOADING SNA & NLP ENGINES...")
        self.sna = GraphEngine()
        self.nlp = SentimentEngine()
        
        # Seed Data
        self.sna.add_connection("TARGET_ALPHA", "COURIER_X")
        self.sna.add_connection("COURIER_X", "FINANCIER_Y")
        self.sna.add_connection("FINANCIER_Y", "TARGET_BETA")

    def analyze_target_network(self, target_id):
        print(f"\n[*] RUNNING DEEP LINK ANALYSIS FOR {target_id}...")
        path = self.sna.find_path("TARGET_ALPHA", "TARGET_BETA")
        if path:
            print(f"    > LINK DISCOVERED: {' -> '.join(path)}")
        else:
            print("    > No direct links found.")
            
    def scan_intercepts(self, text):
        print(f"[*] NLP SCANNING: '{text[:20]}...'")
        score, hits = self.nlp.analyze_comms(text)
        if score > 0:
            print(f"\033[1;31m    [!] THREAT DETECTED (Score: {score})\033[0m")
            print(f"    > KEYWORDS: {', '.join(hits)}")
        else:
            print("    [+] Content Benign.")
