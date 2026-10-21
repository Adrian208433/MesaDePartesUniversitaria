import json
import os
import re

ARCHIVO_DATOS = "postulantes_upn.json"

# Carreras disponibles
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
    """Carga los postulantes guardados en JSON."""
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
    """Guarda los postulantes en JSON."""
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

        print("Error: este campo no puede quedar vacio. Intentelo de nuevo.")


def leer_nombre():
    """Valida nombres y apellidos: solo letras y espacios."""
    while True:
        nombre = input("Ingrese los nombres y apellidos: ").strip()

        # Permite letras Unicode, espacios y nombres compuestos.
        if nombre and all(
            caracter.isalpha() or caracter.isspace()
            for caracter in nombre
        ):
            return nombre

        print(
            "Error: el nombre solo debe contener letras y espacios. "
            "Ingrese los nombres y apellidos nuevamente."
        )


def leer_correo(postulantes):
    """Valida el formato y la unicidad del correo."""
    while True:
        correo = input("Ingrese el correo electronico: ").strip().lower()

        patron = r"^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}$"

        if not re.fullmatch(patron, correo):
            print("Error: ingrese un correo valido, por ejemplo usuario@gmail.com.")
            continue

        if any(p.get("correo", "").lower() == correo for p in postulantes):
            print("Error: ese correo ya se encuentra registrado.")
            continue

        return correo


def leer_telefono(postulantes):
    """Valida que el telefono tenga nueve digitos."""
    while True:
        telefono = input("Ingrese el numero de telefono (9 digitos): ").strip()

        if not telefono.isdigit() or len(telefono) != 9:
            print(
                "Error: el telefono debe contener exactamente 9 digitos. "
                "Intentelo de nuevo."
            )
            continue

        if any(p.get("telefono") == telefono for p in postulantes):
            print("Error: ese telefono ya se encuentra registrado.")
            continue

        return telefono


def leer_dni(postulantes):
    """Valida el DNI y evita duplicados."""
    while True:
        dni = input("Ingrese el DNI (8 digitos): ").strip()

        if not dni.isdigit() or len(dni) != 8:
            print("Error: el DNI debe contener exactamente 8 digitos.")
            continue

        if any(p.get("dni") == dni for p in postulantes):
            print("Error: ese DNI ya se encuentra registrado.")
            continue

        return dni


def seleccionar_opcion(titulo, opciones):
    """Muestra opciones y valida la seleccion."""
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

            print("Opcion fuera de rango. Intentelo de nuevo.")

        except ValueError:
            print("Error: ingrese un numero entero valido.")


def registrar_postulante(postulantes):
    """Registra a una persona interesada en ingresar a la UPN."""

    print("\n=== REGISTRO DE NUEVO POSTULANTE ===")

    correo = leer_correo(postulantes)
    telefono = leer_telefono(postulantes)
    nombre = leer_nombre()
    dni = leer_dni(postulantes)

    carrera = seleccionar_opcion("CARRERAS DISPONIBLES", CARRERAS)
    modalidad = seleccionar_opcion(
        "MODALIDADES DE ADMISION",
        MODALIDADES
    )

    postulante = {
        "correo": correo,
        "telefono": telefono,
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
    """Busca un postulante por correo electronico."""

    if not postulantes:
        print("No hay postulantes registrados.")
        return

    correo = input(
        "Ingrese el correo del postulante que desea buscar: "
    ).strip().lower()

    for postulante in postulantes:
        if postulante.get("correo", "").lower() == correo:
            print("\n=== POSTULANTE ENCONTRADO ===")
            mostrar_postulante(postulante)
            return

    print("No se encontro ningun postulante con ese correo.")


def ordenar_postulantes(postulantes):
    """Ordena los postulantes por correo electronico."""

    if len(postulantes) < 2:
        print("Se necesitan al menos dos postulantes para ordenar.")
        return

    copia_original = postulantes.copy()
    postulantes.sort(key=lambda p: p.get("correo", "").lower())

    if guardar_postulantes(postulantes):
        print("Postulantes ordenados por correo correctamente.")
    else:
        postulantes[:] = copia_original
        print("Advertencia: no se pudo guardar el nuevo orden.")


def mostrar_postulante(postulante):
    """Muestra los datos de un postulante."""

    print("-----------------------------------")
    print(f"Correo:              {postulante.get('correo', 'No registrado')}")
    print(f"Telefono:            {postulante.get('telefono', 'No registrado')}")
    print(f"Nombre:              {postulante.get('nombre', 'No registrado')}")
    print(f"DNI:                 {postulante.get('dni', 'No registrado')}")
    print(f"Carrera elegida:     {postulante.get('carrera', 'No registrada')}")
    print(f"Modalidad de ingreso: {postulante.get('modalidad', 'No registrada')}")
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
    """Muestra el menu principal."""

    print("\n======================================")
    print(" SISTEMA DE ADMISION UNIVERSITARIA")
    print("                  UPN")
    print("======================================")
    print("1. Registrar nuevo postulante")
    print("2. Buscar postulante por correo")
    print("3. Ordenar postulantes por correo")
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
