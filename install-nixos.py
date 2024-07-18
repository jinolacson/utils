"""
Author: leetz-kowd

This Python script performs the following actions:
1. Checks the location of the 'nix' command.
2. Appends Nix initialization script to the user's '.bashrc' file.
3. Reloads the shell configuration by sourcing '.bashrc'.
4. Checks the installed version of 'nix'.
5. Runs 'nix-shell' to install 'cowsay' and 'lolcat'.

The script uses the 'subprocess' module to run shell commands and captures their output. 
Ensure you have the necessary permissions to modify the '.bashrc' file and execute 'nix' commands.

Steps:
1. Find the location of the 'nix' command using a bash shell with no initialization files.
2. Edit the '.bashrc' file to include Nix initialization if it's not already present.
3. Reload the shell configuration by sourcing '.bashrc'.
4. Verify the Nix installation by checking its version.
5. Use 'nix-shell' to install the 'cowsay' and 'lolcat' packages.

"""

import subprocess
import os

# Function to run a shell command and capture the output
def run_command(command):
    result = subprocess.run(command, shell=True, text=True, capture_output=True)
    return result.stdout.strip(), result.stderr.strip()

# Check the location of 'nix'
stdout, stderr = run_command("bash --norc --noprofile -c 'source /etc/bashrc; which nix'")
if stderr:
    print(f"Error finding nix: {stderr}")
else:
    print(f"nix found at: {stdout}")

# Edit the .bashrc file to add nix initialization
bashrc_path = f"{os.path.expanduser('~')}/.bashrc"
nix_init = """
if [ -e /nix/var/nix/profiles/default/etc/profile.d/nix-daemon.sh ]; then
    . /nix/var/nix/profiles/default/etc/profile.d/nix-daemon.sh
fi
"""

try:
    with open(bashrc_path, 'a') as bashrc:
        bashrc.write(nix_init)
    print(f"Added nix initialization to {bashrc_path}")
except IOError as e:
    print(f"Error editing .bashrc: {e}")

# Reload the shell configuration
run_command("source ~/.bashrc")

# Check nix version
stdout, stderr = run_command("nix --version")
if stderr:
    print(f"Error checking nix version: {stderr}")
else:
    print(f"nix version: {stdout}")

# Run nix-shell to install cowsay and lolcat
stdout, stderr = run_command("nix-shell -p cowsay lolcat")
if stderr:
    print(f"Error running nix-shell: {stderr}")
else:
    print(f"nix-shell output: {stdout}")

# Activate nix-shell environment and run commands within it
nix_shell_command = """
nix-shell -p cowsay lolcat --run 'cowsay "Hello, world!" | lolcat'
"""

stdout, stderr = run_command(nix_shell_command)
if stderr:
    print(f"Error running nix-shell environment: {stderr}")
else:
    print(f"nix-shell environment output:\n{stdout}")
