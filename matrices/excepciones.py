# excepciones.py - Kevin Gámez

"""
Excepciones propias de la calculadora de matrices.

¿PARA QUÉ SIRVEN Y POR QUÉ EXISTEN?
-----------------------------------
Son "tipos de error personalizados". En vez de que el usuario vea un
ValueError genérico y críptico, cada problema tiene su propio nombre
y un mensaje claro en español que dice qué pasó.

El árbol de herencia es simple (todas nacen de ValueError):

    ValueError                          <- error nativo de Python
      └── ErrorMatriz                   <- padre de TODA la aplicación
            ├── DimensionesInvalidasError
            ├── DimensionesIncompatiblesError
            ├── MatrizNoCuadradaError
            ├── MatrizSingularError
            └── IndiceFueraDeRangoError

Gracias a esa herencia se puede atrapar en dos niveles:
- Grueso:  "except ErrorMatriz" atrapa CUALQUIER fallo de la app.
           Es lo que usa main.py para mostrar un mensaje amable sin
           que el menú se caiga jamás.
- Fino:    "except MatrizSingularError" atrapa UN caso concreto,
           útil si algún día se quiere tratar ese caso distinto.
"""


class ErrorMatriz(ValueError):
    """Excepción padre. Atrapa cualquier error de la calculadora con 'except ErrorMatriz'."""
    pass


class DimensionesInvalidasError(ErrorMatriz):
    """
    La lista de listas no forma una matriz válida.

    Ocurre al CREAR una Matriz cuando: no hay filas, alguna fila está
    vacía o las filas miden distinto (no es rectangular).
    """
    pass


class DimensionesIncompatiblesError(ErrorMatriz):
    """
    Los tamaños no permiten hacer la operación.

    Ejemplos: sumar una 2x3 con una 3x3, o multiplicar A*B cuando las
    columnas de A no coinciden con las filas de B.
    """
    pass


class MatrizNoCuadradaError(ErrorMatriz):
    """
    Se pidió la INVERSA de una matriz que no es cuadrada.

    Solo las matrices cuadradas (n x n) pueden tener inversa.
    """
    pass


class MatrizSingularError(ErrorMatriz):
    """
    La matriz es singular: matemáticamente NO tiene inversa.

    Se detecta durante Gauss-Jordan cuando ninguna fila aporta un
    pivote usable (todo cero o casi cero) en alguna columna.
    """
    pass


class IndiceFueraDeRangoError(ErrorMatriz):
    """
    Se intentó leer o escribir una posición que no existe.

    Ejemplo: pedir A[5, 0] en una matriz de 2 filas.
    """
    pass
