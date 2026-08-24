# Laboratorio 2 - Instrucciones SIMD (AVX2)

**Estudiante:** Keilin Loaisiga  
**Profesor:** Luis León

## Ejercicios A, B y C
Implementación de multiplicación de vectores (A), reducción/suma (B) 
y su uso combinado en el producto punto para la multiplicación de 
matrices (C), usando intrinsics de AVX2 en `matmul_avx2.c`.

## Ejercicio D — Contraste de tiempos

| Versión | Tiempo de ejecución | Rendimiento |
|---|---|---|
| No vectorizada (escalar) | 8.338271 s | 2.060363 GFLOP/s |
| Vectorizada (AVX2) | 2.670748 s | 6.432607 GFLOP/s |

La versión vectorizada con AVX2 fue **3.12 veces más rápida** que la versión 
no vectorizada (speedup = 8.338271 / 2.670748 ≈ 3.12x).

La versión vectorizada es más rápida porque las instrucciones AVX2 procesan 8 floats al mismo tiempo en cada operación, mientras que la versión escalar procesa un float a la vez. Aun así, el speedup real no llega al 8x teórico porque parte del trabajo, como la reducción de los 8 resultados a un solo valor, 
no se beneficia del mismo nivel de paralelismo. Además, el compilador ya optimiza algo la versión escalar con la bandera -O3, por lo que la diferencia entre ambas versiones es menor de lo que sería si la escalar no tuviera ninguna optimización
