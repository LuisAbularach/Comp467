import face_forward
import face_recognition
import cv2
import os

# Get a reference to webcam #0 (the default one)
video_capture = cv2.VideoCapture(0)

# Create arrays of known face encodings and their names
known_face_encodings = []
known_face_names = []

# Initialize some variables
storage = "caught"
Suspects = "Suspects"

try:  
    os.makedirs(storage)
    os.makedirs(Suspects)
except OSError:  
    print("Directories Already Exist")
    # print ("Creation of the directory %s and %s failed" % storage,Suspects)
else:  
    print("Caught and Suspects directory created")
    # print ("Successfully created the directories %s and %s" % storage, Suspects)

face_locations = []
face_encodings = []
face_names = []
suspicion_levels = []
process_this_frame = True
suspect_num = 0
priority = "0"
solid = True

#We will only anylyze every 5 frames facial features
frame_count = 0

while True:
    # Grab a single frame of video
    ret, frame = video_capture.read()

    # Resize frame of video to 1/4 size for faster face recognition processing
    small_frame = face_forward.transform(frame, 'small')
    frame = face_forward.transform(frame, 'big')

    # Convert the image from BGR color (which OpenCV uses) to RGB color (which face_recognition uses)
    rgb_small_frame = small_frame[:, :, ::-1]

    # Only process every other frame of video to save time
    if process_this_frame:
        # Find all the faces and face encodings in the current frame of video
        face_locations = face_recognition.face_locations(rgb_small_frame)
        face_encodings = face_recognition.face_encodings(rgb_small_frame, face_locations)

        face_names = []
        for face_encoding in face_encodings:
            # See if the face is a match for the known face(s)
            matches = face_recognition.compare_faces(known_face_encodings, face_encoding)
            name = "Unknown"
            

            # If a match was found in known_face_encodings, just use the first one.
            if True in matches:
                first_match_index = matches.index(True)
                name = known_face_names[first_match_index]
                # print(str(suspicion_levels[first_match_index]))
                #only inciment priority once every 10 frames
                suspicion_levels[first_match_index] += 1
                if suspicion_levels[first_match_index]%2 == 0:
                    priority = int(suspicion_levels[first_match_index]/10)
                    if solid:
                        solid = False
                    else:
                        solid = True
                    # print(str(priority))


            #If it wasn't add person jpg
            else:
                suspect_num += 1
                cv2.imwrite(storage + "/suspect_" + str(suspect_num) + ".jpg", frame)
                #load captured image
                suspect_image = face_recognition.load_image_file(storage + "/suspect_" + str(suspect_num) + ".jpg")
                suspect_face_encoding = face_recognition.face_encodings(suspect_image)[0]
                #Initialize suspition level
                suspicion_levels.append(0)
                print("Suspect priorities: "+ str(suspicion_levels))
                #add it to list of known faces
                known_face_encodings.append(suspect_face_encoding)
                known_face_names.append("SUSPECT_" + str(suspect_num))
            face_names.append(name)

    process_this_frame = not process_this_frame


    # Display the results
    for (top, right, bottom, left), name in zip(face_locations, face_names):
        # Draw lines on facial features
        # frame = face_forward.isLookingForward(frame)
        
        # Blow the box to the size of video feed
        top *= 8
        right *= 8
        bottom *= 8
        left *= 8

        priority = int(priority)
        #Set color of bounding box
        TextColor = (255, 255, 255)
        if priority < 5:
        #Green
            color = (0,255,0)
            TextColor = (0, 0, 0)

        elif priority < 15:
            #yellow
            color = (0,255,255)
            TextColor = (0, 0, 0)
        
        elif priority < 30:
            #red
            color = (0, 0, 255)
        else:
            #flashing red/yellow
            if solid:
                color = (0, 0, 255)
            else:
                color = (0,255,255)
                TextColor = (0, 0, 0)

        #Get pos of nose    
        center = int((left+right)/2), int((top+(bottom - 70))/2)
        #Get radius
        radius = int(((bottom-70) - top)/5)
        
        #nose[] = face_forward.getNose(frame)

        # Draw a bounding box around the face
        cv2.rectangle(frame, (left, top), (right, bottom), color, 2)
        #cv2.circle(frame, left, 3, (0,0,255), thickness=1, lineType=8, shift=0)

        # Draw a label with a name below the face
        cv2.rectangle(frame, (left, bottom - 70), (right, bottom), color, cv2.FILLED)
        cv2.circle(frame,center, radius, color)
        font = cv2.FONT_HERSHEY_DUPLEX
        cv2.putText(frame, name, (left + 6, bottom - 38), font, 1.2, TextColor, 1)
        cv2.putText(frame, "Priority: " +  str(priority), (left + 6, bottom - 6), font, 0.8, TextColor, 1)

    # Display the resulting image
    cv2.imshow('Live Feed', frame)

    if priority == 30:
        #Send image notification
        cv2.imwrite(Suspects + "/suspect_" + str(suspect_num) + ".jpg", frame)

    # Hit 'q' on the keyboard to quit!
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release handle to the webcam
video_capture.release()
cv2.destroyAllWindows()

def drawCircle(image, center, radius):
    cv2.circle(image, center, radius, color, thickness=1, lineType=8, shift=0)
