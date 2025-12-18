import json
import cv2
import numpy as np
import base64
from channels.generic.websocket import AsyncWebsocketConsumer
from .person_and_phone import *
from .eye_tracker import *
from .head_pose_estimation import *
from image_ai import service
from asgiref.sync import sync_to_async

class CameraConsumer(AsyncWebsocketConsumer):
    yolo = YoloV3()
    load_darknet_weights(yolo, 'image_ai/weights/yolov3.weights')
    fd = service.UltraLightFaceDetecion("image_ai/weights/RFB-320.tflite", conf_threshold=0.95)
    fa = service.DepthFacialLandmarks("image_ai/weights/sparse_face.tflite")
    color = (224, 255, 255)

    async def connect(self):
        await self.accept()

    async def disconnect(self, close_code):
        pass

    async def receive(self, text_data):
        from exams.models import ExamResult

        frame_data = json.loads(text_data)
        frame_data_url = frame_data.get('frame')
        exam_id = frame_data.get('examid')
        prev_response = frame_data.get('prevResponse')

        async def update_exam_result():
            try:
                exam_result = await sync_to_async(ExamResult.objects.get)(id=exam_id)
            except ExamResult.DoesNotExist:
                exam_result = ExamResult(id=exam_id)

            frame_data_bytes = base64.b64decode(frame_data_url.split(',')[1])
            img = cv2.imdecode(np.frombuffer(frame_data_bytes, np.uint8), cv2.IMREAD_COLOR)
            img_temp = img.copy()

            img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
            img = cv2.resize(img, (320, 320)).astype(np.float32) / 255
            img = np.expand_dims(img, 0)
            boxes, scores, classes, nums = self.yolo(img)
            # count = sum(1 for i in range(nums[0]) if int(classes[0][i]) == 0)
            # mob_detected = any(int(classes[0][i]) == 67 for i in range(nums[0]))

            count = 0
            mob_detected = None
            for i in range(nums[0]):
                if int(classes[0][i] == 0):
                    count +=1
                if int(classes[0][i] == 67):
                    mob_detected = 'Mobile Phone detected'

            if count == 0: 
                self.status = "No person detected"
                exam_result.no_person += 1 if prev_response != self.status else 0
            elif count > 1:
                self.status = 'More than one person detected'
                exam_result.more_than_one_person += 1 if prev_response != self.status else 0
            elif not mob_detected:
                boxes, _ = self.fd.inference(img_temp)
                feed = img_temp.copy()
                for results in self.fa.get_landmarks(feed, boxes):
                    handler = getattr(service, "pose")
                    hlr = handler(img_temp, results, self.color)[1]
                    if hlr > 40 or hlr < -40: # and prev_response != "Avoid looking right during the exam"
                        self.status = "Avoid looking right during the exam" if hlr > 40 else "Avoid looking left during the exam"
                        
                        if self.status == "Avoid looking left during the exam" or self.status == "Avoid looking right during the exam":
                            exam_result.head_left_right += 1 if prev_response != self.status else 0
            elif mob_detected:
                self.status = 'Mobile Phone Detected'
                exam_result.phone_detected += 1 if prev_response != self.status else 0

            await sync_to_async(exam_result.save)()

        await update_exam_result()
        temp_data = self.status if hasattr(self, 'status') else False
        self.status = False

        response_data = {'status': temp_data}
        await self.send(json.dumps(response_data))
