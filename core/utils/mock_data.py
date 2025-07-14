
import random
import time
from datetime import datetime

def generate_mock_data():
    """
    Generate a mock data line simulating sensor readings.
    """
    timestamp = datetime.now().strftime('%H:%M:%S')
    time_sec = round(time.time() % 60, 3)
    val1 = random.randint(28000, 32000)
    val2 = random.randint(28000, 32000)
    val3 = random.randint(40, 60)
    val4 = random.randint(24000, 26000)
    return f"[{timestamp}] {time_sec} | {val1} | {val2} | {val3} | {val4}"
