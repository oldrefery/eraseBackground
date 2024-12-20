#!/bin/bash

# Check if parameter is passed
if [ $# -lt 1 ]; then
    echo "Error: No video file name specified"
    echo "How to use: ./run.sh videofile_name.ext [frames_from_one_sec]"
    exit 1
fi

# Get video file name from parameter
VIDEO_FILE="$1"

# Get frames per second (default: 1)
FRAMES_FROM_ONE_SEC=${2:-1}
echo "Frames from 1 sec of video is: $FRAMES_FROM_ONE_SEC"

# Check if input directory exists
if [ ! -d "data/input" ]; then
    echo "Error: The data/input directory doesn't exist"
    echo "Create the data/input directory in the project folder"
    exit 1
fi

# Check if video file exists
if [ ! -f "data/input/$VIDEO_FILE" ]; then
    echo "Error: File $VIDEO_FILE not found in directory data/input"
    echo "Put the video file in the data/input directory and try again"
    exit 1
fi

# Create output directory if it does not exist
mkdir -p data/output

# Define image name
IMAGE_NAME="erase-background:latest"

# Building Docker image
echo "Building the Docker image..."
if ! docker build -t $IMAGE_NAME .; then
    echo "Error: Failed to build Docker image"
    exit 1
fi

# Running container
echo "Starting video processing..."
if ! docker run --rm -it \
    -v "$(pwd)/data/input:/app/data/input" \
    -v "$(pwd)/data/output:/app/data/output" \
    $IMAGE_NAME \
    --input_video "/app/data/input/$VIDEO_FILE" \
    --output_dir /app/data/output \
    --frames_from_one_sec $FRAMES_FROM_ONE_SEC
then
    echo "Error: Failed to process the video"
    exit 1
fi

echo "Done! The result is located in the data/output directory"