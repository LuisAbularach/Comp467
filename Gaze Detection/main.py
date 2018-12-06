import PIL
from PIL import Image,ImageTk
import pytesseract
import cv2
import real_time

from tkinter import *
started = False

def show_frame():
    _, frame = cap.read()
    # frame = cv2.flip(frame, 1)
    frame = real_time.startRecording()
    cv2image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGBA)
    img = PIL.Image.fromarray(cv2image)
    imgtk = ImageTk.PhotoImage(image=img)
    lmain.imgtk = imgtk
    lmain.configure(image=imgtk)
    lmain.after(10, show_frame)
    
def start():
    started = True

i = 1

width, height = 1600, 1200
cap = cv2.VideoCapture(0)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, width*2)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, height*2)

root = Tk()

# root.geometry("1600x1200")
root.title("Gaze Detection")
# root.wm_iconbitmap("eyecon.ico")
topFrame = Frame(root)
topFrame.pack()
root.bind('<Escape>', lambda e: root.quit())
button = Button(topFrame, text="Start System", fg="black",font =('', 18), height = 2, width = 20,COMMAND=start())
lmain = Label(root)

button.pack()
lmain.pack()    

show_frame()

root.mainloop()

