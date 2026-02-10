import time
from pyfingerprint.pyfingerprint import PyFingerprint, FINGERPRINT_CHARBUFFER1, FINGERPRINT_CHARBUFFER2

class SensorHuella:

    def __init__(self, puerto='/dev/ttyS0', baudrate=57600):
        try:
            self.sensor = PyFingerprint(puerto, baudrate, 0xFFFFFFFF, 0x00000000)
            if not self.sensor.verifyPassword():
                raise ValueError('La contraseña del sensor es incorrecta')
        except Exception as e:
            raise Exception('No se pudo inicializar el sensor: ' + str(e))

    def registrar_huella(self):
        print('Esperando dedo para registro...')
        while not self.sensor.readImage():
            pass

        self.sensor.convertImage(FINGERPRINT_CHARBUFFER1)

        result = self.sensor.searchTemplate()
        positionNumber = result[0]

        if positionNumber >= 0:
            raise Exception(f'Huella ya registrada en la posicion {positionNumber}')

        print('Retire el dedo')
        time.sleep(2)

        print('Coloque el mismo dedo nuevamente')
        while not self.sensor.readImage():
            pass

        self.sensor.convertImage(FINGERPRINT_CHARBUFFER2)

        if self.sensor.compareCharacteristics() == 0:
            raise Exception('Los dedos no coinciden')

        self.sensor.createTemplate()
        positionNumber = self.sensor.storeTemplate()

        return positionNumber

    def verificar_huella(self):
        print('Esperando dedo para verificacion...')
        while not self.sensor.readImage():
            pass

        self.sensor.convertImage(FINGERPRINT_CHARBUFFER1)

        result = self.sensor.searchTemplate()
        positionNumber = result[0]

        if positionNumber == -1:
            return False
        else:
            return True
