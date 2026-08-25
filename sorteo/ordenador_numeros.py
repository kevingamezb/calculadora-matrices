# ordenador_numeros.py - Alvaro Orjuela
#
# Punto del ejercicio: ordenar números decimales aleatorios con varios
# métodos y poder compararlos.
#
# PATRÓN DE DISEÑO DE LA CLASE (decisión tomada):
# - El constructor guarda TODO el estado: la cantidad pedida, la lista
#   original y una casillita para el resultado de cada método.
# - Los métodos de ordenamiento NO reciben parámetros NI devuelven
#   nada: trabajan sobre los datos internos del objeto (self) y guardan
#   su resultado en su casilla correspondiente.
# - El main consulta los resultados a través de métodos "get".
#
# Regla compartida por todos los sorts: primero se hace una COPIA de
# la lista original. Así se puede correr cualquier método sin arruinar
# los números de partida, y comparar resultados entre sí con sentido.

import random


class OrdenadorNumeros:

    def __init__(self):
        """Prepara las casillas vacías; todo empieza sin datos."""
        self.cantidad = 0                    # cuántos números generar
        self.numeros = []                    # lista original (la base)
        self.resultado_burbuja = []          # salida de cada sort...
        self.resultado_insercion = []
        self.resultado_seleccion = []
        self.resultado_mergesort = []
        self.resultado_sort_python = []

    def generar_numeros(self):
        """Rellena self.numeros con 'cantidad' decimales aleatorios entre 0 y 100."""
        # Lista por comprensión, repetida 'cantidad' veces:
        # random.uniform(0, 100) -> decimal aleatorio entre 0 y 100;
        # round(..., 2)          -> lo deja con máximo 2 decimales.
        self.numeros = [
            round(random.uniform(0, 100), 2)
            for _ in range(self.cantidad)
        ]

    def ordenar_burbuja(self):
        """
        Idea en una frase: recorrer la lista comparando VECINOS e
        intercambiándolos si están al revés, muchas pasadas seguidas.

        En cada pasada el número más grande de lo que resta "flota"
        hasta el final (como una burbuja), así que la zona final va
        quedando fija y cada vuelta revisa un poquito menos.
        """
        copia = list(self.numeros)   # nunca tocamos la original
        n = len(copia)

        # Pasada número j: tras ella, los últimos j+1 ya están en su lugar.
        for j in range(n - 1):

            # Recorre pares de vecinos hasta donde aún hay desorden.
            for i in range(n - j - 1):

                if copia[i] > copia[i + 1]:
                    # Vecinos invertidos: intercambio en una sola línea.
                    copia[i], copia[i + 1] = copia[i + 1], copia[i]

        self.resultado_burbuja = copia

    def ordenar_insercion(self):
        """
        Idea en una frase: como ordenar CARTAS EN LA MANO — se toma un
        número y se lo desliza hacia atrás hasta encajar entre los que
        ya estaban ordenados.

        La parte izquierda de la copia siempre está ordenada; solo hay
        que encontrarle hueco al siguiente elemento.
        """
        copia = list(self.numeros)

        for j in range(1, len(copia)):
            numero_actual = copia[j]   # la "carta" a ubicar en esta vuelta
            i = j - 1                  # último índice de la parte ordenada

            # Mientras los de la izquierda sean MAYORES, corrélos un
            # paso a la derecha para hacerle hueco.
            while i >= 0 and copia[i] > numero_actual:
                copia[i + 1] = copia[i]
                i -= 1

            # Suelta la carta justo donde dejó de haber mayores.
            copia[i + 1] = numero_actual

        self.resultado_insercion = copia

    def ordenar_seleccion(self):
        """
        Idea en una frase: buscar al MENOR de lo que queda y ponerlo al
        frente; repetir hasta terminar.

        Pocos intercambios (uno por vuelta) pero muchísimas
        comparaciones: siempre escanea todo el resto desordenado.
        """
        copia = list(self.numeros)
        n = len(copia)

        for i in range(n - 1):
            minimo = i   # candidato a ser el menor de esta zona

            # Escanea el resto desordenado buscando de verdad al menor.
            for j in range(i + 1, n):

                if copia[j] < copia[minimo]:
                    minimo = j

            # Solo intercambia si el menor no era quien ya estaba ahí.
            if minimo != i:
                copia[i], copia[minimo] = copia[minimo], copia[i]

        self.resultado_seleccion = copia

    def ordenar_mergesort(self):
        """
        Idea en una frase: DIVIDIR Y VENCER — partir la lista a la
        mitad, ordenar cada mitad recursivamente y luego COMBINAR las
        dos mitades ya ordenadas en una sola.

        Es el único sort aquí abajo que usa funciones ayudantes
        (_mergesort y _combinar); el guion bajo indica que son para
        uso interno de la clase.
        """
        self.resultado_mergesort = self._mergesort(list(self.numeros))

    def _mergesort(self, lista):
        """Parte recursiva: divide la lista y devuelve la versión ordenada."""
        # CASO BASE: con 0 o 1 elementos no hay nada que ordenar;
        # aquí se frena la recursión y empieza el "regreso".
        if len(lista) <= 1:
            return lista

        # Divide: corta por la mitad y ordena cada mitad por separado.
        medio = len(lista) // 2
        izquierda = self._mergesort(lista[:medio])
        derecha = self._mergesort(lista[medio:])

        # Vencer: junta las dos mitades YA ordenadas.
        return self._combinar(izquierda, derecha)

    def _combinar(self, izquierda, derecha):
        """Recibe dos mitades ORDENADAS y las funde en una sola ordenada."""
        resultado = []
        pos_izq = pos_der = 0   # puntero de avance dentro de cada mitad

        # Mientras queden cartas en ambas mitades, toma SIEMPRE la
        # menor de las dos puntas y avanza ese puntero.
        while pos_izq < len(izquierda) and pos_der < len(derecha):

            if izquierda[pos_izq] <= derecha[pos_der]:
                resultado.append(izquierda[pos_izq])
                pos_izq += 1
            else:
                resultado.append(derecha[pos_der])
                pos_der += 1

        # Una mitad se agotó; la otra ya viene ordenada, se vuelca
        # entera. (Uno de estos dos quedará vacío y no aporta nada.)
        resultado.extend(izquierda[pos_izq:])
        resultado.extend(derecha[pos_der:])
        return resultado

    def ordenar_sort_python(self):
        """
        Usa el sort() NATIVO de Python (internamente es Timsort).

        Sirve como referencia: es el método "profesional" contra el
        cual comparar los cuatro implementados a mano.
        """
        copia = list(self.numeros)
        copia.sort()
        self.resultado_sort_python = copia

    # -----------------------------------------------------------------
    # Métodos get: la única puerta de lectura hacia el main.
    # Cada uno devuelve SU casilla; nada más.
    # -----------------------------------------------------------------

    def get_numeros(self):
        """Devuelve la lista original generada (sin ordenar)."""
        return self.numeros

    def get_resultado_burbuja(self):
        """Devuelve el resultado del método burbuja."""
        return self.resultado_burbuja

    def get_resultado_insercion(self):
        """Devuelve el resultado del método inserción."""
        return self.resultado_insercion

    def get_resultado_seleccion(self):
        """Devuelve el resultado del método selección."""
        return self.resultado_seleccion

    def get_resultado_mergesort(self):
        """Devuelve el resultado del mergesort."""
        return self.resultado_mergesort

    def get_resultado_sort_python(self):
        """Devuelve el resultado del sort nativo de Python."""
        return self.resultado_sort_python
