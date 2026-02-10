import RPi.GPIO as GPIO
import time

class SensorUltrasonico:
    def __init__(self, trig_pin, echo_pin, buzzer_pin):
        self.trig_pin = trig_pin
        self.echo_pin = echo_pin
        self.buzzer_pin = buzzer_pin

        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.trig_pin, GPIO.OUT)
        GPIO.setup(self.echo_pin, GPIO.IN)
        GPIO.setup(self.buzzer_pin, GPIO.OUT)

        GPIO.output(self.trig_pin, GPIO.LOW)

    def obtener_distancia(self):
        GPIO.output(self.trig_pin, GPIO.HIGH)
        time.sleep(0.00001)
        GPIO.output(self.trig_pin, GPIO.LOW)

        while GPIO.input(self.echo_pin) == GPIO.LOW:
            pulse_start = time.time()

        while GPIO.input(self.echo_pin) == GPIO.HIGH:
            pulse_end = time.time()

        pulse_duration = pulse_end - pulse_start
        distancia = pulse_duration * 17150
        distancia = round(distancia, 2)  #Convertir a cm
        return distancia

    def activar_buzzer_alarma(self):
        GPIO.output(self.buzzer_pin, GPIO.HIGH)  #Activar buzzer

    def apagar_buzzer(self):
        GPIO.output(self.buzzer_pin, GPIO.LOW)  #Apagar buzzer

    def limpiar(self):
        GPIO.cleanup()
