import numpy as np
import plotly.graph_objects as go
from scipy.integrate import solve_ivp
import matplotlib.pyplot as plt

# Parámetros del sistema
m=1 # masa (kg)
k=1 # constante del resorte (N/m)
x_0=1 # posición inicial (m)
v_0=0 # velocidad inicial (m/s)
b=0.15 # coeficiente de fricción (N·s/m)


# Sistema de ecuaciones
def resorte(t,x_v):
    x,v=x_v
    dx_dt=v
    dv_dt=-k/m*x-b*v
    return [dx_dt,dv_dt]

# Intervalo de tiempo para la simulación
t_span=(0,75)
t_eval=np.linspace(t_span[0],t_span[1],750)

# Resolver la ecuación diferencial
sol=solve_ivp(resorte,t_span,[x_0,v_0],t_eval=t_eval)

x=sol.y[0]
v=sol.y[1]

frames=[]
for i in range(len(t_eval)):
    frame=go.Frame(data=[go.Scatter(x=[x[i]],y=[0],mode='markers',marker=dict(size=15, color='red'))],name=str(i))
    frames.append(frame)

sliders=[{
    "steps":[
        {
            "args":[[str(i)],{"frame":{"duration":0,"redraw":True},"mode":"immediate"}],
            "label":f"{t_eval[i]:.1f}s",
            "method":"animate"
        }
        for i in range(len(t_eval))
    ],
    "transition":{"duration":0},
    "x":0.1,"xanchor":"left",
    "y":-0.1,"yanchor":"top"
}]

# Figura base
fig=go.Figure(
    data=[go.Scatter(x=[x[0]],y=[0],mode='markers',marker=dict(size=15, color='red'))],
    layout=go.Layout(
        title="Resorte Amortiguado",
        xaxis=dict(range=[-1,1],autorange=False),
        yaxis=dict(range=[-1,1],autorange=False,scaleanchor="x",scaleratio=1),
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
        )],
        sliders=sliders
    ),
    frames=frames
)

fig.show()

plt.figure()
plt.plot(t_eval,x,'c-')
plt.xlabel('Tiempo (s)')   
plt.ylabel('Posición (m)')
plt.title('Posición del Resorte Amortiguado')
plt.grid()

plt.figure()
plt.plot(t_eval,v,'r-')
plt.xlabel('Tiempo (s)')   
plt.ylabel('Velocidad (m/s)')
plt.title('Velocidad del Resorte Amortiguado')
plt.grid()

E=0.5*m*v**2+0.5*k*x**2

plt.figure()
plt.plot(t_eval,E,'m-')
plt.xlabel('Tiempo (s)')   
plt.ylabel('Energía (J)')
plt.title('Energía del Resorte Amortiguado')
plt.grid()

plt.figure()
plt.plot(v,x,'g-')
plt.xlabel('Velocidad (m/s)')   
plt.ylabel('Posición (m)')
plt.title('Espacio de Fase del Resorte Amortiguado')
plt.grid()

plt.show()