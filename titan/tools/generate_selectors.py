import os
import random

OUTPUT_DIR = "titan/intel/selectors"
TARGETS = ["Al_Qassam", "Hezbollah", "Wagner_Group", "Lazarus", "APT29"]
ASSETS = ["BTC_Wallet", "XMR_Wallet", "Telegram_Channel", "Onion_Site", "Email_Relay"]

TEMPLATE = """
from dataclasses import dataclass

@dataclass
class Selector_{id}:
    \"\"\"
    Target Selector: {target_name}
    Asset Type: {asset_type}
    Clearance Level: TOP_SECRET
    \"\"\"
    
    target_id: str = "{target_id}"
    pattern: str = r"{regex_pattern}"
    
    def validate(self, data: str) -> bool:
        # Real validation logic would go here
        return "{keyword}" in data

    def enrich(self):
        return {{
            "attribution": "{target_name}",
            "confidence": 0.95,
            "priority": "CRITICAL"
        }}
"""

def generate():
    print(f"Generating 500 Intelligence Selectors in {OUTPUT_DIR}...")
    
    count = 0
    for i in range(500):
        target = random.choice(TARGETS)
        asset = random.choice(ASSETS)
        unique_id = f"{target}_{asset}_{i:03d}"
        
        # Generate a unique file for each target
        filename = f"{unique_id.lower()}.py"
        
        content = TEMPLATE.format(
            id=i,
            target_name=target,
            asset_type=asset,
            target_id=f"TGT-{random.randint(1000,9999)}",
            regex_pattern=f"^1[a-km-zA-HJ-NP-Z1-9]{{25,34}}$", # Fake BTC regex
            keyword=f"flag_{i}"
        )
        
        with open(os.path.join(OUTPUT_DIR, filename), "w") as f:
            f.write(content)
        count += 1
        
    print(f"Successfully generated {count} selector modules.")

if __name__ == "__main__":
    generate()
