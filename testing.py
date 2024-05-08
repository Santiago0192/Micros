import serial

print('Starting...')
ser = serial.Serial('COM5', 9600)

while True:
    s = ser.readline()
    s = s.decode()
    valores_texto  = s.strip().split(',')
    valores_flotantes = [float(valor) for valor in valores_texto ]

    print('---------------')
    print('s:   ',valores_flotantes)