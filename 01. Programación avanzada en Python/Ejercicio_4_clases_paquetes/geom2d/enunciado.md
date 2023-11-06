# Paquete geometria

En este ejercocio vamos a asentar los conocimientos para
- Crear paquetes
- Crear clases
- Métodos especiales de python

Se trata de crear un proyecto que va a incluir un módulo llamado
`geom2d`. Vamos a incluir 2 clases: Vector y Punto.

- La clase `Vector` la hemos visto en clase
- La clase `Point`, aunque tenga los mismo atributo de la clase
  `Vector` va a tener operaciones diferentes:
  * Debe incluir getters (`@property` en terminología Python ) y
    setters
  * Debe incluir métodos para `str` y `repr`.
  * Debe temer un método `hash`. Hay que tener cuidado de definirlo de
    forma que un `Vector` y un `Point` con las mismas coordenadas no
    den el mismo valor. Es posible que sea conveniente redefinir el
    del método vector. **Pista*: el actual de los vectores
		toma como base `(x, y)` donde `x` e `y` con las coordenadas de
    los vectores. Se puede añadir una tercera componente a esa tupla
	para que indique que es un vector.
  * Debe tener definida la resta de forma que si `a` y `b` son puntos,
    `b-a` sea el `Vector` que va de `a` a `b`.
  * Debe tener un método `distance(self, other: Self) -> float` que
    indique la distancia al otro punto.

- Se debe crear una carpeta `tests` con lo tests necesarios para
  comprobar que los métodos son correctos.

- De debe crear el fichero `pyproject.toml` a para poder crear el
  paquete. Recuerda que el directorio de `tests` no debe ser incluido

- Se debe crear el paquete.
