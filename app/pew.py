# import datetime
# import os
import json
import re
import requests
# def analyze_log_file(filepath, start_date_str, end_date_str):
#     """
#     Analyzes a large log file line by line, extracts timestamps,
#     filters entries by a date range (inclusive start, exclusive end),
#     and counts the number of matching entries.

#     Args:
#         filepath (str): The path to the log file (e.g., 'log_data.txt').
#         start_date_str (str): The start date for filtering (inclusive),
#                               in '%Y-%m-%d' format (e.g., '2023-10-27').
#         end_date_str (str): The end date for filtering (exclusive),
#                             in '%Y-%m-%d' format (e.g., '2023-10-29').

#     Returns:
#         int: The total number of log entries that fall within the
#              specified date range. Returns 0 if the file is not found
#              or if date parsing fails.
#     """
#     count = 0
#     # Define the expected timestamp format in the log file
#     log_timestamp_format = '%Y-%m-%d %H:%M:%S'
#     # Define the expected date format for input start/end dates
#     input_date_format = '%Y-%m-%d'

#     try:
#         # 1. Parse start and end dates into datetime objects
#         # The start_date is inclusive, so parse directly.
#         start_datetime = datetime.datetime.strptime(start_date_str, input_date_format)
#         # The end_date is exclusive. Parsing it as a date effectively sets
#         # the time to 00:00:00 of that day. The '<' comparison later
#         # correctly excludes timestamps from the end_date itself.
#         end_datetime = datetime.datetime.strptime(end_date_str, input_date_format)

#     except ValueError:
#         print(f"Error: Invalid date format provided for start_date_str ('{start_date_str}') or end_date_str ('{end_date_str}'). Expected format is '{input_date_format}'.")
#         return 0

#     # Ensure the start date is not after or equal to the end date for a valid range
#     if start_datetime >= end_datetime:
#         print(f"Warning: Start date ('{start_date_str}') is not before end date ('{end_date_str}'). The range is empty.")
#         return 0

#     try:
#         # 2. Efficiently read the log file line by line
#         with open(filepath, 'r') as f:
#             for line in f:
#                 try:
#                     # 3. Extract the timestamp from the log entry.
#                     # Assuming format is [YYYY-MM-DD HH:MM:SS]...
#                     # The timestamp string is inside the square brackets.
#                     # Find the closing bracket ']'
#                     end_bracket_index = line.find(']')
#                     if line.startswith('[') and end_bracket_index != -1:
#                          # Extract the content within the brackets
#                         timestamp_str = line[1:end_bracket_index]

#                         # 4. Parse the timestamp into a datetime object
#                         log_datetime = datetime.datetime.strptime(timestamp_str, log_timestamp_format)

#                         # 5. Filter log entries based on the date range
#                         # (start_date inclusive, end_date exclusive)
#                         if start_datetime <= log_datetime < end_datetime:
#                             # 6. Count the total number of valid log entries
#                             count += 1
#                     else:
#                         # Skip lines that don't start with '[' or don't have a closing ']'
#                         continue

#                 except (ValueError, IndexError):
#                     # Handle lines that do not conform to the expected timestamp format
#                     # within the brackets or have other parsing issues. Skip these lines.
#                     continue
#     except FileNotFoundError:
#         print(f"Error: The file '{filepath}' was not found.")
#         return 0
#     except Exception as e:
#         print(f"An unexpected error occurred while reading the file: {e}")
#         return 0

#     # 7. Return the total count of valid log entries
#     return count

# # --- Example Usage ---

# # Create a dummy log file for demonstration
# log_content = """[2023-10-26 12:00:00] System started.
# [2023-10-27 08:00:00] User logged in.
# [2023-10-27 14:00:00] Critical error occurred.
# [2023-10-28 02:00:00] System backup initiated.
# [2023-10-28 18:00:00] User logged out.
# [2023-10-29 09:00:00] System shutdown.
# [2023-10-29 10:00:00] Another log entry on the end date.
# This line is invalid and will be skipped.
# [2023-10-30 00:00:00] Log entry after the end date.
# """
# file_name = "log_data.txt"

# # Clean up previous dummy file if it exists
# if os.path.exists(file_name):
#     os.remove(file_name)

# with open(file_name, "w") as f:
#     f.write(log_content)

# # Test case from the prompt
# start_date = "2023-10-27"
# end_date = "2023-10-29" # Exclusive

# # Expected entries:
# # [2023-10-27 08:00:00]
# # [2023-10-27 14:00:00]
# # [2023-10-28 02:00:00]
# # [2023-10-28 18:00:00]
# # Total expected count: 4

# count = analyze_log_file(file_name, start_date, end_date)
# print(f"Log entries between {start_date} and {end_date} (exclusive): {count}")

# # Additional Test Cases

# # Test 2: Range for a single day (exclusive end)
# start_date_2 = "2023-10-27"
# end_date_2 = "2023-10-28" # Exclusive
# # Expected entries:
# # [2023-10-27 08:00:00]
# # [2023-10-27 14:00:00]
# # Total expected count: 2
# count_2 = analyze_log_file(file_name, start_date_2, end_date_2)
# print(f"Log entries between {start_date_2} and {end_date_2} (exclusive): {count_2}")

# # Test 3: Range where start and end are the same day (exclusive end means 0)
# start_date_3 = "2023-10-27"
# end_date_3 = "2023-10-27" # Exclusive
# # Expected count: 0
# count_3 = analyze_log_file(file_name, start_date_3, end_date_3)
# print(f"Log entries between {start_date_3} and {end_date_3} (exclusive): {count_3}")

# # Test 4: Range with no matching entries
# start_date_4 = "2023-11-01"
# end_date_4 = "2023-11-05" # Exclusive
# # Expected count: 0
# count_4 = analyze_log_file(file_name, start_date_4, end_date_4)
# print(f"Log entries between {start_date_4} and {end_date_4} (exclusive): {count_4}")

# # Test 5: Invalid date format for input dates
# start_date_5 = "27-10-2023" # Incorrect format
# end_date_5 = "2023-10-29"
# # Expected: Error message and count 0
# count_5 = analyze_log_file(file_name, start_date_5, end_date_5)
# print(f"Log entries between {start_date_5} and {end_date_5} (exclusive): {count_5}")

# # Test 6: Non-existent file
# # Expected: Error message and count 0
# count_6 = analyze_log_file("non_existent_log.txt", "2023-10-27", "2023-10-29")
# print(f"Log entries from non-existent file: {count_6}")

# # Clean up the dummy file
# # os.remove(file_name) # Uncomment this line to remove the dummy file after testing

def for_fun():
    """
    This function is a placeholder for future functionality.
    It currently does nothing but serves as a template for future code.
    """
    for _ in range(1):
        poo = {'poo':12}
        poop = {'poo':12}
        print(f"Fun function is running... {poo == poop}")
    try:
        with open("./app/fun.json", "r") as f:
            data = json.load(f)
            prompt = data.get("prompt", "")
            if not prompt:
                raise ValueError("No 'prompt' key found in fun.json.")
    except Exception as e:
        print(f"Error loading prompt from fun.json: {e}")
        exit()
    else:
        print(f"LETS GOOOOO {prompt}")

for_fun()
CATEGORIES = {
    "HVAC": ["hvac", "h.v.a.c", "heating", "cooling", "air conditioning"],
    "Plumber": ["plumb", "pipefitter"],
    "Electrician": ["electric", "wiring", "electrical", "circuit"],
}

def preprocess_title(title):
    title = title.lower()
    title = re.sub(r'[^a-z\s]', '', title)
    return title

def normalize_title(title):
    cleaned = preprocess_title(title)
    for category, keywords in CATEGORIES.items():
        if any(keyword in cleaned for keyword in keywords):
            return category
    return "Other"
test_cases = [
    ("H.V.A.C Tech", "HVAC"),
    ("hvac technician", "HVAC"),
    ("Master Plumber", "Plumber"),
    ("Electrical Specialist", "Electrician"),
    ("solar installer", "Other")
]

for title, expected in test_cases:
    print(normalize_title(title) == expected)

response = requests.get("https://jsonplaceholder.typicode.com/users")
if response.status_code == 200:
    data = response.json()
    print("Data retrieved successfully:", json.dumps(data, indent=2))
else:
    print("Failed to retrieve data:", response.status_code)