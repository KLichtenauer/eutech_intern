import os
import logging
from datetime import datetime
import shutil

# Get the directory where the script is located
script_directory = os.path.dirname(os.path.abspath(__file__))

# Logging setup
logging.basicConfig(filename='logfile.txt', level=logging.INFO,
                    filemode='w', format='%(asctime)s - %(levelname)s - %(message)s')

logging.info("Script started.")

LINE_FOR_FOLDER_OF_BACKUP = 1
LINE_FOR_NUMBERS_OF_BACKUP = 4
LINE_FOR_BACKUPSTART = 7

# Path to the config file.
config_file_path = os.path.join(script_directory, "config.txt")
# Content of the config file.
config_file = []

# Path to the folder where the backups should be saved.
backup_folder_path = ""
max_number_of_backups = ""

# Load and process the config file
with open(config_file_path) as fp:
    config_file = fp.readlines()

# Remove newline characters from each line
config_file = [line.strip() for line in config_file]

# Display the loaded config lines
for lines in config_file:
    print(lines)

# Extract necessary information from the config file
config_file_path = os.path.join(script_directory, "config.txt")
backup_folder_path = os.path.join(script_directory, config_file[LINE_FOR_FOLDER_OF_BACKUP].strip())
logging.info("The path to the backup folder is: " + backup_folder_path)

max_number_of_backups = config_file[LINE_FOR_NUMBERS_OF_BACKUP].strip()
logging.info(f"The max number of backups is: {max_number_of_backups}")

# Backup files or directories based on the config file.
def backupFiles():
    new_backup_folder_path = createNewBackupFolder()
    for x in range(LINE_FOR_BACKUPSTART, len(config_file)):
        source_file_path = config_file[x].strip()
        logging.info("Backup number {}: {}".format(x, source_file_path))
        print("Source filepath" + source_file_path)
        print("Destination path: " + new_backup_folder_path)
        if os.path.isfile(source_file_path):
            shutil.copy(source_file_path, new_backup_folder_path)
        elif os.path.isdir(source_file_path):
            path_to_folder = os.path.join(new_backup_folder_path, os.path.basename(source_file_path))
            shutil.copytree(source_file_path, path_to_folder)
        else:
            print(f"Source '{source_file_path}' is neither a file nor a folder.")
            logging.error("Given path is not a file or folder")

#Create a new backup folder with a timestamp.
def createNewBackupFolder():
    current_num_of_backups = str(len(os.listdir(backup_folder_path)))
    print(current_num_of_backups)
    logging.info(f"The current number of backups is: {current_num_of_backups}")
    
    if current_num_of_backups == max_number_of_backups:
        deleteOldestBackup()

    current_date = datetime.now().strftime("%Y-%m-%d_%H-%M")
    folder_name = f"backup_{current_date}"
    new_folder_path = os.path.join(backup_folder_path, folder_name)
    os.mkdir(new_folder_path)
    return new_folder_path

#Delete the oldest backup folder if the max number is reached.
def deleteOldestBackup():
    existing_backups = os.listdir(backup_folder_path)

    oldestDate = None
    oldestFolder = None
    for folder in existing_backups: 
        folder_date_str = folder.split('_')[1]
        folder_date_str = folder_date_str + "_" + folder.split('_')[2]
        folder_date = datetime.strptime(folder_date_str, "%Y-%m-%d_%H-%M")

        if oldestDate is None or folder_date < oldestDate:
            oldestDate = folder_date
            oldestFolder = folder
    shutil.rmtree(os.path.join(backup_folder_path, oldestFolder))
    logging.info(f"Oldest backup folder '{oldestFolder}' deleted.")

# Call the backupFiles function to initiate the backup process
backupFiles()
