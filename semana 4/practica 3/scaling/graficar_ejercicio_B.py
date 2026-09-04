#!/usr/bin/env python3
"""
Ejercicio B - Practica de clase 3
"""
import matplotlib.pyplot as plt

# --- Datos reportados por cada programa (linea "Tiempo: X segundos") ---
threads = [1, 2, 3, 4, 5, 6, 7, 8]

tiempos = {
    "softmax_openmp": [1.918103, 1.512720, 1.393136, 1.326736, 1.558101,
                        1.679793, 1.731459, 1.803397],
    "matmul_tiled_openmp": [2.061402, 1.035956, 0.703250, 0.528066, 0.593219,
                             0.500617, 0.450287, 0.509152],
}


def analizar(nombre, t):
    t1 = t[0]
    speedup = [t1 / ti for ti in t]
    eficiencia = [s / p for s, p in zip(speedup, threads)]

    print(f"\n{nombre}")
    print(f"{'Hilos':>6} {'Tiempo(s)':>10} {'Speedup':>9} {'Eficiencia':>11}")
    for p, ti, s, e in zip(threads, t, speedup, eficiencia):
        print(f"{p:>6} {ti:>10.3f} {s:>9.3f} {e:>11.3f}")


for nombre, t in tiempos.items():
    analizar(nombre, t)

# --- grafico: tiempo vs hilos ---
plt.figure()
for nombre, t in tiempos.items():
    plt.plot(threads, t, marker="o", label=nombre)
plt.xlabel("Numero de hilos")
plt.ylabel("Tiempo (s)")
plt.title("Tiempo vs numero de hilos - Ejercicio B")
plt.legend()
plt.grid(True)
plt.savefig("ejercicioB_tiempo.png", dpi=150, bbox_inches="tight")
print("\nGuardado: ejercicioB_tiempo.png")
