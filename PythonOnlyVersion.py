import numpy as np
import matplotlib.pyplot as plt
import tkinter as tk
from tkinter import ttk

# --- Funkcja PID ---
def pid(setpoint, process_variable, Tp, Ti, Td, dt, integral, prev_error, kp):
    error = setpoint - process_variable
    integral += error * dt
    derivative = (error - prev_error) / dt if dt > 0 else 0
    output = kp * (error + (Tp / Ti) * integral + (Td / Tp) * derivative)
    return output, error, integral

# Symulacja tempomatu
def simulate_cruise_control(v0, v_set, mass, drag_coeff, frontal_area, tau, theta, Tp, Ti, Td, kp, dt=0.1, sim_time=50):
    g = 9.81
    time = np.arange(0, sim_time, dt)
    velocity = [v0]
    control_forces = []
    drive_forces = []
    errors = []
    aerodynamic_forces = []
    gravitational_forces = []
    fd = 0
    prev_error = 0
    integral = 0

    for t in time[:-1]:
        current_velocity = velocity[-1]

        # Dynamiczna siła oporu aerodynamicznego
        fa = drag_coeff * frontal_area * current_velocity ** 2
        fg = mass * g * np.sin(np.radians(theta))

        u, error, integral = pid(v_set, current_velocity, Tp, Ti, Td, dt, integral, prev_error, kp)


        fd += (1 / tau) * (u - fd) * dt

        acceleration = (fd - fa - fg) / mass
        new_velocity = max(current_velocity + acceleration * dt, 0)

        velocity.append(new_velocity)
        control_forces.append(u)
        drive_forces.append(fd)
        errors.append(error)
        aerodynamic_forces.append(fa)
        gravitational_forces.append(fg)
        prev_error = error

    return time, velocity, control_forces, drive_forces, errors, aerodynamic_forces, gravitational_forces

# Kontrola jakości
def calculate_quality_indicators(errors, control_forces, Tp):
    iae = Tp * sum(abs(e) for e in errors)
    ise = Tp * sum(e**2 for e in errors)
    iau = Tp * sum(abs(u) for u in control_forces)
    return iae, ise, iau

# Funkcja generowania wykresów
def generate_plots(v0, v_set, car_type, theta, Tp, Ti, Td):
    car_params = {
        "sport": {"frontal_area": 1.03, "mass": 800},
        "personal": {"frontal_area": 2.583, "mass": 1560},
        "truck": {"frontal_area": 5.635, "mass": 5000},
    }
    params = car_params[car_type]

    drag_coeff = 0.3
    frontal_area = params["frontal_area"]
    mass = params["mass"]
    amplification_factor = 2000
    tau = 0.35
    dt = 0.1
    sim_time = 21

    time, velocity, control_forces, drive_forces, errors, fa, fg = simulate_cruise_control(
        v0 / 3.6,
        v_set / 3.6,
        mass,
        drag_coeff,
        frontal_area,
        tau,
        theta,
        Tp,
        Ti,
        Td,
        amplification_factor,
        dt,
        sim_time,
    )

    # Rysowanie wykresów
    plt.figure(figsize=(12, 6))

    # Wykres prędkości
    plt.subplot(1, 2, 1)
    plt.plot(time, [v * 3.6 for v in velocity], label="Prędkość")
    plt.plot(time, [v_set] * len(time), 'r--', label="Prędkość docelowa")
    plt.xlabel("Czas [s]")
    plt.ylabel("Prędkość [km/h]")
    plt.title("Przebieg zmian prędkości w czasie")
    plt.legend()

    # Wykres sił
    plt.subplot(1, 2, 2)
    plt.plot(time[:-1], drive_forces, label="Siła napędowa")
    plt.plot(time[:-1], [mass * 9.81 * np.sin(np.radians(theta))] * len(time[:-1]), 'g--', label="Siła grawitacyjna")
    plt.plot(time[:-1], fa, label="Siła oporu aerodynamicznego")
    plt.xlabel("Czas [s]")
    plt.ylabel("Siła [N]")
    plt.title("Przebieg zmian sił działających na pojazd")
    plt.legend()

    plt.tight_layout()
    plt.show()

# Funkcja interfejsu GUI w Tkinter
def run_gui():
    def on_generate_click():
        v0 = v0_slider.get()
        v_set = v_slider.get()
        car_type = car_type_combobox.get()
        theta = angle_slider.get()
        Tp = Tp_slider.get()
        Ti = Ti_slider.get()
        Td = Td_slider.get()
        generate_plots(v0, v_set, car_type, theta, Tp, Ti, Td)

    # Tworzenie głównego okna
    root = tk.Tk()
    root.title("Symulacja Tempomatu")

    # Sliders
    v0_slider = tk.Scale(root, from_=0, to=100, orient=tk.HORIZONTAL, label="Prędkość początkowa [km/h]", tickinterval=20)
    v0_slider.set(20)
    v0_slider.pack()

    v_slider = tk.Scale(root, from_=0, to=150, orient=tk.HORIZONTAL, label="Prędkość docelowa [km/h]", tickinterval=25)
    v_slider.set(75)
    v_slider.pack()

    angle_slider = tk.Scale(root, from_=-30, to=30, orient=tk.HORIZONTAL, label="Kąt nachylenia [°]", tickinterval=5)
    angle_slider.set(15)
    angle_slider.pack()

    Tp_slider = tk.Scale(root, from_=0, to=3, orient=tk.HORIZONTAL, label="Okres próbkowania [s]: Tp", resolution=0.3)
    Tp_slider.set(0.6)
    Tp_slider.pack()

    Ti_slider = tk.Scale(root, from_=0, to=2, orient=tk.HORIZONTAL, label="Czas zdwojenia [s]: Ti", resolution=0.1)
    Ti_slider.set(1)
    Ti_slider.pack()

    Td_slider = tk.Scale(root, from_=0, to=2, orient=tk.HORIZONTAL, label="Czas wyprzedzenia [s]: Td", resolution=0.1)
    Td_slider.set(0.4)
    Td_slider.pack()

    # Dropdown for car type
    car_type_label = tk.Label(root, text="Typ samochodu:")
    car_type_label.pack()

    car_type_combobox = ttk.Combobox(root, values=["sport", "personal", "truck"])
    car_type_combobox.set("personal")
    car_type_combobox.pack()

    # Button to generate plots
    generate_button = tk.Button(root, text="Generuj wykresy", command=on_generate_click)
    generate_button.pack()

    # Uruchomienie GUI
    root.mainloop()

# Uruchomienie aplikacji
if __name__ == "__main__":
    run_gui()
