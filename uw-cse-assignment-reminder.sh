#!/bin/zsh
################################################################################

## -- Setup -- 

# 1. Update the variables in -- Configs -- below.

# 2. Navigate to that fodler/directory containing this file using 
# `cd [path to this folder]` in your terminal.

# 3. Run `chmod +x cse-assignment-fetch-script.sh` to make this file 
# executable. Optionally ensure it works properly by running
# `./cse-assignment-fetch-script.sh` while in the same directory.

# 4. Run `crontab -e` in the terminal to create the script. This will open up 
# vim and allow you to configure your automation. A cron job has the following 
# format:
#
# m h d M D command
#
# The variables correspond to
# m - minute (0-59, or * for every minute)
# h - hour (0-23, or * for every hour)
# d - day of the month (1-31, or * for every day)
# M - month (1-12, or * for every month)
# D - day of the week (0-6, 0 is Sunday, or * for every day of the week)
# and the command is the command to execute.
# 
# For example, to have the script run every day at 10 am and 4 pm, input:
# 0 10,16 * * * cd ~/[path to this folder] && ./cse-assignment-fetch-script.sh
#
# To ensure you have the desired configurations, see https://crontab.guru/.
#
# To input in vim, hit `i` to enter insert mode. When you are finished, hit 
# escape and type `:wq` (write quit) to save the file and quit. 
#
# To display the logs from when this script runs, include
# ` >> /full/path/to/logfile` at the end of your cron job line. i.e
# 0 10,16 * * * cd ~/[directory name] && ./cse-assignment-fetch-script.sh >> /full/path/to/logfile

# 5. You have created your script! As long as your mac is turned on at the set
# time, this will fetch your assignemnts in the background and update the
# logfile when it runs!

################################################################################

## -- Configs --

# Insert full path to your script
SCRIPT_PATH="/Users/me/created-scripts/cse_assignment_fetch_script.py"

# Insert path to python exectuable - run `which python` in your terminal 
# to find
PYTHON_PATH="/opt/anaconda3/bin/python"

# Set debug status
DEBUG=false

################################################################################

## -- Script --

# Optional - log message to check script is running
if [ "$DEBUG" = true ] ; then
    echo "Script $SCRIPT_PATH is running." 
fi

# Run the script
$PYTHON_PATH $SCRIPT_PATH

################################################################################
