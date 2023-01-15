from tkinter import *
from tkinter import ttk
from tkinter import filedialog
import pytesseract
from PIL import Image, ImageTk
import cv2
import numpy as np
from tabulate import tabulate
from bs4 import BeautifulSoup
import requests

# Para que pytesseract encuentre la ruta de donde esta instalado el programa
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

# Crear aplicación de Frame
class Application(ttk.Frame):
    def __init__(self, window):
        super().__init__(window)
        # Configurar ventana de la aplicacion
        window.title("Aplicación IA") # Titulo de la ventana
        # window.attributes('-fullscreen', True) # Pantalla completa
        window.bind("<F11>", lambda event: window.attributes('-fullscreen', not window.attributes("-fullscreen"))) # Intercambiar entre completa o no
        window.bind("<Escape>", lambda event: window.attributes('-fullscreen', False)) # Salir de completa
        window.columnconfigure(0, weight=1)
        window.rowconfigure(0, weight=1)
        
        self.place(relwidth=1, relheight=1)
        self.buttonClose = Button(self, text='Exit', command=window.destroy)
        self.buttonClose.grid(row=0, column=1)
        self.createFrameImagenToText("gray")
        self.createFrame("Detectar QR", "Abrir Imagen", "gray", 2, self.detectarCodigoQR)
        self.createFrame("Detectar Rostros", "Abrir Imagen", "gray", 3, self.detectarRostros)
        self.createFrame("Detectar html tabla", "Abrir html", "gray", 4, self.detectarTabla)
        self.grid(sticky="nsew")

    def createFrameImagenToText(self, color):
        global combo
        # Convertir de imagen a texto
        frameImagenText = Frame(self, width=200, height=400, background=color)
        Label(frameImagenText, text="Transformar imagen a texto", bg=color).pack()
        combo = ttk.Combobox(
            frameImagenText,
            state="readonly",
            values=["spa", "eng"]
        )
        combo.current(1)
        combo.pack()
        # Boton para cargar la imagen
        Button(frameImagenText, text='Seleccionar Imagen', command=self.convertirImagenTexto, relief="sunken").pack()
        frameImagenText.grid(row=1, column=0)
        
    # Crear un nuevo frame con el (Texto del Label), (Texto del boton), (color de fondo), (fila del grid), (funcion a procesar en el boton)
    def createFrame(self, labelText, buttonText, color, r, fun):
        frame = Frame(self, width=500, height=400, background=color)
        Label(frame, text=labelText, bg=color).pack()
        Button(frame, text=buttonText, command=fun, relief="sunken").pack()
        frame.grid(row=r, column=0)
    
    # Funcion para convertir una imagen a texto   
    def convertirImagenTexto(self):
        global file_path
        global label_image
        # Mostramos el cuadro de diálogo y guardamos la ruta del archivo seleccionado en la variable file_path
        file_path = filedialog.askopenfilename(initialdir="C:/", filetypes=[("Archivos JPG",".jpg"),("Archivos PNG",".png")])
        imageText = Image.open(file_path)
        imageText = imageText.resize((200, 200))
        image = ImageTk.PhotoImage(imageText)
        # Coger el spa(Español) o eng(English)
        lenguage = combo.get()
        # Transformar la imagen y detectar si hay texto en ella y lang para el idioma con sus caracteres correspondientes
        result = pytesseract.image_to_string(file_path, lang=lenguage)
        # Imprimir resultado en una nueva ventana
        self.nuevaVentana("Image to text", image, result)
    
    # Detectar un codigo QR
    def detectarCodigoQR(self):
        # Abrir imagen del directorio
        file_path = filedialog.askopenfilename(initialdir="C:/", filetypes=[("Archivos JPG",".jpg"),("Archivos PNG",".png")])
        image = cv2.imread(file_path)
        
        # Crear detector de código QR
        qrDetector = cv2.QRCodeDetector()
        # Guardar la dirección web y su imagen del QR
        data, bbox, rectifiedImage = qrDetector.detectAndDecode(image)
        
        if (len(data) > 0):
            # Transformar una imagen de cv2 a tkinter
            imgResult = self.transformCV2ToTkinter(rectifiedImage, False)
            # Nueva ventana con el resultado
            self.nuevaVentana("Detector QR", imgResult, data)
        else:
            # Transformar una imagen de cv2 a tkinter
            imageTransform = self.transformCV2ToTkinter(image, True)
            # Nueva ventana con un resultado erroneo
            self.nuevaVentana("Detector QR", imageTransform, "No es un QR")

    def detectarRostros(self):
        # Cargar base de datos con los puntos de entrenamiento parad etectar rostros
        faceClassif = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
        
        # Cargar imagen del directorio seleccionado
        file_path = filedialog.askopenfilename(initialdir="C:/", filetypes=[("Archivos JPG",".jpg"),("Archivos PNG",".png")])
        image = cv2.imread(file_path)
        imageChange = cv2.imread(file_path)
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        
        # Entrenamiento del modelo para detectar las imagenes
        faces = faceClassif.detectMultiScale(gray,
            scaleFactor=1.1, # Reducción de la imagen en un 10 %
            minNeighbors=5, # Numero minimo de vecinos que puede tener, numero mas alto mas bajo da falsos positivos
            minSize=(30,30), # Establecer cual puede ser el tamaño minimo y maximo que puede tener una cara
            maxSize=(200,200))

        # Añadir rectangulos de las caras
        for (x,y,w,h) in faces:
            cv2.rectangle(imageChange,(x,y),(x+w,y+h),(0,255,0),2)

        # Transformar imagen
        imResult = self.transformCV2ToTkinter(imageChange, True)
        # Nueva ventana con resultado
        newWindow = self.nuevaVentana("Detector de Rostros", imResult, "¿Quiéres guardar los rostros?")
        Button(newWindow, text="Guardar", command= lambda: self.guardarRostros(image, faces), relief="sunken").pack()
    
    # Guardar rostros en la ruta especificada
    def guardarRostros(self, image, faces):
        # Guardar archivo en ruta especificada
        file_path = filedialog.asksaveasfilename(initialdir="C:/", title="Rostro", filetypes=[("Archivos JPG",".jpg"),("Archivos PNG",".png")])
        
        # Guardar las caras detectadas
        i = 0
        for (x,y,w,h) in faces:
            i = i + 1
            cv2.imwrite(file_path + str(i) + ".jpg", image[y:y+h,x:x+w])
            
    def detectarTabla(self):
        # Leer ruta html
        file_path = filedialog.askopenfilename(initialdir="C:/", filetypes=[("Archivos HTML",".html")])
        
        # Leer html
        with open(file_path, 'r') as f:
            html = f.read()
            soup = BeautifulSoup(html, 'html.parser')

        # Crear tabla, th para encabezados y tr para resto de filas
        table = list()
        row_data = ""
        # Recorrer bucle en las etiquetas tr del html
        for row in soup.find_all('tr'):
            # Encontrar etiquetas th, de encabezado
            cells = row.find_all('th')
            if cells:
                # Guardar etiquetas th en array con su contenido si existe
                row_data = [cell.text for cell in cells]
            else:
                # Si no existe buscar las etiquetas td y guardarlas en array si existe
                cells = row.find_all('td')
                if cells:
                    row_data = [cell.text for cell in cells]
            # Añadir contenido a la matriz
            table.append(row_data)

        # Formato tabla SQL
        result = tabulate(table, headers='firstrow', tablefmt='psql')

        # Ventana con resultado
        newWindow = self.nuevaVentana("Detector de tablas html", any, result)
        Button(newWindow, text="Guardar", command= lambda: self.guardarTabla(result), relief="sunken").pack()
        
    def guardarTabla(self, result):
        # Guardar ruta de resultado
        file_path = filedialog.asksaveasfilename(initialdir="C:/", title="Rostro", filetypes=[("Archivos TXT",".txt")])
        
        # Crear txt
        with open(file_path + ".txt", 'w') as f:
            # Guardar archivo
            f.write(result) 
    
    # Abrir una nueva ventana con un nuevo resultado
    def nuevaVentana(self, title, image, result):
        # Nueva Ventana
        newWindow = Toplevel(window)
    
        # Titulo de la ventana
        newWindow.title(title)
        newWindow.config(bg="green")
        
        # Cargar la imagen en la pantalla
        if (image != any):
            label_image = Label(newWindow, image=image)
            label_image.image = image  # Almacenar una referencia a la imagen
            label_image.pack(side="top")
        # Cargar el texto en la pantalla
        text = Text(newWindow, bg="green")
        # Cambiar color de fondo
        text.configure(bg=window.cget('bg'))
        # Desabilitar edicion de texto, para que solo sea subrayable
        text.configure(state="disabled")
        text.pack()
        return newWindow
    
    # Transformar una imagen leida con cv2 a que la pueda interpretar tkinter 
    def transformCV2ToTkinter(self, image, isNotQR):
        # Si no es un QR porque da fallo la que devuelve el metodo de QR porque esta en escala de grises
        if (isNotQR):
            blue,green,red = cv2.split(image)
            image = cv2.merge((red,green,blue))
        # Transformar imagen
        im = Image.fromarray(image)
        imgResult = ImageTk.PhotoImage(image=im)
        return imgResult

# Crear aplicación
window = Tk()
app = Application(window)
app.mainloop()
