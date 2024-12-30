import numpy as np
import matplotlib.pyplot as plt

# Parametry pojazdu i środowiska
M = 1200  # masa pojazdu [kg]
Cd = 0.3  # współczynnik oporu powietrza [-]
A = 2.5  # powierzchnia czołowa [m^2]
rho = 1.225  # gęstość powietrza [kg/m^3]
g = 9.81  # przyspieszenie ziemskie [m/s^2]
alpha = np.deg2rad(5)  # kąt nachylenia drogi [stopnie -> radiany]

# Parametry regulatora PI
kp = 500  # wzmocnienie proporcjonalne
Ti = 5  # czas zdwojenia [s]
Tp = 0.1  # okres próbkowania [s]
F_max = 4000  # maksymalna siła napędowa [N]

# Prędkość docelowa (wybrana przez użytkownika)
v_zadane = 27  # 27 m/s (ok. 100 km/h)

# Inicjalizacja zmiennych
czas_symulacji = 60  # czas symulacji [s]
n = int(czas_symulacji / Tp)
v = np.zeros(n)  # prędkość [m/s]
Fd = np.zeros(n)  # siła napędowa [N]
e = np.zeros(n)  # uchyb prędkości
u = np.zeros(n)  # sygnał sterujący

# Symulacja regulatora PI
for i in range(1, n):
    # Uchyb prędkości
    e[i] = v_zadane - v[i-1]
    
    # Algorytm przyrostowy PI
    du = kp * (e[i] - e[i-1]) + (Tp / Ti) * e[i]
    u[i] = u[i-1] + du
    
    # Ograniczenie siły napędowej
    Fd[i] = np.clip(u[i], 0, F_max)
    
    # Siła aerodynamiczna i grawitacyjna
    Fa = Cd * rho * A * v[i-1]**2
    Fg = M * g * np.sin(alpha)
    
    # Równanie ruchu
    dv = (Fd[i] - Fa - Fg) / M
    v[i] = v[i-1] + dv * Tp

# Wykres wyników
plt.figure(figsize=(12, 6))
plt.plot(np.arange(0, czas_symulacji, Tp), v, label='Prędkość [m/s]')
plt.plot(np.arange(0, czas_symulacji, Tp), u, label='Sygnał regulatora [N]')
plt.axhline(y=v_zadane, color='r', linestyle='--', label='Prędkość zadana')
plt.xlabel('Czas [s]')
plt.ylabel('Wartość')
plt.title('Symulacja tempomatu z regulatorem PI')
plt.legend()
plt.grid(True)
plt.show()
