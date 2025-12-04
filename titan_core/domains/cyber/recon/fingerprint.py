class ServiceIdentifier:
    """
    Identifies software based on banner text.
    """
    def identify(self, banner):
        if not banner: return "Unknown"
        
        banner = banner.lower()
        if "ssh" in banner: return "OpenSSH (Secure Shell)"
        if "apache" in banner: return "Apache Web Server"
        if "nginx" in banner: return "Nginx Proxy"
        if "ftp" in banner: return "VSFTPD"
        if "microsoft" in banner: return "Windows Server"
        if "ubuntu" in banner: return "Ubuntu Linux Kernel"
        
        return "Generic TCP Service"
