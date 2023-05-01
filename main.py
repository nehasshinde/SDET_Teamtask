# One-way Synchronization program to sync two folders: source_folder and replica_folder
# after every specific given time interval with logging functionality

import hashlib
import os
import shutil
import sys
import time


# Function to find the MD5 checksums of the contents of the file as a hexadecimal string
def get_file_checksum(file_path):
    with open(file_path, "rb") as f:
        file_data = f.read()
        return hashlib.md5(file_data).hexdigest()


# Function to start the sync process of two folders & log the logs in the log_file
def sync_folders(source_folder, replica_folder, log_file_path):

    # Checks if provided source_folder exists
    if not os.path.isdir(source_folder):
        print("Error: Source Folder not found")
        return
    else:
        # checks if provided replica_folder exists and creates it if not
        if not os.path.exists(replica_folder):
            os.makedirs(replica_folder)

        with open(log_file_path, "a") as log_file:
            print("Syncing started at", time.ctime(), file=log_file)
            # to check if any new directory/files are added and copy them to replica_folder
            for dir_path, dir_names, filenames in os.walk(source_folder):
                relative_path = os.path.relpath(dir_path, source_folder)
                replica_path = os.path.join(replica_folder, relative_path)
                os.makedirs(replica_path, exist_ok=True)
                for filename in filenames:
                    source_file_path = os.path.join(dir_path, filename)
                    replica_file_path = os.path.join(replica_path, filename)
                    if not os.path.exists(replica_file_path) or \
                            get_file_checksum(source_file_path) != get_file_checksum(replica_file_path):
                        shutil.copy2(source_file_path, replica_file_path)
                        print("Copied", source_file_path, "to", replica_file_path, file=log_file)
                for dir_name in dir_names:
                    source_dir_path = os.path.join(dir_path, dir_name)
                    replica_dir_path = os.path.join(replica_path, dir_name)
                    if not os.path.exists(replica_dir_path):
                        os.makedirs(replica_dir_path)
                        print("Created directory", replica_dir_path, file=log_file)

            # To check if any directory/files are deleted and remove them from replica_folder
            for dir_path, dir_names, filenames in os.walk(replica_folder, topdown=False):
                relative_path = os.path.relpath(dir_path, replica_folder)
                source_path = os.path.join(source_folder, relative_path)
                for dir_name in dir_names:
                    source_dir_path = os.path.join(source_path, dir_name)
                    replica_dir_path = os.path.join(dir_path, dir_name)
                    if not os.path.exists(source_dir_path):
                        shutil.rmtree(replica_dir_path)
                        print("Removed directory", replica_dir_path, file=log_file)
                for filename in filenames:
                    source_file_path = os.path.join(source_path, filename)
                    replica_file_path = os.path.join(dir_path, filename)
                    if not os.path.exists(source_file_path):
                        os.remove(replica_file_path)
                        print("Removed file", replica_file_path, file=log_file)
            print("Syncing finished at", time.ctime(), file=log_file)


def main():
    if len(sys.argv) != 5:
        print("Please provide source_folder replica_folder log_file_path sync_interval")
    else:
        source = sys.argv[1]
        replica = sys.argv[2]
        log_filepath = sys.argv[3]
        sync_interval = sys.argv[4]
        while True:
            sync_folders(source, replica, log_filepath)
            time.sleep(sync_interval)


if __name__ == '__main__':
    main()