import cv2
import argparse
import numpy as np
import time

def capture_long_exposure(exposure_time=5, output_file='long_exposure.jpg'):
    """
    Captures a long exposure image from a USB camera with real-time progress bar.
    Accumulates light over time and normalizes output to maximum brightness.
    Args:
        exposure_time: Total capture time in seconds
        output_file: Output filename for the resulting image
    """
    cap = cv2.VideoCapture(0)
    
    if not cap.isOpened():
        print("Error: Could not open camera")
        return

    start_time = time.time()
    frames = []
    
    try:
        while (time.time() - start_time) < exposure_time:
            ret, frame = cap.read()
            if ret:
                # Convert to float32 for accumulation
                frames.append(frame.astype(np.float32))
                # Calculate progress
                elapsed = time.time() - start_time
                progress_pct = elapsed / exposure_time
                bar_length = 40
                filled = int(bar_length * progress_pct)
                bar = '#' * filled + '-' * (bar_length - filled)
                print(f'\rProgress: [{bar}] {progress_pct:.0%}', end='', flush=True)
            else:
                print("Warning: Frame capture failed")
                
        print()  # Move to new line after progress bar
        if len(frames) > 0:
            # Sum all frames and normalize to maximum brightness
            sum_frame = np.sum(frames, axis=0)
            
            # Normalize to 0-255 range
            max_val = sum_frame.max()
            if max_val > 0:
                sum_frame = (sum_frame * (255.0 / max_val)).clip(0, 255)
            
            final_frame = sum_frame.astype(np.uint8)
            cv2.imwrite(output_file, final_frame)
            print(f"Successfully saved long exposure image to {output_file}")
            
    except Exception as e:
        print(f"Error occurred: {str(e)}")
    finally:
        cap.release()

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--exposure_time', type=float, default=5.0,
                       help='Exposure time in seconds (default: 5)')
    parser.add_argument('--output', type=str, default='long_exposure.jpg',
                       help='Output filename (default: long_exposure.jpg)')
    args = parser.parse_args()
    
    capture_long_exposure(args.exposure_time, args.output)
