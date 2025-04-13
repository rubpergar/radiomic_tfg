import csv
from utils.utils import verificar_ruta, print_coloreado


def calcular_variacion(valor1, valor2):
    try:
        num1 = float(valor1)
        num2 = float(valor2)
        if num1 == 0:
            return print_coloreado("    [!] Indefinido (división por cero)"), None
        variacion = abs(((num2 - num1) / abs(num1)) * 100)
        return f"{variacion:.15f}%", variacion
    except ValueError:
        return "Texto o encabezado", None


def comparar_csv(archivo1, archivo2):
    diferencias = []
    valores_variacion = []

    try:
        with open(archivo1, 'r', encoding='utf-8') as f1, open(archivo2, 'r', encoding='utf-8') as f2:
            lector1 = csv.reader(f1)
            lector2 = csv.reader(f2)

            for i, (fila1, fila2) in enumerate(zip(lector1, lector2), start=1):
                if fila1 and fila2 and fila1[0] == 'diagnostics_Image-original_Hash':
                    continue

                if fila1 != fila2:
                    variaciones = []
                    for v1, v2 in zip(fila1, fila2):
                        str_var, num_var = calcular_variacion(v1, v2)
                        variaciones.append(str_var)
                        if num_var is not None:
                            valores_variacion.append(num_var)
                    diferencias.append((i, fila1, fila2, variaciones))

        if diferencias:
            print_coloreado("\n    [X] Se encontraron diferencias entre los archivos CSV:")
            for linea, fila1, fila2, variaciones in diferencias:
                print(f"\n    Línea {linea}:")
                print(f"        Archivo 1: {fila1}")
                print(f"        Archivo 2: {fila2}")
                print(f"        Variación: {variaciones}")

            promedio = sum(valores_variacion) / len(valores_variacion) if valores_variacion else 0
            print(f"\n    Total de diferencias detectadas: {len(diferencias)}")
            print(f"    Variación promedio: {promedio:.15f}%")
            print_coloreado("\n    [X] Los archivos CSV son distintos.")
            return False
        else:
            print_coloreado("\n    [√] Los archivos CSV son idénticos.")
            return True

    except Exception as e:
        print_coloreado(f"    [!] Error al comparar archivos CSV: {e}")
        return False
    

def main():
    archivo1 = verificar_ruta("Introduce la ruta del primer archivo CSV: ", ".csv")
    archivo2 = verificar_ruta("Introduce la ruta del segundo archivo CSV: ", ".csv")

    son_iguales = comparar_csv(archivo1, archivo2)

    if son_iguales:
        input("\nPresiona ENTER cuando hayas finalizado.")
    else:
        input("\nPresiona ENTER cuando hayas finalizado la lectura.")


if __name__ == "__main__":
    main()
