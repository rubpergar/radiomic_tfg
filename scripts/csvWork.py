import os
import pandas as pd
from sklearn.preprocessing import MinMaxScaler
from utils.utils import si_o_no, verificar_ruta, print_coloreado


def leer_csvs_de_carpeta(ruta_raiz):
    datos_combinados = []

    for nombre_paciente in os.listdir(ruta_raiz):
        carpeta_paciente = os.path.join(ruta_raiz, nombre_paciente)
        if os.path.isdir(carpeta_paciente):
            archivos_csv = [f for f in os.listdir(carpeta_paciente) if f.endswith('.csv')]
            if archivos_csv:
                ruta_csv = os.path.join(carpeta_paciente, archivos_csv[0])
                df = pd.read_csv(ruta_csv, header=None)
                df.columns = ['Característica', 'Valor']
                df['Patient'] = nombre_paciente
                df = df.pivot(index='Patient', columns='Característica', values='Valor').reset_index()
                datos_combinados.append(df)
            else:
                print_coloreado(f"    [!] No se encontró ningún archivo CSV en {carpeta_paciente}")

    if datos_combinados:
        df_final = pd.concat(datos_combinados, ignore_index=True)
        ruta_salida = os.path.join(ruta_raiz, 'radiomicas_combinadas.csv')
        df_final.to_csv(ruta_salida, index=False)
        print_coloreado(f"\n    [√] Archivo combinado guardado en: '{ruta_salida}'\n")
        return ruta_salida
    else:
        print_coloreado("\n    [X] No se encontraron datos para combinar.")
        return None


def normalizar_csv(ruta_csv):
    df = pd.read_csv(ruta_csv)

    ids = df.iloc[:, 0]
    datos = df.iloc[:, 1:]

    scaler = MinMaxScaler(feature_range=(-1, 1))
    datos_normalizados = scaler.fit_transform(datos)

    df_normalizado = pd.DataFrame(datos_normalizados, columns=datos.columns)
    df_normalizado.insert(0, 'Patient', ids)

    ruta_salida = ruta_csv.replace('.csv', '_normalizado.csv')
    df_normalizado.to_csv(ruta_salida, index=False)

    print_coloreado(f"\n    [√] Datos normalizados guardados en: '{ruta_salida}'\n")
    return ruta_salida


def calcular_diferencia_pre_post(ruta_csv):
    df = pd.read_csv(ruta_csv)
    df['Patient'] = df['Patient'].astype(str)
    df['ID_Base'] = df['Patient'].str.replace(r'(_)?(-PRE|-POST)', '', regex=True).str.strip()

    df_pre = df[df['Patient'].str.contains('PRE', case=False)].copy()
    df_post = df[df['Patient'].str.contains('POST', case=False)].copy()

    df_pre['ID_Base'] = df_pre['ID_Base']
    df_post['ID_Base'] = df_post['ID_Base']

    df_merged = pd.merge(df_pre, df_post, on='ID_Base', suffixes=('_PRE', '_POST'))

    columnas_caracteristicas = [col for col in df_merged.columns if '_PRE' in col and col != 'Patient_PRE']
    diferencias = {}

    for col in columnas_caracteristicas:
        base = col.replace('_PRE', '')
        diferencias[base] = (df_merged[col] - df_merged[base + '_POST']).abs()

    df_resultado = pd.DataFrame(diferencias)
    df_resultado.insert(0, 'Patient', df_merged['ID_Base'])

    ruta_salida = ruta_csv.replace('.csv', '_diferencia.csv')
    df_resultado.to_csv(ruta_salida, index=False)

    print_coloreado(f"\n    [√] Diferencia PRE vs POST calculada y guardada en: '{ruta_salida}'\n")
    return ruta_salida


def listar_caracteristicas_por_estabilidad(ruta_diferencia):
    df = pd.read_csv(ruta_diferencia)
    df_features = df.drop(columns=['Patient'])

    desv_std = df_features.std()
    desv_std = desv_std[desv_std > 0].sort_values()

    print("\nCaracterísticas ordenadas por desviación estándar (de más estables a más variables):")
    for i, (caracteristica, valor) in enumerate(desv_std.items(), start=1):
        print(f"{i:3d}. {caracteristica:50s} → Desviación: {valor:.10f}")


def main():
    print("Los nombres pueden variar, pero el nombre de las carpetas del paciente deberán llevar")
    print("el sufijo '-PRE' y '-POST' para facilitar la idenficación de caso correspondiente:")
    print("""
    Carpeta_raiz/
    ├── Id_paciente1-POST/
    │   └── ...radiomics.csv
    ├── Id_paciente1-PRE/
    │   └── ...radiomics.csv
    ├── Id_paciente2-POST/
    │   └── ...radiomics.csv
    ├── Id_paciente2-PRE/
    │   └── ...radiomics.csv
    ...
    """)
    
    ruta_raiz = verificar_ruta("Introduce la ruta de la carpeta raíz con las carpetas de pacientes: ")

    ruta_combinada = leer_csvs_de_carpeta(ruta_raiz)

    if ruta_combinada:
        if si_o_no("¿Deseas normalizar los datos combinados? (si/no): ") == 'si':
            ruta_combinada = normalizar_csv(ruta_combinada)

        if si_o_no("¿Deseas calcular la diferencia entre tests PRE y POST? (si/no): ") == 'si':
            ruta_diferencias = calcular_diferencia_pre_post(ruta_combinada)

            if si_o_no("¿Deseas listar las características ordenadas por estabilidad? (si/no): ") == 'si':
                listar_caracteristicas_por_estabilidad(ruta_diferencias)

    print_coloreado("\n    [√] Proceso completado.")
    input("\nPresiona ENTER cuando hayas finalizado.")


if __name__ == "__main__":
    main()
