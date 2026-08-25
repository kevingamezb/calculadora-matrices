# main.py - Alvaro Orjuela
#
# Menú del ejercicio de ordenamiento.
#
# CÓMO EJECUTARLO: desde DENTRO de esta carpeta:
#     python main.py
#
# FLUJO GENERAL:
# 1. Pregunta cuántos números aleatorios generar y los crea.
# 2. Muestra la lista original.
# 3. Bucle infinito: ofrece los 5 métodos de ordenamiento, regenerar
#    la lista o salir; tras cada acción espera un Enter.
#
# NOTA DE DISEÑO: aquí se usa una cadena de if/elif (a diferencia del
# despacho por diccionario de la calculadora de matrices). Funciona
# igual de bien; es solo otra forma de organizar un menú.

from ordenador_numeros import OrdenadorNumeros


def leer_cantidad_numeros():
    """Pide cuántos números generar; repite hasta recibir un entero mayor que 0."""
    while True:
        texto = input("¿Cuántos números aleatorios quieres generar? ").strip()

        try:
            valor = int(texto)

            if valor <= 0:
                print("  -> Debe ser un número entero mayor que 0.")
                continue

            return valor

        except ValueError:
            print("  -> Entrada inválida. Escribe un número entero (ej: 10).")


def mostrar_lista(lista):
    """Imprime la lista bonita: cada número con 2 decimales, entre corchetes."""
    print("[" + ", ".join(f"{x:.2f}" for x in lista) + "]")


def mostrar_menu():
    """Dibuja las opciones disponibles."""
    print("\nOrdenamiento de Números Aleatorios")
    print("1. Ordenar por Burbuja")
    print("2. Ordenar por Inserción")
    print("3. Ordenar por Selección")
    print("4. Ordenar por Mergesort")
    print("5. Ordenar con sort() de Python")
    print("6. Generar una nueva lista de números")
    print("7. Cerrar")


def main():
    """Crea el objeto ordenador y atiende las opciones del menú (1-7)."""
    # ÚNICO objeto del programa: guarda la lista original y un
    # resultado por método. Cada sort trabaja "dentro" del objeto y
    # después se lee su resultado con el getter correspondiente.
    ordenador = OrdenadorNumeros()

    # Primera carga de datos.
    ordenador.cantidad = leer_cantidad_numeros()
    ordenador.generar_numeros()

    print("\nLista original:")
    mostrar_lista(ordenador.get_numeros())

    while True:
        mostrar_menu()
        opcion = input("Elige una opción (1-7): ").strip()

        # Opciones 1 a 5 comparten el mismo patrón:
        # ordenar dentro del objeto -> mostrar SU resultado.
        if opcion == "1":
            ordenador.ordenar_burbuja()
            print("\nResultado (Burbuja):")
            mostrar_lista(ordenador.get_resultado_burbuja())

        elif opcion == "2":
            ordenador.ordenar_insercion()
            print("\nResultado (Inserción):")
            mostrar_lista(ordenador.get_resultado_insercion())

        elif opcion == "3":
            ordenador.ordenar_seleccion()
            print("\nResultado (Selección):")
            mostrar_lista(ordenador.get_resultado_seleccion())

        elif opcion == "4":
            ordenador.ordenar_mergesort()
            print("\nResultado (Mergesort):")
            mostrar_lista(ordenador.get_resultado_mergesort())

        elif opcion == "5":
            ordenador.ordenar_sort_python()
            print("\nResultado (sort de Python):")
            mostrar_lista(ordenador.get_resultado_sort_python())

        # Opción 6: tirar los dados de nuevo con nueva cantidad.
        elif opcion == "6":
            ordenador.cantidad = leer_cantidad_numeros()
            ordenador.generar_numeros()
            print("\nNueva lista original:")
            mostrar_lista(ordenador.get_numeros())

        # Opción 7: rompe el bucle infinito y termina el programa.
        elif opcion == "7":
            print("\nCerrando el programa. ¡Hasta luego!")
            break

        else:
            print("\n  -> Opción inválida. Elige un número entre 1 y 7.")

        input("\nPresiona Enter para continuar...")


if __name__ == "__main__":
    main()
