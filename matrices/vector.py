# vector.py - Andrés León

"""
Define la clase Vector: una lista de números que representa una columna.

Se usa principalmente para la operación Matriz * Vector.

¿POR QUÉ EXISTE COMO CLASE APARTE (y no como lista cualquiera)?
---------------------------------------------------------------
- Un vector es un objeto matemático con reglas propias: conviene que
  se valide al nacer, sepa imprimirse en columna y pueda multiplicarse
  con una Matriz usando el símbolo *.
- Sigue la MISMA filosofía de diseño que Matriz (ver matriz.py):
  * los datos viven en self._datos (el guion bajo = "uso interno"),
  * se hace copia defensiva para no depender de la lista original,
  * toda posición se valida antes de usarse.
"""

from excepciones import IndiceFueraDeRangoError


class Vector:
    """Una columna de números. Ejemplo mental: [1, 2, 3] en vertical."""

    def __init__(self, datos):
        """Crea un vector a partir de una lista de números."""
        # Debe recibir una lista (o tupla); cualquier otra cosa es error.
        if not isinstance(datos, (list, tuple)):
            raise TypeError(
                "Un Vector debe construirse a partir de una lista de números."
            )

        # Un vector vacío no representaría nada útil.
        if len(datos) == 0:
            raise ValueError("Un Vector no puede estar vacío.")

        # Copia defensiva: si luego cambian la lista original,
        # este vector queda intacto.
        self._datos = list(datos)

    def dimension(self):
        """Devuelve cuántos elementos tiene el vector."""
        return len(self._datos)

    def get(self):
        """Retorna los datos crudos (la lista interna) para imprimirlos."""
        return self._datos

    def _validar_indice(self, indice):
        """Verifica que el índice esté dentro del rango válido."""
        n = len(self._datos)

        if indice < 0 or indice >= n:
            raise IndiceFueraDeRangoError(
                f"Índice {indice} fuera de rango. "
                f"El vector tiene {n} elementos (0 a {n - 1})."
            )

    def __getitem__(self, indice):
        """Permite leer: v[i]. Python llama aquí automáticamente."""
        self._validar_indice(indice)
        return self._datos[indice]

    def __setitem__(self, indice, valor):
        """Permite escribir: v[i] = valor. También validado."""
        self._validar_indice(indice)
        self._datos[indice] = valor

    def __str__(self):
        """Al imprimirlo se muestra en columna, un elemento por línea."""
        return "\n".join(f"[{x}]" for x in self._datos)

    def __eq__(self, otro):
        """Dos vectores son iguales si tienen exactamente los mismos elementos."""
        if not isinstance(otro, Vector):
            return False
        return self._datos == otro._datos
