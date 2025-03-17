
import os
import shutil


def encontrar_carpeta_ct(ruta_datos):
    for subdir in os.listdir(ruta_datos):
        ruta_subdir = os.path.join(ruta_datos, subdir)
        if os.path.isdir(ruta_subdir):
            archivos = [f for f in os.listdir(ruta_subdir) if os.path.isfile(os.path.join(ruta_subdir, f))]
            if len(archivos) > 2:
                return ruta_subdir  # Retorna la primera carpeta con más de 2 archivos
    return None


def reorganizar_carpetas(ruta_base):
    for paciente in os.listdir(ruta_base):
        ruta_paciente = os.path.join(ruta_base, paciente)

        if os.path.isdir(ruta_paciente) and paciente.startswith("LUNG1-"):
            # Buscar la carpeta de datos del paciente
            for subcarpeta in os.listdir(ruta_paciente):
                ruta_datos = os.path.join(ruta_paciente, subcarpeta)

                if os.path.isdir(ruta_datos):
                    # Identificar la carpeta CT
                    ruta_ct = encontrar_carpeta_ct(ruta_datos)

                    # Identificar la carpeta SEG
                    ruta_seg = None
                    for subdir in os.listdir(ruta_datos):
                        if "Segmentation" in subdir:
                            ruta_seg = os.path.join(ruta_datos, subdir)
                            break

                    # Copiar CT
                    if ruta_ct and os.path.exists(ruta_ct):
                        shutil.copytree(ruta_ct, os.path.join(ruta_paciente, "CT"), dirs_exist_ok=True)

                    # Copiar SEG
                    if ruta_seg and os.path.exists(ruta_seg):
                        shutil.copytree(ruta_seg, os.path.join(ruta_paciente, "SEG"), dirs_exist_ok=True)

                    # Eliminar la carpeta de datos del paciente
                    shutil.rmtree(ruta_datos, ignore_errors=True)


if __name__ == "__main__":
    ruta_raiz = input("Enter the root folder: ").strip()
    if os.path.exists(ruta_raiz) and os.path.isdir(ruta_raiz):
        reorganizar_carpetas(ruta_raiz)
        print("\n-------------------------------------- Process completed --------------------------------------\n")
    else:
        print("Invalid route.")
