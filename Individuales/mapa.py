import tkinter as tk
from tkintermapview import TkinterMapView

def update_map():
    # Aquí puedes obtener las coordenadas de alguna fuente, como una variable, una función, etc.
    # Por ahora, simplemente supongamos que las coordenadas se almacenan en una variable llamada 'coordenadas'
    # Puedes reemplazar 'coordenadas' con la fuente real de tus coordenadas.
    coordenadas = "20.609607060772223, -103.41441576294228"
    gmap_widget.set_address(coordenadas, marker=True)
    win.after(1000, update_map)  # Actualiza las coordenadas cada segundo

win = tk.Tk()

gmap_widget = TkinterMapView(win, width=600, height=400)
gmap_widget.pack(fill='both')

gmap_widget.set_tile_server("https://a.tile.openstreetmap.org/{z}/{x}/{y}.png")  # OpenStreetMap (default)

win.geometry("600x600")
win.title("Google Map Viewer")
win.resizable(False, False)

# Comienza la actualización de las coordenadas
update_map()

win.mainloop()
