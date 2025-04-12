import os
import warnings
import pandas as pd
import pingouin as pg
from scipy.stats import wilcoxon
from utils.utils import verificar_ruta

warnings.filterwarnings("ignore", category=RuntimeWarning)


def calcular_icc(archivo_csv):
    df = pd.read_csv(archivo_csv)
    df['Patient'] = df['Patient'].astype(str)
    df['BaseID'] = df['Patient'].str.replace(r'(_)?(-PRE|-POST)', '', regex=True).str.strip()

    df_pre = df[df['Patient'].str.contains('PRE', case=False)].copy()
    df_post = df[df['Patient'].str.contains('POST', case=False)].copy()

    icc_resultados = {}
    columnas = [col for col in df.columns if col not in ['Patient', 'BaseID']]

    for columna in columnas:
        df_icc_pre = pd.DataFrame({
            'targets': df_pre['BaseID'],
            'raters': ['PRE'] * len(df_pre),
            'ratings': df_pre[columna]
        })
        df_icc_post = pd.DataFrame({
            'targets': df_post['BaseID'],
            'raters': ['POST'] * len(df_post),
            'ratings': df_post[columna]
        })

        df_completo = pd.concat([df_icc_pre, df_icc_post], ignore_index=True)

        try:
            icc = pg.intraclass_corr(data=df_completo, targets='targets', raters='raters', ratings='ratings')
            valor_icc = icc[icc['Type'] == 'ICC2']['ICC'].values[0]
            icc_resultados[columna] = valor_icc
        except Exception:
            continue

    return pd.DataFrame.from_dict(icc_resultados, orient='index', columns=['icc'])


def calcular_wilcoxon(archivo_csv):
    df = pd.read_csv(archivo_csv)
    df['Patient'] = df['Patient'].astype(str)
    df['BaseID'] = df['Patient'].str.replace(r'(_)?(-PRE|-POST)', '', regex=True).str.strip()

    df_pre = df[df['Patient'].str.contains('PRE', case=False)].copy()
    df_post = df[df['Patient'].str.contains('POST', case=False)].copy()

    pvalores = {}
    columnas = [col for col in df.columns if col not in ['Patient', 'BaseID']]

    for columna in columnas:
        try:
            estadistico, pvalor = wilcoxon(df_pre[columna], df_post[columna])
            pvalores[columna] = pvalor
        except Exception:
            continue

    return pd.DataFrame.from_dict(pvalores, orient='index', columns=['pval'])


def filtrar_caracteristicas(icc_df, pval_df, umbral_icc=0.8, umbral_pval=0.05):
    combinados = icc_df.join(pval_df)
    filtrados = combinados[
        (combinados['icc'] > umbral_icc) &
        (combinados['pval'] > umbral_pval)
    ]
    return filtrados


def main():
    ruta_archivo = verificar_ruta("Introduce la ruta del .csv normalizado con los casos PRE y POST (radiomicas_combinadas_normalizado.csv): ", ".csv")

    print("\n    [~] Calculando estadísticas de características...")

    icc_df = calcular_icc(ruta_archivo)
    pval_df = calcular_wilcoxon(ruta_archivo)

    resultado = filtrar_caracteristicas(icc_df, pval_df)

    print(f"\n    [√] Se encontraron {len(resultado)} características robustas (ICC > 0.8 y p > 0.05):")
    print(resultado)

    salida = os.path.join(os.path.dirname(ruta_archivo), 'mejores_radiomicas.csv')
    resultado.to_csv(salida)

    print(f"\n    [✓] Resultados guardados en: '{salida}'")

    input("\nPresiona ENTER cuando hayas finalizado la lectura.")

if __name__ == "__main__":
    main()
