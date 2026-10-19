import json
import os

ARCHIVO_DATOS = "estudiantes_upn.json"
MAX_ESTUDIANTES = 100

TIPOS_TRAMITE = [
    "Constancia de estudios",
    "Solicitud de beca",
    "Reserva de matrícula",
    "Retiro de universidad",
    "Solicitud de certificados",
    "Actualización de datos",
    "Reclamo académico",
    "Solicitud de cambio de carrera",
    "Retiro de curso",
    "Otros trámites"
]


def cargar_estudiantes():
    """Carga los registros guardados; si el archivo no existe, inicia una lista vacía."""
    if not os.path.exists(ARCHIVO_DATOS):
        return []
    try:
        with open(ARCHIVO_DATOS, "r", encoding="utf-8") as archivo:
            datos = json.load(archivo)
        if isinstance(datos, list):
            return datos
        print("Advertencia: el archivo no contiene una lista válida. Se iniciará vacío.")
        return []
    except (json.JSONDecodeError, OSError):
        print("Advertencia: no se pudo leer el archivo. Se iniciará una lista vacía.")
        return []


def guardar_estudiantes(estudiantes):
    """Guarda los registros en un archivo JSON para conservarlos entre ejecuciones."""
    try:
        with open(ARCHIVO_DATOS, "w", encoding="utf-8") as archivo:
            json.dump(estudiantes, archivo, ensure_ascii=False, indent=4)
        return True
    except OSError:
        print("Error: no se pudieron guardar los datos.")
        return False


def leer_texto(mensaje):
    """Solicita texto no vacío y elimina espacios sobrantes."""
    while True:
        valor = input(mensaje).strip()
        if valor:
            return valor
        print("El campo no puede quedar vacío. Inténtelo nuevamente.")


def seleccionar_tramite():
    """Muestra los tipos de trámite y valida la opción elegida."""
    print("\nTIPOS DE TRÁMITE")
    for indice, tramite in enumerate(TIPOS_TRAMITE, start=1):
        print(f"{indice}. {tramite}")
    while True:
        try:
            opcion = int(input(f"Seleccione un trámite (1-{len(TIPOS_TRAMITE)}): "))
            if 1 <= opcion <= len(TIPOS_TRAMITE):
                return TIPOS_TRAMITE[opcion - 1]
            print(f"Opción fuera de rango. Elija un número del 1 al {len(TIPOS_TRAMITE)}.")
        except ValueError:
            print("Ingrese un número entero válido.")


def registrar_estudiante(estudiantes):
    """Registra un estudiante y el trámite asociado a su código."""
    if len(estudiantes) >= MAX_ESTUDIANTES:
        print("No se pueden registrar más estudiantes: se alcanzó el límite.")
        return

    codigo_estudiante = leer_texto("Código de estudiante UPN: ").upper()
    if any(estudiante["codigo_estudiante"] == codigo_estudiante
           for estudiante in estudiantes):
        print("Error: ya existe un registro con ese código de estudiante.")
        return

    nombre = leer_texto("Nombre completo del estudiante: ")
    tramite = seleccionar_tramite()
    descripcion = leer_texto("Descripción breve del trámite: ")

    estudiante = {
        "codigo_estudiante": codigo_estudiante,
        "nombre": nombre,
        "tramite": tramite,
        "descripcion": descripcion
    }
    estudiantes.append(estudiante)

    if guardar_estudiantes(estudiantes):
        print("Registro del estudiante guardado correctamente.")
    else:
        estudiantes.pop()
        print("El registro no se confirmó porque no pudo guardarse.")


def buscar_estudiante(estudiantes):
    """Busca el registro de un estudiante mediante su código."""
    codigo_estudiante = leer_texto("Ingrese el código de estudiante que desea buscar: ").upper()
    for estudiante in estudiantes:
        if estudiante["codigo_estudiante"] == codigo_estudiante:
            mostrar_estudiante(estudiante)
            return
    print("No se encontró ningún registro para ese código de estudiante.")


def mostrar_estudiante(estudiante):
    print("\n--- DATOS DEL ESTUDIANTE / TRÁMITE ---")
    print(f"Código de estudiante: {estudiante['codigo_estudiante']}")
    print(f"Nombre:               {estudiante['nombre']}")
    print(f"Trámite:              {estudiante['tramite']}")
    print(f"Descripción:          {estudiante['descripcion']}")


def mostrar_estudiantes(estudiantes):
    """Muestra todos los registros disponibles."""
    if not estudiantes:
        print("Todavía no hay estudiantes registrados.")
        return
    print("\n--- REGISTROS DE ESTUDIANTES ---")
    for estudiante in estudiantes:
        mostrar_estudiante(estudiante)
    print(f"\nTotal de registros: {len(estudiantes)}")


def ordenar_estudiantes(estudiantes):
    """Ordena los registros por código de estudiante y guarda el nuevo orden."""
    estudiantes.sort(key=lambda estudiante: estudiante["codigo_estudiante"])
    if guardar_estudiantes(estudiantes):
        print("Registros ordenados por código de estudiante y guardados correctamente.")
    mostrar_estudiantes(estudiantes)


def menu():
    estudiantes = cargar_estudiantes()
    while True:
        print("\n======================================")
        print(" MESA DE PARTES DIGITAL UNIVERSITARIA")
        print("                 UPN")
        print("======================================")
        print("1. Registrar estudiante y trámite")
        print("2. Buscar por código de estudiante")
        print("3. Ordenar por código de estudiante")
        print("4. Mostrar todos los registros")
        print("5. Salir")
        opcion = input("Seleccione una opción (1-5): ").strip()

        if opcion == "1":
            registrar_estudiante(estudiantes)
        elif opcion == "2":
            buscar_estudiante(estudiantes)
        elif opcion == "3":
            ordenar_estudiantes(estudiantes)
        elif opcion == "4":
            mostrar_estudiantes(estudiantes)
        elif opcion == "5":
            print("Gracias por utilizar la Mesa de Partes Digital UPN.")
            break
        else:
            print("Opción inválida. Seleccione un número del 1 al 5.")


if __name__ == "__main__":
    menu()
