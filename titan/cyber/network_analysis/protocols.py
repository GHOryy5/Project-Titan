import struct
import socket
import textwrap

class EthernetFrame:
    """
    Layer 2: Ethernet Frame Parser
    Extracts Destination MAC, Source MAC, and Protocol Type.
    """
    def __init__(self, raw_data):
        dest, src, prototype = struct.unpack('! 6s 6s H', raw_data[:14])
        self.dest_mac = self._get_mac_addr(dest)
        self.src_mac = self._get_mac_addr(src)
        self.proto = socket.htons(prototype)
        self.data = raw_data[14:]

    def _get_mac_addr(self, bytes_addr):
        bytes_str = map('{:02x}'.format, bytes_addr)
        return ':'.join(bytes_str).upper()

    def __str__(self):
        return f"[ETH] Src: {self.src_mac}, Dst: {self.dest_mac}, Proto: {self.proto}"


class IPv4Header:
    """
    Layer 3: IPv4 Packet Parser
    Unpacks Version, Header Length, TTL, Protocol, Source/Dest IP.
    """
    def __init__(self, raw_data):
        version_header_length = raw_data[0]
        self.version = version_header_length >> 4
        self.header_length = (version_header_length & 15) * 4
        
        # Unpack standard IPv4 fields
        self.ttl, self.proto, src, target = struct.unpack('! 8x B B 2x 4s 4s', raw_data[:20])
        self.src_ip = self._ipv4(src)
        self.target_ip = self._ipv4(target)
        self.data = raw_data[self.header_length:]

    def _ipv4(self, addr):
        return '.'.join(map(str, addr))

    def __str__(self):
        return f"[IPv4] Src: {self.src_ip}, Dst: {self.target_ip}, TTL: {self.ttl}, Proto: {self.proto}"


class ICMPPacket:
    """
    Layer 4 (Control): ICMP Parser
    Used for Ping sweeps and network diagnostics.
    """
    def __init__(self, raw_data):
        self.type, self.code, self.checksum = struct.unpack('! B B H', raw_data[:4])
        self.data = raw_data[4:]

    def __str__(self):
        return f"[ICMP] Type: {self.type}, Code: {self.code}, Checksum: {self.checksum}"


class TCPHeader:
    """
    Layer 4 (Transport): TCP Segment Parser
    Critical for detecting Port Scans, SYN Floods, and C2 Beacons.
    """
    def __init__(self, raw_data):
        (self.src_port, self.dest_port, self.sequence, self.acknowledgment, 
         offset_reserved_flags) = struct.unpack('! H H L L H', raw_data[:14])
        
        # Bitwise operations to extract flags
        self.offset = (offset_reserved_flags >> 12) * 4
        self.flag_urg = (offset_reserved_flags & 32) >> 5
        self.flag_ack = (offset_reserved_flags & 16) >> 4
        self.flag_psh = (offset_reserved_flags & 8) >> 3
        self.flag_rst = (offset_reserved_flags & 4) >> 2
        self.flag_syn = (offset_reserved_flags & 2) >> 1
        self.flag_fin = offset_reserved_flags & 1
        
        self.data = raw_data[self.offset:]

    def __str__(self):
        flags = []
        if self.flag_syn: flags.append("SYN")
        if self.flag_ack: flags.append("ACK")
        if self.flag_fin: flags.append("FIN")
        if self.flag_rst: flags.append("RST")
        flag_str = "|".join(flags)
        return f"[TCP] Port: {self.src_port} -> {self.dest_port} | Flags: {flag_str} | Seq: {self.sequence}"


class UDPHeader:
    """
    Layer 4 (Transport): UDP Datagram Parser
    Used for DNS tunneling detection and Voip monitoring.
    """
    def __init__(self, raw_data):
        self.src_port, self.dest_port, self.size = struct.unpack('! H H 2x H', raw_data[:8])
        self.data = raw_data[8:]

    def __str__(self):
        return f"[UDP] Port: {self.src_port} -> {self.dest_port} | Size: {self.size}"
