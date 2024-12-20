# src/main.py

import os
import argparse
from utils import (
    extract_frames_from_video,
    preprocess_images,
    placeholder_feature_extraction,
    placeholder_feature_matching,
    placeholder_3d_reconstruction
)
from progress import ProgressTracker
from timing import timing_stats


def main(input_video_path, output_dir, frames_from_one_sec):
    progress = ProgressTracker(output_dir)

    try:
        # Step 1: Extract frames from video
        if not progress.is_completed('extract_frames'):
            print("Step 1: Extracting frames from video...")
            progress.mark_started('extract_frames')
            images_dir = os.path.join(output_dir, 'images')
            os.makedirs(images_dir, exist_ok=True)
            extract_frames_from_video(input_video_path, images_dir, frames_from_one_sec)
            progress.mark_completed('extract_frames')
        else:
            print("Step 1: Extracting frames from video... [Completed]")

        # Step 2: Preprocess images
        if not progress.is_completed('preprocess_images'):
            print("Step 2: Preprocessing images...")
            progress.mark_started('preprocess_images')
            images_dir = os.path.join(output_dir, 'images')
            processed_images_dir = os.path.join(output_dir, 'processed_images')
            os.makedirs(processed_images_dir, exist_ok=True)
            preprocess_images(images_dir, processed_images_dir)
            progress.mark_completed('preprocess_images')
        else:
            print("Step 2: Preprocessing images... [Completed]")

        # Step 3: Feature extraction (Placeholder)
        if not progress.is_completed('feature_extraction'):
            print("Step 3: Feature extraction...")
            progress.mark_started('feature_extraction')
            placeholder_feature_extraction()
            progress.mark_completed('feature_extraction')
        else:
            print("Step 3: Feature extraction... [Completed]")

        # Step 4: Feature matching (Placeholder)
        if not progress.is_completed('feature_matching'):
            print("Step 4: Feature matching...")
            progress.mark_started('feature_matching')
            placeholder_feature_matching()
            progress.mark_completed('feature_matching')
        else:
            print("Step 4: Feature matching... [Completed]")

        # Step 5: 3D Reconstruction (Placeholder)
        if not progress.is_completed('3d_reconstruction'):
            print("Step 5: 3D Reconstruction...")
            progress.mark_started('3d_reconstruction')
            placeholder_3d_reconstruction()
            progress.mark_completed('3d_reconstruction')
        else:
            print("Step 5: 3D Reconstruction... [Completed]")
    finally:
        timing_stats.print_summary()

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='3D Model Reconstruction from Video')
    parser.add_argument('--input_video', type=str, required=True, help='Path to input video file')
    parser.add_argument('--output_dir', type=str, required=True, help='Directory to save outputs')
    parser.add_argument('--frames_from_one_sec', type=int, default=1, help='Number of frames to extract from one second of video')
    args = parser.parse_args()

    main(args.input_video, args.output_dir, args.frames_from_one_sec)
