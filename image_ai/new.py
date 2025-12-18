import service
import cv2


fd = service.UltraLightFaceDetecion("weights/RFB-320.tflite",
                                        conf_threshold=0.95)
fa = service.DepthFacialLandmarks("weights/sparse_face.tflite")

cap = cv2.VideoCapture(0)
color=(224, 255, 255)
handler = getattr(service, "pose")
while True:
        ret, frame = cap.read()

        if not ret:
            break

        # face detection
        boxes, scores = fd.inference(frame)

        # raw copy for reconstruction
        feed = frame.copy()

        for results in fa.get_landmarks(feed, boxes):
            handler(frame, results, color)

        # cv2.imwrite(f'draft/gif/trans/img{counter:0>4}.jpg', frame)

        cv2.imshow("demo", frame)
        if cv2.waitKey(1) == ord("q"):
            break

