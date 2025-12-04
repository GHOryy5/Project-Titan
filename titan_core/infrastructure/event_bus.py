import threading
from typing import Callable, Dict, List

class EventBus:
    """
    Central Nervous System of TITAN.
    Decouples modules so they don't depend on each other directly.
    """
    def __init__(self):
        self.subscribers: Dict[str, List[Callable]] = {}
        self.lock = threading.Lock()

    def subscribe(self, event_type: str, callback: Callable):
        with self.lock:
            if event_type not in self.subscribers:
                self.subscribers[event_type] = []
            self.subscribers[event_type].append(callback)

    def publish(self, event_type: str, data: dict):
        """
        Broadcasts an event to all listening modules.
        """
        # In a real system, this would be async/threaded
        if event_type in self.subscribers:
            for callback in self.subscribers[event_type]:
                try:
                    callback(data)
                except Exception as e:
                    print(f"[BUS ERROR] Subscriber failed on {event_type}: {e}")

# Global Singleton Instance
bus = EventBus()
