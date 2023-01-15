import cv2
import numpy as np

# capture = cv2.VideoCapture(0)

# while(capture.isOpened()) :
#     ret, frame = capture.read()
    
#     if (cv2.waitKey(1) == ord('s')):
#         break
    
#     qrDetector = cv2.QRCodeDetector()
#     data, bbox, rectifiedImage = qrDetector.detectAndDecode(frame)
    
#     if (len(data) > 0):
#         print(f'Dato: {data}')
#         cv2.imshow('webCam', rectifiedImage)
#     else:
#         cv2.imshow('webCam', frame)

# Cargar imagen
image = cv2.imread('QR.png')   

# Crear detector de código QR
qrDetector = cv2.QRCodeDetector()

# Guardar la dirección web y su imagen del QR
data, bbox, rectifiedImage = qrDetector.detectAndDecode(image)

if (len(data) > 0):
        print(f'Dato: {data}')
        cv2.imshow('webCam', rectifiedImage)
else:
        cv2.imshow('webCam', image)

cv2.waitKey(0)
cv2.destroyAllWindows()