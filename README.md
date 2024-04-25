# Automate7z

Automate7z is a Python script that automates the process of archiving files and folders using the 7z compression utility. It allows you to easily create password-protected and encrypted archives with just a few simple steps.

## Features

- **Automated Archiving**: Quickly compress files and folders into 7z archives with a single command.
- **Password Encryption**: Secure your archives by encrypting them with a password of your choice.
- **Multi-Volume Archives**: Automatically split large archives into multiple volumes for easier storage and transfer.
- **Customizable Settings**: Modify compression options and encryption settings to suit your preferences.

## Requirements

- Python 3.x
- 7-Zip (installed and added to system PATH)

## Usage

1. Clone or download the Automate7z repository to your local machine.
2. Open a terminal or command prompt.
3. Navigate to the directory containing the `ArchiveEverything.py` script.
4. Run the script by executing the following command:
```bash
python ArchiveEverything.py
```
5. Follow the on-screen prompts to enter the password for encryption.
6. Sit back and let Automate7z handle the archiving process for you!

## Notes

- Make sure to customize the `seven_zip_path` variable in the script to point to the location of the 7z executable on your system.
- By default, the script will create archives in the same directory as the Python script. Ensure that you have write permissions in that directory.

