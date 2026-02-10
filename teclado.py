import RPi.GPIO as GPIO
import time

class TecladoMatricial:
    def __init__(self, filas, columnas):
        self.filas = filas
        self.columnas = columnas

        GPIO.setmode(GPIO.BCM)

        for fila_pin in self.filas:
            GPIO.setup(fila_pin, GPIO.OUT)
            GPIO.output(fila_pin, GPIO.HIGH)

        for col_pin in self.columnas:
            GPIO.setup(col_pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)

        self.teclas = [
            ['1','2','3','A'],
            ['4','5','6','B'],
            ['7','8','9','C'],
            ['*','0','#','D']
        ]

    def leer_tecla(self):
        tecla_presionada = None
        while tecla_presionada is None:
            for i, fila_pin in enumerate(self.filas):
                GPIO.output(fila_pin, GPIO.LOW)
                for j, col_pin in enumerate(self.columnas):
                    if GPIO.input(col_pin) == GPIO.LOW:
                        tecla_presionada = self.teclas[i][j]
                        while GPIO.input(col_pin) == GPIO.LOW:
                            time.sleep(0.02)  # espera a que suelte la tecla
                        GPIO.output(fila_pin, GPIO.HIGH)
                        return tecla_presionada
                GPIO.output(fila_pin, GPIO.HIGH)
            time.sleep(0.01)

    def cleanup(self):
        GPIO.cleanup()
