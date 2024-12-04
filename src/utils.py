# src/utils.py
FRAMES_FROM_ONE_SEC = 3
SHOW_DEBUG_INFO = False

import cv2
import numpy as np
import os
import time
from sys import stdout
from timing import timing_decorator, get_estimated_time


# frame_rate = how much images take from 1 sec
@timing_decorator
def extract_frames_from_video(video_path, output_dir, frame_rate=FRAMES_FROM_ONE_SEC):
    """
    Extract frames from video at a specified frame rate.
    Shows progress and estimated time remaining.
    """
    vidcap = cv2.VideoCapture(video_path)
    success, image = vidcap.read()
    count = 0
    fps = vidcap.get(cv2.CAP_PROP_FPS)
    total_frames = int(vidcap.get(cv2.CAP_PROP_FRAME_COUNT))
    interval = int(fps / frame_rate)
    start_time = time.time()
    
    print(f"Total frames in video: {total_frames}")
    print(f"FPS: {fps}")
    print(f"Extracting every {interval}th frame")

    while success:
        if count % interval == 0:
            frame_id = int(count / interval)
            frame_filename = os.path.join(output_dir, f"frame_{frame_id:05d}.jpg")
            cv2.imwrite(frame_filename, image)
            
            # Calculate progress and ETA
            elapsed_time = time.time() - start_time
            eta = get_estimated_time(count, total_frames, elapsed_time)
            progress = (count / total_frames) * 100
            
            stdout.write(f"\rProgress: {progress:.1f}% | Frame {count}/{total_frames} | ETA: {eta}")
            stdout.flush()
            
        success, image = vidcap.read()
        count += 1
    
    vidcap.release()
    print("\nFrame extraction completed!")


@timing_decorator
def preprocess_images(input_dir, output_dir):
    """
    Preprocess images by removing the background using Mask R-CNN.
    Shows progress and estimated time remaining.
    """
    # Load pre-trained Mask R-CNN model and configuration
    model_weights = '/app/models/frozen_inference_graph.pb'
    model_config = '/app/models/mask_rcnn_inception_v2_coco_2018_01_28.pbtxt'
    net = cv2.dnn.readNetFromTensorflow(model_weights, model_config)

    if net.empty():
        print("Error: Could not load the neural network.")
        return

    output_layers_names = ['detection_out', 'detection_masks']
    print("Output layer names:", output_layers_names)

    person_class_id = 1

    image_files = [f for f in os.listdir(input_dir) if f.lower().endswith(('.png', '.jpg', '.jpeg'))]
    total_images = len(image_files)
    start_time = time.time()

    print(f"\nStarting preprocessing of {total_images} images...")

    for idx, image_file in enumerate(sorted(image_files), 1):
        src_path = os.path.join(input_dir, image_file)
        dst_path = os.path.join(output_dir, image_file)

        # Compute progress and ETA
        elapsed_time = time.time() - start_time
        eta = get_estimated_time(idx, total_images, elapsed_time)
        progress = (idx / total_images) * 100

        # Overwrite the previous line in the console
        stdout.write(f"\rProgress: {progress:.1f}% | Image {idx}/{total_images} | ETA: {eta} | Processing: {image_file}")
        stdout.flush()

        # Read the image
        img = cv2.imread(src_path)
        if img is None:
            print(f"Warning: Could not read image {src_path}")
            continue

        height, width = img.shape[:2]
        blob = cv2.dnn.blobFromImage(img, swapRB=True, crop=False)
        net.setInput(blob)

        try:
            boxes, masks = net.forward(output_layers_names)
        except cv2.error as e:
            print(f"Error during forward pass: {e}")
            continue

        person_detected = False
        final_mask = np.zeros((height, width), dtype=np.uint8)
        num_detections = boxes.shape[2]

        for i in range(num_detections):
            class_id = int(boxes[0, 0, i, 1])
            confidence = boxes[0, 0, i, 2]
            if class_id == person_class_id and confidence > 0.5:
                box = boxes[0, 0, i, 3:7]
                x1 = int(box[0] * width)
                y1 = int(box[1] * height)
                x2 = int(box[2] * width)
                y2 = int(box[3] * height)
                if (SHOW_DEBUG_INFO):
                    print(f"  Detection {i}: Confidence {confidence:.2f}, Box [{x1}, {y1}, {x2}, {y2}]")

                x1 = max(0, min(x1, width - 1))
                y1 = max(0, min(y1, height - 1))
                x2 = max(0, min(x2, width - 1))
                y2 = max(0, min(y2, height - 1))

                if x2 - x1 <= 0 or y2 - y1 <= 0:
                    print(f"  Invalid bounding box for detection {i}. Skipping.")
                    continue

                mask = masks[i, class_id - 1]
                mask = cv2.resize(mask, (x2 - x1, y2 - y1), interpolation=cv2.INTER_LINEAR)
                mask = (mask > 0.5).astype(np.uint8)

                full_mask = np.zeros((height, width), dtype=np.uint8)
                full_mask[y1:y2, x1:x2] = mask
                final_mask = np.maximum(final_mask, full_mask * 255)
                person_detected = True

        if person_detected:
            img_fg = cv2.bitwise_and(img, img, mask=final_mask)
            cv2.imwrite(dst_path, img_fg)
            if SHOW_DEBUG_INFO:
                print("  Person detected and processed successfully")
        else:
            if SHOW_DEBUG_INFO:
                print(f"  No person detected in {image_file}")
            cv2.imwrite(dst_path, img)

    total_time = time.time() - start_time
    print(f"\nPreprocessing completed! Total time: {total_time:.2f} seconds")

    
def placeholder_feature_extraction():
    """
    Placeholder for feature extraction step.
    """
    print("Feature extraction placeholder executed.")


def placeholder_feature_matching():
    """
    Placeholder for feature matching step.
    """
    print("Feature matching placeholder executed.")


def placeholder_3d_reconstruction():
    """
    Placeholder for 3D reconstruction step.
    """
    print("3D reconstruction placeholder executed.")
