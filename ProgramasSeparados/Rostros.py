import cv2
import numpy as np

faceClassif = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')

image = cv2.imread('oficina.png')
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

# Entrenamiento del modelo para detectar las imagenes
faces = faceClassif.detectMultiScale(gray,
	scaleFactor=1.1, # Reducción de la imagen en un 10 %
	minNeighbors=5,
	minSize=(30,30),
	maxSize=(200,200))


for (x,y,w,h) in faces:
	cv2.rectangle(image,(x,y),(x+w,y+h),(0,255,0),2)

i = 0

for (x,y,w,h) in faces:
    i = i + 1
    cv2.imwrite("cara" + str(i) + ".jpg", image[y:y+h,x:x+w])

cv2.imshow('image',image)
cv2.waitKey(0)
cv2.destroyAllWindows()