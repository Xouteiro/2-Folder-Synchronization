import argparse
import os
import platform
import time

parser = argparse.ArgumentParser(description='Sync two folders.')
parser.add_argument('main_folder_path', type=str, help='Path to the main folder')
parser.add_argument('replica_folder_path', type=str, help='Path to the backup folder')
parser.add_argument('interval', type=int, help='Interval in seconds')
parser.add_argument('log_file', type=str, help='Path to the log file')
args = parser.parse_args()

if platform.system() == 'Windows':
    copy_command = 'copy'
    mkdir_command = 'mkdir'
    double_quotes = '"'
    suppress_command = '>NUL'
else:
    copy_command = 'cp'
    mkdir_command = 'mkdir'
    double_quotes = ''
    suppress_command = ''

def write_report(text,log_file):
    print(text)
    with open(log_file, 'a') as f:
        f.write(text + '\n')

def remove_deleted_files(folder_path, replica_folder_path, log_file):
    replica_folder_content = os.listdir(replica_folder_path)
    for item in replica_folder_content:
        item_path = os.path.join(folder_path, item)
        replica_item_path = os.path.join(replica_folder_path, item)
        if not os.path.exists(item_path):
            if os.path.isfile(replica_item_path):
                os.remove(replica_item_path)
                write_report(f'File {item} deleted from {replica_folder_path}\n', log_file)

            elif os.path.isdir(replica_item_path):
                remove_deleted_files(item_path, replica_item_path, log_file)
                os.rmdir(replica_item_path)
                write_report(f'Directory {item} deleted from {replica_folder_path}\n', log_file)

        elif os.path.isdir(item_path):
            remove_deleted_files(item_path, replica_item_path, log_file)

def get_changes_report(main_content, replica_content, item, log_file):
    if main_content != replica_content:
        write_report(f'Changes detected in file {item}:', log_file)
        main_lines = main_content.splitlines()
        replica_lines = replica_content.splitlines()
        max_lines = max(len(main_lines), len(replica_lines))
        write_report(f'Line: Main | Replica', log_file)
        
        for i in range(max_lines):
            main_line = main_lines[i] if i < len(main_lines) else ''
            replica_line = replica_lines[i] if i < len(replica_lines) else ''

            if main_line != replica_line:
                write_report(f'{i+1}: {main_line} | {replica_line}', log_file)


def synchronize_folders(folder_path, replica_folder_path, log_file):
    folder_content = os.listdir(folder_path)
    for item in folder_content:
        item_path = os.path.join(folder_path, item)

        if os.path.isfile(item_path):
            replica_item_path = os.path.join(replica_folder_path, item)

            if not os.path.exists(replica_item_path):
                os.system(f'{copy_command} {double_quotes}{item_path}{double_quotes} {double_quotes}{replica_item_path}{double_quotes} {suppress_command}')
                write_report(f'File {item} copied to {replica_folder_path}\n', log_file)

            else:
                main_item_time = os.path.getmtime(item_path)
                replica_item_time = os.path.getmtime(replica_item_path)

                if main_item_time > replica_item_time:
                    with open(item_path, 'r') as main_file, open(replica_item_path, 'r') as replica_file:
                        main_content = main_file.read()
                        replica_content = replica_file.read()
                        get_changes_report(main_content, replica_content, item, log_file)
                    os.system(f'{copy_command} {double_quotes}{item_path}{double_quotes} {double_quotes}{replica_item_path}{double_quotes} {suppress_command}')
                    write_report(f'File {item} updated in {replica_folder_path}\n', log_file)
                    

        elif os.path.isdir(item_path):
            replica_item_path = os.path.join(replica_folder_path, item)

            if not os.path.exists(replica_item_path):
                os.system(f'{mkdir_command} {double_quotes}{replica_item_path}{double_quotes}')
                write_report(f'Directory {item} created in {replica_folder_path}\n', log_file)
            synchronize_folders(item_path, replica_item_path, log_file) 
            
    remove_deleted_files(folder_path, replica_folder_path, log_file)




while True:

    print(f'Synchronizing {args.main_folder_path} with {args.replica_folder_path}...\n')
        
    synchronize_folders(args.main_folder_path, args.replica_folder_path, args.log_file)

    print(f'Synchronizing done. Next syncronization in {args.interval} seconds.\n')

    time.sleep(args.interval)