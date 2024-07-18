#!/bin/bash

# Description:
# This script monitors memory usage on a Linux system and allows the user to kill processes that are consuming too much memory.
# It displays the total memory usage and remaining memory, as well as the top processes by memory usage (USER, PID, %MEM).
# The user can choose to kill a process by entering its process ID.

# Author:
# leetz-kowd

# Reason for Development:
# This script was developed to help system administrators and users monitor memory usage on their Linux systems and quickly identify and kill processes that are consuming too much memory.

print_memory_usage() {
  echo "==================================== Current Memory Usage ===================================="
  echo "Total memory usage and remaining memory:"
  free -h | grep Mem | awk '{print "Total: " $2, "Used: " $3, "Free: " $4, "Shared: " $5, "Buff/Cache: " $6, "Available: " $7}'
  echo "=============================================================================================="
  echo "Top processes by memory usage (USER, PID, %MEM):"
  ps aux --sort=-%mem | awk '{print $1, $2, $4}' | head -n 11
}

kill_process_by_id() {
  pid=$1
  kill $pid
  echo "Process with ID $pid has been killed."
}

while true; do
  print_memory_usage
  read -p "Do you want to kill a process? (yes/no): " user_input
  if [ "${user_input,,}" == "yes" ]; then
    read -p "Enter the process ID: " pid
    kill_process_by_id $pid
  elif [ "${user_input,,}" == "no" ]; then
    break
  else
    echo "Invalid input. Please enter 'yes' or 'no'."
  fi
done
