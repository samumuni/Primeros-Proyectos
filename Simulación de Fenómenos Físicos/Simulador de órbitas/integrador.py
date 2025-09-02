import numpy as np
import scipy.integrate as spi
import orbita as ob 

def integrar_orbita(r_t,G,M,t_span,t_eval):
    print("Iniciando la integración numérica de la órbita...")
    sol=spi.solve_ivp(ob.orbita,t_span,r_t,args=(G,M),t_eval=t_eval,method="LSODA",rtol=1e-6,atol=1e-8)
    return sol