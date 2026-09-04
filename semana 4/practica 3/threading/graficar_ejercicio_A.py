#!/usr/bin/env python3
"""
Ejercicio A - Practica de clase 3
Grafica del tiempo real vs numero de hilos para cpu-naive y cpu-affinity
"""
import matplotlib.pyplot as plt

# --- Datos medidos con 'time ./programa', columna 'real' ---
threads = [1, 2, 3, 4, 5, 6, 7, 8]

tiempos = {
    "cpu-naive": [4.098, 4.158, 4.414, 4.534, 4.444, 4.632, 4.795, 4.712],
    "cpu-affinity": [3.750, 3.933, 4.089, 3.993, 4.056, 4.092, 4.093, 3.911],
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

# --- grafico: tiempo real vs hilos ---
plt.figure()
for nombre, t in tiempos.items():
    plt.plot(threads, t, marker="o", label=nombre)
plt.xlabel("Numero de hilos")
plt.ylabel("Tiempo real (s)")
plt.title("Tiempo real vs numero de hilos")
plt.legend()
plt.grid(True)
plt.savefig("ejercicioA_tiempo.png", dpi=150, bbox_inches="tight")
print("\nGuardado: ejercicioA_tiempo.png")
