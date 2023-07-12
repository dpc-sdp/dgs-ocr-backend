#!/bin/bash

API_ENDPOINT="http://localhost:5001/analyze-doc?sample_doc=true"    # Replace with your API endpoint
FOLDER_PATH="/Users/manoj/Downloads/OneDrive_1_30-05-2023"                        # Replace with the path to your folder
LOG_FILE="upload_log_$(date +%Y%m%d%H%M%S).txt"                     # Replace with the desired log file name

# Function to format the time in minutes and seconds
format_time() {
  local time_seconds=$1
  local minutes=$((time_seconds / 60))
  local seconds=$((time_seconds % 60))
  printf "%02d min %02d sec" "$minutes" "$seconds"
}

# Function to upload a document to the API
upload_document() {
  local file_path="$1"
  local file_name=$(basename "$file_path")
  
  echo "Uploading $file_name ..."
  
  # Call the API endpoint and measure the time taken
  start_time=$(date +%s.%N)
  response_code=$(curl -s -o /dev/null -w "%{http_code}" -F "doc=@$file_path" "$API_ENDPOINT")
  end_time=$(date +%s.%N)
  
  # Calculate the time taken for the response
  time_taken=$(awk "BEGIN {print $end_time - $start_time}")  
  # Format the time taken
  formatted_time=$(format_time "${time_taken%.*}")

  # Write the log entry to the log file
  echo "[$(date '+%Y-%m-%d %H:%M:%S')] - Response code: $response_code - Time taken: $formatted_time - Filename: $file_name " >> "$LOG_FILE"
}

# Iterate over the files in the folder
for file in "$FOLDER_PATH"/*; do
  if [ -f "$file" ]; then
    upload_document "$file"
  fi
done
