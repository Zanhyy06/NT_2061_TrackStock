import random
from datetime import datetime, timedelta

def generar_movimientos(numero_movimientos):

    tipos = ["Entrada", "Salida"]
    usuarios = [1, 2, 3, 4, 5]
    detalles = [101, 102, 103]
    fecha_inicio = datetime(2026, 1, 2)
    movimientos = []

    for _ in range(numero_movimientos):
        movimiento = {
            "id_movimiento": random.randint(1, 1000),
            "id_usuario": random.choice(usuarios),
            "id_detalle": random.choice(detalles),
            "fecha": fecha_inicio + timedelta(days=random.randint(0, 60)),
            "tipo": random.choice(tipos)
        }

        #Inyectando errores controlados
        probabilidadError = random.random()

        if probabilidadError < 0.2:
            movimiento["id_movimiento"] = None  

        elif probabilidadError < 0.4:
            movimiento["id_usuario"] = random.choice([None, -1, 9999])  

        elif probabilidadError < 0.6:
            movimiento["id_detalle"] = random.choice([None, -5, 8888]) 

        elif probabilidadError < 0.75:
            movimiento["tipo"] = random.choice(["entrada", "salida", "otro"])  

        elif probabilidadError < 0.9:
            movimiento["fecha"] = None  

        movimientos.append(movimiento)

    return movimientos