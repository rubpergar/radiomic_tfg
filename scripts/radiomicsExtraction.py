
import os
import csv
import logging
from radiomics import featureextractor
from utils.utils import si_o_no, verificar_ruta, verificar_numero, print_coloreado


logging.getLogger('radiomics').setLevel(logging.ERROR)


def extraer_caracteristicas_radiomicas(imagen, mascara):
    print_coloreado(f"    [~] Extrayendo características radiómicas...")
    extractor = featureextractor.RadiomicsFeatureExtractor()
    caracteristicas = extractor.execute(imagen, mascara)
    return {k: v for k, v in caracteristicas.items() if 'diagnostics' not in k}


def guardar_caracteristicas_csv(caracteristicas, ruta_salida):
    with open(ruta_salida, mode='w', newline='') as archivo_csv:
        writer = csv.writer(archivo_csv)
        for clave, valor in caracteristicas.items():
            writer.writerow([clave, valor])
    print_coloreado(f"    [√] Características radiómicas guardadas en: {os.path.normpath(ruta_salida).replace(os.sep, '/')}")


def procesar_un_paciente():
    print("\nLa carpeta del paciente debe contener ambos archivos: CT y SEG (en formato .nrrd)")

    carpeta = verificar_ruta("Introduce la ruta de la carpeta del paciente: ")
    nombre = os.path.basename(os.path.normpath(carpeta))

    print("\nNota: si eliges 'si', se guardarán las características extraídas en la misma carpeta del paciente.")
    print("      si eliges 'no', las características solo se mostrarán por consola.")
    guardar = si_o_no("¿Deseas guardar los resultados en un archivo CSV? (si/no): ")
    print("")

    imagen_path = os.path.join(carpeta, f"{nombre}_CT.nrrd")
    mascara_path = os.path.join(carpeta, f"{nombre}_SEG_MASK.nrrd")

    if not os.path.exists(imagen_path) or not os.path.exists(mascara_path):
        print_coloreado("    [X] No se encontraron el archivo CT o el archivo SEG.")
        return

    caracteristicas = extraer_caracteristicas_radiomicas(imagen_path, mascara_path)

    if guardar == 'si':
        ruta_csv = os.path.join(carpeta, f"{nombre}_radiomics.csv")
        guardar_caracteristicas_csv(caracteristicas, ruta_csv)
        input("\nPresiona ENTER cuando hayas finalizado.")
    else:
        print("\n    Características extraídas:")
        for clave, valor in caracteristicas.items():
            print(f"  - {clave}: {valor}")
        print_coloreado("\n    [√] Proceso completado.")
        input("\nPresiona ENTER cuando hayas finalizado la lectura.")


def procesar_multiples_pacientes():
    print("\nCada subcarpeta debe contener ambos archivos: CT y SEG (en formato .nrrd)")
    carpeta_raiz = verificar_ruta("Introduce la ruta que contiene todas las carpetas de pacientes: ")

    for nombre_paciente in os.listdir(carpeta_raiz):
        carpeta_paciente = os.path.join(carpeta_raiz, nombre_paciente)
        if os.path.isdir(carpeta_paciente):
            imagen = os.path.join(carpeta_paciente, f"{nombre_paciente}_CT.nrrd")
            mascara = os.path.join(carpeta_paciente, f"{nombre_paciente}_SEG_MASK.nrrd")

            if os.path.exists(imagen) and os.path.exists(mascara):
                print(f"\nProcesando paciente: {nombre_paciente}")
                caracteristicas = extraer_caracteristicas_radiomicas(imagen, mascara)
                salida = os.path.join(carpeta_paciente, f"{nombre_paciente}_radiomics.csv")
                guardar_caracteristicas_csv(caracteristicas, salida)
            else:
                print_coloreado(f"    [!] Saltando {nombre_paciente}: faltan archivos CT o SEG.")
    print_coloreado("\n    [√] Proceso completado.")

    input("\nPresiona ENTER cuando hayas finalizado.")


def main():
    num_pacientes = verificar_numero("Introduce la cantidad de casos a procesar: ")

    if num_pacientes == 1:
        procesar_un_paciente()
    else:
        procesar_multiples_pacientes()


if __name__ == "__main__":
    main()
