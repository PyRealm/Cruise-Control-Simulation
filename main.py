import numpy as np
import matplotlib.pyplot as plt
from matplotlib.widgets import Slider

# Parametry Opel Corsa D GSI 2009 1.6L 110kW
M = 1560  # masa [kg]
Cd = 0.3  # współczynnik oporu aerodynamicznego
rho = 1.225  # gęstość powietrza [kg/m^3]
A = 2.583  # powierzchnia czołowa [m^2]
P = 110000  # moc silnika [W]
e = 0.1  # mała liczba, aby uniknąć dzielenia przez zero

def acceleration(v, angle):
    Fg = M * 9.81 * np.sin(np.radians(angle))  # Siła grawitacyjna w zależności od kąta
    Fd = min(P / (v + e), 5165)  # Siła napędowa
    Fa = 0.5 * Cd * rho * A * v**2  # Siła oporu powietrza
    return (Fd - Fa - Fg) / M   # Przyśpieszenie

# Funkcja symulacji
def simulate(v0, vk, angle):
    dt = 0.01  # krok czasowy [s]
    t_max = 100  # maksymalny czas symulacji [s]

    v0 = v0 / 3.6  # Konwersja z km/h na m/s
    vk = vk / 3.6  # Konwersja z km/h na m/s

    time = [0]
    velocity = [v0]

    while (v0 < vk and velocity[-1] < vk) or (v0 > vk and velocity[-1] > vk):
        v_current = velocity[-1]
        t_current = time[-1]
        # Oblicz nową prędkość
        if v0 < vk:
            v_new = v_current + acceleration(v_current, angle) * dt
        else:
            v_new = v_current - acceleration(v_current, angle) * dt
        # Zapisz wartości
        velocity.append(v_new)
        time.append(t_current + dt)

    # Konwersja prędkości na km/h
    velocity_kmh = [v * 3.6 for v in velocity]

    return time, velocity_kmh

# Funkcja aktualizacji wykresu
def update_plot(val):
    v0 = slider_v0.val
    vk = slider_vk.val
    angle = slider_angle.val

    time, velocity = simulate(v0, vk, angle)

    line.set_xdata(time)
    line.set_ydata(velocity)

    ax.relim()
    ax.autoscale_view()

    line_target.set_ydata([vk] * len(time))
    line_target.set_xdata(time)

    fig.canvas.draw_idle()

# Przygotowanie wykresu
fig, ax = plt.subplots(figsize=(10, 6))
mng = plt.get_current_fig_manager()

plt.subplots_adjust(bottom=0.4)
ax.set_xlabel("Czas [s]")
ax.set_ylabel("Prędkość [km/h]")
ax.set_title("Ewolucja prędkości pojazdu w czasie")
ax.grid()

# Początkowy wykres
time, velocity = simulate(0, 30, 0)
line, = ax.plot(time, velocity, label="Prędkość pojazdu")
line_target, = ax.plot(time, [30] * len(time), 'r--', label="Osiągnięcie vk")
ax.legend()

# Slider początkowej prędkości
ax_slider_v0 = plt.axes([0.2, 0.25, 0.6, 0.03])
slider_v0 = Slider(ax_slider_v0, 'Początkowa prędkość [km/h]:', 0, 230, valinit=0)

# Slider końcowej prędkości
ax_slider_vk = plt.axes([0.2, 0.15, 0.6, 0.03])
slider_vk = Slider(ax_slider_vk, 'Końcowa prędkość [km/h]:', 0, 230, valinit=30)

# Slider kąta nachylenia
ax_slider_angle = plt.axes([0.2, 0.05, 0.6, 0.03])
slider_angle = Slider(ax_slider_angle, 'Kąt nachylenia [°]:', -15, 15, valinit=0)

# Podłączenie sliderów do funkcji aktualizacji
slider_v0.on_changed(update_plot)
slider_vk.on_changed(update_plot)
slider_angle.on_changed(update_plot)

plt.show()
