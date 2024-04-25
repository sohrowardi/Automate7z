import os
import subprocess

def zip_with_7z(item, password, script_dir, seven_zip_path):
    # Create archive name relative to the script directory
    if os.path.isdir(item):
        archive_name = os.path.join(script_dir, item + '.7z')
    else:
        archive_name = os.path.join(script_dir, os.path.splitext(os.path.basename(item))[0] + '.7z')

    # Prepare command for compression
    command = [seven_zip_path, 'a', '-p{}'.format(password), '-mhe=on', '-mx=9', '-m0=LZMA2', '-mmt=on', '-v2000m', archive_name, item]

    # Run compression command
    subprocess.run(command)

def main():
    # Get password from user
    password = input("Enter password for encryption: ")

    # Get the directory where the Python script is located
    script_dir = os.path.dirname(os.path.abspath(__file__))

    # Specify the full path to 7z executable
    seven_zip_path = "C:/Program Files/7-Zip/7z.exe"  # Modify this path accordingly

    # List items in the current directory
    items = os.listdir(script_dir)

    # Process each item
    for item in items:
        # Exclude Python script from being zipped
        if item.endswith('.py'):
            continue
        print("Zipping", item)
        zip_with_7z(item, password, script_dir, seven_zip_path)

    # Zip all folders
    for item in items:
        if os.path.isdir(os.path.join(script_dir, item)):
            print("Zipping", item)
            zip_with_7z(os.path.join(script_dir, item), password, script_dir, seven_zip_path)

if __name__ == "__main__":
    main()
