# -*- coding: utf-8 -*-
################################################################################
# CSE Assignment Fetcher
################################################################################

## Imports - Ensure all modules are downloaded locally

import requests                  # For fetching HTML
from bs4 import BeautifulSoup    # For parsing HTML  
import subprocess                # For creating reminders
import datetime as dt            # For date handling
import os                        # For file path handling
import json                      # For parsing json

################################################################################

## -- Setup --

# 1. Ensure all files in this repository are contained in a folder titled
# uw-cse-assignment-reminder.

# 2. See the settings in -- Configs -- below. This file is currently setup to
# get reminders for cse 333 25su. Due to the variable nature of course sites,
# this file is currently only setup to handle one course at a time. To handle
# multiple courses, duplicating the file works. If you have multiple courses
# with the same assignment page structure, see the directions in the README
# section `3. Multiple Courses` to configure this.

# 3. Next, update the other -- Configs -- below. The other configs just set
# things like reminder times and course end dates.

# 4. Before continuing, see the NOTE in the code below (on line TODO).
# Some course websites might have different HTML tags surrounding assignments.
# Once this is handled, set DEBUG=false to fully run the script.

# 5. This file will work when ran on its own, but follow instructions in 
# cse-assignment-fetch-script.sh if you want to automate the reminders.

################################################################################

## -- Configs --

# Debug flag
DEBUG = True

# Link to course assignment list page
COURSE_URL = "https://courses.cs.washington.edu/courses/cse333/25su/calendar/hwlist.html"

# Filename of the .JSON file to handle seen assignments
JSON_FNAME = "cse333-seen.json"
script_dir = os.path.dirname(os.path.abspath(__file__))
JSON_PATH = os.path.join(script_dir, JSON_FNAME)

# Date to stop script - set to course end
STOP_DATE = dt.date(2025, 8, 22)

# Current date (no need to make reminders for old tasks)
CURR_DATE = dt.datetime.now().date()

# Time for reminder to show up on phone (HH:MM (12 hour format))
R_TIME = "08:00 AM"

# How many days before due date should the reminder show up
DAY_DELTA = 1

################################################################################

## -- Script --

# First log time
print('Fetching assignments -', end=' ')
print(f'{dt.datetime.now().today().date()}', end=' ')
print(f'{dt.datetime.now().time().strftime("%H:%M:%S %p")}')

# First check if past STOP_DATE and set reminder to end the script
if (not DEBUG) and (CURR_DATE > STOP_DATE):
  # Get time to secnd reminder
  curr_time = dt.datetime.now().time()
  r_time = (curr_time + dt.timedelta(hours=1)).strftime("%H:%M %p")

  # Create the script
  applescript = f'tell application "Reminders"\n'
  applescript += f'    set newReminder to make new reminder\n'
  applescript += f'    set name of newReminder to "terminate script"\n'
  applescript += f'    set due date of newReminder to date "{CURR_DATE} {r_time}"\n'
  applescript += f'    save\n'
  applescript += f'end tell'

  # Run the script
  try:
      subprocess.run(['osascript', '-e', applescript], check=True)
      print(f"Reminder 'terminate script' created successfully.")
  except subprocess.CalledProcessError as e:
      print(f"Error creating reminder: {e}")

# Open JSON file and get list of seen assignments
with open(JSON_PATH, 'r') as f:
    data = json.load(f)

# Fetch website html
try:
  r = requests.get(COURSE_URL)
  r.raise_for_status()
except requests.exceptions.HTTPError as errh:
    print(f"HTTP error occurred: {errh}")
except requests.exceptions.ConnectionError as errc:
    print(f"Connection error occurred: {errc}")
except requests.exceptions.Timeout as errt:
    print(f"Timeout error occurred: {errt}")
except requests.exceptions.RequestException as err:
  print(f"Some other error occurred: {err}")

###############################################################################
## NOTE: The following code may need to be changed based on the course
# webpage being used. Lines marked with # Here should be checked before using
# the script to prevent unwated behavior. To update them, run the lines of code
# up to the first # HERE with DEBUG set to True and make sure it is locating 
# the correct HTML elements. If it is not, see (TODO)
# in the README for instructions to fix this.
# try running 
# print(soup.prettify())
# and locate the html tags surrounding the elements containing
# The below format works with the
# cse 333 25su page listed in -- Configs --.

# Initialize a beautiful soup parser and locate assignment table
soup = BeautifulSoup(r.text, 'html.parser')
# print(soup.prettify())
rows = soup.find('table', {'class': 'listtable'}).find_all('tr')         # HERE
print(rows[1].find('td').contents)

# Iterate through rows to add to seen
# Keep track of if we find new assignments
found = 0
for row in rows:
  cell = row.find('td')                                                  # HERE

  # Ensure we find something
  if cell == None:
    continue

  # Format dates
  date = cell.contents[0] + ", 2025"
  date = dt.datetime.strptime(date, "%B %d, %Y").date()                  # HERE

  # Check if assignment is relevant
  if date < CURR_DATE:
    continue

  # Get the assignment and add to seen
  assignment = cell.contents[1].find('span').text

  # Ensure we dont create duplicate reminders
  if assignment in data['seen']:
    continue

  # Found a new reminder
  found += 1

  # Set reminder date
  r_date = (date + dt.timedelta(days=-1*DAY_DELTA)).strftime("%m/%d/%Y")

  if not DEBUG:
    # Create the script
    applescript = f'tell application "Reminders"\n'
    applescript += f'    set newReminder to make new reminder\n'
    applescript += f'    set name of newReminder to "{assignment}"\n'
    applescript += f'    set due date of newReminder to date "{r_date} {R_TIME} AM"\n'
    applescript += f'    save\n'
    applescript += f'end tell'

    # Run the script
    try:
        subprocess.run(['osascript', '-e', applescript], check=True)
        print(f"Reminder '{assignment}' created successfully.")

        # Only write to seen JSON file if sucessfully ran
        data['seen'].append(assignment)
        with open(JSON_PATH, 'w') as f:
          json.dump(data, f)
    except subprocess.CalledProcessError as e:
        print(f"Error creating reminder: {e}")

# Print status
print(f'Created reminders for {found} new assignments')

################################################################################
