from PIL import Image, ImageDraw
import face_recognition
import sys
import cv2
import time
import math

def main():
    start = time.time()
    #Test with image
    dir = "test_images/"
    # Load the jpg file into a numpy array
    image = face_recognition.load_image_file(dir + sys.argv[1] + ".jpg")
    facial_features = facial_coordinates(image)
    # display(facial_features)
    end = time.time()
    
    timer = end - start  
    print(facial_features[0][0])
    print(str(timer))

def up_sample(landmark_list , sample_size=4):
    for face_landmark in landmark_list:
        if len(face_landmark) > 1:
            for key in face_landmark.keys():
                face_landmark[key] = [(w[0]*sample_size , w[1]*sample_size) for w in face_landmark[key]]
    return landmark_list

def facial_coordinates(image):
    #print ('starting isForward')
    small_frame = cv2.resize(image, (0, 0), fx=0.25, fy=0.25)
    face_landmarks_list = face_recognition.face_landmarks(small_frame)
    face_landmarks_list = up_sample(face_landmarks_list)


    pil_image = Image.fromarray(image)
    d = ImageDraw.Draw(pil_image)

    for face_landmarks in face_landmarks_list:
        # Let's trace out each facial feature in the image with a line!
        
        for facial_feature in face_landmarks.keys():
            #if facial_feature == "nose_bridge" or facial_feature == "nose_tip":
            #print("The {} in this face has the following points: {}".format(facial_feature, face_landmarks[facial_feature]))
            return face_landmarks["nose_bridge"], face_landmarks["nose_tip"]

    # return the picture
    # return pil_image

def nose_inCircle(nose, center, radius):
    distance_from_center = calculate_length(nose, center)
    if distance_from_center <= radius:
        #Point is within the circle
        return True


    return False


def calculate_length(a, b):
    #calculations to get length with points
    # (Xa, Ya) and (Xb, Yb) 
    delta_x = abs(b[0] - a[0])
    delta_y = abs(b[1] - a[1])

    size = math.sqrt(delta_x**2 + delta_y**2)

    return size


def display(image):
    a = facial_coordinates(image)
    print("Point: " + a)
    # d.line(face_landmarks[facial_feature], width=5)
    # image.show()

def transform(image, size):
    #Shrink image to a fourth of the size to process faster
    image = cv2.resize(image, (0, 0), fx=size, fy=size)
    
    return image

def textColor(color):
    #Find color that is visible with the background
    red = color[0]
    green = color[1]
    blue = color[2]
    text = (255,255,255)
    # print("COLORS: " + str(red) + " " + str(green) + " " + str(blue))
    if (red*0.299 + green*0.587 + blue*0.114) > 186:
         #turn black
         text = (0,0,0)

    return text

if __name__ == '__main__':
    main()
