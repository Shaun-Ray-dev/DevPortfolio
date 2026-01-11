#!/bin/bash
PROCESS_NAME="notepad.exe"

if tasklist.exe | grep -i "$PROCESS_NAME" > /dev/null; then
    echo "$PROCESS_NAME is running."
else
    echo "$PROCESS_NAME is NOT running!"
    read -p "Do you want to start $PROCESS_NAME? (Y/N) " response
    if [[ "$response" =~ ^[Yy]$ ]]; then
        echo "Starting $PROCESS_NAME..."
        powershell.exe -Command "Start-Process notepad.exe"
        echo "$PROCESS_NAME started."
    else
        echo "$PROCESS_NAME was not started."
    fi
fi



