import os
import subprocess
import SimpleITK as sitk
import numpy as np
import pydicom
from utils.utils import verificar_ruta, verificar_numero, print_coloreado


def crear_directorio(ruta):
    if not os.path.exists(ruta):
        os.makedirs(ruta)


def es_segmentacion_dicom(ruta_dicom):
    try:
        return pydicom.dcmread(ruta_dicom).Modality == "SEG"
    except Exception:
        return False


def procesar_ct(directorio_ct, salida_ct):
    print_coloreado("\n    [~] Procesando imágenes CT...")
    try:
        subprocess.run([
            "plastimatch", "convert", "--input", directorio_ct,
            "--output-img", salida_ct, "--output-type", "float"
        ], check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        print_coloreado(f"    [√] CT convertida → {os.path.normpath(salida_ct).replace(os.sep, '/')}")
        return True
    except subprocess.CalledProcessError as e:
        print_coloreado(f"    [X] Error al procesar CT: {e}")
        return False


def procesar_segmentacion(directorio_seg, ruta_ct, salida_seg):
    print_coloreado("\n    [~] Procesando segmentación...")
    archivos_seg = [os.path.join(directorio_seg, f) for f in os.listdir(directorio_seg) if f.endswith(".dcm")]
    archivos_validos = [f for f in archivos_seg if es_segmentacion_dicom(f)]

    if not archivos_validos:
        print_coloreado(f"    [X] No se encontraron archivos DICOM de segmentación válidos en {directorio_seg}")
        return False

    archivo_seg = archivos_validos[0]
    try:
        imagen_seg = sitk.ReadImage(archivo_seg)
        imagen_seg = sitk.Cast(imagen_seg, sitk.sitkUInt8)
        array_seg = sitk.GetArrayFromImage(imagen_seg)
        array_seg[array_seg > 0] = 1
        imagen_bin = sitk.GetImageFromArray(array_seg)

        imagen_ct = sitk.ReadImage(ruta_ct)
        imagen_bin.SetOrigin(imagen_ct.GetOrigin())
        imagen_bin.SetDirection(imagen_ct.GetDirection())
        imagen_bin.SetSpacing(imagen_ct.GetSpacing())

        imagen_resampleada = sitk.Resample(
            imagen_bin, imagen_ct, sitk.Transform(), sitk.sitkNearestNeighbor, 0, sitk.sitkUInt8)
        array_resampleado = sitk.GetArrayFromImage(imagen_resampleada)

        if np.sum(array_resampleado) == 0:
            print_coloreado("    [!] La máscara SEG está vacía tras el resampleo.")
        else:
            sitk.WriteImage(imagen_resampleada, salida_seg)
            print_coloreado(f"    [√] SEG convertida y reescalada → {os.path.normpath(salida_seg).replace(os.sep, '/')}")
        return True
    except Exception as e:
        print_coloreado(f"    [X] Error al procesar SEG: {e}")
        return False


def procesar_un_caso():
    directorio_ct = verificar_ruta("\nIntroduce la ruta de la carpeta con imágenes CT (dicom): ")
    directorio_seg = verificar_ruta("Introduce la ruta de la carpeta con la segmentación (dicom): ")
    directorio_salida = verificar_ruta("Introduce la ruta donde guardar los archivos convertidos: ")
    nombre_carpeta = input("Introduce el nombre de la carpeta de salida: ").strip()

    ruta_salida = os.path.join(directorio_salida, nombre_carpeta)
    crear_directorio(ruta_salida)

    salida_ct = os.path.join(ruta_salida, f"{nombre_carpeta}_CT.nrrd").replace(os.sep, '/')
    salida_seg = os.path.join(ruta_salida, f"{nombre_carpeta}_SEG_MASK.nrrd").replace(os.sep, '/')

    if procesar_ct(directorio_ct, salida_ct):
        procesar_segmentacion(directorio_seg, salida_ct, salida_seg)

    print_coloreado("\n    [√] Proceso completado.")
    input("\nPresiona ENTER cuando hayas finalizado.")

def procesar_varios_casos():
    print("\nLos nombres pueden variar, pero se espera que se haya usado la siguiente estructura de ficheros:")
    print("""
    CASOS/
    │── PACIENTE_1/
    │   │── CT/
    │   │   │── img1.dcm
    │   │   └── ...
    │   └── SEG/
    │       └── seg.dcm
    │── PACIENTE_2/
    │   │── CT/
    │   │   │── img1.dcm
    │   │   └── ...
    │   └── SEG/
    │       └── seg.dcm
    ...
    """)

    directorio_raiz = verificar_ruta("Introduce la ruta a la carpeta raíz con los casos de los pacientes a convertir: ")
    directorio_salida = verificar_ruta("Introduce la ruta de salida de la conversión: ")

    pacientes = sorted([
        os.path.join(directorio_raiz, p) for p in os.listdir(directorio_raiz)
        if os.path.isdir(os.path.join(directorio_raiz, p))
    ])

    if not pacientes:
        print_coloreado("    [X] No se encontraron carpetas de pacientes. Saliendo...")
        return

    for paciente in pacientes:
        nombre = os.path.basename(paciente)
        print(f"\nProcesando paciente: {nombre}")

        subdirs = sorted([
            os.path.join(paciente, d) for d in os.listdir(paciente)
            if os.path.isdir(os.path.join(paciente, d))
        ])

        if len(subdirs) < 2:
            print_coloreado(f"    [X] No hay suficientes subcarpetas en {paciente}. Se necesita CT y SEG.")
            continue

        ct_dir, seg_dir = subdirs[:2]
        print(f"    CT detectado en: {ct_dir}")
        print(f"    SEG detectado en: {seg_dir}")

        salida_paciente = os.path.join(directorio_salida, nombre)
        crear_directorio(salida_paciente)

        salida_ct = os.path.join(salida_paciente, f"{nombre}_CT.nrrd").replace(os.sep, '/')
        salida_seg = os.path.join(salida_paciente, f"{nombre}_SEG_MASK.nrrd").replace(os.sep, '/')

        if procesar_ct(ct_dir, salida_ct):
            procesar_segmentacion(seg_dir, salida_ct, salida_seg)

    print_coloreado("\n    [√] Proceso completado.")
    input("\nPresiona ENTER cuando hayas finalizado.")

def main():
    num_casos = verificar_numero("Introduce el número de casos a convertir: ")

    if num_casos == 1:
        procesar_un_caso()
    elif num_casos > 1:
        procesar_varios_casos()
    else:
        print_coloreado("    [X] Número no válido.")


if __name__ == "__main__":
    main()
