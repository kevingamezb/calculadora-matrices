# main.py - Shalon León

"""
Menú principal de la calculadora de matrices.

Este archivo es la "carita" del programa: NO sabe hacer matemática,
solo conversa con el usuario y delega todo el trabajo pesado a:

- Matriz   (matriz.py)      -> las operaciones de verdad
- Vector   (vector.py)      -> para el producto Matriz x Vector
- excepciones.py            -> los errores traducidos a español

Flujo general: se muestra el menú, se lee la opción, la función que
corresponde pide los datos (validando mucho), ejecuta la operación y
muestra el resultado; cualquier error previsto se muestra amable y el
menú sigue vivo.
"""

from matriz import Matriz
from vector import Vector
from excepciones import ErrorMatriz


def leer_entero(mensaje):
    """Pide un número entero positivo; repite hasta recibir uno válido."""
    while True:
        texto = input(mensaje).strip()

        try:
            valor = int(texto)

            # Cero o negativo no sirven como filas/columnas.
            if valor <= 0:
                print("  -> Debe ser un número entero mayor que 0.")
                continue

            return valor

        except ValueError:
            # int() explota con letras u otras cosas raras.
            print("  -> Entrada inválida. Escribe un número entero (ej: 3).")


def leer_fila(num_columnas):
    """
    Pide UNA fila de números separados por espacios.

    Repite hasta que: (1) la cantidad coincida con num_columnas y
    (2) todos sean números válidos (float acepta enteros y decimales).
    """
    while True:
        texto = input(
            f"    Fila ({num_columnas} valores separados por espacio): "
        ).strip()

        partes = texto.split()   # "1 2.5 -3" -> ["1", "2.5", "-3"]

        if len(partes) != num_columnas:
            print(
                f"  -> Se esperaban {num_columnas} valores, "
                f"se recibieron {len(partes)}."
            )
            continue

        try:
            return [float(x) for x in partes]

        except ValueError:
            print(
                "  -> Todos los valores deben ser números "
                "(ej: 1 2.5 -3)."
            )


def leer_matriz(nombre):
    """Conversa para armar una matriz completa y devolverla ya construida."""
    print(f"\n-- Ingresar matriz {nombre} --")

    filas = leer_entero("  Número de filas: ")
    columnas = leer_entero("  Número de columnas: ")

    # Pide una fila por vez; la clase Matriz valida al crearse, pero
    # aquí ya llegan bien formadas gracias a leer_fila.
    datos = [leer_fila(columnas) for _ in range(filas)]

    return datos


def leer_vector():
    """Pide la dimensión y sus valores, y devuelve un Vector."""
    print("\n-- Ingresar vector --")

    dimension = leer_entero("  Número de elementos: ")
    valores = leer_fila(dimension)

    return valores


def operacion_suma():
    """Opción 1: A + B usando el operador sobrecargado de Matriz."""
    a = Matriz(leer_matriz("A"))
    b = Matriz(leer_matriz("B"))
    resultado = a + b          # llama a Matriz.__add__

    print("\nResultado (A + B):")
    print(resultado.get())


def operacion_producto_matrices():
    """Opción 2: A x B con la multiplicación clásica de matrices."""
    a = Matriz(leer_matriz("A"))
    b = Matriz(leer_matriz("B"))

    resultado = a * b          # llama a Matriz.__mul__ (caso Matriz)

    print("\nResultado (A x B):")
    print(resultado.get())


def operacion_inversa():
    """Opción 3: inversa de A vía Gauss-Jordan (ver matriz.py)."""
    a = Matriz(leer_matriz("A"))

    resultado = a.inversa()    # puede lanzar MatrizNoCuadrada/Singular

    print("\nResultado (Inversa de A):")
    print(resultado.get())


def operacion_producto_matriz_vector():
    """Opción 4: A x v donde v es un vector columna."""
    a = Matriz(leer_matriz("A"))
    v = Vector(leer_vector())

    resultado = a * v          # llama a Matriz.__mul__ (caso Vector)

    print("\nResultado (A x v):")
    print(resultado.get())


def mostrar_menu():
    """Dibuja las opciones en pantalla."""
    print("\nCalculadora de Matrices SuperPro:")
    print("1. Suma Matrices")
    print("2. Producto Matrices")
    print("3. Matriz Inversa")
    print("4. Producto Matriz x Vector")
    print("5. Cerrar")


def main():
    """
    Bucle infinito del programa.

    Detalle de diseño: en lugar de un if/elif gigante, las opciones
    viven en un DICCIONARIO donde cada tecla apunta a su función.
    Agregar una opción nueva = agregar un solo renglón aquí.

    Las funciones se guardan SIN paréntesis: guardamos la función
    misma, no su resultado; se ejecutan más abajo con accion().
    """
    opciones = {
        "1": operacion_suma,
        "2": operacion_producto_matrices,
        "3": operacion_inversa,
        "4": operacion_producto_matriz_vector,
    }

    while True:
        mostrar_menu()

        opcion = input("Elige una opción (1-5): ").strip()

        if opcion == "5":
            print("\nCerrando la calculadora. ¡Hasta luego!")
            break

        accion = opciones.get(opcion)   # None si la opción no existe

        if accion is None:
            print("\n  -> Opción inválida. Elige un número entre 1 y 5.")
            continue

        try:
            accion()                    # aquí SÍ se ejecuta la función

        except ErrorMatriz as e:
            # Errores PREVISTOS por la calculadora (dimensiones incorrectas,
            # matriz singular...): su mensaje ya es útil y claro.
            print(f"\n  -> Error: {e}")

        except Exception as e:
            # Red de seguridad: cualquier imprevisto también se muestra
            # sin tumbarnos el menú.
            print(f"\n  -> Ocurrió un error inesperado: {e}")

        input("\nPresiona Enter para volver al menú...")


if __name__ == "__main__":
    main()
