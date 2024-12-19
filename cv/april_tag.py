import cv2
import apriltag

detector = apriltag.Detector()

capture = cv2.VideoCapture(2)

running = True

while running:
    _, frame = capture.read()
    grey_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    april_tags = detector.detect(grey_frame)

    for tag in april_tags:
        tag_id = tag.tag_id
        corners = tag.corners
        center = tag.center
        # pose = tag.pose_R, tag.pose_t, tag.pose_err 

        cv2.polylines(frame, [corners.astype(int)], True, (0, 255, 0), 2)

        cv2.putText(frame, str(tag_id), (int(corners[0][0]), int(corners[0][1])), cv2.FONT_HERSHEY_SIMPLEX, .5, (0, 0, 255), 1)

        print("tag corners\n")
        print(corners)
        print("tag center\n")
        print(center)
    
    cv2.imshow("April Tag Tracking", frame)

    if cv2.waitKey(1) == ord("q"):
        running = False

capture.release()
cv2.destroyAllWindows()
