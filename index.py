import tkinter as tk
from tkinter import filedialog
from PIL import Image, ImageTk
import cv2
import os




class item:
    def __init__(self, filename, locate, image, video):
        self.filename = filename
        self.locate = locate
        self.image = image
        self.video = video
config = item()




root = tk.Tk()
videoFrame = tk.Frame(root).grid()
root.title("Image_Sketch")
root.minsize(800, 600)
config.video = tk.Label(videoFrame)
config.video.grid(column=0, row=3)

pixels_x = 800
pixels_y = 600




def detectFace(img_filename):
    config.video.destroy

    image_rgb = cv2.imread(img_filename)
    print("detectFace : ", img_filename)

    image_gray = cv2.cvtColor(image_rgb, cv2.COLOR_BGR2GRAY)
    image_blur = cv2.GaussianBlur(image_gray, ksize=(21, 21), sigmaX=0, sigmaY=0)
    image_blend = cv2.divide(image_gray, image_blur, scale=255)

    image = Image.fromarray(image_blend)
    if(image.width > 1000 or image.height > 1000):
        image = image.resize((image.width // 5, image.height // 5))#image.resize((pixels_x, pixels_y))
    elif(image.width > 800 or image.height > 800):
        image = image.resize((image.width // 2, image.height // 2))

    imgtk = ImageTk.PhotoImage(image=image)

    config.video = tk.Label(root, image=imgtk)
    config.video.grid(column=0, row=3)
    config.video.imgtk = imgtk
    config.video.configure(image=imgtk)

    config.image = image_blend
    config.locate = img_filename
    #cv2.imwrite('result.jpg', image_blend)
    # cv2.imshow("image_blend",image_blend)


def open_img_file():
    filename = filedialog.askopenfilename(initialdir=os.getcwd(
    ), title="Select file", filetypes=(("jpeg files", "*.jpg"), ("png images", ".png"), ("all files", "*.*")))

    if not filename:
        return

    image = Image.open(filename)
    config.image = image
    if(image.width > 1000 or image.height > 1000):
        image = image.resize((image.width // 5, image.height // 5))#image.resize((pixels_x, pixels_y))
    elif(image.width > 800 or image.height > 800):
        image = image.resize((image.width // 2, image.height // 2))
    
    image = ImageTk.PhotoImage(image)

    
    config.video = tk.Label(root, image=image)
    config.video.image = image
    config.video.grid(column=0, row=3)

    
    print("filename : ", filename)
    config.filename = filename
    config.video.destroy
    


def save_img_file(filename):
    print("save_img_file : ", filename)
    #cv2.imwrite('result.jpg', image_blend)

    edge = Image.fromarray(config.image)
    #tk_edge = ImageTk.PhotoImage(edge)
    #label = tk.Label(root, image=tk_edge)
    #label.grid(column=0, row=4)

    filename = filedialog.asksaveasfile(mode='w', defaultextension=".jpg")
    if not filename:
        return

    edge.save(filename)
    config.video.destroy


button1 = tk.Button(text="Open file", width=10,
                   command=lambda: open_img_file())
button1.grid(column=0, row=0, ipadx=2.5, pady=2.5, sticky=tk.W+tk.N)

button2 = tk.Button(text="Get Sketch", width=10,
                   command=lambda: detectFace(config.filename))
button2.grid(column=0, row=1, ipadx=2.5, pady=2.5, sticky=tk.W+tk.N)

button3 = tk.Button(text="Save as", width=10,
                   command=lambda: save_img_file(config.filename))
button3.grid(column=0, row=2, ipadx=2.5, pady=2.5, sticky=tk.W+tk.N)


root.mainloop()
