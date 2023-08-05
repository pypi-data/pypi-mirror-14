import matplotlib.pyplot as plt
from elastopy import draw
from elastopy import processing


def show():
    plt.show()


def model(mesh, name=None, color='k', dpi=100, ele=False, ele_label=False,
          surf_label=False, nodes_label=False, edges_label=False):
    """Plot the  model geometry

    """
    fig = plt.figure(name, dpi=dpi)
    ax = fig.add_subplot(1, 1, 1)
    ax.set_xlabel(r'x')
    ax.set_ylabel(r'y')
    ax.set_aspect('equal')

    draw.domain(mesh, ax, color=color)

    if ele is True:
        draw.elements(mesh, ax, color=color)

    if ele_label is True:
        draw.elements_label(mesh, ax)

    if surf_label is True:
        draw.surface_label(mesh, ax)

    if nodes_label is True:
        draw.nodes_label(mesh, ax)

    if edges_label is True:
        draw.edges_label(mesh, ax)

    return None


def model_deformed(mesh, U, magf=1, ele=False, name=None, color='Tomato', dpi=100):
    """Plot deformed model

    """
    fig = plt.figure(name, dpi=dpi)
    ax = fig.add_subplot(1, 1, 1)
    ax.set_xlabel(r'x')
    ax.set_ylabel(r'y')
    ax.set_aspect('equal')

    if ele is True:
        draw.elements(mesh, ax, color='SteelBlue')
        draw.deformed_elements(mesh, U, ax, magf=magf, color=color)

    draw.domain(mesh, ax, color='SteelBlue')
    draw.deformed_domain(mesh, U, ax, magf=magf, color=color)


def stress(mesh, sNode, ftr=1, s11=False, s12=False, s22=False, spmax=False,
           spmin=False, dpi=100, name=None, lev=20):
    """Plot stress with nodal stresses

    """
    fig = plt.figure(name, dpi=dpi, facecolor=None)
    ax = fig.add_subplot(1, 1, 1)
    ax.set_aspect('equal')
    ax.set_xlabel(r'x')
    ax.set_ylabel(r'y')

    if s11 is True:
        ax.set_title(r'Stress 11 ('+str(ftr)+' Pa)')
        draw.tricontourf(mesh, sNode[0]/ftr, ax, 'spring', lev=lev)

    if s12 is True:
        ax.set_title(r'Stress 12 ('+str(ftr)+' Pa)')
        draw.tricontourf(mesh, sNode[2]/ftr, ax, 'cool', lev=lev)

    if s22 is True:
        ax.set_title(r'Stress 22 ('+str(ftr)+' Pa)')
        draw.tricontourf(mesh, sNode[1]/ftr, ax, 'autumn', lev=lev)

    if spmax is True:
        spmx = processing.principal_stress_max(sNode[0], sNode[1], sNode[2])
        ax.set_title(r'Stress Principal Max ('+str(ftr)+' Pa)')
        draw.tricontourf(mesh, spmx/ftr, ax, 'plasma', lev=lev)

    if spmin is True:
        spmn = processing.principal_stress_min(sNode[0], sNode[1], sNode[2])
        ax.set_title(r'Stress Principal Min ('+str(ftr)+' Pa)')
        draw.tricontourf(mesh, spmn/ftr, ax, 'viridis', lev=lev)
