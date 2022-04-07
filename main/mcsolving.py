from qutip import *


def mcs(psi,H,tlist,c_ops, e_ops):
    if c_ops != []:
        output = mcsolve(H, psi, tlist, c_ops=c_ops, e_ops = e_ops, ntraj=1, progress_bar=None)
        outstate = (output.states[:, -1])
        return outstate[0]
    else:
        output = sesolve(H, psi, tlist, e_ops = e_ops)
        outstate = output.states[-1]
        return outstate
    # the virtual gates should be able to apply through matrix multiplication
    # if virtualgate != None:
    #   psi0 = virtualgates[i] * psi0

def virtgate(psi,vgate):
    return vgate*psi