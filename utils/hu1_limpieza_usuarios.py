import sys
sys.stdout.reconfigure(encoding="utf-8")
import os
import pandas as pd
from utils.hu3_simulacion_usuarios import generar_usuarios

# ---------------------------------------------
#  HU 1 — Limpieza del set de datos
#  Tabla: USUARIO
# ---------------------------------------------

CSV_ENTRADA = "usuarios.csv"
CSV_SALIDA  = "usuarios_limpios.csv"

TIPOS_VALIDOS = {"proveedor": "Proveedor", "cliente": "Cliente"}


def cargar_datos(csv_path: str) -> pd.DataFrame:
    if os.path.exists(csv_path):
        df = pd.read_csv(csv_path, encoding="utf-8")
        print(f"[OK] Dataset cargado desde '{csv_path}'  ({len(df)} filas)\n")
    else:
        print(f"[AVISO] '{csv_path}' no encontrado. Generando datos de prueba...\n")
        import random
        random.seed(42)
        df = pd.DataFrame(generar_usuarios(1200))
    return df


def reportar_nulos(df: pd.DataFrame) -> None:
    print("=" * 50)
    print("1. VALORES NULOS POR COLUMNA")
    print("=" * 50)
    nulos = df.isnull().sum()
    pct   = (nulos / len(df) * 100).round(2)
    reporte = pd.DataFrame({"nulos": nulos, "porcentaje (%)": pct})
    print(reporte[reporte["nulos"] > 0].to_string())
    print(f"\nTotal celdas nulas: {nulos.sum()}\n")


def eliminar_duplicados(df: pd.DataFrame) -> pd.DataFrame:
    print("=" * 50)
    print("2. REGISTROS DUPLICADOS")
    print("=" * 50)
    antes = len(df)
    df = df.drop_duplicates()
    eliminados = antes - len(df)
    print(f"Duplicados eliminados : {eliminados}")
    print(f"Registros restantes   : {len(df)}\n")
    return df


def corregir_tipo(df: pd.DataFrame) -> pd.DataFrame:
    print("=" * 50)
    print("3. CORRECCIÓN DE CAMPO 'tipo'")
    print("=" * 50)
    antes = df["tipo"].value_counts(dropna=False).to_dict()

    df["tipo"] = (
        df["tipo"]
        .fillna("desconocido")
        .astype(str)
        .str.strip()
        .str.lower()
        .map(lambda v: TIPOS_VALIDOS.get(v, None))
    )

    invalidos = df["tipo"].isnull().sum()
    print(f"Distribución original : {antes}")
    print(f"Filas con tipo inválido/nulo -> se marcan NaN: {invalidos}")
    df = df.dropna(subset=["tipo"])
    print(f"Registros tras eliminar tipos inválidos : {len(df)}\n")
    return df


def limpiar_nombre_empresa(df: pd.DataFrame) -> pd.DataFrame:
    print("=" * 50)
    print("4. NORMALIZACIÓN DE 'nombre_empresa'")
    print("=" * 50)
    con_espacios = df["nombre_empresa"].str.strip() != df["nombre_empresa"].fillna("")
    print(f"Registros con espacios extra : {con_espacios.sum()}")
    df["nombre_empresa"] = df["nombre_empresa"].str.strip().str.title()
    print("Espacios eliminados y formato Title aplicado.\n")
    return df


def validar_correo(df: pd.DataFrame) -> pd.DataFrame:
    print("=" * 50)
    print("5. VALIDACIÓN DE FORMATO 'correo'")
    print("=" * 50)
    invalidos_mask = df["correo"].notna() & ~df["correo"].str.contains("@", na=False)
    print(f"Correos sin '@' (inválidos) : {invalidos_mask.sum()}")
    df.loc[invalidos_mask, "correo"] = None
    nulos_total = df["correo"].isnull().sum()
    print(f"Total correos nulos tras validación : {nulos_total}\n")
    return df


def rellenar_nulos_restantes(df: pd.DataFrame) -> pd.DataFrame:
    print("=" * 50)
    print("6. RELLENO DE NULOS RESTANTES")
    print("=" * 50)
    rellenos = {
        "telefono": "Sin teléfono",
        "correo":   "Sin correo",
        "direccion": "Sin dirección",
        "documento_nit": "Sin documento",
    }
    for col, valor in rellenos.items():
        n = df[col].isnull().sum()
        if n > 0:
            df[col] = df[col].fillna(valor)
            print(f"  '{col}' -> {n} nulos reemplazados por '{valor}'")
    print()
    return df


if __name__ == "__main__":
    df = cargar_datos(CSV_ENTRADA)

    print("\n-- INICIO DE LIMPIEZA --\n")
    reportar_nulos(df)

    df = eliminar_duplicados(df)
    df = corregir_tipo(df)
    df = limpiar_nombre_empresa(df)
    df = validar_correo(df)
    df = rellenar_nulos_restantes(df)

    df.to_csv(CSV_SALIDA, index=False, encoding="utf-8")
    print(f"[OK] Dataset limpio exportado -> '{CSV_SALIDA}'  ({len(df)} filas)")
