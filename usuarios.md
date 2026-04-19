# Historias de Usuario — Tabla USUARIO
**Proyecto:** TrackStock · CESDE · Nuevas Tecnologías 2026-1  
**Responsable:** Juan David Velez Londoño  

---

## Modelo de la tabla

| Campo | Tipo | Descripción |
|---|---|---|
| id_usuario | PK | Identificador único |
| tipo | ENUM | Proveedor o Cliente |
| nombre_empresa | VARCHAR | Nombre o razón social |
| documento_nit | VARCHAR | Documento de identidad o NIT |
| telefono | VARCHAR | Teléfono de contacto |
| correo | VARCHAR | Correo electrónico |
| direccion | VARCHAR | Dirección física |

---

## Orden de ejecución

```
hu3_simulacion_usuarios.py   →  genera usuarios.csv y usuarios.json
hu1_limpieza_usuarios.py     →  genera usuarios_limpios.csv
hu2_exploracion_usuarios.py
hu4_transformacion_usuarios.py
hu5_agrupacion_usuarios.py
```

---

## HU 3 — Simulación y exportación de datos
**Archivo:** `hu3_simulacion_usuarios.py`

### ¿Qué hace?
Genera un conjunto de datos sintético de **1200 registros** para la tabla USUARIO y los exporta en dos formatos.

### Lógica principal
- Crea empresas con nombres aleatorios combinando una base con sufijos (SAS, Ltda, Corp, etc.)
- Genera NITs con formato colombiano (`XXXXXXXXX-D`)
- Asigna teléfonos móviles con prefijos reales (300, 301, 310…)
- Construye correos a partir del nombre de la empresa y dominios comunes
- Genera direcciones con tipo de vía, número y ciudad colombiana

### Errores controlados (~30 % de los registros)
Con el fin de tener datos sucios para limpiar en HU 1, el script inyecta errores intencionales:

| Probabilidad | Error inyectado |
|---|---|
| 5 % | `correo` = None |
| 5 % | `telefono` = None |
| 5 % | `tipo` con valor incorrecto (`"proveedor"`, `"OTRO"`, None) |
| 5 % | `documento_nit` = None |
| 5 % | `nombre_empresa` con espacios y en mayúsculas |
| 5 % | `direccion` = None |

### Archivos generados
- `usuarios.csv` — 1200 filas, separado por comas, UTF-8
- `usuarios.json` — 1200 objetos JSON con la misma estructura

---

## HU 1 — Limpieza del set de datos
**Archivo:** `hu1_limpieza_usuarios.py`

### ¿Qué hace?
Carga `usuarios.csv`, detecta y corrige todos los problemas de calidad del dato, y exporta un dataset limpio.

### Pasos de limpieza

| Paso | Acción |
|---|---|
| 1 | Reporta la cantidad y porcentaje de nulos por columna |
| 2 | Elimina registros duplicados |
| 3 | Corrige el campo `tipo`: normaliza `"proveedor"` → `"Proveedor"`, `"cliente"` → `"Cliente"`, elimina los inválidos |
| 4 | Normaliza `nombre_empresa`: elimina espacios extra y aplica formato Title Case |
| 5 | Valida el formato del `correo`: si no contiene `@`, lo marca como nulo |
| 6 | Rellena nulos restantes con textos descriptivos (`"Sin teléfono"`, `"Sin correo"`, etc.) |

### Archivo generado
- `usuarios_limpios.csv` — dataset corregido, listo para análisis

---

## HU 2 — Descripción exploratoria con Pandas
**Archivo:** `hu2_exploracion_usuarios.py`

### ¿Qué hace?
Carga `usuarios_limpios.csv` y produce un informe exploratorio completo del dataset usando las herramientas estándar de Pandas.

### Secciones del informe

| Sección | Método usado | ¿Qué muestra? |
|---|---|---|
| 1 | `head(5)` | Primeros 5 registros |
| 2 | `tail(5)` | Últimos 5 registros |
| 3 | `info()` | Tipos de dato y conteo de no-nulos por columna |
| 4 | `describe(include='all')` | Estadísticas descriptivas (conteo, moda, frecuencia) |
| 5 | `df.shape` | Total de filas y columnas |
| 6 | `select_dtypes()` | Clasificación de columnas numéricas vs categóricas |
| 7 | `nunique()` | Cantidad de valores únicos por columna categórica |

---

## HU 4 — Transformación de datos con query()
**Archivo:** `hu4_transformacion_usuarios.py`

### ¿Qué hace?
Aplica filtros sobre el dataset limpio usando `query()` de Pandas para responder preguntas concretas de negocio.

### Consultas implementadas

| # | Pregunta de negocio | Condición |
|---|---|---|
| 1 | ¿Cuáles usuarios son Proveedores? | `tipo == 'Proveedor'` |
| 2 | ¿Qué usuarios tienen correo `@gmail.com`? | `str.endswith('@gmail.com')` |
| 3 | ¿Qué Clientes tienen id_usuario <= 600? | `tipo == 'Cliente' and id_usuario_int <= 600` |
| 4 | ¿Qué usuarios no tienen teléfono registrado? | `telefono_str == 'Sin teléfono'` |

Cada consulta muestra el DataFrame resultante y el total de registros encontrados.

---

## HU 5 — Agrupación y resumen de datos
**Archivo:** `hu5_agrupacion_usuarios.py`

### ¿Qué hace?
Agrupa el dataset limpio con `groupby()` para obtener métricas e indicadores por segmento.

### Agrupaciones implementadas

| # | Agrupación | Métricas calculadas |
|---|---|---|
| 1 | Por `tipo` (Proveedor / Cliente) | Conteo y porcentaje del total |
| 2 | Por dominio de correo (gmail, hotmail, etc.) | Conteo de usuarios por dominio |
| 3 | Por ciudad (extraída de `direccion`) | Total, proveedores y clientes — Top 5 ciudades |
| 4 | Por `tipo` sobre `id_usuario` | Mínimo, máximo, promedio e id total |

Los resultados permiten comparar segmentos y entender la composición del conjunto de usuarios registrados en TrackStock.
