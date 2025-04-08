import argparse
import questionary
import sys
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

options = {
    "1. Reorganizar estructura de carpetas": folderStructure.main,
    "2. Convertir DICOM a NRRD": dicom2nrrd.main,
    "3. Extraer características radiómicas": radiomicsExtraction.main,
    "4. Unificar y normalizar CSVs": csvWork.main,
    "5. Calcular estadísticas (ICC, Wilcoxon)": csvStats.main,
    "6. Leer DICOM": dicomReader.main,
    "7. Comparar CSVs": csvComparison.main,
    "8. Comparar NRRDs": nrrdComparison.main,
}


def show_menu():
    choice = questionary.select(
        "\n¿Qué deseas hacer?",
        choices=list(options.keys()) + ["0. Salir"]
    ).ask()

    if choice == "0. Salir" or choice is None:
        print("¡Hasta luego!")
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
    args = parse_arguments()

    if args.convert:
        folderStructure.main()
    elif args.extract:
        dicom2nrrd.main()
    elif args.compare_csv:
        radiomicsExtraction.main()
    elif args.merge_csv:
        csvWork.main()
    elif args.stats:
        csvStats.main()
    elif args.read_dicom:
        dicomReader.main()
    elif args.reorganize:
        csvComparison.main()
    elif args.compare_nrrd:
        nrrdComparison.main()
    else:
        show_menu()


if __name__ == "__main__":
    main()
