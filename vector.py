# vector.py (Kevin Gámez)

"""
Define la clase Vector: una lista de números que representa una columna.

Se usa principalmente para la operación Matriz * Vector.
"""

from excepciones import IndiceFueraDeRangoError


class Vector:
    """Una columna de números. Ejemplo: Vector([1, 2, 3])"""

    def __init__(self, datos):
        """Crea un vector a partir de una lista de números."""
        if not isinstance(datos, (list, tuple)):
            raise TypeError("Un Vector debe construirse a partir de una lista de números.")

        if len(datos) == 0:
            raise ValueError("Un Vector no puede estar vacío.")

        self._datos = list(datos)

    def dimension(self):
        """Devuelve cuántos elementos tiene el vector."""
        return len(self._datos)

    def _validar_indice(self, indice):
        """Verifica que el índice esté dentro del rango válido."""
        n = len(self._datos)

        if indice < 0 or indice >= n:
            raise IndiceFueraDeRangoError(
                f"Índice {indice} fuera de rango. "
                f"El vector tiene {n} elementos (0 a {n - 1})."
            )

    def __getitem__(self, indice):
        """Permite leer: v[i]"""
        self._validar_indice(indice)
        return self._datos[indice]

    def __setitem__(self, indice, valor):
        """Permite escribir: v[i] = valor"""
        self._validar_indice(indice)
        self._datos[indice] = valor

    def __str__(self):
        """Muestra el vector como columna: [1]\\n[2]\\n[3]"""
        return "\n".join(f"[{x}]" for x in self._datos)

    def __eq__(self, otro):
        """Dos vectores son iguales si tienen los mismos elementos."""
        if not isinstance(otro, Vector):
            return False
        return self._datos == otro._datos
