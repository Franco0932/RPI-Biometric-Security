import drivers
from time import sleep

display = drivers.Lcd()

def mostrar_bienvenida():
    display.lcd_clear()
    display.lcd_display_string("   Sistema de", 1)
    display.lcd_display_string("   Seguridad", 2)
    sleep(2)
    display.lcd_clear()

def solicitar_password():
    display.lcd_clear()
    display.lcd_display_string("  Introduce el", 1)
    display.lcd_display_string("    Password", 2)
    sleep(1)

def mostrar_mensaje_error():
    display.lcd_clear()
    display.lcd_display_string("Wrong Password", 1)
    sleep(2)
    display.lcd_clear()

def desbloquear_sistema():
    display.lcd_clear()
    display.lcd_display_string("   Bienvenido", 1)
    display.lcd_display_string("  Sys Unlocked", 2)
    sleep(2)
    display.lcd_clear()

def mostrar_menu(opciones):
    display.lcd_clear()
    display.lcd_display_string(opciones[0], 1)
    display.lcd_display_string(opciones[1], 2)

def mostrar_opcion_invalida():
    display.lcd_clear()
    display.lcd_display_string("Opcion invalida", 1)
    sleep(2)
    display.lcd_clear()

def mostrar_nueva_password():
    display.lcd_clear()
    display.lcd_display_string("Introduzca", 1)
    display.lcd_display_string("Nueva password", 2)
    sleep(2)

def mostrar_cambio_exitoso():
    display.lcd_clear()
    display.lcd_display_string("Cambio", 1)
    display.lcd_display_string("Exitoso", 2)
    sleep(2)
    display.lcd_clear()

def solicitar_huella():
    display.lcd_clear()
    display.lcd_display_string(" Ingrese su", 1)
    display.lcd_display_string("   huella", 2)

def mostrar_huella_no_coincide():
    display.lcd_clear()
    display.lcd_display_string(" No coincide", 1)
    display.lcd_display_string("  la huella", 2)
    sleep(2)
    display.lcd_clear()

def mostrar_huella_registrada():
    display.lcd_clear()
    display.lcd_display_string("   Huella", 1)
    display.lcd_display_string(" Registrada", 2)
    sleep(2)
    display.lcd_clear()

def mostrar_esperar_dedo():
    display.lcd_clear()
    display.lcd_display_string("Coloque el", 1)
    display.lcd_display_string("dedo sensor", 2)
