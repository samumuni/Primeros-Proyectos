import numpy as np

def orbita(t,r_t,G,M):
    x,y,z,v_x,v_y,v_z=r_t[0],r_t[1],r_t[2],r_t[3],r_t[4],r_t[5]
    r=np.sqrt(x**2+y**2+z**2)
    dx_dt=v_x
    dy_dt=v_y
    dz_dt=v_z
    dv_x_dt=-G*M*x/r**3
    dv_y_dt=-G*M*y/r**3
    dv_z_dt=-G*M*z/r**3
    return [dx_dt,dy_dt,dz_dt,dv_x_dt,dv_y_dt,dv_z_dt]