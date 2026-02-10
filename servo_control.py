import RPi.GPIO as GPIO
import time

class ServoChapa:
    def __init__(self, pin=18):
        GPIO.setmode(GPIO.BCM)
        GPIO.setwarnings(False)
        GPIO.setup(pin, GPIO.OUT)
        self.pin = pin
        self.pwm = GPIO.PWM(pin, 50)  # 50 Hz PWM
        self.pwm.start(0)
        time.sleep(1)
        self._mover_a_angulo(0)  # Posición cerrada al inicio

    def abrir(self):
        self._mover_a_angulo(90)

    def cerrar(self):
        self._mover_a_angulo(0)

    def _mover_a_angulo(self, angulo):
        duty = angulo / 18 + 2
        GPIO.output(self.pin, True)
        self.pwm.ChangeDutyCycle(duty)
        time.sleep(0.5)
        GPIO.output(self.pin, False)
        self.pwm.ChangeDutyCycle(0)

    def cleanup(self):
        self.pwm.stop()
        GPIO.cleanup()
