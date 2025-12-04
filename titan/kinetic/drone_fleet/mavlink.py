import struct
import time

class MavLinkBridge:
    STX = 0xFD
    SYS_ID = 1
    COMP_ID = 1
    
    MSG_HEARTBEAT = 0
    MSG_SET_POSITION_TARGET = 84

    @staticmethod
    def pack_heartbeat() -> bytes:
        header = struct.pack('<BBBBBBBH', 
            MavLinkBridge.STX, 9, 0, 0, 0, 
            MavLinkBridge.SYS_ID, MavLinkBridge.COMP_ID, MavLinkBridge.MSG_HEARTBEAT
        )
        payload = struct.pack('<IBBBBB', 0, 6, 8, 209, 4, 3)
        checksum = MavLinkBridge._calculate_crc(header + payload)
        return header + payload + checksum

    @staticmethod
    def pack_vector(lat: float, lon: float, alt: float, velocity: float) -> bytes:
        header = struct.pack('<BBBBBBBH', 
            MavLinkBridge.STX, 53, 0, 0, 0, 
            MavLinkBridge.SYS_ID, MavLinkBridge.COMP_ID, MavLinkBridge.MSG_SET_POSITION_TARGET
        )
        
        lat_int = int(lat * 1e7)
        lon_int = int(lon * 1e7)
        
        # CHANGED: 'Q' for timestamp (8 bytes), plus the 9 floats 'fffffffff'
        payload = struct.pack('<Qfffffffffiii', 
            int(time.time() * 1000), 
            0.0, 0.0, 0.0,           
            velocity, 0.0, 0.0,      
            0.0, 0.0, 0.0,           
            lat_int, lon_int, int(alt)
        )
        
        checksum = MavLinkBridge._calculate_crc(header + payload)
        return header + payload + checksum

    @staticmethod
    def _calculate_crc(data: bytes) -> bytes:
        crc = 0xFFFF
        for byte in data:
            tmp = byte ^ (crc & 0xFF)
            tmp = (tmp ^ (tmp << 4)) & 0xFF
            crc = (crc >> 8) ^ (tmp << 8) ^ (tmp << 3) ^ (tmp >> 4)
        return struct.pack('<H', crc)

    def transmit(self, packet: bytes, interface_ip: str, port: int):
        print(f"[MAVLINK] TX {len(packet)} bytes to {interface_ip}:{port} | HEX: {packet.hex()[:20]}...")
