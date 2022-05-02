__all__ = ['createCollapseOperators']

from math import sqrt
from . import gateLib as gl


def createCollapseOperators(Qblist):
    """Function for creating the collapse operators for mcsolve.
     Input: Qblist = List of Qubit objects (see Qb_class)
     output: list of tensored qobj with correct dimensions for each noise"""
    c_ops = []
    for i in range(0, len(Qblist)):
        if Qblist[i].noisert_vec[0] > 0.0:  # Relaxation
            c_ops.append(sqrt(Qblist[i].noisert_vec[0]) * gl.PM(Qblist, i))
        if Qblist[i].noisert_vec[1] > 0.0:  # Dephasing
            c_ops.append(sqrt(Qblist[i].noisert_vec[1]) * gl.PZ(Qblist, i)/2)
        if Qblist[i].noisert_vec[2] > 0.0:  # Thermal
            c_ops.append(sqrt(Qblist[i].noisert_vec[3]) * gl.PP(Qblist, i))
    return c_ops
