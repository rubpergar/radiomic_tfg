import platform
import os


#############################################################


def si_o_no(prompt):
    while True:
        response = input(prompt).strip().lower()
        if response in ['si', 'no']:
            return response
        else:
            print("    [!] Por favor, introduce 'si' o 'no'.")


#############################################################


def limpiar_consola():
    if platform.system() == "Windows":
        os.system('cls')
    else:
        os.system('clear')


#############################################################


def verificar_ruta(prompt, extension=None):
    while True:
        ruta = input(prompt).strip()
        if not os.path.exists(ruta):
            print("    [!] La ruta no existe. Por favor, introdúcela de nuevo.")
            continue
        if extension and not ruta.lower().endswith(extension.lower()):
            print(f"    [!] El archivo no es de tipo {extension}. Por favor, introdúcelo de nuevo")
            continue
        return ruta


#############################################################


def verificar_numero(prompt):
    while True:
        try:
            valor = int(input(prompt))
            if valor >= 1:
                return valor
            print("    [!] Introduce un número entero positivo.")
        except ValueError:
            print("    [!] Entrada no válida. Por favor, introduce un número entero.")