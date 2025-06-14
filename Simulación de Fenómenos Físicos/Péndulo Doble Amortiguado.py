import numpy as np
import plotly.graph_objects as go
import matplotlib.pyplot as plt
import scipy.integrate as spi

#Parametros del sistema
g=9.81  # gravedad (m/s^2)
L1=1.0  # longitud del primer péndulo (m)
L2=1.0  # longitud del segundo péndulo (m)
m1=1.0  # masa del primer péndulo (kg)
m2=1.0  # masa del segundo péndulo (kg)
b1=0.15  # coeficiente de fricción del primer péndulo (N·s/m)
b2=0.15  # coeficiente de fricción del segundo péndulo (N·s/m)
theta1_0=np.pi/2  # ángulo inicial del primer péndulo (rad)
theta2_0=np.pi/2  # ángulo inicial del segundo péndulo (rad)
omega1_0=0.0  # velocidad angular inicial del primer péndulo (rad/s)
omega2_0=0.0  # velocidad angular inicial del segundo péndulo (rad/s)

# Sistema de ecuaciones
def pendulo_doble(t,y):
    theta1,omega1,theta2,omega2=y
    delta=theta2-theta1
    den1=(m1+m2)*L1-m2*L1*np.cos(delta)**2
    den2=(L2/L1)*den1
    dtheta1_dt=omega1
    dtheta2_dt=omega2
    domega1_dt=(m2*L1*omega1**2*np.sin(delta)*np.cos(delta)
              +m2*g*np.sin(theta2)*np.cos(delta)
              +m2*L2*omega2**2*np.sin(delta)
              -(m1+m2)*g*np.sin(theta1)
              -b1*omega1)/den1
    domega2_dt=(-m2*L2*omega2**2*np.sin(delta)*np.cos(delta)
              +(m1+m2)*(g*np.sin(theta1)*np.cos(delta)
              -L1*omega1**2*np.sin(delta)
              -g*np.sin(theta2))
              -b2*omega2)/den2
    return [dtheta1_dt,domega1_dt,dtheta2_dt,domega2_dt]

# Intervalo de tiempo para la simulación
t_span=(0,30)
t_eval=np.linspace(t_span[0],t_span[1],750)

# Resolver la ecuación diferencial
sol=spi.solve_ivp(pendulo_doble,t_span,[theta1_0,omega1_0,theta2_0,omega2_0],t_eval=t_eval,method='RK45',rtol=1e-8,atol=1e-10)

# Obtener ángulos y coordenadas cartesianas
theta1=sol.y[0]
theta2=sol.y[2]
omega1=sol.y[1]
omega2=sol.y[3]
x1=L1*np.sin(theta1)
y1=-L1*np.cos(theta1)
x2=L1*np.sin(theta1)+L2*np.sin(theta2)
y2=-L1*np.cos(theta1)-L2*np.cos(theta2)

frames=[]
for i in range(len(t_eval)):
    frame=go.Frame(data=[
        go.Scatter(x=[0,x1[i],x2[i]],y=[0,y1[i],y2[i]],mode='lines+markers',line=dict(width=4),
                  marker=dict(size=[0,20,20],color='red'))
    ],name=str(i))
    frames.append(frame)

# Figura base
fig=go.Figure(
    data=[go.Scatter(x=[0,x1[0],x2[0]],y=[0,y1[0],y2[0]],mode='lines+markers',line=dict(width=4),
                     marker=dict(size=[0,20,20],color='red'))],
    layout=go.Layout(
        title="Péndulo Doble Amortiguado",
        xaxis=dict(range=[-2,2],autorange=False),
        yaxis=dict(range=[-2,2],autorange=False, scaleanchor="x",scaleratio=1),
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

# Gráficos parámetros del sistema
plt.figure()
plt.plot(t_eval,theta1,'b-',label='Ángulo 1(rad)')
plt.plot(t_eval,theta2,'r-', label='Ángulo 2(rad)')
plt.xlabel('Tiempo (s)')
plt.ylabel('Ángulo (rad)')
plt.title('Ángulos del Péndulo Doble Amortiguado')
plt.legend()
plt.grid()

plt.figure()
plt.plot(t_eval,omega1,'b-',label='Frecuencia Angular 1(rad)')
plt.plot(t_eval,omega2,'r-',label='Frecuencia Angular 2(rad)')
plt.xlabel('Tiempo (s)')
plt.ylabel('Frecuencia Angular (rad/s)')
plt.title('Frecuencias Angulares del Péndulo Doble Amortiguado')
plt.legend()
plt.grid()

plt.show()