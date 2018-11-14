from PIL import Image, ImageDraw
import face_recognition
import sys
import cv2

def main():
    #Test with image
    dir = "test_images/"
    # Load the jpg file into a numpy array
    image = face_recognition.load_image_file(dir + sys.argv[1] + ".jpg")
    facial_features = getNose(image)
    display(facial_features)


def getNose(image):
    print ('starting isForward')
    face_landmarks_list = face_recognition.face_landmarks(image,model="small")

    pil_image = Image.fromarray(image)
    d = ImageDraw.Draw(pil_image)

    for face_landmarks in face_landmarks_list:
        # Let's trace out each facial feature in the image with a line!
        
        for facial_feature in face_landmarks.keys():
            if facial_feature == "chin" or facial_feature == "nose_tip":
                d.line(face_landmarks[facial_feature], width=5)
                print("The {} in this face has the following points: {}".format(facial_feature, face_landmarks[facial_feature]))
            

    # Show the picture
    return pil_image


def display(image):
    image.show()

if __name__ == '__main__':
    main()

