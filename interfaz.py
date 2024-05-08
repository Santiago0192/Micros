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

ser = serial.Serial('COM5',9600)
width,height = 400,400
len1,len2 = 0.85,0.3
ray = int(0.7*width/2)
x0,y0 = width/2,width/2
min_speed,max_speed = 0,220
step_speed = 20

root = Tk()

meter_font = Font(family="Tahoma",size=12,weight='normal')
temp = ser.readline()

battery_level = 100

coordinates = "0, -0"

def update_map():
    coordenadas = "20.609607060772223, -103.41441576294228"
    gmap_widget.set_address(coordenadas, marker=True)
    root.after(1000, update_map)

def update_battery_level(new_battery_level):
    global battery_level  # Usamos global para poder modificar la variable global dentro de la función
    battery_level = new_battery_level
    battery_bar['value'] = battery_level
    battery_label.config(text=f"Battery Level: {battery_level}%")
    root.after(1000, update_battery_level, new_battery_level)

def setTitles(): 
    root.title('Carrito')
    speed.itemconfig(speed.title,text='Speed')
    speed.itemconfig(speed.unit,text='KMPH')
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

#Medidor de Velocidad
meters = Frame(root,width=width,height=width,bg="white")
speed = Meter(meters,width=width,height=height)
speed.drawSpeed(min_speed,max_speed,step_speed,"Speed","KMPH")
speed.pack(side=LEFT)
meters.pack(side=LEFT, anchor=SE,fill=Y,expand=True)
setTitles()

cSpeed=Canvas(root, width=30, height=30,bg="white")
cSpeed.place(x=width*0.5,y=0.6*height)
x=Message(cSpeed, width = 100,text='')
x.place(x=0,y=0)
x.pack()

#Batería
battery_label = tk.Label(root, text=f"Battery Level: {battery_level}%")
battery_label.pack(pady=5)

battery_bar = ttk.Progressbar(root, orient='horizontal', length=200, mode='determinate')
battery_bar.pack(pady=5)

#Mapa
gmap_widget = TkinterMapView(root, width=600, height=400)
gmap_widget.pack(fill='both')
gmap_widget.set_tile_server("https://a.tile.openstreetmap.org/{z}/{x}/{y}.png")  # OpenStreetMap (default)


update_map()
update_battery_level(100)



while True:
    #update_map()
    s = ser.readline()
    s = s.decode()
    valores_texto  = s.strip().split(',')
    arr = [float(valor) for valor in valores_texto ]
    v=StringVar()
    kmph=(int)(arr[0]*30)
    speed.draw_needle(kmph)
    x.config(text=kmph)
    root.update_idletasks()
    root.update()
    update_battery_level((int)(arr[1]*30))

    print('s:   ',arr)
'''
for i in range(100):
    s = f"{i} 1"
    arr = s.split()
    v = StringVar()
    kmph = int(arr[0])
    speed.draw_needle(kmph)
    x.config(text=kmph)
    root.update_idletasks()
    root.update()
    
    if( i == 100):
        i = 0 
'''