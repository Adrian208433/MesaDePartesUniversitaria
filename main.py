import json
import os
import re

ARCHIVO_DATOS = "solicitudes_upn.json"

TIPOS_TRAMITE = [
    "Constancia de estudios",
    "Certificado de estudios",
    "Solicitud de traslado",
    "Reserva de matricula",
    "Reincorporacion academica",
    "Retiro de ciclo",
    "Solicitud de beca",
    "Solicitud de examen sustitutorio",
    "Solicitud de cambio de carrera",
    "Otros"
]


def cargar_solicitudes():
    if os.path.exists(ARCHIVO_DATOS):
        try:
            with open(ARCHIVO_DATOS, "r", encoding="utf-8") as archivo:
                datos = json.load(archivo)
                return datos if isinstance(datos, list) else []
        except (json.JSONDecodeError, OSError):
            print("Error al cargar los datos.")
    return []


def guardar_solicitudes(solicitudes):
    try:
        with open(ARCHIVO_DATOS, "w", encoding="utf-8") as archivo:
            json.dump(solicitudes, archivo, indent=4, ensure_ascii=False)
    except OSError:
        print("Error al guardar las solicitudes.")


def registrar_solicitud(solicitudes):
    while True:
        codigo = input(
            "\nIngrese su correo institucional UPN: "
        ).strip().upper()

        if not re.fullmatch(r"N[0-9]{8}@UPN\.PE", codigo):
            print("Error: use el formato N00543593@upn.pe.")
            continue

        if any(s["codigo"] == codigo for s in solicitudes):
            print("Error: el correo institucional ya esta registrado.")
            continue

        while True:
            estudiante = input(
                "Ingrese el nombre completo del estudiante: "
            ).strip()

            if not 3 <= len(estudiante) <= 60:
                print("Error: el nombre debe tener entre 3 y 60 caracteres.")
                continue

            if not re.fullmatch(
                r"[^\W\d_]+(?:\s+[^\W\d_]+)*",
                estudiante,
                re.UNICODE
            ):
                print("Error: use solamente letras y espacios.")
                continue

            break

        while True:
            print("\n=== TIPOS DE TRAMITE DISPONIBLES ===")

            for i, tipo in enumerate(TIPOS_TRAMITE, start=1):
                print(f"{i}. {tipo}")

            try:
                opcion = int(input("Seleccione el tramite (1-10): "))

                if 1 <= opcion <= len(TIPOS_TRAMITE):
                    tramite = TIPOS_TRAMITE[opcion - 1]
                    break

                print("Opcion fuera de rango. Elija del 1 al 10.")

            except ValueError:
                print("Entrada invalida. Ingrese un numero del 1 al 10.")

        solicitudes.append({
            "codigo": codigo,
            "estudiante": estudiante,
            "tramite": tramite
        })

        guardar_solicitudes(solicitudes)

        print("\nSolicitud registrada correctamente.")
        print(f"Correo institucional: {codigo}")
        print(f"Estudiante: {estudiante}")
        print(f"Tramite: {tramite}")

        continuar = input(
            "\n¿Desea registrar otra solicitud? (s/n): "
        ).strip().lower()

        if continuar != "s":
            break


def buscar_solicitud(solicitudes):
    codigo = input(
        "Ingrese el correo institucional UPN que desea buscar: "
    ).strip().upper()

    for solicitud in solicitudes:
        if solicitud["codigo"] == codigo:
            print("\n=== SOLICITUD ENCONTRADA ===")
            print(f"Correo institucional: {solicitud['codigo']}")
            print(f"Estudiante: {solicitud['estudiante']}")
            print(f"Tipo de tramite: {solicitud['tramite']}")
            return

    print("No se encontro la solicitud.")


def ordenar_solicitudes(solicitudes):
    if len(solicitudes) < 2:
        print("Se necesitan al menos dos solicitudes.")
        return

    solicitudes.sort(key=lambda s: s["codigo"])
    guardar_solicitudes(solicitudes)
    print("Solicitudes ordenadas por correo institucional.")


def mostrar_solicitudes(solicitudes):
    if not solicitudes:
        print("No hay solicitudes registradas.")
        return

    print("\n=== SOLICITUDES UNIVERSITARIAS UPN ===")

    for solicitud in solicitudes:
        print("----------------------------")
        print(f"Correo institucional: {solicitud['codigo']}")
        print(f"Estudiante: {solicitud['estudiante']}")
        print(f"Tramite: {solicitud['tramite']}")


def mostrar_menu():
    print("\n=== MESA DE PARTES UNIVERSITARIA ===")
    print("=== Gestion de solicitudes UPN ===")
    print("1. Registrar solicitud")
    print("2. Buscar solicitud")
    print("3. Ordenar solicitudes por codigo")
    print("4. Mostrar solicitudes")
    print("5. Salir")


def main():
    solicitudes = cargar_solicitudes()

    while True:
        mostrar_menu()
        opcion = input("Seleccione una opcion: ").strip()

        if opcion == "1":
            registrar_solicitud(solicitudes)
        elif opcion == "2":
            buscar_solicitud(solicitudes)
        elif opcion == "3":
            ordenar_solicitudes(solicitudes)
        elif opcion == "4":
            mostrar_solicitudes(solicitudes)
        elif opcion == "5":
            print("Cerrando el sistema de solicitudes...")
            break
        else:
            print("Opcion no valida. Elija del 1 al 5.")


if __name__ == "__main__":
    main()