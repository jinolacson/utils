"""
Author: leetz-kowd

This Python script is designed to check and activate battery conservation mode on Lenovo laptops.
It performs the following actions:
1. Checks the current value of the battery start charge threshold (START_CHARGE_THRESH_BAT0).
2. If the value is 0, it updates the threshold to 1 to activate battery conservation mode.
3. If the threshold is already set, it prints the current conservation mode status.
4. Finally, it displays the battery status.

The script uses the 'subprocess' module to run shell commands and capture their output.
Ensure you have the necessary permissions to execute the required 'sudo' commands.

Steps:
1. Execute a command to retrieve the current START_CHARGE_THRESH_BAT0 value.
2. Check if the current value is 0 and update it to 1 if necessary.
3. Print the specific line showing the conservation mode status if it's already set.
4. Display the overall battery status using 'tlp-stat -b'.

"""

import subprocess

def execute_command(command):
    process = subprocess.Popen(command, stdout=subprocess.PIPE, shell=True)
    output, error = process.communicate()
    if error:
        print(f"Error: {error}")
    return output.decode("utf-8").strip()

# Get the current value of START_CHARGE_THRESH_BAT0
current_value = execute_command("sudo tlp-stat -b | grep 'START_CHARGE_THRESH_BAT0' | awk '{print $3}'")

# Check if the current value is 0
if current_value == "0":
    # Update START_CHARGE_THRESH_BAT0 to 1
    execute_command("sudo tlp setcharge START_CHARGE_THRESH_BAT0 1")
    print("Battery conservation mode is now activated (START_CHARGE_THRESH_BAT0 set to 1).")
else:
    # If already set, print the specific line
    output = execute_command("sudo tlp-stat -b | grep 'conservation_mode' | awk '{print $1, $3, $4}'")
    print(output)
    
# Display battery status
output = execute_command("sudo tlp-stat -b")
print(output)
