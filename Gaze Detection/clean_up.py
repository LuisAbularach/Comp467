import face_recognition
import os  

dir = "caught/"
files = os.listdir(dir)
fileCount = len(files)
print("num of images: " + str(fileCount))

# Removes duplicates of suspects
def cleanUp(): 
    if(os.path.exists(dir + "suspect_1.jpg")):
        # Adds suspect_1 to the individual suspects array
        suspect1 = face_recognition.load_image_file(dir + "suspect_1.jpg")
        suspect1Encoding = face_recognition.face_encodings(suspect1)[0]
        individual_suspects = [suspect1Encoding]
        i=2
        # Iterates from suspect_2 to the last suspect
        for suspects in range(2,fileCount+1):
            image,i = loadNextImage(i)
            imageEncoding = face_recognition.face_encodings(image)[0]
                
            # results is a boolean array that compares the encoding with each individual suspect
            results = face_recognition.compare_faces(individual_suspects, imageEncoding)
            if(not True in results):
                # suspect is a new individual and is added to the array
                individual_suspects.append(imageEncoding)
            else:
                os.remove(dir + "suspect_" + str(i)+ ".jpg")
                print("suspect_" + str(i) + " was removed")
            i+=1
        numIndividualSuspects = len(individual_suspects)
        print("num of individual suspects: " + str(numIndividualSuspects))
    else:
        return
    
# Gets the next valid image
# i is the index of the next valid image
def loadNextImage(j):
    i=j
    while os.path.exists(dir):
        try:
            image = face_recognition.load_image_file(dir + "suspect_" + str(i) +".jpg")
            return image,i
        except FileNotFoundError:
            i+=1
            continue

cleanUp()