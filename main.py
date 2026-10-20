import json
import os

MAX_POSTULANTES = 100
ARCHIVO_DATOS = "postulantes_upn.json"

# Carreras disponibles para los postulantes
CARRERAS = [
    "Administracion",
    "Administracion y Negocios Internacionales",
    "Arquitectura",
    "Derecho",
    "Enfermeria",
    "Ingenieria Civil",
    "Ingenieria de Sistemas Computacionales",
    "Ingenieria Industrial",
    "Medicina Humana",
    "Nutricion y Dietetica",
    "Psicologia",
    "Contabilidad y Finanzas",
    "Comunicacion y Publicidad",
    "Marketing",
    "Ingenieria Ambiental",
    "Ingenieria de Software"
]

# Modalidades de admision
MODALIDADES = [
    "Examen de admision",
    "Ingreso directo",
    "Traslado externo",
    "Primeros puestos",
    "Otra modalidad"
]


def cargar_postulantes():
    """Carga los postulantes guardados en el archivo JSON."""
    if not os.path.exists(ARCHIVO_DATOS):
        return []

    try:
        with open(ARCHIVO_DATOS, "r", encoding="utf-8") as archivo:
            datos = json.load(archivo)

        if isinstance(datos, list):
            return datos

        print("Advertencia: el archivo no contiene una lista valida.")
        return []

    except (json.JSONDecodeError, OSError):
        print("Advertencia: no se pudieron cargar los registros.")
        return []


def guardar_postulantes(postulantes):
    """Guarda los postulantes en un archivo JSON."""
    try:
        with open(ARCHIVO_DATOS, "w", encoding="utf-8") as archivo:
            json.dump(
                postulantes,
                archivo,
                ensure_ascii=False,
                indent=4
            )
        return True

    except OSError:
        print("Error: no se pudieron guardar los datos.")
        return False


def leer_texto(mensaje):
    """Solicita un texto obligatorio."""
    while True:
        texto = input(mensaje).strip()

        if texto:
            return texto

        print("Error: este campo no puede quedar vacio.")


def seleccionar_opcion(titulo, opciones):
    """Muestra una lista y valida la seleccion."""
    print(f"\n=== {titulo} ===")

    for indice, opcion in enumerate(opciones, start=1):
        print(f"{indice}. {opcion}")

    while True:
        try:
            numero = int(input(
                f"Seleccione una opcion (1-{len(opciones)}): "
            ))

            if 1 <= numero <= len(opciones):
                return opciones[numero - 1]

            print("Opcion fuera de rango.")

        except ValueError:
            print("Ingrese un numero entero valido.")


def registrar_postulante(postulantes):
    """Registra a una persona que desea ingresar a la UPN."""

    if len(postulantes) >= MAX_POSTULANTES:
        print("Se alcanzo el limite de 100 postulantes.")
        return

    print("\n=== REGISTRO DE NUEVO POSTULANTE ===")

    codigo = leer_texto("Ingrese el codigo del postulante: ").upper()

    # Validar que el codigo no exista
    for postulante in postulantes:
        if postulante["codigo"] == codigo:
            print("Error: ese codigo de postulante ya existe.")
            return

    nombre = leer_texto("Ingrese los nombres y apellidos: ")
    dni = leer_texto("Ingrese el DNI: ")

    # Validar que el DNI contenga 8 digitos
    if not dni.isdigit() or len(dni) != 8:
        print("Error: el DNI debe contener exactamente 8 digitos.")
        return

    # Evitar registrar el mismo DNI dos veces
    for postulante in postulantes:
        if postulante["dni"] == dni:
            print("Error: ese DNI ya se encuentra registrado.")
            return

    carrera = seleccionar_opcion("CARRERAS DISPONIBLES", CARRERAS)
    modalidad = seleccionar_opcion(
        "MODALIDADES DE ADMISION",
        MODALIDADES
    )

    postulante = {
        "codigo": codigo,
        "nombre": nombre,
        "dni": dni,
        "carrera": carrera,
        "modalidad": modalidad
    }

    postulantes.append(postulante)

    if guardar_postulantes(postulantes):
        print("\nPostulante registrado correctamente.")
        mostrar_postulante(postulante)
    else:
        postulantes.pop()
        print("No se pudo confirmar el registro.")


def buscar_postulante(postulantes):
    """Busca un postulante por su codigo."""

    if not postulantes:
        print("No hay postulantes registrados.")
        return

    codigo = leer_texto(
        "Ingrese el codigo del postulante que desea buscar: "
    ).upper()

    for postulante in postulantes:
        if postulante["codigo"] == codigo:
            print("\n=== POSTULANTE ENCONTRADO ===")
            mostrar_postulante(postulante)
            return

    print("No se encontro ningun postulante con ese codigo.")


def ordenar_postulantes(postulantes):
    """Ordena los postulantes por codigo."""

    if len(postulantes) < 2:
        print("Se necesitan al menos dos postulantes para ordenar.")
        return

    postulantes.sort(key=lambda p: p["codigo"])

    if guardar_postulantes(postulantes):
        print("Postulantes ordenados por codigo correctamente.")
    else:
        print("Advertencia: no se pudo guardar el nuevo orden.")


def mostrar_postulante(postulante):
    """Muestra los datos de un postulante."""

    print("-----------------------------------")
    print(f"Codigo:              {postulante['codigo']}")
    print(f"Nombre:              {postulante['nombre']}")
    print(f"DNI:                 {postulante['dni']}")
    print(f"Carrera elegida:     {postulante['carrera']}")
    print(f"Modalidad de ingreso: {postulante['modalidad']}")
    print("-----------------------------------")


def mostrar_postulantes(postulantes):
    """Muestra todos los postulantes registrados."""

    if not postulantes:
        print("Todavia no hay postulantes registrados.")
        return

    print("\n=== LISTA DE POSTULANTES UPN ===")

    for postulante in postulantes:
        mostrar_postulante(postulante)

    print(f"Total de postulantes: {len(postulantes)}")


def mostrar_menu():
    """Muestra el menu principal del sistema."""

    print("\n======================================")
    print(" SISTEMA DE ADMISION UNIVERSITARIA")
    print("                  UPN")
    print("======================================")
    print("1. Registrar nuevo postulante")
    print("2. Buscar postulante por codigo")
    print("3. Ordenar postulantes por codigo")
    print("4. Mostrar todos los postulantes")
    print("5. Salir")
    print("======================================")


def main():
    """Controla la ejecucion del sistema."""

    postulantes = cargar_postulantes()

    while True:
        mostrar_menu()
        opcion = input("Seleccione una opcion (1-5): ").strip()

        if opcion == "1":
            registrar_postulante(postulantes)

        elif opcion == "2":
            buscar_postulante(postulantes)

        elif opcion == "3":
            ordenar_postulantes(postulantes)

        elif opcion == "4":
            mostrar_postulantes(postulantes)

        elif opcion == "5":
            print("\nGracias por utilizar el sistema de admision UPN.")
            print("Cerrando el programa...")
            break

        else:
            print("Opcion invalida. Seleccione un numero del 1 al 5.")


if __name__ == "__main__":
    main()