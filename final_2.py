import math
import serial
import tkinter as tk
from tkinter import ttk
from tkintermapview import TkinterMapView

try:
    from random import randrange
    from Tkinter import *
    from Tkinter.font import Font
    import Tkinter.filedialog
    import Tkinter.messagebox
except ImportError:
    from tkinter import *
    from tkinter.font import Font
    import tkinter.filedialog
    import tkinter.messagebox

#ser = serial.Serial('COM5',9600)
width,height = 400,400
len1,len2 = 0.85,0.3
ray = int(0.7*width/2)
x0,y0 = width/2,width/2
min_speed,max_speed = 0,220
step_speed = 20

battery_level = 100
coordinates = "0, -0"

root = Tk()

meter_font = Font(family="Tahoma",size=12,weight='normal')
#temp = ser.readline()

# Función para actualizar la posición del mapa
def update_map_position(latitude, longitude):
    #latitude = (float(str(latitude)[2:]))/60
    #longitude = -1*(float(str(latitude)[2:]))/60 
    gmap_widget.set_position(latitude, longitude)
    marker_1.set_position(latitude, longitude)

def update_battery_level(new_battery_level):
    global battery_level  # Usamos global para poder modificar la variable global dentro de la función
    battery_level = battery_level/5.5
    battery_level = new_battery_level
    battery_bar['value'] = battery_level
    battery_label.config(text=f"Battery Level: {battery_level}%")
    root.after(1000, update_battery_level, new_battery_level)

def setTitles(): 
    root.title('Carrito')
    speed.itemconfig(speed.title,text='Speed')
    speed.itemconfig(speed.unit,text='m/s')
    root.after(1000, setTitles)

class Meter(Canvas):

    def drawSpeed(self,vmin,vmax,step,title,unit):
        self.vmin = vmin
        self.vmax = vmax
        x0 = width/2
        y0 = width/2
        ray = int(0.7*width/2)
        self.title = self.create_text(width/2,12,fill="#000",
            font=meter_font)
        self.create_oval(x0-ray*1.1,y0-ray*1.1,x0+ray*1.1,y0+ray*1.1,
            fill="blue")
        self.create_oval(x0-ray,y0-ray,x0+ray,y0+ray,fill="#000")
        coef = 0.1
        self.create_oval(x0-ray*coef,y0-ray*coef,x0+ray*coef,y0+ray*coef,
            fill="white")

        for i in range(1+int((vmax-vmin)/step)):
            v = vmin + step*i
            angle = (5+6*((v-vmin)/(vmax-vmin)))*math.pi/4
            self.create_line(x0+ray*math.sin(angle)*0.9,
                y0 - ray*math.cos(angle)*0.9,
                x0+ray*math.sin(angle)*0.98,
                y0 - ray*math.cos(angle)*0.98,fill="#FFF",width=2)
            self.create_text(x0+ray*math.sin(angle)*0.75,
                y0 - ray*math.cos(angle)*0.75,
                text=v,fill="#FFF",font=meter_font)
            if i==int(vmax-vmin)/step:
                continue
            for dv in range(1,5):
                angle = (5+6*((v+dv*(step/5)-vmin)/(vmax-vmin)))*math.pi/4
                self.create_line(x0+ray*math.sin(angle)*0.94,
                    y0 - ray*math.cos(angle)*0.94,
                    x0+ray*math.sin(angle)*0.98,
                    y0 - ray*math.cos(angle)*0.98,fill="#FFF")
        self.unit = self.create_text(width/2,y0+0.8*ray,fill="#FFF",
            font=meter_font)
        self.needle = self.create_line(x0-ray*math.sin(5*math.pi/4)*len2,
            y0+ray*math.cos(5*math.pi/4)*len2,
            x0+ray*math.sin(5*math.pi/4)*len1,
            y0-ray*math.cos(5*math.pi/4)*len1,
            width=2,fill="#FFF")
        lb1=Label(self, compound='right', textvariable=v)

    def draw_needle(self,v):
        v = max(v,self.vmin)
        v = min(v,self.vmax)
        angle = (5+6*((v-self.vmin)/(self.vmax-self.vmin)))*math.pi/4
        self.coords(self.needle,x0-ray*math.sin(angle)*len2,
            y0+ray*math.cos(angle)*len2,
            x0+ray*math.sin(angle)*len1,
            y0-ray*math.cos(angle)*len1)

#Batería
battery_label = tk.Label(root, text=f"Porcentaje  de Bateria: {battery_level}%")
battery_label.pack(pady=5)

battery_bar = ttk.Progressbar(root, orient='horizontal', length=200, mode='determinate')
battery_bar.pack(pady=5)

#Medidor de Velocidad
meters = Frame(root,width=width,height=width,bg="white")
speed = Meter(meters,width=width,height=height)
speed.drawSpeed(min_speed,max_speed,step_speed,"Velocidad","M/S")
speed.pack(side=LEFT)
meters.pack(side=LEFT, anchor=SE,fill=Y,expand=True)
setTitles()

cSpeed=Canvas(root, width=30, height=30,bg="white")
cSpeed.place(x=width*0.5,y=0.6*height)
x=Message(cSpeed, width = 100,text='')
x.place(x=0,y=0)
x.pack()

#Mapa
gmap_widget = TkinterMapView(root, width=800, height=600, corner_radius=0)
gmap_widget.place(relx=0.5, rely=0.5, anchor=tkinter.CENTER)
gmap_widget.pack(fill='both')

# Inicialmente establece la posición del mapa
initial_latitude = 48.860381
initial_longitude = 2.338594
marker_1 = gmap_widget.set_position(initial_latitude, initial_longitude, marker=True)  # Paris, France
gmap_widget.set_zoom(30)

import random

def rpm_to_mps(rpm):
    return (2 * math.pi * .025 * rpm) / 60

def generar_array():
    registros = []
    valor_1, valor_2 = 2,2
    valor_1 = (valor_1 + 1) % 11
    valor_2 = (valor_2 + 1) % 11

    registros = [valor_1, valor_2, random.uniform(20.605, 20.600), random.uniform(-103.415, -103.420)]

    #Ejemplo
    '''103.41553295970421         #Longitud * -1
    20.604852059341194,        #Latitud
    550                        #Bateria
    5                          #PWM'''

    return registros

def update_values():
    #s = ser.readline().decode().strip()  # Leer datos del puerto serial
    #valores_texto = s.split("\n")
    #print('valores_texto',valores_texto)
    #arr = [float(valor) for valor in valores_texto]4
    # .replace(',', '')
    arr = generar_array()
    kmph = int(arr[0] * 30)

    speed.draw_needle(kmph)
    x.config(text=kmph)
    print('----------------------------')
    print('Velocidad: ',kmph,' m/s')

    # Actualizar los valores de la batería
    new_battery_level = int(arr[1] * 30)
    update_battery_level(new_battery_level)
    print('Bateria: ', new_battery_level)

    # Actualiza la posición del mapa a nuevas coordenadas
    update_map_position(arr[2], arr[3])
    print('Latitud: ', arr[2], ' Longitud:', arr[3])
    print('----------------------------')

    print(lines[0])
    # Programar la próxima actualización después de 1000 ms (1 segundo)
    root.after(2000, update_values)

# Iniciar la primera actualización
update_values()

# Iniciar el bucle principal de tkinter
root.mainloop()
