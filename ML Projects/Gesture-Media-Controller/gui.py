from tkinter import *
import cv2
import tkinter as tk
from PIL import Image, ImageTk 
import tkinter.messagebox as tmsg
import tensorflow as tf
import numpy as np
import requests
import time
import subprocess


vid = cv2.VideoCapture(0) 
width, height = 400, 500
model = tf.keras.models.load_model('model2.h5')
# Set the width and height 
vid.set(cv2.CAP_PROP_FRAME_WIDTH, width) 
vid.set(cv2.CAP_PROP_FRAME_HEIGHT, height) 

vlc_url = 'http://localhost:8080/requests/status.xml'
vlc_user = ''
vlc_password = 'harsh' 
vlc_command = r'VLC\vlc.exe'
music_file_path = 'music'
subprocess.Popen([vlc_command, music_file_path])

def play_pause():
    pause_command = 'pl_pause'  
    response = requests.get(vlc_url, auth=(vlc_user, vlc_password), params={'command': pause_command})
    time.sleep(5)
def next():
    pause_command = 'pl_next'   
    response = requests.get(vlc_url, auth=(vlc_user, vlc_password), params={'command': pause_command})
    time.sleep(5)
def volumedown():
    volume_up_command = 'volume' 
    volume_value = 25
    response = requests.get(vlc_url, auth=(vlc_user, vlc_password), params={'command': volume_up_command,'val':f'-{volume_value}'})
def volumeup():
    volume_up_command = 'volume'  
    volume_value = 25
    response = requests.get(vlc_url, auth=(vlc_user, vlc_password), params={'command': volume_up_command,'val':f'+{volume_value}'})
    
def camera():
    op = {0: 'fist', 1: 'no gesture', 2: 'ok', 3: 'palm', 4: 'two up'}
    com = {0: 'Volume Up',1:'No Command',2:'Volume down',3:'Pause/Play',4:'Next Track'}
    global label1

    if vid.isOpened():
        _, frame = vid.read()

        opencv_image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGBA)
        captured_image = Image.fromarray(opencv_image)
        photo_image = ImageTk.PhotoImage(image=captured_image)

        label_widget.photo_image = photo_image
        label_widget.configure(image=photo_image)

        resized_frame = np.array(Image.fromarray(frame).resize((224, 224)))
        input_data = np.expand_dims(resized_frame, axis=0)

        predictions = model.predict(input_data)
        predicted_class = np.argmax(predictions)
        print(predicted_class)

        label_text = tk.StringVar()
        label_text.set(f"Action : {op[predicted_class]}\nCommand :{com[predicted_class]}")

        if 'label1' in globals():
            label1.pack_forget()
        label1 = tk.Label(root, textvariable=label_text, font=("Helvetica", 16))
        label1.pack(pady=20,padx=100,side='right')

        if predicted_class == 0:
            volumeup()
        elif predicted_class == 1:
            pass
        elif predicted_class == 2:
            volumedown()
        elif predicted_class == 3:
            play_pause()
        else:
            next()
        label_widget.after(10, camera)
    else:
        vid.release()
        label_widget.configure(image=None)  
        camera_button["text"] = "Start Camera"  
        camera_button["command"] = start_camera  
def start_camera():
    global vid
    # Initialize the VideoCapture object
    vid = cv2.VideoCapture(0)
    
    # Change button text
    camera_button["text"] = "Stop Camera"
    
    # Change button command
    camera_button["command"] = stop_camera
    camera_button["bg"] = "red"
    camera_button.place(x=5, y=485)

    response = requests.get(vlc_url, auth=(vlc_user, vlc_password))
    xml_content = response.content.decode('utf-8')
    status =xml_content.split('<state>')[1].split('</state>')[0]

    # Start capturing frames
    camera()
def stop_camera():
    global vid
    # Stop capturing frames
    vid.release()
    
    # Clear the label
    label_widget.configure(image=None)

    # Change button text
    camera_button["text"] = "Start Camera"
    camera_button["bg"] = "Green"

    # Change button command
    camera_button["command"] = start_camera
    resp = tmsg.askquestion('Warning','Do you want to close the application ?')
    if resp=='yes':
        quit()
    else:
        pass

root = Tk()
root.configure(bg="lightblue")
label_widget = Label(root) 
label_widget.pack() 
root.bind('<Escape>', lambda e: root.quit()) 
root.geometry("600x600")
camera_button = Button(root,text='Start Camera',command=start_camera,width=20, height=5,font="Ariel 13 bold",bg='Green')
camera_button.place(x=180, y=350)

root.mainloop()