#ifndef PYSPACE_H
#define PYSPACE_H

void brute_force_update(double* x, double* y, double* z, 
        double* v_x, double* v_y, double* v_z,
        double* a_x, double* a_y, double* a_z,
        double* m, double G, double dt, int num_planets);

#endif
