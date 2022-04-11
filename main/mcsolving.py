from qutip import *


def mcs(psi,H,tlist,c_ops, e_ops, returnFullList = False):
    if c_ops != []:
        output = mcsolve(H, psi, tlist, c_ops=c_ops, e_ops = e_ops, ntraj=1, progress_bar=None)
        if not returnFullList:
            outstate = (output.states[:, -1])
            return outstate[0]
        else:
            outstate = (output.states)
            return outstate

    else:
        output = sesolve(H, psi, tlist, e_ops = e_ops)
        if not returnFullList:
            outstate = output.states[-1]
        else:
            outstate = output.states
        return outstate
    # the virtual gates should be able to apply through matrix multiplication
    # if virtualgate != None:
    #   psi0 = virtualgates[i] * psi0

def virtgate(psi,vgate):
    return vgate*psi