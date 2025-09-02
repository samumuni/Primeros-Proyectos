import numpy as np
import plotly.graph_objects as go

def graficar_orbitas(solutions,nombres,R_tierra=1.0):
    data=[]
    frames_dict={}
    for i,sol in enumerate(solutions):
        xs,ys,zs=sol.y[0],sol.y[1],sol.y[2]
        orbit_trace=go.Scatter3d(
            x=xs,y=ys,z=zs,
            mode="lines",name=f"Órbita{nombres[i]}",
            visible=(i==0)
        )
        sat_trace=go.Scatter3d(
            x=[xs[0]],y=[ys[0]],z=[zs[0]],
            mode="markers", name=f"Satélite {nombres[i]}",
            marker=dict(size=5,color="red"),
            visible=(i==0)
        )
        data.extend([orbit_trace,sat_trace])
        frames=[]
        tail_length=50
        for j in range(len(xs)):
            start=max(0,j-tail_length)
            frames.append(go.Frame(data=[
                go.Scatter3d(x=xs,y=ys,z=zs,mode="lines"),
                go.Scatter3d(x=[xs[j]],y=[ys[j]],z=[zs[j]],
                             mode="markers",marker=dict(size=5,color="red")),
                go.Scatter3d(x=xs[start:j+1],y=ys[start:j+1],z=zs[start:j+1],
                             mode="lines",line=dict(width=3,color="red"))
            ], name=f"{nombres[i]}_frame{j}"))
        frames_dict[nombres[i]]=frames

    phi=np.linspace(0,np.pi,30)
    theta=np.linspace(0,2*np.pi,60)
    phi,theta=np.meshgrid(phi,theta)
    X=R_tierra*np.sin(phi)*np.cos(theta)
    Y=R_tierra*np.sin(phi)*np.sin(theta)
    Z=R_tierra*np.cos(phi)
    earth_surface=go.Surface(x=X,y=Y,z=Z,colorscale="Blues",
                            opacity=0.7,showscale=False,name="Tierra")

    buttons=[dict(label="Play",method="animate",
             args=[None,dict(frame=dict(duration=30,redraw=True),
                            fromcurrent=True)]),
        dict(label="Pause",method="animate",
             args=[[None],dict(frame=dict(duration=0,redraw=False),
                            mode="immediate")])
    ]

    dropdown=[dict(
        buttons=[
            dict(label=nombre,
                 method="animate",
                 args=[frames_dict[nombre],
                       dict(frame=dict(duration=30,redraw=True),
                            mode="immediate")])
            for nombre in nombres
        ],
        direction="down",
        showactive=True,
        x=0.15,y=1.15,xanchor="left",yanchor="top"
    )]

    layout=go.Layout(
        title="Simulación orbital 3D con varias órbitas",
        scene=dict(
            xaxis=dict(title="X+"),
            yaxis=dict(title="Y"),
            zaxis=dict(title="Z"),
            aspectmode="data"
        ),
        updatemenus=[dict(type="buttons",buttons=buttons,
                          x=0,y=1.15,xanchor="left",yanchor="top")]+dropdown
    )
    all_frames=sum(frames_dict.values(),[])
    fig=go.Figure(data=[earth_surface]+data,
                    layout=layout,frames=all_frames)
    fig.show()
