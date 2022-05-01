from typing import List
import numpy as np
from shapely.geometry  import Polygon
from sectionproperties.pre.geometry import Geometry, CompoundGeometry
import matplotlib.pyplot as plt
#plt.style.use('science')
#plt.style.context(['science','no-latex']) # If don't have latex de-comment

def create_concio(first_point:List[float], centre:List[float], delta_radius:float, delta_theta:float) -> List[List[float]]:
    x1, y1 = first_point
    xc, yc = centre
    radius = np.sqrt((x1-xc)**2 + (y1-yc)**2)
    if x1<xc:
        try:
            alpha = np.arctan(abs((y1-yc)/(x1-xc)))
        except:
            alpha = 0
        x2, y2 = xc - radius*np.cos(alpha+delta_theta), yc + radius*np.sin(alpha+delta_theta)
        x4, y4 = xc - (radius+delta_radius)*np.cos(alpha), yc + (radius+delta_radius)*np.sin(alpha)
        x3, y3 = xc - (radius+delta_radius)*np.cos(alpha+delta_theta), yc + (radius+delta_radius)*np.sin(alpha+delta_theta)
    else:
        try:
            beta = abs(np.arctan(abs((y1-yc)/(x1-xc))))
        except:
            beta = np.pi/2
        x2, y2 = xc + radius*np.cos(beta-delta_theta), yc + radius*np.sin(beta-delta_theta)
        x4, y4 = xc + (radius+delta_radius)*np.cos(beta), yc + (radius+delta_radius)*np.sin(beta)
        x3, y3 = xc + (radius+delta_radius)*np.cos(beta-delta_theta), yc + (radius+delta_radius)*np.sin(beta-delta_theta)
    
    return [[x1,y1],[x2,y2], [x3,y3] ,[x4,y4]]

def create_riempimento_from_concio(concio:List[List[float]], h:float) -> List[List[float]]:
    """
    concio: a list of coordinated created with create_concio()
    h is from the first point of concio (h1 in the figure)
    """
    if h<concio[2][1]:
        raise ValueError("Height h must be greater (or equal) than the top of concio. See h1 in the figure")
    x1,y1 = concio[3]
    x2,y2 = concio[2]
    x3,y3 = concio[2][0], h
    x4,y4 = concio[3][0], h
    return [[x1,y1],[x2,y2], [x3,y3] ,[x4,y4]]

def create_finitura_from_riempimento(riempimento:List[List[float]], h:float) -> List[List[float]]:
    """
    criempimento: a list of coordinated created with create_concio()
    h is from the first point of concio (h2 in the figure)
    """
    if h<riempimento[2][1]:
        raise ValueError("Height h must be greater (or equal) than the top of rimpimento. See h2 in the figure")
    x1,y1 = riempimento[3]
    x2,y2 = riempimento[2]
    x3,y3 = riempimento[2][0], h
    x4,y4 = riempimento[3][0], h
    return [[x1,y1],[x2,y2], [x3,y3] ,[x4,y4]]

def create_sovraccarico_from_finitura(finitura:List[List[float]], h:float) -> List[List[float]]:
    """
    criempimento: a list of coordinated created with create_concio()
    h is from the first point of concio (h3 in the figure)
    """
    if h<finitura[2][1]:
        raise ValueError("Height h must be greater (or equal) than the top of finitura. See h3 in the figure")
    x1,y1 = finitura[3]
    x2,y2 = finitura[2]
    x3,y3 = finitura[2][0], h
    x4,y4 = finitura[3][0], h
    return [[x1,y1],[x2,y2], [x3,y3] ,[x4,y4]]

#################################################################################

def create_conci(n_conci:int, first_point:List[float], centre:List[float], delta_radius:float, theta:float) -> List[List[List[float]]]:
    delta_theta = theta/n_conci
    print(f"delta_theta = {np.rad2deg(delta_theta)} deg")
    points = []
    fp = first_point
    for concio in range(n_conci):
        c = create_concio(first_point=fp, centre=centre, delta_radius=delta_radius, delta_theta=delta_theta)
        points.append(c)
        fp = c[1]
    return points
    
def create_riempimenti(list_of_conci:List[List[List[float]]], h:float) -> List[List[List[float]]]:
    """
    h is from the first point of the first concio (h1 in the figure)
    """
    return [create_riempimento_from_concio(concio=concio, h=h) for concio in list_of_conci]

def create_finiture(list_of_riempimenti:List[List[List[float]]], h:float) -> List[List[List[float]]]:
    """
    h is from the first point of the first concio (h2 in the figure)
    """
    return [create_finitura_from_riempimento(riempimento=riempimento, h=h) for riempimento in list_of_riempimenti]

def create_sovraccarichi(list_of_finiture:List[List[List[float]]], h:float) -> List[List[List[float]]]:
    """
    h is from the first point of the first concio (h3 in the figure)
    """
    return [create_sovraccarico_from_finitura(finitura=finitura, h=h) for finitura in list_of_finiture]

def create_arco_geom(n_conci:int, first_point:List[float], centre:List[float], delta_radius:float, theta:float, h1:float, h2:float, h3:float) -> CompoundGeometry:

    list_of_conci = create_conci(n_conci=n_conci, first_point=first_point, centre=centre, delta_radius=delta_radius, theta=theta)
    conci_geom = [Geometry(Polygon(concio)) for concio in list_of_conci]

    list_of_riempimenti = create_riempimenti(list_of_conci=list_of_conci, h=h1)
    riempimenti_geom = [Geometry(Polygon(riempimenti)) for riempimenti in list_of_riempimenti]

    list_of_finiture = create_finiture(list_of_riempimenti=list_of_riempimenti, h=h2)
    finiture_geom = [Geometry(Polygon(finitura)) for finitura in list_of_finiture]

    list_of_sovraccarichi = create_sovraccarichi(list_of_finiture=list_of_finiture, h=h3)
    sovraccarichi_geom = [Geometry(Polygon(sovraccarico)) for sovraccarico in list_of_sovraccarichi]

    arc:List[Geometry] = []
    arc.extend(conci_geom)
    arc.extend(riempimenti_geom)
    arc.extend(finiture_geom)
    arc.extend(sovraccarichi_geom)

    arco = arc[0]
    for geom in arc[1:]:
        arco +=geom

    return arco

if __name__ == "__main__":
    arco = create_arco_geom(n_conci=20, first_point=[0,0], centre=[1.7928,-1.255], delta_radius=.5, theta=np.deg2rad(111.0526), h1=2, h2=2.3, h3=2.8)
    arco.plot_geometry()

