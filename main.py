import json
from datetime import datetime, timedelta
import re
from functools import reduce
import logging
import traceback


def imprimir_linea():
    print("==================================================")


def imprimir_separador(mensaje=""):
    print("\n" + "=" * 50)
    if mensaje:
        print(f"✨ {mensaje} ✨")
    print("=" * 50)


# Función para cargar los usuarios
def cargar_usuarios(archivo):
    try:
        with open(archivo, "r") as f:
            data = json.load(f)
            dni_existentes = set()
            usuarios = {}
            for dni, nombre in data.items():
                if int(dni) not in dni_existentes:
                    usuarios[int(dni)] = nombre
                    dni_existentes.add(int(dni))
                else:
                    print(f"⚠ El DNI {dni} está duplicado y será ignorado.")
            return usuarios
    except (FileNotFoundError, json.JSONDecodeError) as e:
        logging.critical(e)
        logging.critical(traceback.format_exc())
        usuarios = {45622304: "Renzo", 4: "M"}
        guardar_usuarios(archivo, usuarios)
        return usuarios


# Función para guardar usuarios
def guardar_usuarios(archivo, usuarios):
    with open(archivo, "w") as f:
        json.dump(usuarios, f, indent=4)


# Función de autenticación de usuario
def autenticar_usuario(archivo_usuarios):
    usuarios = cargar_usuarios(archivo_usuarios)
    intentos = 0
    imprimir_separador("🔑 Ingreso al Sistema 🔑")

    while intentos < 5:
        try:
            dni_usuario = int(input("Ingresa tu ID: "))
        except ValueError as e:
            logging.error(e)
            logging.error(traceback.format_exc())
            print("⚠ El ID debe ser un número entero. Intenta de nuevo.")
            intentos += 1
            print(f"Te quedan {5 - intentos} intentos.")
            continue

        if dni_usuario in usuarios:
            imprimir_linea()
            nombre_usuario = input("Ingresa tu contraseña: ")

            while intentos < 5:
                if usuarios[dni_usuario] == nombre_usuario:
                    imprimir_linea()
                    print(f"✅ Bienvenido al Sistema {nombre_usuario}.")
                    return dni_usuario
                else:
                    print(f"❌ La contraseña es incorrecta")
                    intentos += 1
                    print(f"Te quedan {5 - intentos} intentos.")
                    if intentos < 5:
                        imprimir_linea()
                        nombre_usuario = input("Ingresa tu contraseña: ")
            break
        else:
            print(f"❌ El ID {dni_usuario} no está registrado.")
            intentos += 1
            print(f"Te quedan {5 - intentos} intentos.")
    else:
        imprimir_linea()
        print("❌ Te quedaste sin intentos, bloqueando sistema por seguridad....")
        print("⚠ El acceso fue bloqueado.")
        return None


# Funcion actualizar el archivo de la reserva
def cancelar_reserva_clientes(archivo, clientes):
    with open(archivo, "w") as f:
        json.dump(clientes, f, indent=4)


# Función para cargar clientes
def cargar_clientes(archivo):
    try:
        with open(archivo, "r") as f:
            clientes = json.load(f)
            return clientes
    except (FileNotFoundError, json.JSONDecodeError) as e:
        logging.critical(e)
        logging.critical(traceback.format_exc())
        return {}


# Función para guardar clientes
def guardar_clientes(archivo, nuevos_clientes):
    try:
        clientes_existentes = cargar_clientes(archivo)

        for dni, datos_nuevos in nuevos_clientes.items():
            dni = str(dni)
            if dni in clientes_existentes:
                reservas_existentes = clientes_existentes[dni].get("reservas", [])
                nuevas_reservas = datos_nuevos.get("reservas", [])

                for nueva_reserva in nuevas_reservas:
                    if nueva_reserva not in reservas_existentes:
                        reservas_existentes.append(nueva_reserva)

                clientes_existentes[dni]["reservas"] = reservas_existentes
            else:

                clientes_existentes[dni] = datos_nuevos

        with open(archivo, "w") as f:
            json.dump(clientes_existentes, f, indent=4)

        print("✅ Clientes guardados correctamente.")
    except Exception as e:
        logging.critical(e)
        logging.critical(traceback.format_exc())
        print(f"❌ Error al guardar clientes: {e}")


# Función para solicitar DNI
def solicitar_dni():
    try:
        dni = int(input("Por favor, ingrese el DNI: "))
        if 6 <= len(str(dni)) <= 14:
            return dni
        else:
            print("⚠ El DNI debe tener entre 6 y 14 dígitos. Intente de nuevo.")
            return solicitar_dni()  # Llamada recursiva
    except ValueError:
        print("❌ Entrada inválida. Asegúrese de ingresar solo números.")
        return solicitar_dni()  # Llamada recursiva


# Función para solicitar una fecha
def solicitar_fecha(mensaje):
    while True:
        imprimir_separador()
        fecha_str = input(f"{mensaje} (YYYY-MM-DD): ")
        try:
            fecha = datetime.strptime(fecha_str, "%Y-%m-%d")
            return fecha
        except ValueError as e:
            logging.error(e)
            logging.error(traceback.format_exc())
            print("⚠ Formato de fecha inválido. Usa 'YYYY-MM-DD'.")


# Función para mostrar el calendario de una habitación
def mostrar_calendario_habitacion(calendario, habitaciones, inicio, fin):
    imprimir_separador("📅 Mostrar Calendario 📅")

    habitacion = input(
        f"Introduce el nombre de la habitación ({', '.join(habitaciones)}): "
    )
    if habitacion not in habitaciones:
        print(f"❌ La habitación '{habitacion}' no existe.")
        return

    try:
        anio = int(input("Introduce el año: "))

        anio_inicio = inicio.year
        anio_fin = fin.year

        anos_disponibles = list(range(anio_inicio, anio_fin + 1))

        if anio not in anos_disponibles:
            print(f"❌ El año debe estar entre {anio_inicio} y {anio_fin}.")
            return
    except ValueError as e:
        logging.error(e)
        logging.error(traceback.format_exc())
        print("❌ Entrada inválida. Introduce un número entero para el año.")
        return

    imprimir_separador(f"📅 Calendario de {habitacion} para el año {anio} 📅")
    print("✔ Disponible | ❌ Ocupado\n")

    meses = [
        "Enero",
        "Febrero",
        "Marzo",
        "Abril",
        "Mayo",
        "Junio",
        "Julio",
        "Agosto",
        "Septiembre",
        "Octubre",
        "Noviembre",
        "Diciembre",
    ]

    for mes in range(1, 13):
        imprimir_separador(f"{meses[mes - 1]} {anio}")
        fechas_del_mes = [
            (fecha, estado)
            for fecha, estado in calendario[habitacion]
            if fecha.year == anio and fecha.month == mes
        ]

        if fechas_del_mes:
            semanas = []
            semana = []

            for fecha, estado in fechas_del_mes:
                semana.append(
                    f"{fecha.strftime('%Y-%m-%d')} {'✔' if estado == 'disponible' else '❌'}"
                )
                if fecha.weekday() == 6:
                    semanas.append(semana)
                    semana = []

            if semana:
                semanas.append(semana)

            for semana in semanas:
                print("  ".join(semana))
        else:
            print("No hay datos para este mes.")
    imprimir_separador()


# Función para realizar una reserva
def mostrar_habitaciones_disponibles(calendario):
    habitaciones_disponibles = [
        hab
        for hab, fechas in calendario.items()
        if any(est == "disponible" for _, est in fechas)
    ]
    if not habitaciones_disponibles:
        print("❌ No hay habitaciones disponibles.")
    else:
        print("Habitaciones disponibles:")
        # for hab in habitaciones_disponibles:
        #     print(f"  - {hab}")
    return habitaciones_disponibles


# Función para verificar si el cliente tiene una reserva en la habitación
def verificar_reserva_existente(dni, habitacion, clientes):
    if dni in clientes and habitacion in clientes[dni]["reservas"]:
        print(f"❌ Ya tienes una reserva en la habitación '{habitacion}'.")
        return True
    return False


# Función auxiliar para validar nombres y apellidos
def validar_nombre_apellido(nombre):

    return bool(re.fullmatch(r"[A-Za-zÁÉÍÓÚáéíóúÑñ ]+", nombre.strip()))


# Función para solicitar el DNI y verificar que el cliente esté registrado
def solicitar_dni_cliente(dni, clientes):
    dni = str(dni).strip()

    print(f"Buscando DNI: '{dni}'")
    #print(f"Claves en el diccionario: {list(clientes.keys())}")
    if clientes.get(dni) is None:

        while True:
            nombre = input("Introduce tu nombre: ").strip()
            if validar_nombre_apellido(nombre):
                break
            print(
                "⚠ El nombre ingresado no es válido. Solo se permiten letras y espacios."
            )

        while True:
            apellido = input("Introduce tu apellido: ").strip()
            if validar_nombre_apellido(apellido):
                break
            print(
                "⚠ El apellido ingresado no es válido. Solo se permiten letras y espacios."
            )

        clientes[dni] = {"nombre": nombre, "apellido": apellido, "reservas": []}
    return clientes


# Función para validar las fechas de entrada y salida
def validar_fechas():
    anio_inicio = 2024
    anio_fin = 2026

    # Validar fecha de entrada
    while True:
        fecha_entrada = input("Introduce la fecha de entrada (YYYY-MM-DD): ")
        try:
            fecha_entrada = datetime.strptime(fecha_entrada, "%Y-%m-%d")
            if not (anio_inicio <= fecha_entrada.year <= anio_fin):
                print(
                    f"⚠ La fecha de entrada debe estar entre {anio_inicio} y {anio_fin}."
                )
            else:
                break  # Fecha válida
        except ValueError as e:
            logging.error(e)
            logging.error(traceback.format_exc())
            print(
                "⚠ Fecha de entrada inválida. Asegúrate de usar el formato 'YYYY-MM-DD'."
            )

    # Validar fecha de salida
    while True:
        fecha_salida = input("Introduce la fecha de salida (YYYY-MM-DD): ")
        try:
            fecha_salida = datetime.strptime(fecha_salida, "%Y-%m-%d")
            if not (anio_inicio <= fecha_salida.year <= anio_fin):
                print(
                    f"⚠ La fecha de salida debe estar entre {anio_inicio} y {anio_fin}."
                )
            elif fecha_salida <= fecha_entrada:
                print("⚠ La fecha de salida debe ser posterior a la fecha de entrada.")
            else:
                break  # Fecha válida
        except ValueError as e:
            logging.error(e)
            logging.error(traceback.format_exc())
            print(
                "⚠ Fecha de salida inválida. Asegúrate de usar el formato 'YYYY-MM-DD'."
            )

    return fecha_entrada, fecha_salida


# Función para comprobar la disponibilidad de fechas en el calendario
def comprobar_disponibilidad_fechas(
    fecha_entrada, fecha_salida, habitacion, calendario
):
    fechas_a_reservar = []
    fechas_no_disponibles = []

    for fecha in (
        fecha_entrada + timedelta(days=n)
        for n in range((fecha_salida - fecha_entrada).days + 1)
    ):
        fecha_encontrada = False
        for i in range(len(calendario[habitacion])):
            if calendario[habitacion][i][0].date() == fecha.date():
                if calendario[habitacion][i][1] == "disponible":
                    fechas_a_reservar.append(fecha)
                else:
                    fechas_no_disponibles.append(fecha)
                fecha_encontrada = True
                break
        if not fecha_encontrada:
            print(
                f"🚫 La fecha {fecha.strftime('%Y-%m-%d')} no existe en el calendario de la habitación '{habitacion}'."
            )
            return None, None

    return fechas_a_reservar, fechas_no_disponibles


# Función para confirmar la reserva
def confirmar_reserva(
    fechas_a_reservar,
    habitacion,
    calendario,
    clientes,
    dni,
    fecha_entrada,
    fecha_salida,
    archivo_calendario,
):
    dni = str(dni).strip()
    while True:
        confirmar = input("¿Deseas confirmar la reserva? (s/n): ").lower()
        if confirmar == "s":
            for fecha in fechas_a_reservar:
                for i in range(len(calendario[habitacion])):
                    if calendario[habitacion][i][0].date() == fecha.date():
                        calendario[habitacion][i] = (
                            calendario[habitacion][i][0],
                            "reservado",
                        )

            precio_por_dia = tipo_habitaciones[habitacion]["precio"]
            dias = (fecha_salida - fecha_entrada).days
            monto_total = dias * precio_por_dia

            print(type("dni"), dni)

            if "reservas" not in clientes[dni]:
                clientes[dni]["reservas"] = []

            clientes[dni]["reservas"].append(
                {
                    "habitacion": habitacion,
                    "fecha_entrada": fecha_entrada.strftime("%Y-%m-%d"),
                    "fecha_salida": fecha_salida.strftime("%Y-%m-%d"),
                    "dias": (fecha_salida - fecha_entrada).days,
                    "monto_total": monto_total,
                    "fechas_reservadas": [
                        fecha.strftime("%Y-%m-%d") for fecha in fechas_a_reservar
                    ],
                }
            )

            guardar_clientes("clientes.json", clientes)
            guardar_calendario(archivo_calendario, calendario)
            print("✅ Reserva confirmada.")
            break
        elif confirmar == "n":
            print("❌ Reserva cancelada.")
            break


def buscar_reserva(archivo_clientes):
    imprimir_separador("🔍 Buscar Reserva por DNI 🔍")
    clientes = cargar_clientes(archivo_clientes)

    while True:
        try:
            dni = int(input("Introduce el DNI del cliente: "))
        except ValueError as e:
            logging.error(e)
            logging.error(traceback.format_exc())
            print("⚠ El DNI debe ser un número entero. Por favor, inténtalo de nuevo.")
            continue

        cliente = clientes.get(str(dni))
        if cliente:
            print(
                f"\n✅ Reservas encontradas para {cliente['nombre']} {cliente['apellido']} (DNI: {dni}):"
            )
            if cliente["reservas"]:
                for i, reserva in enumerate(cliente["reservas"], 1):
                    print(f"🔹 Reserva {i}:")
                    print(f"   🏨 Habitación: {reserva['habitacion']}")
                    print(f"   📅 Fecha de entrada: {reserva['fecha_entrada']}")
                    print(f"   📅 Fecha de salida: {reserva['fecha_salida']}")
                    print(f"   📆 Cantidad de días: {reserva['dias']}")
                    print(f"   💲 Monto total: {reserva['monto_total']}")
                imprimir_separador("Fin de reservas.")
            else:
                print("❌ Este cliente no tiene reservas registradas.")
            break
        else:
            print(f"❌ No se encontró ningún cliente con el DNI {dni}.")
            respuesta = (
                input("¿Deseas intentar con otro DNI? (si/no): ").strip().lower()
            )
            if respuesta == "no":
                print("Volviendo al menú principal...")
                return


# Función para convertir un objeto datetime a una cadena de texto
def fecha_a_str(fecha):
    return fecha.strftime("%Y-%m-%d")


# Función para convertir una cadena de texto a un objeto datetime
def str_a_fecha(fecha_str):
    return datetime.strptime(fecha_str, "%Y-%m-%d")


# Función para generar el calendario de habitaciones si no existe
def generar_calendario_por_habitaciones(
    inicio, fin, habitaciones, calendario_existente
):
    calendario = calendario_existente if calendario_existente else {}

    for habitacion in habitaciones:
        if habitacion not in calendario:
            calendario[habitacion] = [
                (inicio + timedelta(days=i), "disponible")
                for i in range((fin - inicio).days + 1)
            ]
    return calendario


# Función para cargar el calendario desde el archivo
def cargar_calendario(archivo_calendario):
    try:
        with open(archivo_calendario, "r") as f:
            calendario = json.load(f)
            for habitacion, fechas in calendario.items():
                for i, (fecha_str, estado) in enumerate(fechas):
                    calendario[habitacion][i] = (str_a_fecha(fecha_str), estado)
            return calendario
    except (FileNotFoundError, json.JSONDecodeError) as e:
        logging.critical(e)
        logging.critical(traceback.format_exc())
        print(
            "El archivo de calendario no existe o está dañado. Creando calendario nuevo."
        )
        return {}


# Función para guardar el calendario actualizado
def guardar_calendario(archivo_calendario, calendario):
    try:
        calendario_serializado = {
            habitacion: list(map(lambda x: (fecha_a_str(x[0]), x[1]), fechas))
            for habitacion, fechas in calendario.items()
        }

        with open(archivo_calendario, "w") as f:
            json.dump(calendario_serializado, f, indent=4)
        # print("✅ Calendario guardado correctamente.")
    except Exception as e:
        print(f"❌ Error al guardar el calendario: {e}")


# Diccionario de tipo de habitaciones
tipo_habitaciones = {
    "A101": {"tipo": "Habitación Simple", "precio": 50},
    "A102": {"tipo": "Habitación Doble", "precio": 80},
    "B101": {"tipo": "Habitación Triple", "precio": 120},
    "B102": {"tipo": "Habitación Cuádruple", "precio": 150},
}


# Función para realizar la reserva (ajustada para trabajar con el calendario persistido)
def realizar_reserva(calendario, archivo_clientes, archivo_calendario):
    imprimir_separador("🏨 Realizar Reserva 🏨")

    habitaciones_disponibles = mostrar_habitaciones_disponibles(calendario)
    if not habitaciones_disponibles:
        return

    tipos_legenda = "".join(
        [f"{hab}: {tipo_habitaciones[hab]}" for hab in habitaciones_disponibles]
    )
    for hab, datos in tipo_habitaciones.items():
        print(f"  - {hab} {datos['tipo']} - ${datos['precio']}")

    while True:
        habitacion = input("Introduce el nombre de la habitación que deseas reservar: ")
        if habitacion in habitaciones_disponibles:
            break
        else:
            print(
                f"⚠ La habitación ingresada no existe o es inválida. Por favor, intente de nuevo."
            )

    clientes = cargar_clientes(archivo_clientes)
    dni = solicitar_dni()
    clientes = solicitar_dni_cliente(dni, clientes)

    while True:
        fecha_entrada, fecha_salida = validar_fechas()
        fechas_a_reservar, fechas_no_disponibles = comprobar_disponibilidad_fechas(
            fecha_entrada, fecha_salida, habitacion, calendario
        )

        if fechas_a_reservar:
            print("\nDías disponibles para la reserva:")
            for fecha in fechas_a_reservar:
                print(f"  - {fecha.strftime('%Y-%m-%d')}")

            dias_reservados = len(fechas_a_reservar) - 1
            precio_por_dia = tipo_habitaciones[habitacion]["precio"]
            monto_total = dias_reservados * precio_por_dia
            print(
                f"💲 Monto total de la reserva de ({dias_reservados} días): ${monto_total}"
            )
            break
        else:
            print("❌ No hay días disponibles en el rango seleccionado.")
            print("   Por favor, intenta con un rango de fechas diferente.")

    confirmar_reserva(
        fechas_a_reservar,
        habitacion,
        calendario,
        clientes,
        dni,
        fecha_entrada,
        fecha_salida,
        archivo_calendario,
    )


def verificar_disponibilidad_avanzada(calendario, habitacion, fecha_inicio, fecha_fin):
    try:
        imprimir_separador(f"📋 Verificando Disponibilidad para {habitacion} 📋")

        fecha_inicio = datetime.combine(fecha_inicio, datetime.min.time())
        fecha_fin = datetime.combine(fecha_fin, datetime.max.time())

        fechas_rango = list(
            filter(lambda x: fecha_inicio <= x[0] <= fecha_fin, calendario[habitacion])
        )

        dias_disponibles = reduce(
            lambda acc, x: acc + 1 if x[1] == "disponible" else acc, fechas_rango, 0
        )

        matriz = [[fecha[0].strftime("%Y-%m-%d"), fecha[1]] for fecha in fechas_rango]

        print(
            f"Días disponibles en el rango {fecha_inicio.date()} - {fecha_fin.date()}: {dias_disponibles}"
        )
        print("Detalles de la disponibilidad:")
        for dia in matriz:
            print(
                f"Fecha: {dia[0]} - Estado: {'✔' if dia[1] == 'disponible' else '❌'}"
            )

        return dias_disponibles
    except KeyError as e:
        logging.error(e)
        logging.error(traceback.format_exc())
        print(f"⚠ La habitación '{habitacion}' no existe en el calendario.")
    except Exception as e:
        print(f"❌ Error al verificar disponibilidad: {e}")


def validar_habitacion(habitacion):
    return bool(re.fullmatch(r"[A-Z]\d{3}", habitacion.strip()))


def solicitar_habitacion(habitaciones):
    while True:
        habitacion = input(
            f"Introduce el nombre de la habitación ({', '.join(habitaciones)}): "
        ).strip()
        if validar_habitacion(habitacion) and habitacion in habitaciones:
            return habitacion
        print("⚠ Habitación inválida o no disponible.")


# Funcion de cancelar reserva
def cancelar_reserva(archivo_clientes, archivo_calendario, calendario):
    imprimir_separador("❌ Cancelar Reserva ❌")

    # Cargar los datos de los archivos
    clientes = cargar_clientes(archivo_clientes)
    calendario = cargar_calendario(archivo_calendario)

    # Buscar reservas del cliente
    while True:
        dni = solicitar_dni()
        cliente = clientes.get(str(dni))
        if cliente:
            print(
                f"\n✅ Reservas encontradas para {cliente['nombre']} {cliente['apellido']} (DNI: {dni}):"
            )
            if cliente["reservas"]:
                for i, reserva in enumerate(cliente["reservas"], 1):
                    print(f"🔹 Reserva {i}:")
                    print(f"   🏨 Habitación: {reserva['habitacion']}")
                    print(f"   📅 Fecha de entrada: {reserva['fecha_entrada']}")
                    print(f"   📅 Fecha de salida: {reserva['fecha_salida']}")
                    print(f"   📆 Cantidad de días: {reserva['dias']}")
                    print(f"   💲 Monto total: {reserva['monto_total']}")
                imprimir_separador("Fin de reservas.")
            else:
                print("❌ Este cliente no tiene reservas registradas.")
            break
        else:
            print(f"❌ No se encontró ningún cliente con el DNI {dni}.")
            respuesta = (
                input("¿Deseas intentar con otro DNI? (si/no): ").strip().lower()
            )
            if respuesta == "no":
                print("Volviendo al menú principal...")
                break

    # Solicitar selección de reserva
    seleccion = 0
    while True:
        try:
            if not cliente:
                break
            seleccion = int(input("Elige el número de la reserva que desea cancelar: "))
            if 1 <= seleccion <= len(cliente["reservas"]):
                break
            else:
                print(f"⚠ Ingresa un número entre 1 y {len(cliente['reservas'])}.")
        except ValueError as e:
            logging.error(e)
            logging.error(traceback.format_exc())
            print("⚠ Entrada inválida. Ingresa un número válido.")

    # Cancelar la reserva seleccionada
    if seleccion > 0:
        reserva_cancelada = cliente["reservas"].pop(seleccion - 1)
        habitacion = reserva_cancelada["habitacion"]

        # Actualizar las fechas en el calendario
        for fecha_str in reserva_cancelada["fechas_reservadas"]:
            fecha = datetime.strptime(fecha_str, "%Y-%m-%d")
            for i, (cal_fecha, estado) in enumerate(calendario[habitacion]):
                if cal_fecha == fecha:
                    calendario[habitacion][i] = (cal_fecha, "disponible")

        # Guardar los cambios en los archivos
        cancelar_reserva_clientes(archivo_clientes, clientes)
        guardar_calendario(archivo_calendario, calendario)

        print(
            f"✅ La reserva en la habitación {habitacion} desde {reserva_cancelada['fecha_entrada']} "
            f"hasta {reserva_cancelada['fecha_salida']} ha sido cancelada."
        )


def modificar_fechas_y_habitacion(archivo_clientes, archivo_calendario, calendario):
    imprimir_separador("✨ Modificar Reserva ✨")

    # Cargar los datos de los archivos
    clientes = cargar_clientes(archivo_clientes)
    calendario = cargar_calendario(archivo_calendario)

    # Buscar reservas del cliente
    while True:
        dni = solicitar_dni()
        cliente = clientes.get(str(dni))
        if cliente:
            print(
                f"\n✅ Reservas encontradas para {cliente['nombre']} {cliente['apellido']} (DNI: {dni}):"
            )
            if cliente["reservas"]:
                for i, reserva in enumerate(cliente["reservas"], 1):
                    print(f"🔹 Reserva {i}:")
                    print(f"   🏨 Habitación: {reserva['habitacion']}")
                    print(f"   📅 Fecha de entrada: {reserva['fecha_entrada']}")
                    print(f"   📅 Fecha de salida: {reserva['fecha_salida']}")
                    print(f"   📆 Cantidad de días: {reserva['dias']}")
                    print(f"   💲 Monto total: {reserva['monto_total']}")

                imprimir_linea()
            else:
                print("❌ Este cliente no tiene reservas registradas.")
            break
        else:
            print(f"❌ No se encontró ningún cliente con el DNI {dni}.")
            respuesta = (
                input("¿Deseas intentar con otro DNI? (si/no): ").strip().lower()
            )
            if respuesta == "no":
                print("Volviendo al menú principal...")
                break

    # Solicitar selección de reserva
    seleccion = 0
    while True:
        try:
            if not cliente:
                break
            seleccion = int(
                input("Elige el número de la reserva que desea modificar: ")
            )
            if 1 <= seleccion <= len(cliente["reservas"]):
                break
            else:
                print(f"⚠ Ingresa un número entre 1 y {len(cliente['reservas'])}.")
        except ValueError as e:
            logging.error(e)
            logging.error(traceback.format_exc())
            print("⚠ Entrada inválida. Ingresa un número válido.")

    # Eliminar la reserva seleccionada
    if seleccion > 0:
        reserva_cancelada = cliente["reservas"].pop(seleccion - 1)
        habitacion = reserva_cancelada["habitacion"]

        # Actualizar las fechas en el calendario
        for fecha_str in reserva_cancelada["fechas_reservadas"]:
            fecha = datetime.strptime(fecha_str, "%Y-%m-%d")
            for i, (cal_fecha, estado) in enumerate(calendario[habitacion]):
                if cal_fecha == fecha:
                    calendario[habitacion][i] = (cal_fecha, "disponible")

        # Guardar los cambios en los archivos
        cancelar_reserva_clientes(archivo_clientes, clientes)
        guardar_calendario(archivo_calendario, calendario)
    realizar_reserva(calendario, archivo_clientes, archivo_calendario)


def main():
    archivo_usuarios = "usuarios.json"
    archivo_clientes = "clientes.json"
    archivo_calendario = "calendario.json"
    logging.basicConfig(
        filename="error.log",
        level=logging.DEBUG,
        format="%(asctime)s - %(levelname)s - %(message)s",
    )

    dni_usuario = autenticar_usuario(archivo_usuarios)
    if dni_usuario is None:
        return

    calendario_existente = cargar_calendario(archivo_calendario)

    habitaciones = ["A101", "A102", "B101", "B102"]
    inicio = datetime(2024, 1, 1)
    fin = datetime(2026, 12, 31)
    calendario = generar_calendario_por_habitaciones(
        inicio, fin, habitaciones, calendario_existente
    )

    while True:
        imprimir_separador(" Menú de Opciones ")
        print("1. Realizar reserva")
        print("2. Cancelar reseva")
        print("3. Modificar reseva")
        print("4. Buscar reserva por DNI")
        print("5. Mostrar calendario de una habitación")
        print("6. Verificar disponibilidad en rango de fechas")
        print("7. Salir")
        opcion = input("Elige una opción: ")

        if opcion == "1":
            realizar_reserva(calendario, archivo_clientes, archivo_calendario)
        elif opcion == "2":
            cancelar_reserva(archivo_clientes, archivo_calendario, calendario)
        elif opcion == "3":
            modificar_fechas_y_habitacion(
                archivo_clientes, archivo_calendario, calendario
            )
        elif opcion == "4":
            buscar_reserva(archivo_clientes)
        elif opcion == "5":
            mostrar_calendario_habitacion(calendario, habitaciones, inicio, fin)
        elif opcion == "6":
            habitacion = solicitar_habitacion(habitaciones)
            fecha_inicio, fecha_fin = validar_fechas()
            verificar_disponibilidad_avanzada(
                calendario, habitacion, fecha_inicio, fecha_fin
            )
        elif opcion == "7":
            print("👋 Hasta pronto!")
            break
        else:
            print("⚠  Opción inválida.")


#if __name__ == "_main_":
main()