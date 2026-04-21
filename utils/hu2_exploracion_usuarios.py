import sys
sys.stdout.reconfigure(encoding="utf-8")
import os
import pandas as pd

# ---------------------------------------------
#  HU 2 — Descripción exploratoria con Pandas
#  Tabla: USUARIO
# ---------------------------------------------

CSV_LIMPIO  = "usuarios_limpios.csv"
CSV_CRUDO   = "usuarios.csv"


def cargar_datos() -> pd.DataFrame: # sirve para cargar el dataset limpio o crudo, dependiendo de cuál esté disponible
    for ruta in (CSV_LIMPIO, CSV_CRUDO):
        if os.path.exists(ruta):
            df = pd.read_csv(ruta, encoding="utf-8")
            print(f"[OK] Dataset cargado desde '{ruta}'\n")
            return df
    raise FileNotFoundError(
        "No se encontró 'usuarios_limpios.csv' ni 'usuarios.csv'. "
        "Ejecuta primero hu3_simulacion_usuarios.py y hu1_limpieza_usuarios.py."
    )


def explorar(df: pd.DataFrame) -> None:

    print("=" * 55)
    print("1. PRIMERAS 5 FILAS  (head)")
    print("=" * 55)
    print(df.head(5).to_string(index=False))

    print("\n" + "=" * 55)
    print("2. ÚLTIMAS 5 FILAS  (tail)")
    print("=" * 55)
    print(df.tail(5).to_string(index=False))

    print("\n" + "=" * 55)
    print("3. ESTRUCTURA DEL DATAFRAME  (info)")
    print("=" * 55)
    df.info()

    print("\n" + "=" * 55)
    print("4. ESTADÍSTICAS DESCRIPTIVAS  (describe)")
    print("=" * 55)
    print(df.describe(include="all").to_string())

    print("\n" + "=" * 55)
    print("5. DIMENSIONES DEL DATASET")
    print("=" * 55)
    filas, columnas = df.shape
    print(f"  Filas    : {filas}")
    print(f"  Columnas : {columnas}")
    print(f"  Nombres  : {list(df.columns)}")

    print("\n" + "=" * 55)
    print("6. CLASIFICACIÓN DE COLUMNAS")
    print("=" * 55)
    numericas    = df.select_dtypes(include="number").columns.tolist()
    categoricas  = df.select_dtypes(exclude="number").columns.tolist()
    print(f"  Numéricas   ({len(numericas)})  : {numericas}")
    print(f"  Categóricas ({len(categoricas)}) : {categoricas}")

    print("\n" + "=" * 55)
    print("7. VALORES ÚNICOS POR COLUMNA CATEGÓRICA")
    print("=" * 55)
    for col in categoricas:
        unicos = df[col].nunique()
        print(f"  {col:<25} -> {unicos} valores únicos")


if __name__ == "__main__":
    df = cargar_datos()
    explorar(df)
