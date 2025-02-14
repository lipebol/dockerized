#!/bin/bash

# Start the first process
./scheduler.sh &

# Start the second process
./webserver.sh &

# Wait for any process to exit
wait -n

# Exit with status of process that exited first
exit $?