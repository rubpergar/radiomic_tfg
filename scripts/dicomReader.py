import os
import sys
import pydicom
from utils.utils import si_o_no, verificar_ruta, print_coloreado


def leer_dicom(ruta):
    try:
        return pydicom.dcmread(ruta)
    except Exception as e:
        print_coloreado(f"\n    [!] Error al leer el archivo DICOM: {e}\n")
        return None


def exportar_a_txt(ds, ruta_salida):
    try:
        with open(ruta_salida, "w", encoding="utf-8") as f:
            f.write(str(ds))
        print_coloreado(f"\n    [√] Archivo exportado correctamente en: {ruta_salida}")
    except Exception as e:
        print_coloreado(f"\n    [!] Error al exportar el archivo: {e}\n")


def main():
    ruta_dicom = verificar_ruta("Introduce la ruta del archivo DICOM: ", ".dcm")
    ds = leer_dicom(ruta_dicom)
    if ds is None:
        sys.exit(1)

    exportar = si_o_no("\n¿Deseas exportarlo a un archivo de texto? (si/no): ")
    if exportar == "si":
        ruta_salida = verificar_ruta("\nIntroduce la ruta donde deseas guardar el archivo: ")

        nombre_archivo = os.path.basename(ruta_dicom).replace(".dcm", ".txt")
        ruta_completa = os.path.join(ruta_salida, nombre_archivo)
        exportar_a_txt(ds, ruta_completa)

    mostrar = si_o_no("\n¿Deseas mostrar el contenido por consola? (si/no): ")
    if mostrar == "si":
        print("")
        print(ds)
        input("\nPresiona ENTER cuando hayas finalizado la lectura.")


if __name__ == "__main__":
    main()
