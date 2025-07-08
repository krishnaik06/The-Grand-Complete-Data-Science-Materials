import tkinter as tk
from tkinter import *
import cv2
from PIL import Image, ImageTk
import os
import numpy as np


global last_frame1                                    #creating global              variable
last_frame1 = np.zeros((480, 640, 3), dtype=np.uint8)
global last_frame2                                      #creating global      variable
last_frame2 = np.zeros((480, 640, 3), dtype=np.uint8)
global cap1
global cap2
cap1 = cv2.VideoCapture("./test2.mp4")
cap2 = cv2.VideoCapture("./test2.mp4")

def show_vid():                                       
    if not cap1.isOpened():                             
        print("cant open the camera1")
    flag1, frame1 = cap1.read()
    frame1 = cv2.resize(frame1,(600,500))
    if flag1 is None:
        print ("Major error!")
    elif flag1:
        global last_frame1
        last_frame1 = frame1.copy()
        pic = cv2.cvtColor(last_frame1, cv2.COLOR_BGR2RGB)     
        img = Image.fromarray(pic)
        imgtk = ImageTk.PhotoImage(image=img)
        lmain.imgtk = imgtk
        lmain.configure(image=imgtk)
        lmain.after(10, show_vid)


def show_vid2():
    if not cap2.isOpened():                             
        print("cant open the camera2")
    flag2, frame2 = cap2.read()
    frame2 = cv2.resize(frame2,(600,500))
    if flag2 is None:
        print ("Major error2!")
    elif flag2:
        global last_frame2
        last_frame2 = frame2.copy()
        pic2 = cv2.cvtColor(last_frame2, cv2.COLOR_BGR2RGB)
        img2 = Image.fromarray(pic2)
        img2tk = ImageTk.PhotoImage(image=img2)
        lmain2.img2tk = img2tk
        lmain2.configure(image=img2tk)
        lmain2.after(10, show_vid2)

if __name__ == '__main__':
    root=tk.Tk()   
    img = ImageTk.PhotoImage(Image.open("logo.png"))
    heading = Label(root,image=img, text="Lane-Line Detection")
    # heading.configure(background='#CDCDCD',foreground='#364156')
    heading.pack() 
    heading2=Label(root,text="Lane-Line Detection",pady=20, font=('arial',45,'bold'))                                 
    heading2.configure(foreground='#364156')
    heading2.pack()
    lmain = tk.Label(master=root)
    lmain2 = tk.Label(master=root)

    lmain.pack(side = LEFT)
    lmain2.pack(side = RIGHT)
    root.title("Lane-line detection")            
    root.geometry("1250x900+100+10") 
    
    exitbutton = Button(root, text='Quit',fg="red",command=   root.destroy).pack(side = BOTTOM,)
    show_vid()
    show_vid2()
    root.mainloop()                                  
    cap.release()