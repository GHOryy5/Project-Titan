import socket
import threading
from queue import Queue
from titan_core.config.settings import Config

class PortScanner:
    def __init__(self):
        self.socket_timeout = 0.5
        self.lock = threading.Lock()
    
    def scan_target(self, ip, port_list):
        """
        Multi-threaded Connect Scan.
        Returns a list of (port, banner_text) tuples.
        """
        results = []
        queue = Queue()
        
        # Populate Queue
        for p in port_list:
            queue.put(p)
            
        def worker():
            while not queue.empty():
                port = queue.get()
                try:
                    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                    s.settimeout(self.socket_timeout)
                    code = s.connect_ex((ip, port))
                    
                    if code == 0:
                        # Grab Banner
                        try:
                            s.send(b"HEAD / HTTP/1.0\r\n\r\n")
                            banner = s.recv(1024).decode().strip()
                        except:
                            banner = "UNKNOWN_SERVICE"
                        
                        with self.lock:
                            results.append((port, banner))
                    s.close()
                except:
                    pass
                finally:
                    queue.task_done()

        # Launch Threads
        threads = []
        for _ in range(20): # Increased thread count
            t = threading.Thread(target=worker)
            t.daemon = True
            t.start()
            threads.append(t)
            
        for t in threads:
            t.join()
            
        return results
