import os
import subprocess
import shutil
import time

def get_total_size(directory):
    total = 0
    for path, dirs, files in os.walk(directory):
        for f in files:
            fp = os.path.join(path, f)
            total += os.path.getsize(fp)
    return total

def zip_with_7z(item, password, script_dir, seven_zip_path):
    # Exclude files already in .7z format
    if item.endswith('.7z'):
        return
    
    # Create archive name relative to the script directory
    if os.path.isdir(item):
        archive_name = os.path.join(script_dir, item + '.7z')
        # Get total size of directory
        total_size = get_total_size(item)
    else:
        archive_name = os.path.join(script_dir, os.path.splitext(os.path.basename(item))[0] + '.7z')
        # Get size of file
        total_size = os.path.getsize(item)

    # Properly quote paths to handle spaces and special characters
    item_quoted = f'"{item}"'
    archive_name_quoted = f'"{archive_name}"'
    password_quoted = f'"{password}"'

    # Check file/folder size and add volume splitting option if size exceeds 2GB
    if total_size > 2 * 1024 * 1024 * 1024:  # 2GB in bytes
        archive_name_quoted = f'"{archive_name[:-3]}"'  # Remove .7z extension
        command = [
            seven_zip_path,
            'a',
            '-bsp1',
            f'-p{password_quoted}',
            '-mhe=on',
            '-mx=0',
            '-m0=Copy',
            '-mmt=on',
            '-v2000M',  # Add volume splitting option (2000M per volume)
            archive_name_quoted,
            item_quoted
        ]
    else:
        command = [
            seven_zip_path,
            'a',
            '-bsp1',
            f'-p{password_quoted}',
            '-mhe=on',
            '-mx=0',
            '-m0=Copy',
            '-mmt=on',
            archive_name_quoted,
            item_quoted
        ]

    # Run compression command and capture output
    process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, universal_newlines=True)
    
    while True:
        output = process.stdout.readline()
        if not output and process.poll() is not None:
            break
        if output:
            if "%" in output:  # Only print the line containing the progress percentage
                print(output.strip(), end='\r')  # Print each line of output on the same line
                time.sleep(0.1)  # Add a small delay to make the progress bar visible

    print("\nCompression completed for:", item)


def main():
    # Get password from user
    password = input("Enter password for encryption: ")

    # Get the directory where the Python script is located
    script_dir = os.path.dirname(os.path.abspath(__file__))

    # Specify the full path to 7z executable
    seven_zip_path = "C:/Program Files/7-Zip/7z.exe"  # Modify this path accordingly

    # List items in the current directory
    items = os.listdir(script_dir)

    # Ask user if they want to delete the original files after archiving
    delete_files = input("Do you want to delete the original files after archiving? (yes/no): ").lower()

    # Process each item
    for item in items:
        # Exclude Python script from being zipped
        if item.endswith('.py'):
            continue
        print("Zipping", item)
        zip_with_7z(item, password, script_dir, seven_zip_path)
        
        # Delete original files if user chooses to do so
        if delete_files == 'yes' or delete_files == 'y':
            time.sleep(1)  # Add a delay before deletion to ensure all processes are completed
            
            item_path = os.path.join(script_dir, item)
            if os.path.isdir(item_path):
                shutil.rmtree(item_path)  # Recursively delete directories
            else:
                os.remove(item_path)  # Delete individual files
            
            print("Deleted original file:", item)

    print("Compression completed successfully.")

if __name__ == "__main__":
    main()

    # Add this line to wait for user input before exiting
    input("Press any key to exit...")
