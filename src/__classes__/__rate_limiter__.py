import time

class RateLimiter:
    def __init__(self, max_requests, period):
        self.max_requests = max_requests
        self.period = period
        self.timestamps = []
        
    def wait(self):
        if len(self.timestamps) >= self.max_requests:
            elapsed = time.time() - self.timestamps[0]
            
            if elapsed < self.period:
                time_to_wait = self.period - elapsed
                print(f"Rate limit reached. Waiting for {time_to_wait:.2f} seconds.")
                time.sleep(time_to_wait)
            
            self.timestamps.pop(0)
        
        self.timestamps.append(time.time())