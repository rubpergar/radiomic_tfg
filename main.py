import argparse
import questionary
import sys
from questionary import Style
from scripts import (
    dicom2nrrd,
    radiomicsExtraction,
    csvComparison,
    csvStats,
    csvWork,
    dicomReader,
    folderStructure,
    nrrdComparison
)
from utils.utils import clear_console

# Estilo personalizado para el menú
custom_style = Style([
    ('instruction', 'fg:#ffffff bold'),    # Texto de la pregunta
    ('pointer', 'fg:#34eb9b bold'),     # Puntero (»)
    ('highlighted', 'fg:#34eb9b bold'), # Opción resaltada
    ('separator', 'fg:#cc5454'),        # Separador
])

# Opciones del menú con separadores
menu_options = [
    {"name": "Reorganizar estructura de carpetas", "value": "1"},
    {"name": "Convertir DICOM a NRRD", "value": "2"},
    {"name": "Extraer características radiómicas", "value": "3"},
    {"name": "Unificar y normalizar CSVs", "value": "4"},
    {"name": "Calcular estadísticas (ICC, Wilcoxon)", "value": "5"},
    questionary.Separator(line="─" * 45),
    {"name": "Leer DICOM", "value": "6"},
    {"name": "Comparar CSVs", "value": "7"},
    {"name": "Comparar NRRDs", "value": "8"},
    questionary.Separator(line="─" * 45),
    {"name": "Salir", "value": "0"},
    questionary.Separator(line=" " * 1),
]

options = {
    "1": folderStructure.main,
    "2": dicom2nrrd.main,
    "3": radiomicsExtraction.main,
    "4": csvWork.main,
    "5": csvStats.main,
    "6": dicomReader.main,
    "7": csvComparison.main,
    "8": nrrdComparison.main,
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

    if choice == "0" or choice is None:
        print("\n¡Hasta luego!\n")
        sys.exit(0)

    options[choice]()


def parse_arguments():
    parser = argparse.ArgumentParser(description="Toolkit para características radiómicas")
    parser.add_argument("--reorganize", action="store_true", help="Reorganizar estructura de carpetas")
    parser.add_argument("--extract", action="store_true", help="Extraer características radiómicas")
    parser.add_argument("--merge-csv", action="store_true", help="Unificar y normalizar CSVs")
    parser.add_argument("--convert", action="store_true", help="Convertir DICOM a NRRD")
    parser.add_argument("--stats", action="store_true", help="Calcular ICC y Wilcoxon") # python main.py --stats
    parser.add_argument("--read-dicom", action="store_true", help="Leer DICOM")
    parser.add_argument("--compare-csv", action="store_true", help="Comparar CSVs")
    parser.add_argument("--compare-nrrd", action="store_true", help="Comparar NRRDs")

    return parser.parse_args()


def main():
    clear_console()
    args = parse_arguments()

    if args.reorganize:
        folderStructure.main()
    elif args.convert:
        dicom2nrrd.main()
    elif args.extract:
        radiomicsExtraction.main()
    elif args.merge_csv:
        csvWork.main()
    elif args.stats:
        csvStats.main()
    elif args.read_dicom:
        dicomReader.main()
    elif args.compare_csv:
        csvComparison.main()
    elif args.compare_nrrd:
        nrrdComparison.main()
    else:
        show_menu()


if __name__ == "__main__":
    main()
