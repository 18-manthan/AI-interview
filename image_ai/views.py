from django.shortcuts import render,redirect
from django.views.generic import View
from django.http import JsonResponse
from django.core.files.base import ContentFile
from .person_and_phone import *
from .eye_tracker import *
import cv2
import numpy as np
from .head_pose_estimation import *
import face_recognition
import tensorflow as tf
from base64 import b64decode
from .spoof import *
from tensorflow.keras import Model
from exams.models import CapturedImage
import dlib
# Create your views here.


class IndexView(View):
    def get(self, request, *args, **kwargs):   
        return render(request=request, template_name='image_ai/index.html')
 
def user_registration(request):
    if request.user.is_authenticated:
        captured_image = CapturedImage.objects.filter(user=request.user.id).exists()   
        return render(request=request, template_name='image_ai/indexG.html',context={"verified":captured_image})
    else:
        return redirect('users:login')


class SavePicture(View):
    face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
    def post(self, request, *args, **kwargs):
        is_ajax = request.headers.get('X-Requested-With') == 'XMLHttpRequest'
        if is_ajax:
            data_url = request.POST.get('image_data')
            if data_url:
            
                data = data_url.split(',')[-1]
                image_data = b64decode(data)
                img = cv2.imdecode(np.frombuffer(image_data, np.uint8), cv2.IMREAD_COLOR)
                
                gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
                faces = self.face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))

                for (x, y, w, h) in faces:
                    face_roi = img[y:y+h, x:x+w]

                    face_resized = cv2.resize(face_roi, (224, 224))
                    retval, buffer = cv2.imencode('.jpg', face_resized)
                    image_data = np.array(buffer).tobytes()

                    image = CapturedImage.objects.create(user=request.user)
                    image.image.save('captured.jpg', ContentFile(image_data))
                    image.save()
                return JsonResponse({'message': 'Image saved successfully'})
        else:
            return JsonResponse({'error': 'Invalid request method.'})



                   
class Validate_Image(View):   
    yolo = YoloV3()
    load_darknet_weights(yolo, 'image_ai/weights/yolov3.weights')
    face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

    def post(self,request,*args,**kwargs):
        is_ajax = request.headers.get('X-Requested-With') == 'XMLHttpRequest'
        if is_ajax:
            data_url = request.POST.get('image_data')

            data = data_url.split(',')[-1]
            image_data = b64decode(data)
            img = cv2.imdecode(np.frombuffer(image_data, np.uint8), cv2.IMREAD_COLOR)
            gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            faces = self.face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))

            for (x, y, w, h) in faces:
                face_roi = img[y:y+h, x:x+w]

            img_resized = cv2.resize(face_roi, (320, 320))
           
            spoof_real = check_spoofing(img_resized)
            
            if(spoof_real == "Spoof"):
                return JsonResponse({'message': "Image potentially altered or manipulated. " })

            # status = head_pose(img)
            
            # status =  eye_detect(img)
            img = cv2.resize(img, (320, 320))

            img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

            img = img.astype(np.float32)
            img = np.expand_dims(img, 0)
            img = img / 255
            boxes, scores, classes, nums = self.yolo(img)
            count=0
            status = False
            for i in range(nums[0]):
                if int(classes[0][i] == 0):
                    count +=1
                if int(classes[0][i] == 67):

                    status = 'Mobile Phone detected'
                    
            if count == 0:
                status = "No person detected"

            elif count > 1:     
                status = 'More than one person detected'
            print(status)
            return JsonResponse({'message': status })





class FaceIdentificaton(View):
    yolo = YoloV3()
    load_darknet_weights(yolo, 'image_ai/weights/yolov3.weights')
    base_model  = tf.keras.applications.vgg19.VGG19(
            include_top=True,
            weights='imagenet',
            input_tensor=None,
            input_shape=None,
            pooling=None,
            classes=1000,
            classifier_activation='softmax'
        )
    # embedding_model = Model(inputs=base_model.input, outputs=base_model.get_layer('fc2').output)
    face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
    detector = dlib.get_frontal_face_detector()
    def post(self,request,*args,**kwargs):
        is_ajax = request.headers.get('X-Requested-With') == 'XMLHttpRequest'
        if is_ajax: 
            data_url = request.POST.get('image_data')

            data = data_url.split(',')[-1]
            image_data = b64decode(data)
            image_to_recognize = cv2.imdecode(np.frombuffer(image_data, np.uint8), cv2.IMREAD_COLOR)
            img = image_to_recognize
            gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            faces = self.face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))
            
            img_detect = cv2.cvtColor(image_to_recognize, cv2.COLOR_BGR2RGB)
            img_detect = cv2.resize(img_detect, (320, 320)).astype(np.float32) / 255
            img_detect = np.expand_dims(img_detect, 0)
            face_roi = np.array([])
            for (x, y, w, h) in faces:
                face_roi = img[y:y+h, x:x+w]
            if face_roi.any():
                img = cv2.resize(face_roi, (320, 320))
                spoof_real = check_spoofing(img)
                
                if(spoof_real == "Spoof"):
                    return JsonResponse({'message': "Image potentially altered or manipulated. " })
                img = img.astype(np.float32)
                img = np.expand_dims(img, 0)
                img = img / 255
                boxes, scores, classes, nums = self.yolo(img_detect)
                count=0
                status = False
                for i in range(nums[0]):
                    if int(classes[0][i] == 0):
                        count +=1
                    if int(classes[0][i] == 67):

                        status = 'Mobile Phone detected'
                        
                if count == 0:
                    status = "No person detected"

                elif count > 1:     
                    status = 'More than one person detected'
            else:
                status = "Face not detected"
           
            if status:
                return JsonResponse({'status': False,'message':status })

           

            captured_image = CapturedImage.objects.get(user=request.user.id)
            img1 = cv2.imread("media/"+str(captured_image.image))
           
            # img = face_recognition.load_image_file("media/"+str(captured_image.image))
            
            image_of_person_1_rgb = cv2.cvtColor(img1, cv2.COLOR_BGR2RGB)
            
                
            image_of_person_2_rgb = cv2.cvtColor(face_roi, cv2.COLOR_BGR2RGB)
          
            
#git add






            faces_person_1 = self.detector(image_of_person_1_rgb, 0)
            faces_person_2 = self.detector(image_of_person_2_rgb, 0)

            # Extract face locations as tuples for face_recognition usage
            face_locations_person_1 = [(face.top(), face.right(), face.bottom(), face.left()) for face in faces_person_1]
            face_locations_person_2 = [(face.top(), face.right(), face.bottom(), face.left()) for face in faces_person_2]

            # Check if a single face is detected in each image
            if len(face_locations_person_1) == 1 and len(face_locations_person_2) == 1:
                # Get the facial encodings for both faces
                encoding_of_person_1 = face_recognition.face_encodings(image_of_person_1_rgb, known_face_locations=face_locations_person_1)[0]
                encoding_of_person_2 = face_recognition.face_encodings(image_of_person_2_rgb, known_face_locations=face_locations_person_2)[0]

                # Compare the faces by calculating the Euclidean distance between their encodings
                euclidean_distance = face_recognition.face_distance([encoding_of_person_1], encoding_of_person_2)

                # The result is a value between 0 and 1; lower values indicate more similar faces
                # You can set a threshold to determine if the faces are considered a match based on your requirements
                threshold = 0.3  # Adjust as needed

                if euclidean_distance[0] < threshold:
                    print("These faces are a match!")
                    return JsonResponse({'status': True,'message': request.user.username })
                else:
                    print("These faces are not a match.")
                    return JsonResponse({'status': False,'message': "face not authorised"})
            else:
                print("Unable to compare faces. Ensure a single face is detected in each image.", len(faces_person_1), len(faces_person_2) )
                return JsonResponse({'status': False,'message': "Unable to compare faces. Ensure a single face is detected in each image"})
