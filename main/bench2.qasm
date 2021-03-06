OPENQASM 2.0;
include "qelib1.inc";

qreg q[4];
creg c[4];

ry(2) q[0];
ry(6) q[1];
ry(3) q[2];
ry(2) q[3];
cz q[0], q[1];
ry(5) q[0];
cz q[1], q[3];
id q[0];
id q[1];
id q[2];
id q[3];
cz q[1], q[2];
ry(9) q[3];
ry(2) q[1];
ry(2) q[2];
cz q[0], q[1];
ry(2) q[0];
cz q[1], q[3];
cz q[1], q[2];
ry(6*pi) q[1];
ry(3*2) q[2];
ry((2*5*7)/5*7) q[3];