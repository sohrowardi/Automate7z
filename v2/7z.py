import os
import shutil
import subprocess
import time
from tqdm import tqdm
import getpass
import logging

def get_folder_size(folder):
    """Calculate the total size of the folder."""
    total_size = 0
    for dirpath, dirnames, filenames in os.walk(folder):
        for f in filenames:
            fp = os.path.join(dirpath, f)
            total_size += os.path.getsize(fp)
    return total_size

def compress_item(item_path, password, delete_originals, seven_zip_path, output_dir, split_size):
    """Compress a file or folder using 7-Zip."""
    item_name = os.path.basename(item_path)
    compressed_name = os.path.join(output_dir, f"{item_name}.7z")
    
    if item_name.endswith(".7z"):
        logging.info(f"Skipping already compressed file: {item_name}")
        return

    item_size = get_folder_size(item_path) if os.path.isdir(item_path) else os.path.getsize(item_path)
    
    logging.info(f"Compressing {item_name} ({item_size / (1024**3):.2f} GB)")

    cmd = [seven_zip_path, 'a', '-t7z', '-mhe=on', f'-p{password}', compressed_name, item_path]

    if item_size > split_size:
        cmd += [f'-v{split_size}b']

    with tqdm(total=item_size, unit='B', unit_scale=True, desc=compressed_name, dynamic_ncols=True) as pbar:
        with subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, universal_newlines=True) as process:
            for line in process.stdout:
                pbar.update(len(line))

    if process.wait() == 0:
        logging.info(f"Compression of {item_name} completed.")
        if delete_originals:
            time.sleep(2)  # wait for a moment before deleting the original files
            if os.path.isdir(item_path):
                shutil.rmtree(item_path)
            else:
                os.remove(item_path)
            logging.info(f"Deleted original {item_name}.")
    else:
        logging.error(f"Compression of {item_name} failed.")

def main():
    """Main function to handle user inputs and initiate the compression process."""
    logging.basicConfig(filename='compression.log', level=logging.INFO,
                        format='%(asctime)s - %(levelname)s - %(message)s')
    try:
        password = getpass.getpass("Enter password for encryption: ")
        script_dir = os.path.dirname(os.path.realpath(__file__))
        
        seven_zip_path = input("Enter the path to 7-Zip executable (default is C:\\Program Files\\7-Zip\\7z.exe): ") or "C:\\Program Files\\7-Zip\\7z.exe"
        if not os.path.exists(seven_zip_path):
            raise FileNotFoundError(f"7-Zip executable not found at {seven_zip_path}")
        
        output_dir = input("Enter the output directory (leave empty for current directory): ") or script_dir
        if not os.path.exists(output_dir):
            raise FileNotFoundError(f"Output directory not found at {output_dir}")
        
        split_size = input("Enter split size in bytes (default 2GB): ")
        split_size = int(split_size) if split_size else 2 * 1024**3
        
        items = os.listdir(script_dir)
        delete_originals = input("Delete originals after compression? (y/n): ").lower() == 'y'

        for item in items:
            item_path = os.path.join(script_dir, item)
            if item_path == __file__:
                continue
            compress_item(item_path, password, delete_originals, seven_zip_path, output_dir, split_size)

        logging.info("Compression done.")
        print("Compression done. Press any key to exit.")
        input()

    except Exception as e:
        logging.error(f"An error occurred: {e}")
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    main()
