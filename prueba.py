import smbus
import time
import struct
import math

# Configura la dirección I2C del esclavo (el Arduino)
I2C_SLAVE_ADDRESS = 0x08

# Inicia el bus I2C
bus = smbus.SMBus(1)

modo = 12;

def leer_arduino():
    while True:
        try:
            # Solicita 4 bytes del esclavo
            data = bus.read_i2c_block_data(I2C_SLAVE_ADDRESS, 0, 4)
            # Convierte los 4 bytes a un float
            float_data = struct.unpack('f', bytes(data))[0]
            return float_data
        except Exception as e:
            print(f"Error: {str(e)}, reintentando...")
            time.sleep(1)  # Espera un segundo antes de reintentar

def escribir_arduino(comando):
    try:
        bus.write_byte(I2C_SLAVE_ADDRESS, comando)
    except Exception as e:
        print(f"Error al enviar: {str(e)}")

def seleccionar_modo():
    valor = None  # Inicializa valor a None
    escribir_arduino(1)
    while True:
        try:
            valor = leer_arduino()
            print(valor)
            #if valor != 0:
            #    break  # Sale del bucle si se recibe un valor diferente de 0
            time.sleep(1)
        except Exception as e:
            print(f"Error: {str(e)}")
    return valor  # Devuelve el valor recibido


def seleccionar_modo_encoder():
    valor = None  # Inicializa valor a None
    escribir_arduino(1)
    while True:
        try:
            valor = leer_arduino()
            print(valor)
            if math.isnan(valor):
                break  # Sale del bucle si el valor es NaN
        except Exception as e:
            print(f"Error: {str(e)}")
    # Vuelve a leer el valor para obtener la última posición
    time.sleep(0.3)
    escribir_arduino(1)
    try:
        valor = leer_arduino()
        print(f"Última posición: {valor}")
    except Exception as e:
        print(f"Error al leer la última posición: {str(e)}")

    return valor  # Devuelve el valor recibido

def recolectar_medidas():
    while True:
        medidas = {'tension': None, 'corriente': None, 'potencia': None}

        if modo >= 0 and modo <=5:
            # Envía un comando para obtener tensión
            try:
                escribir_arduino(20)
                medidas['tension'] = leer_arduino()
            except Exception as e:
                print(f"Error al leer tensión: {str(e)}")

            # Envía un comando para obtener corriente
            try:
                escribir_arduino(21)
                medidas['corriente'] = leer_arduino()
            except Exception as e:
                print(f"Error al leer corriente: {str(e)}")

            # Envía un comando para obtener potencia
            try:
                escribir_arduino(22)
                medidas['potencia'] = leer_arduino()
            except Exception as e:
                print(f"Error al leer potencia: {str(e)}")

        elif modo >= 6 and modo <=11:

            # Envía un comando para obtener tensión
            try:
                escribir_arduino(23)
                medidas['tension'] = leer_arduino()
            except Exception as e:
                medidas['tension'] = 0

            # Envía un comando para obtener corriente
            try:
                escribir_arduino(24)
                medidas['corriente'] = leer_arduino()
            except Exception as e:
                medidas['corriente'] = 0

            # Envía un comando para obtener potencia
            try:
                escribir_arduino(25)
                medidas['potencia'] = leer_arduino()
            except Exception as e:
                medidas['potencia'] = 0

        print(f"Medidas: {medidas}")

        time.sleep(1)  # Espera antes de volver a tomar las medidas

while True:
        eleccion = input("[1] Elegir Modo, [2] Recolectar Datos: ")
        if eleccion == '1':
                modo = seleccionar_modo_encoder()
                print(f"El modo seleccionado es el {modo}")

        elif eleccion == '2':
                recolectar_medidas()

