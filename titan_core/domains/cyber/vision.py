import random

class TitanVision:
    def __init__(self):
        print("[*] TITAN VISION: IMAGE FORENSICS LOADED")

    def analyze_image(self, image_path):
        """
        Simulates extracting EXIF metadata from a captured terrorist image.
        In real life, this uses the 'Pillow' library to read ExifTags.
        """
        print(f"[*] Scanning {image_path} for hidden metadata...")
        
        # Simulation: 30% chance the image contains hidden coordinates
        has_data = True 
        
        if has_data:
            # Simulate extracting GPS coordinates hidden in the file headers
            extracted_lat = 34.5000 + random.uniform(0.01, 0.09)
            extracted_long = 69.1000 + random.uniform(0.01, 0.09)
            print(f"\033[1;31m[!] STEGANOGRAPHY DETECTED: Hidden GPS Data Found!\033[0m")
            print(f"    > LAT: {extracted_lat}")
            print(f"    > LONG: {extracted_long}")
            return extracted_lat, extracted_long
        else:
            print("[-] No hidden data found.")
            return None, None
