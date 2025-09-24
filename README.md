# AI Feedback - YOLO Object Detection

This project uses [YOLO](https://github.com/ultralytics/ultralytics) with OpenCV to detect a specific object (class 39, e.g., "bottle") from a webcam feed. For each detected object, the script calculates and displays:

- **Distance from the center of the frame (in cm)**
- **Angle from the center of the frame (in degrees)**
- **Labels each detected object as "Bottle N" both on the video and in the terminal**

## Requirements

- Python 3.8+
- [ultralytics](https://pypi.org/project/ultralytics/)
- OpenCV (`opencv-python`)

Install dependencies:
```bash
pip install ultralytics opencv-python
```

## Usage

1. Place your YOLO model file (e.g., `yolo11m.pt`) in the project directory.
2. Adjust camera parameters in `main.py` if needed:
   - `FOCAL_LENGTH_PX`
   - `REAL_OBJECT_WIDTH_CM`
   - `H_FOV_DEG` (horizontal field of view)
3. Run the script:
   ```bash
   python main.py
   ```
4. The webcam window will open. Detected bottles will be labeled and their distance/angle printed in the terminal.

## Notes

- The script is set to detect only class 39. Change this value in `main.py` if your target object has a different class index.
- For accurate distance estimation, calibrate `FOCAL_LENGTH_PX` and `REAL_OBJECT_WIDTH_CM` for your camera and object.
- Press `q` to exit the webcam window.