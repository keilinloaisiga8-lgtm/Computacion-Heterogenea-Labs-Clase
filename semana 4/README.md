# Práctica de clase 3 y 4 — Sistemas Multiprocesador


## Entorno de pruebas

Todas las mediciones se corrieron en mi computadora con las siguientes caracteristicas:

- **CPU:** Intel(R) Core(TM) i5-1135G7 @ 2.40GHz
- **Núcleos físicos:** 4
- **Hilos lógicos (con hyperthreading):** 8
- **Sistema operativo:** Linux
- **Compilador:** gcc

---

## Práctica 3

### Ejercicio A — cpu-naive, cpu-affinity

Se modificó el `#define NUM_THREADS` de `cpu-naive.c` y `cpu-affinity.c` de
forma manual, recompilando y midiendo el tiempo real con `time` para cada cantidad de hilos, 
de 1 a 8 (el máximo de hilos lógicos disponibles en mi computadora).

**Tabla de tiempos (segundos, tiempo real reportado por `time`):**

| Hilos | cpu-naive | cpu-affinity |
|:-----:|:---------:|:------------:|
| 1     | 4.098     | 3.750        |
| 2     | 4.158     | 3.933        |
| 3     | 4.414     | 4.089        |
| 4     | 4.534     | 3.993        |
| 5     | 4.444     | 4.056        |
| 6     | 4.632     | 4.092        |
| 7     | 4.795     | 4.093        |
| 8     | 4.712     | 3.911        |

**Gráfico:**

![Tiempo real vs número de hilos - Ejercicio A](semana%203/threading/ejercicioA_tiempo.png)

**Análisis — escalabilidad, proporción de código paralelo y eficiencia:**


---

### Ejercicio B — `semana 3/scaling/` (matmul_tiled_openmp, softmax_openmp)

A diferencia del Ejercicio A, estos programas ya reciben el número de hilos
como argumento de línea de comandos, así que no fue necesario modificar ni
recompilar el código entre cada corrida. Se ejecutaron variando el número de
hilos de 1 a 8, usando el tiempo que cada aplicación reporta internamente.

**Tabla de tiempos (segundos, reportados por cada programa):**

| Hilos | softmax_openmp | matmul_tiled_openmp |
|:-----:|:--------------:|:--------------------:|
| 1     | 1.918          | 2.061                |
| 2     | 1.513          | 1.036                |
| 3     | 1.393          | 0.703                |
| 4     | 1.327          | 0.528                |
| 5     | 1.558          | 0.593                |
| 6     | 1.680          | 0.501                |
| 7     | 1.731          | 0.450                |
| 8     | 1.803          | 0.509                |

**Gráfico:**

![Tiempo vs número de hilos - Ejercicio B](semana%203/scaling/ejercicioB_tiempo.png)

**Tabla de apoyo — Speedup y eficiencia (`S(p) = T(1)/T(p)`, `E(p) = S(p)/p`):**

| Hilos | Speedup softmax | Efic. softmax | Speedup matmul | Efic. matmul |
|:-----:|:---------------:|:--------------:|:---------------:|:--------------:|
| 1     | 1.000            | 1.000           | 1.000            | 1.000           |
| 2     | 1.268            | 0.634           | 1.990            | 0.995           |
| 3     | 1.377            | 0.459           | 2.931            | 0.977           |
| 4     | 1.446            | 0.361           | 3.904            | 0.976           |
| 5     | 1.231            | 0.246           | 3.475            | 0.695           |
| 6     | 1.142            | 0.190           | 4.118            | 0.686           |
| 7     | 1.108            | 0.158           | 4.578            | 0.654           |
| 8     | 1.064            | 0.133           | 4.049            | 0.506           |

**Análisis — escalabilidad, proporción de código paralelo y eficiencia:**


---

## Práctica 4

*(Pendiente — se completa con el Ejercicio A y B de bibliotecas estática y
dinámica.)*

---