import numpy as np
from integrador import integrar_orbita
from simulador import graficar_orbitas

# Constantes
G=1.0
M=1.0
mu=G*M
t_span=(0,20)
t_eval=np.linspace(t_span[0],t_span[1],1000)

# Escenarios de condiciones iniciales
escenarios={
    "Circular":[1.0,0.0,0.0,0.0,np.sqrt(mu/1.0),0.0],
    "Elíptica":[1.2,0.0,0.0,0.0,0.7*np.sqrt(mu/1.2),0.0],
    "Inclinada":[1.0,0.0,0.0,0.0,0.8*np.sqrt(mu/1.0),0.4]
}

solutions=[]
nombres=[]
for nombre,r_t in escenarios.items():
    sol=integrar_orbita(r_t,G,M,t_span,t_eval)
    solutions.append(sol)
    nombres.append(nombre)

# Graficamos todas juntas con menú
graficar_orbitas(solutions,nombres,R_tierra=0.2)
