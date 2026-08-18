# matriz.py (Kevin Gámez)

"""
Define la clase Matriz y sus operaciones: suma, producto, inversa, etc.
"""

from excepciones import (
    DimensionesInvalidasError,
    DimensionesIncompatiblesError,
    MatrizNoCuadradaError,
    MatrizSingularError,
    IndiceFueraDeRangoError,
)


class Matriz:
    """Matriz rectangular de números. Ejemplo: Matriz([[1, 2], [3, 4]])"""

    def __init__(self, datos):
        """Crea una matriz a partir de una lista de listas."""
        if not isinstance(datos, (list, tuple)):
            raise TypeError(
                "Debe ser una lista de listas. Ejemplo: Matriz([[1, 2], [3, 4]])"
            )

        if len(datos) == 0:
            raise DimensionesInvalidasError("Debe tener al menos una fila.")

        cols = len(datos[0])

        for i, fila in enumerate(datos):
            if not isinstance(fila, (list, tuple)):
                raise DimensionesInvalidasError(f"La fila {i} no es una lista.")

            if len(fila) == 0:
                raise DimensionesInvalidasError(f"La fila {i} está vacía.")

            if len(fila) != cols:
                raise DimensionesInvalidasError(
                    f"Las filas no tienen el mismo tamaño. "
                    f"Fila 0 tiene {cols} columnas, fila {i} tiene {len(fila)}."
                )

        self._datos = [list(fila) for fila in datos]

    @property
    def filas(self):
        return len(self._datos)

    @property
    def columnas(self):
        return len(self._datos[0])

    def dimensiones(self):
        """Devuelve (filas, columnas)."""
        return (self.filas, self.columnas)

    def _validar_indice(self, fila, col):
        """Verifica que la posición [fila, col] exista en la matriz."""
        if fila < 0 or fila >= self.filas:
            raise IndiceFueraDeRangoError(
                f"Fila {fila} no existe. Hay {self.filas} filas (0 a {self.filas - 1})."
            )

        if col < 0 or col >= self.columnas:
            raise IndiceFueraDeRangoError(
                f"Columna {col} no existe. Hay {self.columnas} columnas (0 a {self.columnas - 1})."
            )

    def __getitem__(self, indice):
        """Permite leer: A[fila, columna]"""
        fila, col = indice
        self._validar_indice(fila, col)
        return self._datos[fila][col]

    def __setitem__(self, indice, valor):
        """Permite escribir: A[fila, columna] = valor"""
        fila, col = indice
        self._validar_indice(fila, col)
        self._datos[fila][col] = valor

    def __str__(self):
        """Muestra la matriz fila por fila cuante se imprime."""
        return "\n".join(" ".join(str(x) for x in fila) for fila in self._datos)

    def __eq__(self, otra):
        """Dos matrices son iguales si tienen las mismas dimensiones y valores."""
        if not isinstance(otra, Matriz):
            return False
        return self._datos == otra._datos

    def __add__(self, otra):
        """Suma dos matrices de las mismas dimensiones: C = A + B"""
        if not isinstance(otra, Matriz):
            return NotImplemented

        if self.filas != otra.filas or self.columnas != otra.columnas:
            raise DimensionesIncompatiblesError(
                f"No se pueden sumar: {self.filas}x{self.columnas} y "
                f"{otra.filas}x{otra.columnas}."
            )

        return Matriz([
            [self._datos[i][j] + otra._datos[i][j]
             for j in range(self.columnas)]
            for i in range(self.filas)
        ])

    def __mul__(self, otra):
        """Multiplica por otra Matriz o por un Vector."""
        from vector import Vector

        # Matriz × Matriz
        if isinstance(otra, Matriz):
            if self.columnas != otra.filas:
                raise DimensionesIncompatiblesError(
                    f"No se puede multiplicar: {self.filas}x{self.columnas} × "
                    f"{otra.filas}x{otra.columnas}."
                )

            resultado = []

            for i in range(self.filas):
                fila = []

                for j in range(otra.columnas):
                    # Producto punto de la fila i de A con la columna j de B
                    suma = sum(
                        self._datos[i][k] * otra._datos[k][j]
                        for k in range(self.columnas)
                    )
                    fila.append(suma)

                resultado.append(fila)

            return Matriz(resultado)

        # Matriz × Vector
        if isinstance(otra, Vector):
            if self.columnas != otra.dimension():
                raise DimensionesIncompatiblesError(
                    f"Matriz {self.filas}x{self.columnas} × "
                    f"Vector de dim {otra.dimension()} no es posible."
                )

            return Vector([
                sum(self._datos[i][j] * otra[j] for j in range(self.columnas))
                for i in range(self.filas)
            ])

        return NotImplemented

    def inversa(self):
        """
        Calcula la inversa con Gauss-Jordan.
        La matriz debe ser cuadrada y no singular.
        """
        if self.filas != self.columnas:
            raise MatrizNoCuadradaError(
                f"No cuadrada: {self.filas}x{self.columnas}."
            )

        n = self.filas

        # Crear matriz aumentada [A | I]
        aug = [
            list(self._datos[i]) + [1.0 if j == i else 0.0 for j in range(n)]
            for i in range(n)
        ]

        for col in range(n):
            # Buscar el pivote más grande en esta columna
            max_row = col
            max_val = abs(aug[col][col])

            for fila in range(col + 1, n):
                if abs(aug[fila][col]) > max_val:
                    max_val = abs(aug[fila][col])
                    max_row = fila

            # Si no hay pivote válido, la matriz es singular
            if max_val < 1e-10:
                raise MatrizSingularError("La matriz es singular, no tiene inversa.")

            # Intercambiar filas si es necesario
            if max_row != col:
                aug[col], aug[max_row] = aug[max_row], aug[col]

            # Normalizar la fila del pivote
            pivote = aug[col][col]

            for j in range(2 * n):
                aug[col][j] /= pivote

            # Eliminar esta columna en las demás filas
            for fila in range(n):
                if fila != col:
                    factor = aug[fila][col]

                    for j in range(2 * n):
                        aug[fila][j] -= factor * aug[col][j]

        # Extraer la inversa (la mitad derecha)
        return Matriz([fila[n:] for fila in aug])

    def traspuesta(self):
        """Devuelve la matriz traspuesta (intercambia filas por columnas)."""
        return Matriz([
            [self._datos[i][j] for i in range(self.filas)]
            for j in range(self.columnas)
        ])

    @staticmethod
    def identidad(n):
        """Crea una matriz identidad de n×n."""
        return Matriz([
            [1 if i == j else 0 for j in range(n)]
            for i in range(n)
        ])
