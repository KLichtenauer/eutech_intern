@echo off

set TASK_NAME=File_Backup
set COMMAND="C:\Users\Kilian\Documents\eutech_intern\task1\backup_script.py"

rem Set the schedule for the task (change values as needed)
set SCHEDULE=DAILY
set START_TIME=17:45

rem Create the scheduled task
schtasks /create /tn "%TASK_NAME%" /tr "%COMMAND%" /sc %SCHEDULE% /st %START_TIME% /f

rem Confirm the task creation
if %errorlevel% equ 0 (
    echo Task created successfully.
) else (
    echo Task creation failed.
)