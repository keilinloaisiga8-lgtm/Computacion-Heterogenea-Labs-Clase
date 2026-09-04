# Práctica de clase 3 y 4 — Sistemas Multiprocesador

## Entorno de pruebas

Todas las mediciones se corrieron en la siguiente máquina:

- **CPU:** Intel(R) Core(TM) i5-1135G7 @ 2.40GHz
- **Núcleos físicos:** 4
- **Hilos lógicos (con hyperthreading):** 8
- **Sistema operativo:** Linux
- **Compilador:** gcc

---

## Práctica 3

### Ejercicio A — cpu-naive, cpu-affinity

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

![Tiempo real vs número de hilos - Ejercicio A](practica%203/threading/ejercicioA_tiempo.png)

**Análisis — escalabilidad, proporción de código paralelo y eficiencia:**

En el gráfico se observa que ninguno de los dos programas escala de forma positiva al incrementar los hilos en el procesador (i5-1135G7 de 4 núcleos físicos y 8 hilos lógicos). Más bien el tiempo tiende a subir: `cpu-naive` pasa de 4.098 s con 1 hilo a 4.712 s con 8 hilos, mientras que `cpu-affinity` pasa de 3.750 s a 3.911 s. La diferencia clara es que `cpu-affinity` se mantiene más rápido en todas las pruebas porque, como se vio en clase, fijar los hilos a un núcleo específico evita el fenómeno de *thread throttling* y la migración de tareas por parte del planificador del sistema operativo. Esto permite conservar la localidad espacial y temporal con datos calientes en las cachés locales L1 y L2 (1 a 4 ns de latencia), evitando pérdidas de ciclos por recargas desde la memoria RAM (60 a 80 ns).

Al calcular la aceleración no se obtiene speedup real, ya que al agregar más hilos el programa tarda más ($S(n) < 1$). Aplicando la Ley de Amdahl ($S(n) = \frac{1}{(1-p) + \frac{p}{n}}$), esto indica que la proporción de código paralelo efectiva es prácticamente nula ($p \approx 0$), estando la carga dominada por la sección serial y la contención en el hardware. Por ello, la eficiencia ($\eta = \frac{S}{n}$) decae rápidamente: con 4 núcleos físicos cae al 22.6% en naive y al 23.5% en affinity, quedando por debajo de la regla vista en clase de no paralelizar cuando la eficiencia es menor al 50%. A partir de 5 hilos el rendimiento se degrada aún más debido a la contención de Hyper-Threading, donde dos hilos lógicos compiten por las mismas unidades funcionales del mismo núcleo físico.

---

### Ejercicio B — matmul_tiled_openmp, softmax_openmp

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

![Tiempo vs número de hilos - Ejercicio B](practica%203/scaling/ejercicioB_tiempo.png)

**Tabla de apoyo — Speedup y eficiencia (`S(p) = T(1)/T(p)`, `E(p) = S(p)/p`):**

| Hilos | Speedup softmax | Efic. softmax | Speedup matmul | Efic. matmul |
|:-----:|:---------------:|:--------------:|:---------------:|:--------------:|
| 1     | 1.000           | 1.000          | 1.000           | 1.000          |
| 2     | 1.268           | 0.634          | 1.990           | 0.995          |
| 3     | 1.377           | 0.459          | 2.931           | 0.977          |
| 4     | 1.446           | 0.361          | 3.904           | 0.976          |
| 5     | 1.231           | 0.246          | 3.475           | 0.695          |
| 6     | 1.142           | 0.190          | 4.118           | 0.686          |
| 7     | 1.108           | 0.158          | 4.578           | 0.654          |
| 8     | 1.064           | 0.133          | 4.049           | 0.506          |

**Análisis — escalabilidad, proporción de código paralelo y eficiencia:**

En el gráfico se aprecian dos perfiles de escalabilidad totalmente opuestos. Por un lado, `matmul_tiled_openmp` escala de forma casi lineal de 1 a 4 hilos (los núcleos físicos disponibles), reduciendo el tiempo de 2.061 s a 0.528 s, y a partir del quinto hilo alcanza el codo de la curva estabilizándose en torno a 0.50 s, ya que Hyper-Threading no duplica las unidades de cálculo aritmético. Por el contrario, `softmax_openmp` presenta una escalabilidad sumamente baja: pasa de 1.918 s con 1 hilo a su mínimo de 1.327 s con 4 hilos, y a partir de ahí empeora hasta 1.803 s con 8 hilos.

Evaluando los resultados con 4 hilos mediante la Ley de Amdahl, `matmul_tiled_openmp` logra un speedup de 3.904 y una eficiencia de 97.6% ($\eta = 0.976$), lo que arroja una proporción de código paralelo de $p \approx 0.992$ (99.2% paralelizable). En cambio, `softmax_openmp` apenas alcanza un speedup de 1.446 y una eficiencia de 36.1% ($\eta = 0.361$), dando un código paralelizable de $p \approx 0.411$ (41.1%), quedando por debajo del umbral del 50% de eficiencia aceptable visto en clase.

Esta disparidad se explica mediante el modelo Roofline. La multiplicación con *tiling* es una carga *compute-bound* que retiene los bloques de datos en la memoria caché L1/L2, reduciendo el tráfico hacia la DRAM y permitiendo a los núcleos calcular a máxima tasa. En cambio, softmax es *memory-bound* y requiere reducciones globales con barreras de sincronización en OpenMP para hallar el máximo y la suma de exponenciales; los hilos pasan más tiempo esperando accesos a memoria y coordinándose entre sí que procesando datos, por lo que superar los 4 núcleos físicos solo añade contención.

---

## Práctica 4

### Ejercicios A y B — bench-static, bench-dynamic

Se compiló todo con `make all` y se ejecutaron las versiones enlazadas con biblioteca estática (`libvectorops.a`) y dinámica (`libvectorops.so`), cada una con `1000000 1000 1.0 2.0` (elementos, iteraciones, offset A, offset B).

**Tabla de resultados:**

| Métrica                        | bench-static (estática) | bench-dynamic (dinámica) |
|---------------------------------|:------------------------:|:--------------------------:|
| fill A (por iteración)          | 490.629 µs               | 1509.541 µs                |
| fill B (por iteración)          | 487.309 µs               | 1537.795 µs                |
| add (por iteración)             | 1052.246 µs              | 1482.743 µs                |
| **Total**                       | **2,030,184 µs (~2.03 s)** | **4,530,080 µs (~4.53 s)** |

**Tamaño de los archivos de biblioteca generados:**

| Archivo               | Tamaño |
|------------------------|:------:|
| `libvectorops.a` (estática)  | 1.8 K |
| `libvectorops.so` (dinámica) | 16 K  |

**Análisis:**

La comparación entre ambas versiones muestra que la biblioteca estática (`bench-static`) supera notablemente en rendimiento a la versión dinámica (`bench-dynamic`), completando la prueba en 2.03 s frente a 4.53 s (una reducción de tiempo superior al 55%). Esta ventaja responde al mecanismo de invocación de funciones: en la versión estática el código objeto se copia directamente dentro del binario final durante el enlazado, resolviendo saltos a direcciones fijas de memoria. En cambio, la biblioteca dinámica requiere código independiente de posición (`-fPIC`) y resuelve los símbolos mediante llamadas indirectas a través de las tablas PLT y GOT (*Procedure Linkage Table* y *Global Offset Table*); esta indirección constante rompe el flujo continuo de ejecución e introduce sobrecarga en cada llamada iterativa. Respecto al tamaño de los archivos, `libvectorops.a` pesa apenas 1.8 KB al ser un simple archivo contenedor (`ar`) de código objeto, mientras que `libvectorops.so` alcanza 16 KB debido a que es un archivo ELF completo que debe incorporar metadatos, secciones de reubicación y tablas dinámicas para permitir su enlace y carga en memoria durante la ejecución.

