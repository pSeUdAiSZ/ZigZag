from datetime import datetime, timedelta
from .models import Service

def timeslot_gen_tf(start, end):
    start_time = datetime.strptime(start, '%I:%M %p')
    end_time = datetime.strptime(end, '%I:%M %p')

    time_slots = []
    current_time = start_time

    while current_time <= end_time:
        time_slot = current_time.strftime('%H:%M:%S')
        time_slots.append(time_slot)
        current_time += timedelta(minutes=15)

    return time_slots
def calculate_end_time(start_time,duration):
    start_time_t=datetime.strptime(start_time, '%H:%M:%S').time()
    start_time_seconds = start_time_t.hour*3600 + start_time_t.minute*60 + start_time_t.second
    duration_in_seconds = int(duration.total_seconds())
    end_time_seconds = start_time_seconds + duration_in_seconds
    hours, remainder = divmod(end_time_seconds, 3600)
    minutes,seconds= divmod(remainder, 60)
    
     
    time_str = f"{hours:02d}:{minutes:02d}:{seconds:02d}"
    
    return time_str
    
        
        # Calculate end time by adding duration to start time
    