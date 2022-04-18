OPENQASM 2.0;
include "qelib1.inc";

qreg q[2];
creg c[2];
h q[0];
h q[1];
barrier q[0];
h q[1];
cz q[0], q[1];
rx(2) q[1];
barrier q[0];
cz q[0], q[1];
h q[1];
barrier q[0];
rz(3*2) q[0];
rz(4) q[1];
rx(5) q[0];
rx(6) q[1];