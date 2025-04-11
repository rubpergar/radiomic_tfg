import nrrd
import numpy as np
from utils.utils import verificar_ruta


def leer_nrrd(ruta):
    try:
        datos, cabecera = nrrd.read(ruta)
        return datos, cabecera
    except Exception as e:
        print(f"    [!] Error al leer el archivo NRRD: {e}")
        return None, None


def normalizar_cabecera(cabecera):
    return {k: str(v) for k, v in cabecera.items() if k != 'modification_time'}


def comparar_nrrd(archivo1, archivo2):
    datos1, cabecera1 = leer_nrrd(archivo1)
    datos2, cabecera2 = leer_nrrd(archivo2)

    if datos1 is None or datos2 is None:
        return False

    datos_iguales = np.array_equal(datos1, datos2)
    cab1 = normalizar_cabecera(cabecera1)
    cab2 = normalizar_cabecera(cabecera2)
    cabeceras_iguales = cab1 == cab2

    if not cabeceras_iguales:
        print("\n    [!] Diferencias en la cabecera:")
        for clave in set(cab1.keys()).union(cab2.keys()):
            val1 = cab1.get(clave, "No está en archivo 1")
            val2 = cab2.get(clave, "No está en archivo 2")
            if val1 != val2:
                print(f"        {clave}: {val1} ≠ {val2}")

    if not datos_iguales:
        print("\n    [!] Diferencias en los datos.")

    return datos_iguales and cabeceras_iguales


def main():
    archivo1 = verificar_ruta("Introduce la ruta del primer archivo NRRD: ", ".nrrd")
    archivo2 = verificar_ruta("Introduce la ruta del segundo archivo NRRD: ", ".nrrd")

    son_iguales = comparar_nrrd(archivo1, archivo2)

    if son_iguales:
        print("\n    [√] Los archivos NRRD son idénticos.")
        input("\nPresiona ENTER cuando hayas finalizado.")
    else:
        print("\n    [X] Los archivos NRRD son diferentes.")
        input("\nPresiona ENTER cuando hayas finalizado la lectura.")


if __name__ == "__main__":
    main()
