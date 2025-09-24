######################################
#             library                #
######################################
from ultralytics import YOLO
import cv2
import math

# model ################################
model = YOLO("yolo11m.pt")
########################################

# Camera parameters ##################
FOCAL_LENGTH_PX = 700
REAL_OBJECT_WIDTH_CM = 20
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

                # Print resualt
                print(f"Bottle {bottle_count}: Distance: {distance_cm:.1f} cm, Angle: {angle_deg:.1f}°")

                # Draw rectangle
                label = f"Bottle {bottle_count}: {distance_cm:.1f}cm, {angle_deg:.1f}°"
                cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
                cv2.putText(frame, label, (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)

                # Draw center lines
                cv2.circle(frame, (center_x, center_y), 5, (255, 0, 0), -1)
                cv2.circle(frame, (obj_x, (y1 + y2) // 2), 5, (0, 0, 255), -1)
                cv2.line(frame, (center_x, center_y), (obj_x, (y1 + y2) // 2), (255, 255, 0), 2)

    cv2.imshow("Main camera", frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
# End of code ###########################