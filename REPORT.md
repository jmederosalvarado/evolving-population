# Proyecto de eventos discretos

> Jorge Mederos Alvarado

## Orden del Problema Asignado

Se desea conocer la evolución de la población de una determinada región. Se conoce que la probabilidad de fallecer de una persona distribuye uniforme y se corresponde, según su edad y sexo, con la siguiente tabla:

| edad   | hombre | mujer |
| ------ | ------ | ----- |
| 0-12   | 0.25   | 0.25  |
| 12-45  | 0.1    | 0.15  |
| 45-76  | 0.3    | 0.35  |
| 76-125 | 0.7    | 0.65  |

Del mismo modo, se conoce que la probabilidad de una mujer se embarace es uniforme y está relacionada con la edad:

| edad   | probabilidad de embarazo |
| ------ | ------------------------ |
| 12-15  | 0.2                      |
| 15-21  | 0.45                     |
| 21-35  | 0.8                      |
| 35-45  | 0.4                      |
| 45-60  | 0.2                      |
| 60-125 | 0.05                     |

Para que una mujer quede embarazada debe tener pareja y no haber tenido el número máximo de hijos que deseaba tener ella o su pareja en ese momento. El número de hijos que cada persona desea tener distribuye uniforme según la tabla siguiente:

| número   | probabilidad |
| -------- | ------------ |
| 1        | 0.6          |
| 2        | 0.75         |
| 3        | 0.35         |
| 4        | 0.2          |
| 5        | 0.1          |
| más de 5 | 0.05         |

Para que dos personas sean pareja deben estar solas en ese instante y deben desear tener pareja. El desear tener pareja está relacionado con la edad:

| edad   | probabilidad de desear pareja |
| ------ | ----------------------------- |
| 12-15  | 0.5                           |
| 15-21  | 0.65                          |
| 21-35  | 0.8                           |
| 35-45  | 0.6                           |
| 45-60  | 0.5                           |
| 60-125 | 0.2                           |

Si dos personas de diferente sexo están solas y ambas desean querer tener parejas entonces la probabilidad de volverse pareja está relacionada con la diferencia de edad:

| diferencia de edad | probabilidad de establecer pareja |
| ------------------ | --------------------------------- |
| 0-5                | 0.45                              |
| 5-10               | 0.4                               |
| 1-15               | 0.35                              |
| 15-20              | 0.25                              |
| 20 o más           | 0.15                              |

Cuando dos personas están en pareja la probabilidad de que ocurra una ruptura distribuye uniforme y es de 0.2. Cuando una persona se separa, o enviuda, necesita estar sola por un período de tiempo que distribuye exponencial con un parámetro que está relacionado con la edad:

| edad   | $\lambda$ |
| ------ | --------- |
| 12-15  | 3 meses   |
| 15-21  | 6 meses   |
| 21-35  | 6 meses   |
| 35-45  | 1 año     |
| 45-60  | 2 años    |
| 60-125 | 4 años    |

Cuando están dadas todas las condiciones y una mujer queda embarazada puede tener o no un embarazo múltiple y esto distribuye uniforme acorde a las probabilidades siguientes:

| Número de bebés | Probabilidad |
| --------------- | ------------ |
| 1               | 0.7          |
| 2               | 0.18         |
| 3               | 0.08         |
| 4               | 0.04         |
| 5               | 0.02         |

La probabilidad del sexo de cada bebé nacido es uniforme 0,5. Asumiendo que se tiene una población inicial de M mujeres y H hombres y que cada poblador, en el instante inicial, tiene una edad que distribuye uniforme (U(0,100)). Realice un proceso de simulación para determinar como evoluciona la población en un período de 100 años.

## Principales Ideas seguidas para la solución del problema

Se sigue la idea de que los eventos sean los que determinan la ejecución de la simulación, es decir, el tiempo actual es determinado por el ultimo evento que ha ocurrido. Para ello se mantiene una cola de prioridad que ordena los eventos acorde al tiempo en que se producen. No se añaden eventos posteriores a la fecha de finalizacion de la simulacion, de esta forma la simulación se garantiza que termina y que lo hace en el periodo deseado. El tiempo es medido en meses durante la simulación.

Los tipos de eventos en el sistema son:

- Creación de una persona:

  Este evento añade una persona a la poblacion, la persona es creada con una edad aleatoria o con edad 0, esto es util para utilizar este evento tanto en la inicializacion del sistema como en el nacimiento de personas. Para inicializar el sistema añadimos `H` y `M` eventos de creación de hombres y mujeres respectivamente

- Fallecimiento de una persona:

  Al crear una persona, se genera un rango de edad para que esta fallezca, y se genera posteriormente una edad de fallecimiento dentro de dicho rango, dada en meses. En este momento se crea entonces un evento de fallecimiento para la fecha calculada. Al ejecutar este evento cambiamos el estado de la persona a `dead` y si esta tiene pareja, encolamos un evento _Ruptura_ para su pareja.

- Buscar emparejamientos:

  En la inicializacion de la simulación, ademas de la creación de los eventos que crean personas, añadimos un evento _Buscar Emparejamientos_, este evento revisa todas las posibles parejas que se podrian formar en la poblacion y genera un evento de _Emparejamiento_ para estas parejas. Este evento ademas se autoañade a la cola de eventos en cada ejecucion, de manera tal que se revisa la formacion de parejas a cada momento.

- Emparejamiento:

  Evento creado cuando una pareja es formada. En este momento se calcula si la pareja romperá en algun momento, en caso positivo se calcula el momento de ruptura utilizando una variable aleatoria uniforme entre el tiempo actual y un periodo de tiempo arbitrariamente grande de años hacia el futuro. Se crea ademas un evento recurrente dentro de tres meses _Tratar de quedar embarazada_.

- Tratar de quedar embarazada:

  Este evento revisa si existen las condiciones para que una pareja tenga un hijo, segun las restricciones del problema, en caso afirmativo genera un evento dar a luz dentro de 9 meses. Este evento se autoencola para dentro de tres meses en caso de no lograr quedar embarazada.

- Dar a luz:

  Es creado para nueve meses despues de que una mujer queda embarazada. En este punto se decide la cantidad de hijos que tendran y se generan los eventos _Nueva Persona_ correspondientes. Al finalizar este evento se volvera a encolar el evento _Tratar de quedar embarazada_ para intentar continuar teniendo hijos si las restricciones lo permiten.

- Ruptura:

  Cuando este evento se lanza se rompe el emparejamiento, en este punto se decide el tiempo de soledad que tendran las personas que formaban parte de la pareja, y se encola un evento _Finalizacion de tiempo de soledad_ para el periodo de tiempo determinado.

- Finalización de tiempo de soledad:

  Este evento restablece la posibilidad de una persona de aceptar pareja, luego de una ruptura o haber enviudado

## Modelo de Simulación de Eventos Discretos desarrollado para resolver el problema

## Consideraciones obtenidas a partir de la ejecución de las simulaciones del problema

A partir de varias ejecuciones de la simulación del problema se aprecia que en el transcurso de un siglo la población parece decrecer. Esto se considera que ocurre debido a que es muy poco probable que las personas deseen mas de uno o dos hijos, lo cual implica que en la mayoria de los casos al fallecer los padres padres, la población disminuye o se mantiene. Ademaás la probabilidad de fallecer en los primeros años de vida es muy alta, por lo que muchas veces las personas no llegan a tener hijos.

## El enlace al repositorio del proyecto en Github

[](https://github.com/jmederosalvarado/evolving-population)
