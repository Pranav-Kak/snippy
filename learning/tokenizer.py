import numpy as np
import cv2
from PIL import Image
import os

#create a copy for manipulation
copy = Image.open('ocr.png')
copy.save('copy.png')

#convert black charachters to red
img = Image.open('copy.png').convert('RGB')
data = np.array(img)
data[(data == (0,0,0)).all(axis = -1)] = (255,0,0)
img = Image.fromarray(data, mode='RGB')
img.save('copy.png')

# Read input image
img = cv2.imread('copy.png')

# Convert from BGR to HSV color space
hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

# Get the saturation plane - all black/white/gray pixels are zero, and colored pixels are above zero.
s = hsv[:, :, 1]

# Apply threshold on s - use automatic threshold algorithm (use THRESH_OTSU).
ret, thresh = cv2.threshold(s, 0, 255, cv2.THRESH_BINARY+cv2.THRESH_OTSU)

# Find contours in thresh (find only the outer contour - only the rectangle).
contours = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)[-2]  # [-2] indexing takes return value before last (due to OpenCV compatibility issues).

# Find contours in thresh (find the triangles).f
contours = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)[-2]  # [-2] indexing takes return value before last (due to OpenCV compatibility issues).

#contour stores all images on absis of their size , so we will first have to store all characters in order of their left most point
i=0
ocr = Image.open('ocr.png').convert('RGB')
data = np.array(ocr)
data[(data != (255,255,255)).all(axis = -1)] = (0,0,0)
ocr = Image.fromarray(data, mode='RGB')
ocr.save('ocr.png')

avg = 0
count = 0
for c in contours:
     avg  = avg + cv2.contourArea(c)
     count = count + 1

avg = avg/count

left = []
right = []
top = []
bottom = []
for c in contours:
    left.append(tuple(c[c[:, :, 0].argmin()][0])[0] - 2) #takin additional 2 pixel area for better
    right.append(tuple(c[c[:, :, 0].argmax()][0])[0] + 2)
    top.append(tuple(c[c[:, :, 1].argmin()][0])[1] - 2)
    bottom.append(tuple(c[c[:, :, 1].argmax()][0])[1] + 2)

print(bottom)
#for getting line by line chekc bottom

length = bottom[0] - top[0] # randomly picked a character to get a height estimate
print(length)
downwards = []
for x in range(len(bottom)):
    downwards.append(bottom[x])

lennn = len(downwards)
for x in range(lennn):
    for y in range(lennn):
        if x==y:
            pass
        else:
            try:
                if downwards[y] <= downwards[x] + length*0.30:
                    downwards.pop(y)
            except:
                pass

print(downwards)
i=0

for x in range(len(downwards)):
    for c in contours:
        minpos = left.index(min(left))
        if bottom[minpos]<= downwards[x] + length:
            l = left[minpos]
            r = right[minpos]
            t = top[minpos]
            b = bottom[minpos]
            im1 = ocr.crop((l, t, r, b))
            im1.save('./tokens/%d.png'%i)
            left.pop(minpos)
            right.pop(minpos)
            top.pop(minpos)
            bottom.pop(minpos)
            i = i+1

os.remove("copy.png")