import time
import argparse
import questionary
from questionary import Style
from utils.utils import limpiar_consola
from scripts import (
    dicom2nrrd,
    radiomicsExtraction,
    csvComparison,
    csvStats,
    csvWork,
    dicomReader,
    nrrdComparison
)


custom_style = Style([
    ('instruction', 'fg:#ffffff bold'),    # Texto de la pregunta
    ('pointer', 'fg:#34eb9b bold'),        # Puntero (»)
    ('highlighted', 'fg:#34eb9b bold'),    # Opción resaltada
    ('separator', 'fg:#cc5454'),           # Separador
])


menu_options = [
    {"name": "Convertir DICOM a NRRD",                "value": "1"},
    {"name": "Extraer características radiómicas",    "value": "2"},
    {"name": "Unificar y normalizar CSVs",            "value": "3"},
    {"name": "Calcular estadísticas (ICC, Wilcoxon)", "value": "4"},
    questionary.Separator(line="─" * 45),
    {"name": "Leer DICOM",                            "value": "5"},
    {"name": "Comparar CSVs",                         "value": "6"},
    {"name": "Comparar NRRDs",                        "value": "7"},
    questionary.Separator(line="─" * 45),
    {"name": "Salir",                                 "value": "0"},
    questionary.Separator(line=" " * 1),
]

options = {
    "1": dicom2nrrd.main,
    "2": radiomicsExtraction.main,
    "3": csvWork.main,
    "4": csvStats.main,
    "5": dicomReader.main,
    "6": csvComparison.main,
    "7": nrrdComparison.main,
}


def show_menu():
    choice = questionary.select(
        "\n ",
        choices=menu_options,
        style=custom_style,
        qmark="",
        pointer="→",
        instruction="¿QUÉ DESEAS HACER? Use las teclas de flecha para moverse, Enter para seleccionar\n",
        use_indicator=True
    ).ask()
    return choice


def parse_arguments():
    parser = argparse.ArgumentParser(description="Toolkit para características radiómicas")
    parser.add_argument("--convert", action="store_true", help="Convertir DICOM a NRRD")
    parser.add_argument("--extract", action="store_true", help="Extraer características radiómicas")
    parser.add_argument("--merge-csv", action="store_true", help="Unificar y normalizar CSVs")
    parser.add_argument("--stats", action="store_true", help="Calcular ICC y Wilcoxon")
    parser.add_argument("--read-dicom", action="store_true", help="Leer DICOM")
    parser.add_argument("--compare-csv", action="store_true", help="Comparar CSVs")
    parser.add_argument("--compare-nrrd", action="store_true", help="Comparar NRRDs")

    return parser.parse_args()


def main():
    limpiar_consola()
    args = parse_arguments()

    try:
        if args.convert:
            dicom2nrrd.main()
            return
        if args.extract:
            radiomicsExtraction.main()
            return
        if args.merge_csv:
            csvWork.main()
            return
        if args.stats:
            csvStats.main()
            return
        if args.read_dicom:
            dicomReader.main()
            return
        if args.compare_csv:
            csvComparison.main()
            return
        if args.compare_nrrd:
            nrrdComparison.main()
            return

        while True:
            try:
                choice = show_menu()
                if choice == "0" or choice is None:
                    print("\n¡Hasta luego!\n")
                    break

                try:
                    options[choice]()
                except KeyboardInterrupt:
                    print("\n\n Volviendo al menú inicial...\n")
                    time.sleep(0.4)

                limpiar_consola()

            except KeyboardInterrupt:
                print("\n¡Hasta luego!\n")
                break

    except Exception as e:
        print(f"\n    [X] Error inesperado: {e}\n")


if __name__ == "__main__":
    main()
