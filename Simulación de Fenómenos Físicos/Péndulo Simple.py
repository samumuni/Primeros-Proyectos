import numpy as np
from scipy.integrate import solve_ivp
import plotly.graph_objects as go
import matplotlib.pyplot as plt

# Parámetros del péndulo
g=9.81      # gravedad (m/s^2)
L=1.0       # longitud de la cuerda (m)
theta0=np.pi/4  # ángulo inicial (45 grados)
omega0=0.0        # velocidad angular inicial

# Sistema de ecuaciones
def pendulo(t,y):
    theta,omega=y
    dtheta_dt=omega
    domega_dt=-(g/L)*np.sin(theta)
    return [dtheta_dt,domega_dt]

# Intervalo de tiempo para la simulación
t_span=(0,10)
t_eval=np.linspace(t_span[0],t_span[1],750)

# Resolver la ecuación diferencial
sol=solve_ivp(pendulo,t_span,[theta0,omega0],t_eval=t_eval)

# Obtener ángulos y coordenadas cartesianas
theta=sol.y[0]
omega=sol.y[1]
x=L*np.sin(theta)
y=-L*np.cos(theta)

frames=[]
for i in range(len(t_eval)):
    frame=go.Frame(data=[go.Scatter(x=[0,x[i]],y=[0,y[i]],mode='lines+markers',line=dict(width=4))],name=str(i))
    frames.append(frame)

# Figura base
fig=go.Figure(
    data=[go.Scatter(x=[0,x[0]],y=[0,y[0]],mode='lines+markers',line=dict(width=4))],
    layout=go.Layout(
        title="Péndulo Simple",
        xaxis=dict(range=[-1.2, 1.2], autorange=False),
        yaxis=dict(range=[-1.2, 0.2], autorange=False, scaleanchor="x", scaleratio=1),
        updatemenus=[dict(
            type="buttons",
            showactive=False,
            buttons=[dict(label="▶ Play", method="animate",
                          args=[None, {
                              "frame": {"duration": 20, "redraw": True},
                              "transition": {"duration": 0},
                              "fromcurrent": True,
                              "mode": "immediate"
                          }]
            )]
        )]
    ),
    frames=frames
)


fig.show()

plt.figure()
plt.plot(t_eval, theta,'c-' ,label='Ángulo (rad)')
plt.xlabel('Tiempo (s)')   
plt.ylabel('Ángulo (rad)')
plt.title('Ángulo del Péndulo Simple')
plt.grid()

plt.figure()
plt.plot(t_eval, omega,'r-' ,label='Frecuencia angular (rad/s)')
plt.xlabel('Tiempo (s)')   
plt.ylabel('Frecuencia angular (rad/s)')
plt.title('Frecuencia Angular del Péndulo Simple')
plt.grid()

plt.show()