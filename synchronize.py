import os
import shutil
import time
import argparse


    
def synchronize_folders(source_folder, replica_folder, Log_path):
    # Check if source folder path is correct
    if not os.path.exists(source_folder):
        print(f"Source folder '{source_folder}' does not exist.")
        return

    # See all files from the source folder
    for root, dirs, files in os.walk(source_folder):
        
        # Get relative path from source folder to do the same in the replicate folder
        relative_path = os.path.relpath(root, source_folder)
        
        # Create the new path for the copied files
        replica_path = os.path.join(replica_folder, relative_path)
        
        # Create replica folder if it doesn't exist
        if not os.path.exists(replica_path):
            os.makedirs(replica_path)

        # Copy files from source to replica
        for file in files:
            source_file_path = os.path.join(root, file)
            replica_file_path = os.path.normpath(os.path.join(replica_path, file))
            #Copy if the file doesn't exist in replica or if it's different,
            #here i saw the diference with the time the file was created or modified
            #it is not the best approach, but it is more eficient than comparing files
            #this system can be hacked if someone wants to. by manualy modifing the date.
            #but using MD5 even though it is harder, it is doable in the same way too.
            #SHA-256 could be easily used here(hashlib), but without more information
            #i am going with performance rather than security
            if not os.path.exists(replica_file_path):
                shutil.copy2(source_file_path, replica_file_path)
                description = f"Copied: {source_file_path} -> {replica_file_path}"
                print(description)
                Log(description, Log_path)

                
            if os.path.getmtime(source_file_path) != os.path.getmtime(replica_file_path):
                shutil.copy2(source_file_path, replica_file_path)
                description = f"Updated: {source_file_path} -> {replica_file_path}"
                print(description)
                Log(description, Log_path)

        #Delete files that exist in replica but are no longer in source
        for root, dirs, files in os.walk(replica_folder):
            for file in files:
                replica_file_path = os.path.join(root, file)
                source_file_path = os.path.join(source_folder, os.path.relpath(replica_file_path, replica_folder))
                if not os.path.exists(source_file_path):
                    os.remove(replica_file_path)
                    description = f"Removed: {replica_file_path}"
                    #we can add the time this modification happened to be also saved
                    print(description)
                    Log(description, Log_path)
        
    print("Synchronization complete.")


def Log(description, Log_path):
    if not os.path.exists(Log_path):
        open("Logs.txt", "a").close()

    with open("Logs.txt", "a+") as f:
        f.write(description + "\n")


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("source_folder", help="Path to the source folder")
    parser.add_argument("replica_folder", help="Path to the replica folder")
    parser.add_argument("log_path", help="Path to the log file")
    #here we can multiply for 60 and ask the user to chose the interval in minutes or hours
    #probably makes more sense than seconds
    parser.add_argument("interval", type=int, default=10, help="Interval in seconds for synchronization (default: 10)")
    return parser.parse_args()
    
def main():
    # cd C:\Users\marce\OneDrive\Ambiente de Trabalho\project 
    # python3 synchronize.py Source Replica Logs.txt 10
    args = parse_args()

    source_folder = args.source_folder
    replica_folder = args.replica_folder
    Log_path = args.log_path
    interval = args.interval


    try:
        while True:
            synchronize_folders(source_folder, replica_folder, Log_path)
            time.sleep(interval)
            
    except KeyboardInterrupt:
        print("Script terminated by user.")


if __name__ == "__main__":
    main()
