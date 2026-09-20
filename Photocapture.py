import tkinter as tk
import cv2
from PIL import Image, ImageTk

def capture_photo():
    global panel 

    ret, frame = cap.read() 
    if ret:
        cv2.imwrite("captured_image.jpg", frame)
        label.config(text="Photo captured and saved!")
    else:
        label.config(text="Error capturing photo.")

def show_frame():
    global panel
    _, frame = cap.read()
    cv2image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB) 
    img = Image.fromarray(cv2image)
    imgtk = ImageTk.PhotoImage(image=img)
    panel.imgtk = imgtk 
    panel.config(image=imgtk)
    root.after(20, show_frame) 

root = tk.Tk()
root.title("Photo Capture with Preview")

# Create a label to display the video stream
panel = tk.Label(root)
panel.pack()

# Initialize the video capture
cap = cv2.VideoCapture(0) 

# Start the video stream in a separate thread
show_frame()

# Define the label here (outside of the functions)
label = tk.Label(root, text="Click the button to capture a photo.") 
label.pack(pady=20)

# Create the capture button
button = tk.Button(root, text="Capture Photo", command=capture_photo)
button.pack(pady=20)

root.mainloop()
