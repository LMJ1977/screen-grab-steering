# this script print the coordinates of the mouse pointer when cliked
# first, takes a screenshot of the screen
# second, display the screenshot and wait for a click
# third, print the coordinates of the mouse pointer when cliked

import numpy as np
import cv2
import matplotlib.pyplot as plt
#import matplotlib.image as mpimg
#import PIL
from PIL import ImageGrab
import tkinter as tk
import pytesseract
global text 
text = ""
pytesseract.pytesseract.tesseract_cmd = r'C:\Users\lmonzon\AppData\Local\Tesseract-OCR\tesseract.exe'
tesseract_config = r'--oem 3 --psm 7 -c tessedit_char_whitelist=-.0123456789'
def mouse_event(event):
    print('x: {} and y: {}'.format(event.xdata, event.ydata))
    # parse the event data to global variables
    global x, y
    x = event.xdata
    y = event.ydata
    # close the figure
    plt.close()



#main function
def get_corner(id):
    #get the screen image as grayscale
    img = ImageGrab.grab()
    #convert the screen image to an grayscale image

    img = cv2.cvtColor(np.array(img), cv2.COLOR_RGBA2RGB)
    
    #display the screen image full screen
    fig = plt.figure()
    #fig = plt.figure()
    cid = fig.canvas.mpl_connect('button_press_event', mouse_event)
    plt.imshow(img)
    plt.title('Please select the corner {}'.format(id))
    plt.show()
    #return the coordinates of the corner
    return x, y

# call the main function
# Define a function to print the text in a loop
def do_OCR():
   if running:
    img = ImageGrab.grab(bbox=(x1, y1, x2, y2))
    img = cv2.cvtColor(np.array(img), cv2.COLOR_RGBA2GRAY)
    thresh = cv2.threshold(img, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)[1]
    #img = 255 - cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    # ocr the selected area of the screen
    global text
    text = pytesseract.image_to_string(thresh, config=tesseract_config)
    # print the ocr result
    print(text)
    label2.config(text=text)

   root.after(1, do_OCR)

# Define a function to start the loop
def on_start():
   global running
   running = True

# Define a function to stop the loop
def on_stop():
   global running
   running = False
# get the coordinates of the first corner
x1, y1 = get_corner(1)
# get the coordinates of the second corner
x2, y2 = get_corner(2)

# print the coordinates of the corners
print('x1: {} and y1: {}'.format(x1, y1))
print('x2: {} and y2: {}'.format(x2, y2))

flag_close = False
root = tk.Tk() 
label2 = None
root.attributes('-topmost', True)
running = True
root.title("OCR")
# put the window in the top left corner
root.geometry("+0+0")
# Add a Button to start/stop the loop
start = tk.Button(root, text="Start", command=on_start)
start.pack(padx=10)

stop = tk.Button(root, text="Stop", command=on_stop)
stop.pack(padx=10)

# print the ocr result in the tkinter window in a new box
label = tk.Label(root, text='OCR result')
label.pack()
label2 = tk.Label(root, text=text)
label2.pack()
# Run a function to print text in window
root.after(1, do_OCR)

root.mainloop()

