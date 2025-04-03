import time

def start_interview_round(round_info):
    duration_seconds = round_info["duration_minutes"] * 60
    start_time = time.time()
    end_time = start_time + duration_seconds
    return start_time, end_time

def check_time_remaining(start_time, end_time):
    if start_time is None or end_time is None:
        return None  # Return None instead of causing an error

    current_time = time.time()
    time_left = end_time - current_time
    return max(time_left, 0)  # Ensure non-negative remaining time
