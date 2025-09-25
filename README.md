# AI Feedback - YOLO Object Detection & STM32 Communication

This project uses [YOLO](https://github.com/ultralytics/ultralytics) with OpenCV to detect a specific object (class 39, e.g., "bottle") from a webcam feed. For each detected object, the script calculates and displays:

- **Distance from the center of the frame (in cm)**
- **Angle from the center of the frame (in degrees)**
- **Labels each detected object as "Bottle N" both on the video and in the terminal**
- **Sends bottle number, distance, and angle to an STM32F411RE via USB serial**

## Requirements

- Python 3.8+
- [ultralytics](https://pypi.org/project/ultralytics/)
- OpenCV (`opencv-python`)
- Pyserial (`pyserial`)
- YOLO model file (e.g., `yolo11m.pt`)
- STM32F411RE with USB CDC firmware (for serial communication)

Install dependencies:
```bash
pip install ultralytics opencv-python pyserial
```

## Usage

1. Place your YOLO model file (e.g., `yolo11m.pt`) in the project directory.
2. Adjust camera and object parameters in `main.py` if needed:
   - `FOCAL_LENGTH_PX`
   - `REAL_OBJECT_WIDTH_CM`
   - `H_FOV_DEG` (horizontal field of view)
3. Connect your STM32F411RE to your computer via USB and ensure it appears as a serial device (e.g., `/dev/tty.usbmodem411RE`).
4. Run the script:
   ```bash
   python main.py
   ```
5. The webcam window will open. Detected bottles will be labeled and their distance/angle printed in the terminal.
6. Data for each detected bottle (`bottle_number,distance_cm,angle_deg`) will be sent to the STM32 via USB serial.

## STM32 Communication

- The script sends data to the STM32 in the format:  
  `bottle_number,distance_cm,angle_deg\n`  
  Example: `1,123.4,15.6\n`
- Ensure your STM32 firmware is set up to receive and parse this data via USB CDC (virtual COM port).

## Notes

- The script is set to detect only class 39. Change this value in `main.py` if your target object has a different class index.
- For accurate distance estimation, calibrate `FOCAL_LENGTH_PX` and `REAL_OBJECT_WIDTH_CM` for your camera and object.
- Press `q` to exit the webcam window.
- If you have multiple bottles detected, each will be labeled and sent with its own number.

---