# Test-Task
A program that synchronizes two folders: source and replica. The program should maintain a full, identical copy of source folder at replica folder.

to run the script:

python3 synchronize.py "Source_file" "Replica_file" "Logs_file".txt "time in seconds"

example for working in the folder the script is and with an interval of 10seconds synchronization: 

python3 synchronize.py Source Replica Logs.txt 10
