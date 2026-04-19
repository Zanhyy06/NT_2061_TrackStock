import sys
sys.stdout.reconfigure(encoding="utf-8")
import os
import pandas as pd

# ---------------------------------------------
#  HU 4 — Transformación de datos con query()
#  Tabla: USUARIO
# ---------------------------------------------

CSV_LIMPIO = "usuarios_limpios.csv"


def cargar_datos() -> pd.DataFrame:
    if not os.path.exists(CSV_LIMPIO):
        raise FileNotFoundError(
            f"No se encontró '{CSV_LIMPIO}'. "
            "Ejecuta primero hu3_simulacion_usuarios.py y hu1_limpieza_usuarios.py."
        )
    df = pd.read_csv(CSV_LIMPIO, encoding="utf-8")
    print(f"[OK] Dataset cargado: {len(df)} registros\n")
    return df


def mostrar_resultado(titulo: str, consulta: str, df_resultado: pd.DataFrame) -> None:
    print("=" * 55)
    print(f"  {titulo}")
    print(f"  Consulta : {consulta}")
    print("=" * 55)
    print(df_resultado.to_string(index=False))
    print(f"\n  -> Total registros encontrados: {len(df_resultado)}\n")


if __name__ == "__main__":
    df = cargar_datos()

    # -- Columnas auxiliares para poder usar query() con str --
    df["correo_lower"]    = df["correo"].str.lower().fillna("")
    df["telefono_str"]    = df["telefono"].fillna("").astype(str)
    df["id_usuario_int"]  = pd.to_numeric(df["id_usuario"], errors="coerce")

    print("======================================================")
    print("  CONSULTAS CON query() — TABLA USUARIO")
    print("======================================================\n")

    # -- Consulta 1: Todos los Proveedores --
    q1 = "tipo == 'Proveedor'"
    r1 = df.query(q1)[["id_usuario", "tipo", "nombre_empresa", "documento_nit", "telefono"]]
    mostrar_resultado("CONSULTA 1 — Usuarios de tipo Proveedor", q1, r1)

    # -- Consulta 2: Correos del dominio gmail.com --
    gmail_usuarios = df[df["correo_lower"].str.endswith("@gmail.com")]
    print("=" * 55)
    print("  CONSULTA 2 — Usuarios con correo @gmail.com")
    print("  (filtro aplicado vía str.endswith sobre columna auxiliar)")
    print("=" * 55)
    r2 = gmail_usuarios[["id_usuario", "nombre_empresa", "correo"]]
    print(r2.to_string(index=False))
    print(f"\n  -> Total registros encontrados: {len(r2)}\n")

    # -- Consulta 3: Clientes con id_usuario par (≤ 600) --
    q3 = "tipo == 'Cliente' and id_usuario_int <= 600"
    r3 = df.query(q3)[["id_usuario", "tipo", "nombre_empresa", "correo", "direccion"]]
    mostrar_resultado(
        "CONSULTA 3 — Clientes con id_usuario ≤ 600",
        q3,
        r3,
    )

    # -- Consulta 4 (bonus): Usuarios sin teléfono registrado --
    sin_tel = df[df["telefono_str"].isin(["Sin teléfono", ""])]
    print("=" * 55)
    print("  CONSULTA 4 — Usuarios sin teléfono registrado")
    print("  (filtro sobre columna auxiliar 'telefono_str')")
    print("=" * 55)
    r4 = sin_tel[["id_usuario", "tipo", "nombre_empresa", "telefono"]]
    print(r4.to_string(index=False))
    print(f"\n  -> Total registros encontrados: {len(r4)}\n")
