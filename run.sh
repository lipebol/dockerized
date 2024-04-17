#!/bin/bash

# Start the first process
./start_scheduler.sh &

# Start the second process
./start_webserver.sh &

# Wait for any process to exit
wait -n

# Exit with status of process that exited first
exit $?