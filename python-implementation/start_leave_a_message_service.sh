#!/bin/bash
script_dir="$(dirname "$(readlink -f "$0")")"
# Specify the file to which you want to redirect the output
output_file="/$script_dir/output.log"

# Redirect stdout and stderr to the specified file
exec &>> "$output_file"

cd "$script_dir"
python3 leave-a-message.py 
