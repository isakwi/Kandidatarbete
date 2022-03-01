"""
Definition of functions:
- CreateGates (Gate, target, NoOfGates, QbLevel) - > Tensored operator where gate acts on correct qubit
- TimeDependGates (tlist) - > QobjEvo of time dependant gate with correct drive interval
- AddGates ( QobjEvo ) - > Adds QobjEvos to final Hamiltonian

"""

import GateLib