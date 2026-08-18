# excepciones.py (Kevin Gámez)

"""
Excepciones propias de la calculadora de matrices.
Todas heredan de ValueError para que se puedan atrapar con "except ValueError".
"""


class ErrorMatriz(ValueError):
    """Excepción padre. Atrapa cualquier error de la calculadora con 'except ErrorMatriz'."""
    pass


class DimensionesInvalidasError(ErrorMatriz):
    """La lista de listas no es una matriz válida (vacía, filas vacías o filas de distinto tamaño)."""
    pass


class DimensionesIncompatiblesError(ErrorMatriz):
    """Las dimensiones de las matrices no permiten la operación (suma, producto, etc.)."""
    pass


class MatrizNoCuadradaError(ErrorMatriz):
    """Se intentó calcular la inversa de una matriz que no es cuadrada."""
    pass


class MatrizSingularError(ErrorMatriz):
    """La matriz no tiene inversa (es singular)."""
    pass


class IndiceFueraDeRangoError(ErrorMatriz):
    """Se intentó acceder a una posición que no existe en la matriz o vector."""
    pass
