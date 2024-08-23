# 2 Folders Synchronization
Python program that synchronizes two folders, source and replica, and maintain a full, identical copy of source folder at replica folder.

- This program works in Linux Bash and in Windows PowerShell.
- Synchronization is one-way: after the synchronization the content of the replica folder is modified to match the content of the main
folder.
- Synchronization is performed periodically.
- File creation/copying/removal operations are logged to a file and to the console output.
- Additionally, when a file in the main folder is updated, the changes made to it are also logged.
- Main and replica folder paths, synchronization interval and log file path must be provided as arguments like in the example below:
```bash
$ python3 sync_2_folders.py ./main_folder ./replica_folder 5  log.txt
```
