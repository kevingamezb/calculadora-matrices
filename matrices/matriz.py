# matriz.py - Kevin Gámez

"""
Define la clase Matriz y sus operaciones: suma, producto, inversa, etc.

¿CÓMO ESTÁ PENSADO ESTE ARCHIVO? (decisiones de diseño)
-------------------------------------------------------
1) ¿Por qué una CLASE y no listas sueltas?
   Una matriz al final son listas de listas, pero metiéndolas en una
   clase ganamos dos cosas:
   - Validar UNA sola vez (en __init__) que los datos formen una
     matriz de verdad (no vacía, filas del mismo tamaño). Después de
     ese control, TODOS los demás métodos pueden confiar en que el
     objeto es válido: nunca hay que volver a revisarlo.
   - Que la matriz tenga comportamientos propios (sumarse,
     multiplicarse, invertirse) en vez de funciones sueltas.

2) ¿Por qué los números viven en self._datos?
   El guion bajo inicial (_) es la convención de Python para decir
   "atributo de uso interno: no lo toques desde afuera". Además se
   guarda una COPIA fila por fila ([list(fila) for fila in datos]),
   así que si alguien modifica las listas originales después de crear
   la matriz, esta no se entera (copia defensiva).

3) ¿Por qué métodos con nombres raros como __add__ o __getitem__?
   Son "métodos mágicos": Python los llama solos cuando usamos los
   símbolos normales. Gracias a ellos el código se lee como matemática:
       A + B      llama a __add__
       A * B      llama a __mul__
       A[i, j]    llama a __getitem__

4) ¿Qué significa devolver NotImplemented?
   Es la manera educada de decirle a Python "yo NO sé operar con ese
   tipo". Python entonces pregunta al otro operando y, si nadie sabe,
   lanza un TypeError estándar. (No confundir con NotImplementedError).

5) ¿Por qué excepciones propias? (ver excepciones.py)
   Para que cada error explique en español qué pasó ("No se pueden
   sumar: 2x3 y 3x3") y para que main.py atrape todo junto con un
   "except ErrorMatriz" y el programa nunca se caiga.

6) ¿Cómo consigue la inversa? (método inversa)
   Con Gauss-Jordan sobre la "matriz aumentada" [A | I]: se pega la
   identidad a la derecha de A y, con operaciones de fila (multiplicar
   una fila por un número, sumarle otra, intercambiarlas), se va
   transformando la izquierda en la identidad; lo que quede del lado
   derecho ES la inversa. Para elegir pivote se toma siempre el número
   de mayor valor absoluto de la columna (pivoteo parcial): divide
   entre números grandes evita resultados basura cuando hay decimales.
"""

from excepciones import (
    DimensionesInvalidasError,
    DimensionesIncompatiblesError,
    MatrizNoCuadradaError,
    MatrizSingularError,
    IndiceFueraDeRangoError,
)

# Vector se importa aquí arriba sin miedo: vector.py SOLO depende de
# excepciones.py, jamás importa a Matriz, así que no existe ciclo.
# (Antes este import vivía adentro de __mul__ por precaución, pero
# nunca hizo falta.)
from vector import Vector


class Matriz:
    """
    Matriz rectangular de números guardada como lista de listas.

    Ejemplo: Matriz([[1, 2], [3, 4]]) representa:

        | 1  2 |
        | 3  4 |

    Promesa de diseño: todo objeto Matriz salió validado de __init__,
    por eso ningún otro método re-chequea que sea rectangular.
    """

    def __init__(self, datos):
        """
        Crea una matriz a partir de una lista de listas.

        Aquí vive la ÚNICA validación de formato de toda la clase:
        si algo está mal se avisa de inmediato y no se crea objeto.
        """
        # Debe ser una lista (o tupla) de filas; cualquier otra cosa
        # (un número, un string...) es error inmediato.
        if not isinstance(datos, (list, tuple)):
            raise TypeError(
                "Debe ser una lista de listas. Ejemplo: Matriz([[1, 2], [3, 4]])"
            )

        # Sin filas no hay matriz.
        if len(datos) == 0:
            raise DimensionesInvalidasError("Debe tener al menos una fila.")

        # Todas las filas deben medir lo mismo que la primera.
        cols = len(datos[0])

        for i, fila in enumerate(datos):
            # Cada fila también debe ser lista...
            if not isinstance(fila, (list, tuple)):
                raise DimensionesInvalidasError(f"La fila {i} no es una lista.")

            # ...con al menos un valor dentro...
            if len(fila) == 0:
                raise DimensionesInvalidasError(f"La fila {i} está vacía.")

            # ...y del mismo largo que las demás (rectangularidad).
            if len(fila) != cols:
                raise DimensionesInvalidasError(
                    f"Las filas no tienen el mismo tamaño. "
                    f"Fila 0 tiene {cols} columnas, fila {i} tiene {len(fila)}."
                )

        # Todo bien: copia defensiva fila por fila.
        self._datos = [list(fila) for fila in datos]

    @property
    def filas(self):
        """Cantidad de filas; se lee como atributo: m.filas"""
        return len(self._datos)

    @property
    def columnas(self):
        """Cantidad de columnas; se lee como atributo: m.columnas"""
        return len(self._datos[0])

    def dimensiones(self):
        """Devuelve (filas, columnas). Cómodo para comparar tamaños."""
        return (self.filas, self.columnas)

    def get(self):
        """
        Entrega los datos crudos (lista de listas).

        Es la "ventanita" legítima hacia _datos: la usa main.py para
        imprimir el resultado tal cual, sin depender de __str__.
        """
        return self._datos

    def _validar_indice(self, fila, col):
        """
        Verifica que la posición [fila, col] exista.

        Lo usan tanto la lectura como la escritura (__getitem__ y
        __setitem__), por eso vive en UN solo lugar y no repetido.
        """
        if fila < 0 or fila >= self.filas:
            raise IndiceFueraDeRangoError(
                f"Fila {fila} no existe. Hay {self.filas} filas (0 a {self.filas - 1})."
            )

        if col < 0 or col >= self.columnas:
            raise IndiceFueraDeRangoError(
                f"Columna {col} no existe. Hay {self.columnas} columnas (0 a {self.columnas - 1})."
            )

    def __getitem__(self, indice):
        """Permite leer: A[fila, columna]."""
        fila, col = indice          # Python desempaca la tupla (i, j)
        self._validar_indice(fila, col)
        return self._datos[fila][col]

    def __setitem__(self, indice, valor):
        """Permite escribir: A[fila, columna] = valor."""
        fila, col = indice
        self._validar_indice(fila, col)
        self._datos[fila][col] = valor

    def __str__(self):
        """Al imprimir: una línea por fila, valores separados por espacio."""
        return "\n".join(" ".join(str(x) for x in fila) for fila in self._datos)

    def __eq__(self, otra):
        """Dos matrices son iguales si miden igual Y tienen los mismos valores."""
        if not isinstance(otra, Matriz):
            return False
        return self._datos == otra._datos

    def __add__(self, otra):
        """Suma celda a celda. Solo posible entre matrices del MISMO tamaño."""
        if not isinstance(otra, Matriz):
            return NotImplemented

        # Sumar exige dimensiones idénticas.
        if self.filas != otra.filas or self.columnas != otra.columnas:
            raise DimensionesIncompatiblesError(
                f"No se pueden sumar: {self.filas}x{self.columnas} y "
                f"{otra.filas}x{otra.columnas}."
            )

        # Recorrido clásico: para cada celda [i][j], resultado[i][j]
        # = self[i][j] + otra[i][j].
        return Matriz([
            [self._datos[i][j] + otra._datos[i][j]
             for j in range(self.columnas)]
            for i in range(self.filas)
        ])

    def __mul__(self, otra):
        """
        Multiplicación con doble personalidad:

        - Matriz * Matriz -> nueva Matriz
        - Matriz * Vector -> nuevo Vector

        Decide preguntando el tipo de 'otra' (polimorfismo manual).
        """
        # ---- CASO 1: Matriz × Matriz ---------------------------------
        if isinstance(otra, Matriz):
            # Regla de oro: columnas de la primera == filas de la segunda.
            if self.columnas != otra.filas:
                raise DimensionesIncompatiblesError(
                    f"No se puede multiplicar: {self.filas}x{self.columnas} × "
                    f"{otra.filas}x{otra.columnas}."
                )

            resultado = []

            # Cada celda del resultado es el "producto punto":
            # fila i de la izquierda · columna j de la derecha.
            for i in range(self.filas):
                fila = []

                for j in range(otra.columnas):
                    # Se recorre k a la par en ambas y se acumula:
                    # A[i,0]*B[0,j] + A[i,1]*B[1,j] + ...
                    suma = sum(
                        self._datos[i][k] * otra._datos[k][j]
                        for k in range(self.columnas)
                    )
                    fila.append(suma)

                resultado.append(fila)

            return Matriz(resultado)

        # ---- CASO 2: Matriz × Vector ---------------------------------
        if isinstance(otra, Vector):
            # Igual que antes: columnas de la matriz == elementos del vector.
            if self.columnas != otra.dimension():
                raise DimensionesIncompatiblesError(
                    f"Matriz {self.filas}x{self.columnas} × "
                    f"Vector de dim {otra.dimension()} no es posible."
                )

            # Cada fila de la matriz "traga" al vector completo y da
            # un solo número; con todas las filas sale el vector resultante.
            return Vector([
                sum(self._datos[i][j] * otra[j] for j in range(self.columnas))
                for i in range(self.filas)
            ])

        # No es Matriz ni Vector: que Python decida qué hacer.
        return NotImplemented

    def inversa(self):
        """
        Calcula la inversa con Gauss-Jordan (requiere cuadrada y no singular).

        Estrategia resumida (los detalles están comentados abajo):
        1. Armar [A | I] pegando la identidad a la derecha.
        2. Columna por columna, fabricar un 1 en la diagonal y 0s
           alrededor usando operaciones de fila.
        3. Cuando la izquierda quedó identidad, la derecha es A⁻¹.
        """
        if self.filas != self.columnas:
            raise MatrizNoCuadradaError(
                f"No cuadrada: {self.filas}x{self.columnas}."
            )

        n = self.filas   # es cuadrada: n x n

        # PASO 0 - Matriz aumentada [A | I].
        # Cada fila de A se copia y a su lado se agrega la fila de la
        # identidad correspondiente (1 en su posición, 0s resto).
        matriz_aumentada = [
            list(self._datos[i]) +
            [1.0 if j == i else 0.0 for j in range(n)]
            for i in range(n)
        ]

        # Bucle principal: una vuelta por cada columna a "limpiar".
        for col in range(n):

            # PASO 1 - Pivoteo parcial: buscar en esta columna el número
            # con MAYOR valor absoluto (desde la diagonal hacia abajo).
            # Dividir entre el más grande hace el cálculo más estable
            # con decimales.
            fila_pivote = col
            mayor_valor = abs(matriz_aumentada[col][col])

            for fila in range(col + 1, n):
                if abs(matriz_aumentada[fila][col]) > mayor_valor:
                    mayor_valor = abs(matriz_aumentada[fila][col])
                    fila_pivote = fila

            # Si el mejor candidato es prácticamente cero, ninguna jugada
            # posterior lo arregla: la matriz es singular y no hay inversa.
            # (Se compara contra 1e-10 porque con flotantes el cero exacto
            # casi nunca aparece.)
            if mayor_valor < 1e-10:
                raise MatrizSingularError(
                    "La matriz es singular, no tiene inversa."
                )

            # PASO 2 - Traer la fila del buen pivote hasta la diagonal.
            if fila_pivote != col:
                matriz_aumentada[col], matriz_aumentada[fila_pivote] = matriz_aumentada[fila_pivote], matriz_aumentada[col]

            # PASO 3 - Normalizar: dividir TODA la fila del pivote entre
            # el pivote para que en [col][col] quede exactamente 1.
            pivote = matriz_aumentada[col][col]

            for j in range(2 * n):
                matriz_aumentada[col][j] /= pivote

            # PASO 4 - Eliminar hacia arriba y abajo: a cada OTRA fila se
            # le resta (su valor en esta columna) veces la fila del pivote,
            # dejando 0 en toda la columna excepto la diagonal.
            for fila in range(n):
                if fila != col:
                    factor = matriz_aumentada[fila][col]

                    for j in range(2 * n):
                        matriz_aumentada[fila][j] -= factor * matriz_aumentada[col][j]

        # Terminamos: la izquierda es la identidad, así que la mitad
        # DERECHA de cada fila es la inversa prometida.
        return Matriz([fila[n:] for fila in matriz_aumentada])

    def traspuesta(self):
        """Devuelve la traspuesta: las filas se vuelven columnas."""
        # Se recorre por columnas primero (j afuera) para "voltear" el orden.
        return Matriz([
            [self._datos[i][j] for i in range(self.filas)]
            for j in range(self.columnas)
        ])

    @staticmethod
    def identidad(n):
        """
        Crea la matriz identidad n×n (1s en diagonal, 0s afuera).

        @staticmethod = fábrica: no necesita una matriz existente para
        invocarse, se usa directo como Matriz.identidad(3).
        """
        return Matriz([
            [1 if i == j else 0 for j in range(n)]
            for i in range(n)
        ])
