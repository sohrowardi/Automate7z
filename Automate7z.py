import os
import subprocess
import shutil
import time

def zip_with_7z(item, password, script_dir, seven_zip_path):
    # Exclude files already in .7z format
    if item.endswith('.7z'):
        return
    
    # Exclude certain files from compression
    if item == 'compression.log':
        return
    
    # Create archive name relative to the script directory
    if os.path.isdir(item):
        archive_name = os.path.join(script_dir, item + '.7z')
    else:
        archive_name = os.path.join(script_dir, os.path.splitext(os.path.basename(item))[0] + '.7z')

    # Prepare command for compression
    command = [seven_zip_path, 'a', '-p{}'.format(password), '-mhe=on', '-mx=9', '-m0=LZMA2', '-mmt=on', archive_name, item]

    # Run compression command
    result = subprocess.run(command, capture_output=True, text=True)
    
    # Parse the output to find the archive size
    output_lines = result.stdout.split('\n')
    for line in output_lines:
        if line.startswith('Archive size:'):
            print(line)
            break
    else:
        print("Failed to retrieve archive size information.")

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
