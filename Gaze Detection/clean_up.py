import face_recognition
import os  

# Removes duplicates of suspects
def cleanUp():
    dir = "caught/"
    files = os.listdir(dir)
    fileCount = len(files)
    print("num of images: " + str(fileCount)) 
                           
    # Adds suspect_1 to the individual suspects array
    suspect1 = face_recognition.load_image_file(dir + "suspect_1.jpg")
    sus1Encoding = face_recognition.face_encodings(suspect1)[0]
    individual_suspects = [sus1Encoding]

    for i in range(2,fileCount+1):
        image = face_recognition.load_image_file(dir + "suspect_" + str(i) +".jpg")
        try:
            imageEncoding = face_recognition.face_encodings(image)[0]
        except IndexError:
            print("Unable to locate any faces. Aborting...")
            quit()      
        # results is a boolean array that compares the encoding with each individual suspect
        results = face_recognition.compare_faces(individual_suspects, imageEncoding)
        print("New suspect? {}".format(not True in results))
        if(not True in results):
            # suspect is a new individual and is added to the array
            individual_suspects.append(imageEncoding)
        else:
            os.remove(dir + "suspect_" + str(i) +".jpg")
    print("num of individual suspects: " + str(len(individual_suspects)))
cleanUp()