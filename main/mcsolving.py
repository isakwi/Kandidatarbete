from qutip import *

#options = Options()
#options.store_states = True  # If e_ops != 0, it wont store states?

def mcs(psi,H,tlist,c_ops, e_ops, returnFullList = False):
    if c_ops != []:
        output = mcsolve(H, psi, tlist, c_ops=c_ops, e_ops = [], ntraj=1, progress_bar=None) #, options=options)
        if not returnFullList:
            outstate = (output.states[:, -1])
            return outstate[0]
        else:
            outstate = (output.states)
            return outstate
    else:
        output = sesolve(H, psi, tlist, e_ops = [])
        if not returnFullList:
            outstate = output.states[-1]
        else:
            outstate = output.states
        return outstate

def mcs_expectation(psi, H, tlist, c_ops, e_ops, returnFullList=True):
    """Use this if StoreTimeDynamics=True . So that we don't need the if returnFullList , might be nicer/quicker ?"""
    if c_ops != []:
        output = mcsolve(H, psi, tlist, c_ops=c_ops, e_ops=[], ntraj=1, progress_bar=None) #, options=options)
        outstates = output.states
        return outstates
    else:
        output = sesolve(H, psi, tlist, e_ops=[]) #, options=options)
        expectvals = output.expect
        outstates = output.states
        return outstates



    # the virtual gates should be able to apply through matrix multiplication
    # if virtualgate != None:
    #   psi0 = virtualgates[i] * psi0

def virtgate(psi,vgate):
    return vgate*psi