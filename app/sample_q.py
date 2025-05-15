# Log Format:
# Each log entry is a string with comma-separated values:
# "TechnicianID,ServiceType,StartTime,EndTime"
import datetime
from typing import List
# TechnicianID: A string (e.g., "Tech001")
# ServiceType: A string (e.g., "Maintenance", "Repair", "Installation")
# StartTime: Time in "HH:MM" format (24-hour, e.g., "09:00", "14:30")
# EndTime: Time in "HH:MM" format (e.g., "10:30", "17:00")
# You can assume all logs are for the same day, and EndTime is always after StartTime.

# Task:
# Write a Python function calculate_total_service_time(logs: list[str], target_service_type: str) -> int that:

# Takes a list of log strings (logs) and a target_service_type string.
# Parses each log entry.
# For entries matching the target_service_type:
# Calculates the duration of the service in minutes.
# Handles potential errors in log format (e.g., missing fields, incorrect time format). Malformed or irrelevant logs should be skipped.
# Returns the total time in minutes spent on the target_service_type across all valid matching logs. If no valid logs for the target service type are found, return 0.

# (You would place the function definition above this in CoderPad)

def calculate_total_service_time(logs: List[str], target_service_type: str) -> int:
    """
    Calculate the total service time for a specific service type from a list of log entries.

    Args:
        logs (list[str]): List of log entries in the format "TechnicianID,ServiceType,StartTime,EndTime".
        target_service_type (str): The service type to filter by (e.g., "Repair", "Maintenance").

    Returns:
        int: Total time in minutes spent on the target service type.
    """
    total_time = 0
    time_format = "%H:%M"
    for log in logs:
        try:
            parts = log.split(',')
            technician_id = parts[0].strip()
            service_type = parts[1].strip()
            start_time_str = parts[2].strip()
            end_time_str = parts[3].strip()
            if service_type == target_service_type:
                # Parse times

                    start_time = datetime.datetime.strptime(start_time_str, time_format)
                    end_time = datetime.datetime.strptime(end_time_str, time_format)

                    # Calculate duration
                    duration = end_time - start_time
                    total_time += int(duration.total_seconds() / 60)
        except ValueError:
             continue
        except IndexError:
             continue
    return total_time
    
logs1 = [
    "Tech001,Repair,09:00,10:30",       # 90 mins
    "Tech002,Maintenance,11:00,11:45", # 45 mins
    "Tech001,Installation,13:00,16:30", # 210 mins
    "Tech003,Repair,14:00,14:40",       # 40 mins
    "Tech002,Repair,10:00,12:00",       # 120 mins
    "Tech004,Maintenance,invalid,17:00", # Malformed time
    "Tech005,Repair",                    # Malformed entry
]

# Test cases
print(f"Total Repair time: {calculate_total_service_time(logs1, 'Repair')}")
# Expected output: Total Repair time: 250 (90 + 40 + 120)

print(f"Total Maintenance time: {calculate_total_service_time(logs1, 'Maintenance')}")
# Expected output: Total Maintenance time: 45

print(f"Total Installation time: {calculate_total_service_time(logs1, 'Installation')}")
# Expected output: Total Installation time: 210

print(f"Total Consultation time: {calculate_total_service_time(logs1, 'Consultation')}")
# Expected output: Total Consultation time: 0