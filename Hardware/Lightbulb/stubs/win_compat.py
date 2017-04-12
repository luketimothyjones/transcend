import time

# Patch for debugging on PC
if not hasattr(time, 'sleep_ms'):
    setattr(time, 'sleep_ms', lambda t: time.sleep(t / 1000))
