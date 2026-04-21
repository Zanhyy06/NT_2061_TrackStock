import sys
sys.stdout.reconfigure(encoding="utf-8")
import os
import pandas as pd

# ---------------------------------------------
#  HU 5 — Agrupación y resumen de datos
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


def separador(titulo: str) -> None:
    print("\n" + "=" * 55)
    print(f"  {titulo}")
    print("=" * 55)


if __name__ == "__main__":
    df = cargar_datos()

    # -- Columnas derivadas --
    df["dominio_correo"] = (
        df["correo"]
        .fillna("")
        .str.extract(r"@(.+)$")[0]
        .fillna("sin_correo")
    )
    df["ciudad"] = (
        df["direccion"]
        .fillna("")
        .str.extract(r",\s*(.+)$")[0]
        .str.strip()
        .fillna("Sin ciudad")
    )

    # -- Agrupación 1: por tipo (Proveedor / Cliente) --
    separador("AGRUPACIÓN 1 — Usuarios por tipo")
    g1 = (
        df.groupby("tipo", as_index=False)
        .agg(cantidad=("id_usuario", "count"))
    )
    g1["porcentaje (%)"] = (g1["cantidad"] / g1["cantidad"].sum() * 100).round(2)
    print(g1.to_string(index=False))

    # -- Agrupación 2: por dominio de correo --
    separador("AGRUPACIÓN 2 — Usuarios por dominio de correo")
    g2 = (
        df.groupby("dominio_correo", as_index=False)
        .agg(cantidad=("id_usuario", "count"))
        .sort_values("cantidad", ascending=False)
    )
    print(g2.to_string(index=False))

    # -- Agrupación 3: por tipo Y ciudad (top 5 ciudades) --
    separador("AGRUPACIÓN 3 — Conteo por ciudad (Top 5)")
    g3 = (
        df.groupby("ciudad", as_index=False)
        .agg(
            total=("id_usuario", "count"),
            proveedores=("tipo", lambda x: (x == "Proveedor").sum()),
            clientes=("tipo", lambda x: (x == "Cliente").sum()),
        )
        .sort_values("total", ascending=False)
        .head(5)
    )
    print(g3.to_string(index=False))

    # -- Agrupación 4: estadísticas de id_usuario por tipo --
    separador("AGRUPACIÓN 4 — Estadísticas de id_usuario por tipo")
    g4 = (
        df.groupby("tipo")["id_usuario"]
        .agg(["count", "min", "max", "mean"])
        .rename(columns={"count": "total", "min": "id_min",
                         "max": "id_max", "mean": "id_promedio"})
        .round(2)
    )
    print(g4.to_string())

    print("\n[OK] Análisis de agrupación completado.")
