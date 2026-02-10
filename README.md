# RPI-Biometric-Security
Sistema de seguridad inteligente basado en Raspberry Pi 4 y Python. Implementa autenticación de doble factor (Teclado matricial 4x4 y Sensor biométrico AS608), monitoreo de intrusos con ultrasonido (HC-SR04) y registro de logs de eventos.

## Características Principales

**Autenticación de Doble Factor:** Requiere ingresar una contraseña numérica en un teclado matricial y validación biométrica mediante huella dactilar para desbloquear la cerradura[cite: 45, 47].
* **Modo Vigilancia (Intrusión):** Monitoreo continuo mediante sensor ultrasónico. [cite_start]Si se detecta un objeto a menos de 10 cm, se dispara una alarma sonora (Buzzer)[cite: 40, 42].
* **Interfaz de Usuario:** Menú interactivo visualizado en una pantalla LCD 16x2 para gestión del sistema .
* **Gestión Local:**
    * Cambio de contraseña.
    * Registro de nuevas huellas dactilares.
    * Re-activación del sistema de bloqueo.
* [cite_start]**Sistema de Logs:** Registro automático de eventos (fecha y hora) en un archivo de texto local (`logs del sistema.txt`) para auditoría[cite: 56].

## Hardware Requerido

El sistema utiliza los siguientes componentes electrónicos conectados a la Raspberry Pi 4[cite: 59, 61]:

| Componente | Modelo | Función | Protocolo/Conexión |
| :--- | :--- | :--- | :--- |
| **Controlador** | Raspberry Pi 4 | Unidad central de procesamiento | - |
| **Sensor Biométrico** | AS608 | Lectura y validación de huellas | UART |
| **Sensor Distancia** | HC-SR04 | Detección de presencia/intrusos | GPIO |
| **Teclado** | Matricial 4x4 | Ingreso de PIN y navegación | GPIO (Matriz) |
| **Pantalla** | LCD 16x2 | Interfaz visual de usuario | I2C |
| **Actuador** | Servo SG90 | Simulación de cerradura/chapa | PWM |
| **Alarma** | Buzzer Activo 5V | Alerta sonora de intrusión | GPIO |

## Diagrama de Conexiones (Pinout)

Las conexiones físicas a la Raspberry Pi están configuradas de la siguiente manera [cite: 474-512]:

* **Sensor Ultrasónico (HC-SR04):**
    * `Trig` -> GPIO 23 (Pin 16)
    * `Echo` -> GPIO 24 (Pin 18)
* **Buzzer:**
    * `Positivo` -> GPIO 17 (Pin 11)
* **Servo Motor (SG90):**
    * `Señal` -> GPIO 18 (Pin 12) - *PWM*
* **Lector de Huella (AS608):**
    * `TX` -> GPIO 14 (Pin 8)
    * `RX` -> GPIO 15 (Pin 10) - *UART*
* **Pantalla LCD:**
    * `SDA` -> GPIO 2 (Pin 3)
    * `SCL` -> GPIO 3 (Pin 5) - *I2C*
* **Teclado Matricial:**
    * `Filas` -> GPIO 5, 6, 13, 19
    * `Columnas` -> GPIO 12, 16, 20, 21

## Estructura del Proyecto

El código está modularizado para facilitar el mantenimiento y la programación concurrente [cite: 96-469]:

* `main.py`: Script principal. Gestiona la máquina de estados, el menú en el LCD y la lógica de autenticación.
* `huella.py`: Interfaz con la librería `pyfingerprint` para registrar y verificar huellas.
* `teclado.py`: Clase para el escaneo de filas y columnas del teclado matricial 4x4.
* `sensor_ultrasonico.py`: Controla el HC-SR04 y el Buzzer. Calcula distancias en cm.
* `servo_control.py`: Maneja el PWM (50Hz) para abrir (90°) y cerrar (0°) el servomotor.
* `lcd.py` / `drivers.py`: Controladores para la visualización de texto en la pantalla LCD vía I2C.

## Instalación y Uso

1.  **Requisitos previos:**
    * Python 3 instalado en la Raspberry Pi.
    * Habilitar interfaces I2C, Serial y GPIO en `raspi-config`.

2.  **Librerías necesarias:**
    ```bash
    pip3 install RPi.GPIO
    pip3 install spidev
    # La librería pyfingerprint requiere instalación específica desde su repo
    # Ver referencias en el código
    ```

3.  **Ejecución:**
    ```bash
    python3 main.py
    ```
    *La contraseña por defecto (si no existe archivo) es `1234`[cite: 116].
