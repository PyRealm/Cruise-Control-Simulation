from flask import Flask, render_template, request
import numpy as np
import plotly.graph_objects as go
from plotly.subplots import make_subplots

app = Flask(__name__)

previous_velocity = None
previous_time = None
previous_drive_forces = None
previous_aerodynamic_forces = None
previous_gravity_forces = None


def pid(setpoint, process_variable, Tp, Ti, Td, dt, integral, prev_error, kp):
    error = setpoint - process_variable
    integral += error * dt
    derivative = (error - prev_error) / dt if dt > 0 else 0
    output = kp * (error + (Tp / Ti) * integral + (Td / Tp) * derivative)
    return output, error, integral


def simulate_cruise_control(v0,
                            v_set,
                            mass,
                            drag_coeff,
                            frontal_area,
                            tau,
                            theta,
                            Tp,
                            Ti,
                            Td,
                            kp,
                            dt=0.1,
                            sim_time=50):
    g = 9.81
    time = np.arange(0, sim_time, dt)
    velocity = [v0]
    drive_forces = []
    errors = []
    aerodynamic_forces = []
    gravity_forces = []
    integral = 0
    prev_error = 0
    fd = 0

    for t in time[:-1]:
        current_velocity = velocity[-1]
        fa = drag_coeff * frontal_area * current_velocity**2
        fg = mass * g * np.sin(np.radians(theta))
        u, error, integral = pid(v_set, current_velocity, Tp, Ti, Td, dt,
                                 integral, prev_error, kp)
        fd += (1 / tau) * (u - fd) * dt
        acceleration = (fd - fa - fg) / mass
        new_velocity = max(current_velocity + acceleration * dt, 0)
        velocity.append(new_velocity)
        drive_forces.append(fd)
        errors.append(error)
        aerodynamic_forces.append(fa)
        gravity_forces.append(fg)
        prev_error = error
    return time, velocity, drive_forces, aerodynamic_forces, gravity_forces


def plot_results(time, velocity, v_set, drive_forces, aerodynamic_forces,
                 gravity_forces, max_time):
    global previous_velocity, previous_time, previous_drive_forces, previous_aerodynamic_forces, previous_gravity_forces

    fig = make_subplots(rows=1,
                        cols=2,
                        subplot_titles=("Przebiegi zmian prędkości",
                                        "Przebiegi zmian sił"),
                        shared_xaxes=True)

    fig.add_trace(go.Scatter(x=time,
                             y=[v * 3.6 for v in velocity],
                             mode='lines',
                             name="Aktualna prędkość"),
                  row=1,
                  col=1)

    if previous_velocity is not None and previous_time is not None:
        fig.add_trace(go.Scatter(x=previous_time,
                                 y=[v * 3.6 for v in previous_velocity],
                                 mode='lines',
                                 name="Poprzednia prędkość",
                                 line=dict(dash='dash')),
                      row=1,
                      col=1)

    fig.add_trace(go.Scatter(x=time,
                             y=[v_set] * len(time),
                             mode='lines',
                             name="Prędkość docelowa",
                             line=dict(dash='dash', color='red')),
                  row=1,
                  col=1)

    fig.update_yaxes(title_text="Prędkość [km/h]", row=1, col=1)

    fig.add_vline(x=max_time,
                  line=dict(color='green', dash='dot'),
                  name="Maksymalny czas",
                  row=1,
                  col=1)

    fig.add_trace(go.Scatter(x=time[:-1],
                             y=drive_forces,
                             mode='lines',
                             name="Siła napędowa"),
                  row=1,
                  col=2)

    fig.add_trace(go.Scatter(x=time[:-1],
                             y=aerodynamic_forces,
                             mode='lines',
                             name="Siła oporu aerodynamicznego"),
                  row=1,
                  col=2)

    fig.add_trace(go.Scatter(x=time[:-1],
                             y=gravity_forces,
                             mode='lines',
                             name="Siła grawitacyjna"),
                  row=1,
                  col=2)

    if previous_drive_forces is not None:
        fig.add_trace(go.Scatter(x=previous_time[:-1],
                                 y=previous_drive_forces,
                                 mode='lines',
                                 name="Poprzednia siła napędowa",
                                 line=dict(dash='dash')),
                      row=1,
                      col=2)
        fig.add_trace(go.Scatter(x=previous_time[:-1],
                                 y=previous_aerodynamic_forces,
                                 mode='lines',
                                 name="Poprzednia siła oporu aerodynamicznego",
                                 line=dict(dash='dash')),
                      row=1,
                      col=2)
        fig.add_trace(go.Scatter(x=previous_time[:-1],
                                 y=previous_gravity_forces,
                                 mode='lines',
                                 name="Poprzednia siła grawitacyjna",
                                 line=dict(dash='dash')),
                      row=1,
                      col=2)

    fig.update_yaxes(title_text="Siła [N]", row=1, col=2)

    fig.update_layout(
        template="simple_white",
        legend=dict(orientation="h",
                    x=0.5,
                    y=-0.3,
                    xanchor="center",
                    yanchor="top",
                    traceorder="normal",
                    font=dict(size=12),
                    bgcolor="rgba(255, 255, 255, 0)",
                    bordercolor="Black",
                    borderwidth=1),
    )

    fig.update_xaxes(title_text="Czas [s]", row=1, col=1)
    fig.update_xaxes(title_text="Czas [s]", row=1, col=2)

    previous_velocity = velocity
    previous_time = time
    previous_drive_forces = drive_forces
    previous_aerodynamic_forces = aerodynamic_forces
    previous_gravity_forces = gravity_forces

    return fig.to_html(full_html=False)


@app.route('/', methods=['GET', 'POST'])
def index():
    plot_html = None
    if request.method == 'POST':
        v0 = float(request.form['v0']) / 3.6
        v_set = float(request.form['v_set']) / 3.6
        theta = float(request.form['theta'])
        Tp = float(request.form['Tp'])
        Ti = float(request.form['Ti'])
        Td = float(request.form['Td'])
        car_type = request.form['car_type']

        car_params = {
            "sport": {
                "frontal_area": 2.53,
                "mass": 1500
            },
            "personal": {
                "frontal_area": 4.583,
                "mass": 2800
            },
            "truck": {
                "frontal_area": 8.635,
                "mass": 8000
            },
        }

        params = car_params[car_type]
        drag_coeff = 0.3
        mass = params["mass"]
        frontal_area = params["frontal_area"]
        tau = 0.35
        kp = 1500

        time, velocity, drive_forces, aerodynamic_forces, gravity_forces = simulate_cruise_control(
            v0, v_set, mass, drag_coeff, frontal_area, tau, theta, Tp, Ti, Td,
            kp)

        max_time = 50

        plot_html = plot_results(time, velocity, v_set * 3.6, drive_forces,
                                 aerodynamic_forces, gravity_forces, max_time)

    v0 = request.form.get('v0', 0)
    v_set = float(request.form['v_set']) if 'v_set' in request.form else 80
    Tp = request.form.get('Tp', 0.5)
    Ti = request.form.get('Ti', 1.0)
    Td = request.form.get('Td', 0.5)
    theta = request.form.get('theta', 15)
    car_type = request.form.get('car_type', 'personal')

    return render_template('index.html',
                           plot_html=plot_html,
                           v0=int(float(v0)),
                           v_set=int(float(v_set)),
                           Tp=float(Tp),
                           Ti=float(Ti),
                           Td=float(Td),
                           theta=int(theta),
                           car_type=car_type)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)
