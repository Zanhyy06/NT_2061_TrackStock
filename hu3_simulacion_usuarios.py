import sys
sys.stdout.reconfigure(encoding="utf-8")
import random
import json
import pandas as pd
from datetime import datetime

# ---------------------------------------------
#  HU 3 — Simulación y exportación de datos
#  Tabla: USUARIO
# ---------------------------------------------

TIPOS = ["Proveedor", "Cliente"]

NOMBRES_EMPRESAS = [
    "Distribuciones Andinas", "Comercial del Norte", "Suministros Globales",
    "Importadora del Valle", "Proveedores Unidos", "TechSupply SAS",
    "Logística Express", "Mercantil del Sur", "Abastecedores Nacionales",
    "Grupo Comercial XYZ", "Inversiones Omega", "Soluciones Empresariales",
    "Distribuidora Latina", "Almacenes Progreso", "Red de Proveedores",
    "Corporación Integral", "Servicios y Bienes SA", "Cadena de Valor SAS",
    "Nexo Comercial", "GlobalTrade Colombia",
]

DOMINIOS_CORREO = ["gmail.com", "hotmail.com", "empresa.co", "outlook.com", "yahoo.com"]

CIUDADES = [
    "Medellín", "Bogotá", "Cali", "Barranquilla", "Cartagena",
    "Pereira", "Manizales", "Bucaramanga", "Cúcuta", "Ibagué",
]

TIPO_VIAS = ["Calle", "Carrera", "Avenida", "Diagonal", "Transversal"]


def _empresa_aleatoria() -> str:
    base = random.choice(NOMBRES_EMPRESAS)
    sufijo = random.choice(["", " SAS", " SA", " Ltda", " & Cía", " Corp"])
    return base + sufijo


def _nit_aleatorio() -> str:
    numero = random.randint(800_000_000, 999_999_999)
    digito = random.randint(0, 9)
    return f"{numero}-{digito}"


def _telefono_aleatorio() -> str:
    prefijos = ["300", "301", "310", "311", "312", "313", "314", "315",
                "316", "317", "318", "319", "320", "321", "350"]
    return random.choice(prefijos) + str(random.randint(1_000_000, 9_999_999))


def _correo_aleatorio(nombre_empresa: str) -> str:
    slug = nombre_empresa.lower().replace(" ", "").replace("&", "")[:12]
    dominio = random.choice(DOMINIOS_CORREO)
    return f"{slug}@{dominio}"


def _direccion_aleatoria() -> str:
    via = random.choice(TIPO_VIAS)
    num1 = random.randint(1, 120)
    num2 = random.randint(1, 99)
    num3 = random.randint(1, 99)
    ciudad = random.choice(CIUDADES)
    return f"{via} {num1} #{num2}-{num3}, {ciudad}"


def generar_usuarios(cantidad: int = 1000) -> list[dict]:
    """Genera `cantidad` registros sintéticos para la tabla USUARIO."""
    usuarios = []
    for i in range(1, cantidad + 1):
        empresa = _empresa_aleatoria()
        usuario = {
            "id_usuario": i,
            "tipo": random.choice(TIPOS),
            "nombre_empresa": empresa,
            "documento_nit": _nit_aleatorio(),
            "telefono": _telefono_aleatorio(),
            "correo": _correo_aleatorio(empresa),
            "direccion": _direccion_aleatoria(),
        }

        # -- Errores controlados (≈30 % de los registros) --
        prob = random.random()
        if prob < 0.05:
            usuario["correo"] = None
        elif prob < 0.10:
            usuario["telefono"] = None
        elif prob < 0.15:
            usuario["tipo"] = random.choice(["proveedor", "cliente", "OTRO", None])
        elif prob < 0.20:
            usuario["documento_nit"] = None
        elif prob < 0.25:
            usuario["nombre_empresa"] = "  " + empresa.upper() + "  "
        elif prob < 0.30:
            usuario["direccion"] = None

        usuarios.append(usuario)

    return usuarios


def exportar(usuarios: list[dict], csv_path: str, json_path: str) -> None:
    df = pd.DataFrame(usuarios)

    df.to_csv(csv_path, index=False, encoding="utf-8")
    print(f"[OK] CSV exportado -> {csv_path}  ({len(df)} filas)")

    with open(json_path, "w", encoding="utf-8") as f:
        json.dump(usuarios, f, ensure_ascii=False, indent=2, default=str)
    print(f"[OK] JSON exportado -> {json_path}  ({len(usuarios)} registros)")

    return df


if __name__ == "__main__":
    random.seed(42)
    datos = generar_usuarios(1200)
    df = exportar(datos, "usuarios.csv", "usuarios.json")

    print("\n-- Vista previa --")
    print(df.head(5).to_string(index=False))
    print(f"\nTotal registros : {len(df)}")
    print(f"Total columnas  : {len(df.columns)}")
    print(f"Columnas        : {list(df.columns)}")
