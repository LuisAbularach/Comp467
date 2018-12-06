import face_recognition
import os  

dir = "caught/"
files = os.listdir(dir)
fileCount = len(files)
print("num of images: " + str(fileCount))

# Removes duplicates of suspects
def cleanUp(): 
                           
    # Adds suspect_1 to the individual suspects array
    suspect1 = face_recognition.load_image_file(dir + "suspect_1.jpg")
    sus1Encoding = face_recognition.face_encodings(suspect1)[0]
    individual_suspects = [sus1Encoding]

    for i in range(2,fileCount+1):
        image = face_recognition.load_image_file(dir + "suspect_" + str(i) +".jpg")
        try:
            imageEncoding = face_recognition.face_encodings(image)[0]
        except IndexError:
            print("Unable to locate any faces")
            continue
            
        # results is a boolean array that compares the encoding with each individual suspect
        results = face_recognition.compare_faces(individual_suspects, imageEncoding)
        print("suspect_" + str(i) + " new suspect? {}".format(not True in results))
        if(not True in results):
            # suspect is a new individual and is added to the array
            individual_suspects.append(imageEncoding)
        else:
            os.remove(dir + "suspect_" + str(i)+ ".jpg")
    numIndividualSuspects = len(individual_suspects)
    print("num of individual suspects: " + str(numIndividualSuspects))
    order()
    
# UNUSED METHOD
# Gets the next valid image
# j is the index of the next valid image
def loadNextImage(i):
    j=i
    while os.path.exists(dir):
        try:
            image = face_recognition.load_image_file(dir + "suspect_" + str(j) +".jpg")
            return image,j
        except FileNotFoundError:
            j+=1
            continue

# renames the files so that suspects are numbered incrementally
def order():
    i=1
    for filename in os.listdir(dir):
        filename = dir + filename
        name = dir + "suspect_" + str(i) + ".jpg"
        os.rename(filename, name)
        i+=1

cleanUp()