import time

def get_time_ms():
    return int(time.time() * 1000)

class Clock:
    def __init__(self, tick) -> None:
        self.gap = int(1000/tick)
        self.next = get_time_ms() + self.gap

    def check(self):
        t = get_time_ms()
        if t >= self.next:
            while self.next <= t:
                self.next += self.gap
            return True