import cv2
import face_recognition
from PIL import Image, ImageDraw
import numpy as np
import face_forward


def PIL2array(img):
    """ Convert a PIL/Pillow image to a numpy array """
    return np.array(img.getdata(),
        np.uint8).reshape(img.size[1], img.size[0], 3)

def up_sample(landmark_list , sample_size=4):
    for face_landmark in landmark_list:
        if len(face_landmark) > 1:
            for key in face_landmark.keys():
                face_landmark[key] = [(w[0]*sample_size , w[1]*sample_size) for w in face_landmark[key]]
    return landmark_list


class FaceLandMarkDetection:

    def predict(self , frame):
        face_landmarks = face_recognition.face_landmarks(frame)
        if down_sampling:
            self.face_landmarks = up_sample(face_landmarks)
        else:
            self.face_landmarks = face_landmarks
            
            
    def plot(self , frame):
        pil_image = Image.fromarray(frame)
        for face_landmarks in self.face_landmarks:
            if len(face_landmarks) > 1:
                d = ImageDraw.Draw(pil_image, 'RGBA')

                # Make the eyebrows into a nightmare
                d.polygon(face_landmarks['left_eyebrow'], fill=(68, 54, 39, 128))
                d.polygon(face_landmarks['right_eyebrow'], fill=(68, 54, 39, 128))
                d.line(face_landmarks['left_eyebrow'], fill=(68, 54, 39, 150), width=5)
                d.line(face_landmarks['right_eyebrow'], fill=(68, 54, 39, 150), width=5)

                # Gloss the lips
                d.polygon(face_landmarks['top_lip'], fill=(150, 0, 0, 128))
                d.polygon(face_landmarks['bottom_lip'], fill=(150, 0, 0, 128))
                d.line(face_landmarks['top_lip'], fill=(150, 0, 0, 64), width=8)
                d.line(face_landmarks['bottom_lip'], fill=(150, 0, 0, 64), width=8)

                # Sparkle the eyes
                d.polygon(face_landmarks['left_eye'], fill=(255, 255, 255, 30))
                d.polygon(face_landmarks['right_eye'], fill=(255, 255, 255, 30))

                # Apply some eyeliner
                d.line(face_landmarks['left_eye'] + [face_landmarks['left_eye'][0]], fill=(0, 0, 0, 110), width=6)
                d.line(face_landmarks['right_eye'] + [face_landmarks['right_eye'][0]], fill=(0, 0, 0, 110), width=6)
            
        return PIL2array(pil_image)

video_capture = cv2.VideoCapture(0)
video_capture.set(cv2.CAP_PROP_FRAME_WIDTH, 1920)
video_capture.set(cv2.CAP_PROP_FRAME_HEIGHT, 1080)


face_landmark_detection = FaceLandMarkDetection()
down_sampling = True
while True:
    # Grab a single frame of video
    ret, frame = video_capture.read()
    
    if down_sampling:
        small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)

        # Find all facial features in all the faces in the image
        face_landmark_detection.predict(small_frame)
    else:
        # Find all facial features in all the faces in the image
        face_landmark_detection.predict(frame)

    ### plot 
    frame = face_landmark_detection.plot(frame)
    
    frame = face_forward.transform(frame, "Big")
    # Display the resulting image
    cv2.imshow('Video', frame)

    # Hit 'q' on the keyboard to quit!
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release handle to the webcam
video_capture.release()
cv2.destroyAllWindows()