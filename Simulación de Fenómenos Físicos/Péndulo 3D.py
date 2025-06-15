import numpy as np
import plotly.graph_objects as go
import matplotlib.pyplot as plt
import scipy.integrate as spi

# Parametros del sistema
m=1.0      # kg
L=1.0      # m
g=9.81     # m/s²
b_1=0.1  # fricción en theta
b_2=0.05    # fricción en phi

theta_0=np.pi/4   # inclinación inicial
phi_0=0.0           # azimutal inicial
v_theta0=0.0
v_phi0=1.0       # inicia girando en torno al eje

def pendulo_3d(t,y):
    theta,v_theta,phi,v_phi=y
    epsilon=1e-6
    sin_theta=np.sin(theta)
    sin_theta_safe=sin_theta if abs(sin_theta)>epsilon else np.sign(sin_theta)*epsilon
    dtheta_dt=v_theta
    dphi_dt=v_phi
    dv_theta_dt=(-g/L)*np.sin(theta)-(b_1*v_theta)/(m*L**2)+v_phi**2*np.sin(theta)*np.cos(theta)
    dv_phi_dt=(-2*v_theta*v_phi*np.cos(theta)/sin_theta_safe)-(b_2*v_phi)/(m*L**2*sin_theta_safe**2)
    return [dtheta_dt,dv_theta_dt,dphi_dt,dv_phi_dt]


# Intervalo de tiempo para la simulación
t_span=(0,60)
t_eval=np.linspace(t_span[0],t_span[1],100)

print('Iniciando la integración numérica del péndulo 3D...')

# Resolver la ecuación diferencial
sol=spi.solve_ivp(pendulo_3d,t_span,[theta_0, v_theta0, phi_0, v_phi0],t_eval=t_eval,method='RK45',rtol=1e-4,atol=1e-5)

if not sol.success:
    print("Integración fallida:", sol.message)
else:
    print("Integración completada correctamente.")

print("¿Hay NaNs?",np.any(np.isnan(sol.y)))
print("¿Hay infs?",np.any(np.isinf(sol.y)))
print("Tiempo final alcanzado:", sol.t[-1])

# Obtener ángulos y coordenadas cartesianas
theta=sol.y[0]
v_theta=sol.y[1]
phi=sol.y[2]
v_phi=sol.y[3]
x=L*np.cos(phi)*np.sin(theta)
y=L*np.sin(phi)*np.sin(theta)
z=-L*np.cos(theta)

frames=[]
for i in range(len(t_eval)):
    frame=go.Frame(data=[
        go.Scatter3d(x=[0,x[i]],y=[0,y[i]],z=[0,z[i]],mode='lines+markers',
                     line=dict(width=4),marker=dict(size=[0,10],color='red'))
    ],name=str(i))
    frames.append(frame)

fig=go.Figure(data=frames[0].data,layout=go.Layout(
    title='Péndulo 3D',
    scene=dict(
        xaxis=dict(range=[-L*1.2,L*1.2],title='X'),
        yaxis=dict(range=[-L*1.2,L*1.2],title='Y'),
        zaxis=dict(range=[-L*1.2,L*1.2],title='Z')
    ),
    updatemenus=[dict(type='buttons',buttons=[dict(label='Play',method='animate',
                args=[None,dict(frame=dict(duration=50,redraw=True),fromcurrent=True)])])]
))

fig.frames=frames
fig.show()

plt.figure()
plt.plot(t_eval,theta,'m-',label='Ángulo (rad)')
plt.plot(t_eval,phi,'c-',label='Acimutal (rad)')
plt.xlabel('Tiempo (s)')   
plt.ylabel('Ángulo (rad)')
plt.title('Ángulo del Péndulo Simple')
plt.legend()
plt.grid()

plt.figure()
plt.plot(t_eval,v_theta,'m-' ,label='Frecuencia angular (rad/s)')
plt.plot(t_eval,v_phi,'c-' ,label='Frecuencia acimutal (rad/s)')
plt.xlabel('Tiempo (s)')   
plt.ylabel('Frecuencia angular (rad/s)')
plt.title('Frecuencias Angulares del Péndulo Simple')
plt.legend()
plt.grid()

plt.show()