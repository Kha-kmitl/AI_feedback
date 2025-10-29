######################################
#             library                #
######################################
from ultralytics import YOLO
import cv2
import math
import serial
# model ################################
model = YOLO("yolo11m.pt")
########################################

# serial port #########################
ser = serial.Serial('/dev/tty.usbmodem411RE', 115200, timeout=1)

# Camera parameters ##################
FOCAL_LENGTH_PX = 389.23  # Use this value for accurate distance calculation
REAL_OBJECT_WIDTH_CM = 32.5

# Boat parameters ####################
DESIRED_TIME_SECONDS = 5.0  # Time to reach the bottle (adjust as needed)
########################################

# video + AI ###########################
cap = cv2.VideoCapture(0)

if not cap.isOpened():
    print("Camera Error")
    exit()

while True:
    ret, frame = cap.read()
    if not ret:
        print("Frame grab Error")
        break

    frame_h, frame_w = frame.shape[:2]
    center_x = frame_w // 2
    center_y = frame_h // 2

    results = model(frame, verbose=False)

    bottle_count = 0
    bottle_close = False  # Track if any bottle is close

    for result in results:
        boxes = result.boxes
        for box in boxes:
            cls = int(box.cls[0])
            if cls == 39:
                bottle_count += 1
                x1, y1, x2, y2 = map(int, box.xyxy[0])

                # Calculate object center
                obj_x = (x1 + x2) // 2

                # Calculate pixel distance from frame center
                dx_px = obj_x - center_x

                # Calculate angle
                H_FOV_DEG = 60
                angle_deg = (dx_px / frame_w) * H_FOV_DEG

                # Estimate distance using pinhole camera model
                box_width_px = x2 - x1
                if box_width_px > 0:
                    distance_cm = (REAL_OBJECT_WIDTH_CM * FOCAL_LENGTH_PX) / box_width_px
                else:
                    distance_cm = 0

                # Calculate required speed to reach bottle
                distance_m = distance_cm / 100.0  # Convert cm to meters
                speed_ms = distance_m / DESIRED_TIME_SECONDS  # Speed in m/s
                speed_kmh = speed_ms * 3.6  # Convert to km/h

                # Check if bottle is close
                if distance_cm < 55:
                    bottle_close = True

                # Print result
                print(f"Bottle {bottle_count}: Distance: {distance_cm:.1f} cm, Angle: {angle_deg:.1f}°, Speed: {speed_kmh:.1f} km/h")

                # Send data to STM32: bottle_number,distance_cm,angle_deg,speed_kmh
                msg = f"{bottle_count},{distance_cm:.1f},{angle_deg:.1f},{speed_kmh:.1f}\n"
                ser.write(msg.encode())

                # Draw rectangle
                label = f"Bottle {bottle_count}: {distance_cm:.1f}cm, {angle_deg:.1f}°, {speed_kmh:.1f}km/h"
                cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
                cv2.putText(frame, label, (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.4, (0, 255, 0), 2)

                # Draw center lines
                cv2.circle(frame, (center_x, center_y), 5, (255, 0, 0), -1)
                cv2.circle(frame, (obj_x, (y1 + y2) // 2), 5, (0, 0, 255), -1)
                cv2.line(frame, (center_x, center_y), (obj_x, (y1 + y2) // 2), (255, 255, 0), 2)

    # Output ON/OFF based on bottle distance and send to STM32
    if bottle_close:
        print("ON")
        ser.write(b"ON\n")
    else:
        print("OFF")
        ser.write(b"OFF\n")

    cv2.imshow("Main camera", frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
ser.close()
# End of code ###########################