#!/bin/bash

input_dir="audio"
output_file="output.mp3"
file_list="file_list.txt"

# Check if input directory exists
if [ ! -d "$input_dir" ]; then
    echo "Input directory does not exist."
    exit 1
fi

# Create a file list
rm -f "$file_list"  # Remove the file list if it already exists
for file in "$input_dir"/*.mp3; do
    if [ -f "$file" ]; then  # Check if file exists
        echo "file '$file'" >> "$file_list"
    else
        echo "File $file does not exist."
        exit 1
    fi
done

# Check if file list is created
if [ ! -f "$file_list" ]; then
    echo "File list $file_list does not exist."
    exit 1
fi

# Combine the files using ffmpeg
ffmpeg -f concat -safe 0 -i "$file_list" -c copy "$output_file"

# Check if ffmpeg succeeded
if [ $? -ne 0 ]; then
    echo "ffmpeg failed to combine the audio files."
    exit 1
fi

# Clean up the file list
rm "$file_list"

echo "Combined audio files into $output_file"
