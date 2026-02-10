import RPi.GPIO as GPIO
from lcd import *
from huella import SensorHuella
from servo_control import ServoChapa
from teclado import TecladoMatricial
from sensor_ultrasonico import SensorUltrasonico
import sys
from datetime import datetime
import time
from threading import Thread

def registrar_log(mensaje):
    ahora = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with open("logs_del_sistema.txt", "a") as archivo_log:
        archivo_log.write(f"[{ahora}] {mensaje}\n")

def leer_password():
    try:
        with open("password.txt", "r") as file:
            return file.read().strip()
    except FileNotFoundError:
        return "1234"

def guardar_password(nueva_password):
    with open("password.txt", "w") as file:
        file.write(nueva_password)

def leer_teclado(teclado, longitud=4):
    password = ""
    while len(password) < longitud:
        tecla = teclado.leer_tecla()
        if tecla == '*': 
            password = password[:-1]
        elif tecla in '0123456789ABCDEF':
            password += tecla
    return password

def manejar_menu_scroll(teclado):
    opciones = ["1.Activar Sistema", "2.Cambiar Password", "3.Registrar Huella"]
    indice = 0

    while True:
        mostrar_menu(opciones[indice:indice+2])
        tecla = teclado.leer_tecla()

        if tecla == 'A' and indice > 0:
            indice -= 1
        elif tecla == 'B' and indice < len(opciones) - 2:
            indice += 1
        elif tecla in ['1', '2', '3']:
            visibles = opciones[indice:indice+2]
            for opt in visibles:
                if opt.startswith(tecla + "."):
                    return tecla

def manejar_password():
    mostrar_bienvenida()
    password_actual = leer_password()

    try:
        sensor = SensorHuella()
        servo = ServoChapa(pin=18)
        teclado = TecladoMatricial([5,6,13,19], [12,16,20,21])
        sensor_ultrasonico = SensorUltrasonico(trig_pin=23, echo_pin=24, buzzer_pin=17)
    except Exception as e:
        registrar_log(f"ERROR: No se pudo inicializar sensor o servo - {e}")
        print(e)
        sys.exit(1)

    sistema_bloqueado = True

    # Hilo para controlar el sensor ultrasonico y el buzzer de manera continua
    def controlar_ultrasonico():
        while True:
            if sistema_bloqueado:
                distancia = sensor_ultrasonico.obtener_distancia()
                print(f"Distancia medida: {distancia} cm")
                if distancia < 10:  # Si la distancia es menor a 10 cm
                    registrar_log("Objeto cercano detectado, buzzer activado!")
                    sensor_ultrasonico.activar_buzzer_alarma()  # Alarma suena por 300 segundos
            else:
                sensor_ultrasonico.apagar_buzzer()  # Apagar buzzer si el sistema esta desbloqueado
            time.sleep(1)  # Hacer la medicion cada 1 segundo

    # Iniciar el hilo para el sensor ultrasonico
    thread_ultrasonico = Thread(target=controlar_ultrasonico)
    thread_ultrasonico.daemon = True  # Para que el hilo termine cuando el programa termine
    thread_ultrasonico.start()

    try:
        while True:
            solicitar_password()
            password_introducido = leer_teclado(teclado)

            if password_introducido == password_actual:
                registrar_log("Contraseña correcta ingresada")
                solicitar_huella()
                if sensor.verificar_huella():
                    desbloquear_sistema()
                    registrar_log("Huella verificada correctamente. Acceso concedido.")
                    servo.abrir()
                    sistema_bloqueado = False  # El sistema ahora esta desbloqueado
                    GPIO.output(sensor_ultrasonico.buzzer_pin, GPIO.LOW)

                else:
                    mostrar_huella_no_coincide()
                    registrar_log("Huella no coincide. Acceso denegado.")
                    servo.cerrar()
                    continue

                while True:
                    opcion = manejar_menu_scroll(teclado)

                    if opcion == "1":
                        registrar_log("Sistema activado. Volviendo a solicitar contraseña.")
                        print("Sistema activado. Volviendo a solicitar contrasena...")
                        servo.cerrar()
                        sistema_bloqueado = True  # El sistema se bloquea nuevamente
                        GPIO.output(sensor_ultrasonico.buzzer_pin, GPIO.LOW)
                        break

                    elif opcion == "2":
                        mostrar_nueva_password()
                        nueva_password = leer_teclado(teclado)
                        password_actual = nueva_password
                        guardar_password(nueva_password)
                        mostrar_cambio_exitoso()
                        registrar_log("Contraseña cambiada")
                        print(f"Contrasena cambiada a: {password_actual}")

                    elif opcion == "3":
                        try:
                            mostrar_esperar_dedo()
                            pos = sensor.registrar_huella()
                            registrar_log(f"Huella registrada en posicion {pos}")
                            print(f'Huella registrada en posicion {pos}')
                            mostrar_huella_registrada()
                        except Exception as e:
                            registrar_log(f"Error al registrar huella: {e}")
                            print(f'Error al registrar huella: {e}')

                    else:
                        registrar_log(f"Opcion invalida seleccionada: {opcion}")
                        mostrar_opcion_invalida()

            else:
                mostrar_mensaje_error()
                registrar_log("Intento de acceso con contraseña incorrecta")
                servo.cerrar()
    finally:
        teclado.cleanup()
        servo.cleanup()
        sensor_ultrasonico.limpiar()

if __name__ == "__main__":
    manejar_password()
