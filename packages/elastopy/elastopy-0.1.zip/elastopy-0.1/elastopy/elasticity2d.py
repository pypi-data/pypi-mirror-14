from scipy.sparse.linalg import spsolve
from scipy import sparse
import elastopy.element2dof as element2dof
import elastopy.assemble2dof as assemble2dof
import elastopy.boundaryconditions2dof as boundaryconditions2dof
import elastopy.processing as processing


def solver(mesh, material, body_forces, traction_imposed,
           displacement_imposed, **kwargs):

    ele = element2dof.Matrices(mesh)

    s = mesh.surfaces
    matDic = {s[i]: material[j] for i, j in enumerate(material)}

    ele.stiffness(matDic)

    ele.body_forces(body_forces)

    ele.initial_strain(kwargs)

    K = assemble2dof.globalMatrix(ele.K, mesh)

    P0q = assemble2dof.globalVector(ele.P0q, mesh)

    P0t = boundaryconditions2dof.neumann(mesh, traction_imposed)

    P0e = assemble2dof.globalVector(ele.P0e, mesh)

    P0 = P0q + P0t + P0e

    Km, P0m = boundaryconditions2dof.dirichlet(K, P0, mesh,
                                               displacement_imposed)

    Ks = sparse.csc_matrix(Km)

    U = spsolve(Ks, P0m)

    sNode, sEle, eEle = processing.stress_recovery_simple2(mesh, U, matDic,
                                                           ele.e0)

    return U, sNode
