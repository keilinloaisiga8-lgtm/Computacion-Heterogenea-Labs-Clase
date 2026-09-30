# Práctica en clase 6 — Introducción a CUDA

Ejercicios: suma de vectores, producto punto y softmax.

**Entorno de ejecución:** Google Colab, GPU NVIDIA Tesla T4, driver 580.82.07, CUDA 12.8 (`nvcc` V12.8.93).

## Cómo compilar y ejecutar

    cd vector-add    # o dot-product, softmax
    make clean
    make
    make run

## Salida de los programas

Ver `salidas.txt`. Todos los programas reportan `OK`.

---

## Ejercicio A: suma de vectores

Se completó `vector_add_kernel` con `c[i] = a[i] + b[i];`. El índice global `i = blockIdx.x * blockDim.x + threadIdx.x` le da a cada hilo un elemento distinto, y `if (i < n)` evita accesos fuera del arreglo.

**¿Cuántos bloques se lanzan cuando N=1048576 y cada bloque tiene 256 hilos?**

El main calcula blocks = (N + 256 − 1) / 256. Con N = 1048576 da 1048576 / 256 = 4096 bloques, o sea 1 048 576 hilos, uno por elemento.

**¿Qué ocurre si N no es múltiplo del tamaño del bloque?**
La fórmula redondea hacia arriba y se lanza un bloque extra parcialmente ocupado. Con N=1000 se lanzan 4 bloques (1024 hilos), los 24 hilos sobrantes tienen `i >= n` y no hacen nada gracias a `if (i < n)`. Sin esa condición accederían fuera de los arreglos. La corrida con N=1000 reporta `OK`.

**¿Qué transferencias de memoria ocurren entre CPU y GPU?**
- CPU → GPU: `cudaMemcpy` de los vectores A y B (`cudaMemcpyHostToDevice`).
- GPU → CPU: después del kernel y `cudaDeviceSynchronize()`, `cudaMemcpy` de C (`cudaMemcpyDeviceToHost`) para verificarlo.
- `cudaMemset` solo inicializa C en ceros dentro de la GPU, no es una transferencia CPU↔GPU.

---

## Ejercicio B: producto punto

Se completó `dot_partial_kernel`: cada hilo calcula `value = a[i] * b[i]` y el bloque reduce en árbol en memoria compartida con `cache[tid] += cache[tid + stride]` (256 → 128 → … → 1). El hilo 0 escribe el parcial del bloque en `partials` y la CPU suma los parciales.

**Papel de `__syncthreads()`:** es una barrera para todos los hilos de un bloque. La primera asegura que todos los productos estén en `cache` antes de reducir,la que está dentro del ciclo asegura que cada paso de la reducción termine antes del siguiente, porque un hilo lee `cache[tid + stride]`, escrito por otro hilo en el paso anterior. Solo sincroniza hilos del mismo bloque.

**¿Por qué este ejercicio no puede resolverse solamente escribiendo un valor independiente por hilo?**
Porque el resultado es un único número que depende de los N productos: los hilos deben combinar sus valores (reducción). Si todos escribieran en la misma variable sin coordinación habría condiciones de carrera y se perderían sumas.

**¿Cuántos valores parciales se copian de GPU a CPU?**
Uno por bloque: N/256. Para N=1048576 son 4096 parciales (16 KB) y para N=4194304 son 16384 parciales (64 KB).

**¿Qué pasaría si se elimina alguna sincronización dentro de la reducción?**
Habría una condición de carrera: los warps de un bloque no avanzan al mismo ritmo, así que un hilo podría leer `cache[tid + stride]` antes de que otro lo escriba. El resultado sería incorrecto y no determinista (a veces `OK`, a veces `ERROR`).

---

## Ejercicio C: softmax

Se completó `softmax_rows_kernel` (un bloque por fila) en tres fases: reducción del máximo con `fmaxf`, cálculo de `expf(x - row_max)` con reducción de la suma, y normalización `output[idx] /= row_sum`.

Además se agregó un `__syncthreads()` después de `float row_max = cache[0];`: como `cache` se reutiliza para las sumas, sin esa barrera el hilo 0 podría sobrescribir `cache[0]` antes de que otros warps leyeran el máximo.

**¿Por qué se calcula primero el máximo de cada fila?**
Por estabilidad numérica: `expf(x)` se desborda a `inf` para x mayor que ~88 en `float`. Restando el máximo, todos los exponentes son ≤ 0 y cada término queda en (0, 1], así que la suma no se desborda. El resultado no cambia porque el factor `e^(-m)` se cancela entre numerador y denominador.

**¿Qué partes del algoritmo requieren cooperación entre hilos del mismo bloque?**
Las dos reducciones: el máximo de la fila y la suma de las exponenciales. Cada hilo procesa solo algunas columnas, así que los parciales se combinan en memoria compartida con `__syncthreads()`. El cálculo de cada exponencial y la normalización son independientes por elemento.

**¿Qué limitación tiene usar un solo bloque por fila cuando `cols` crece mucho?**
Un bloque tiene como máximo 1024 hilos (aquí 256) y se ejecuta en un solo SM, así que con filas muy largas cada hilo recorre muchas columnas en serie y el paralelismo por fila queda limitado. Además, si hay pocas filas se lanzan pocos bloques y muchos SM quedan ociosos. Para filas grandes convendría repartir cada fila entre varios bloques (reducción en dos etapas) o usar reducciones a nivel de warp.
