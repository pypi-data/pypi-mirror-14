#include "pyspace.h"
#include <cmath>
#include <iostream>
#include <omp.h>

#define MAGNITUDE(x, y, z) sqrt(x*x + y*y + z*z)

void brute_force_update(double* x, double* y, double* z,
        double* v_x, double* v_y, double* v_z,
        double* a_x, double* a_y, double* a_z,
        double* m, double G, double dt, int num_planets)
{
    //Calculate and update all pointers
    double a_x_i, a_y_i, a_z_i;
    double v_x_i, v_y_i, v_z_i;
    double r_x_i, r_y_i, r_z_i;
    double r_x_j, r_y_j, r_z_j;
    double x_ji, y_ji, z_ji;
    double temp_a_x = 0, temp_a_y = 0, temp_a_z = 0;
    double dist_ij, cnst;
    double m_j;

    double* x_old = new double[num_planets];
    double* y_old = new double[num_planets];
    double* z_old = new double[num_planets];

    #pragma omp parallel for shared(x_old, y_old, z_old, x, y, z)
    for(int i=0; i<num_planets; i++)
    {
        x_old[i] = x[i];
        y_old[i] = y[i];
        z_old[i] = z[i];
    }

    #pragma omp parallel for shared(x, y, z, x_old, y_old, z_old, v_x, v_y, v_z, \
            a_x, a_y, a_z, m, G, dt) \
    private(a_x_i, a_y_i, a_z_i, v_x_i, v_y_i, v_z_i, r_x_i, r_y_i, r_z_i, r_x_j, \
      r_y_j, r_z_j, x_ji, y_ji, z_ji, temp_a_x, temp_a_y, temp_a_z, dist_ij, \
      cnst, m_j)
    for(int i=0; i<num_planets; i++)
    {
        a_x_i = a_x[i];
        a_y_i = a_y[i];
        a_z_i = a_z[i];

        v_x_i = v_x[i];
        v_y_i = v_y[i];
        v_z_i = v_z[i];

        r_x_i = x[i];
        r_y_i = y[i];
        r_z_i = z[i];

        for(int j=0; j<num_planets; j++)
        {
            if(j == i)
                continue;

            r_x_j = x_old[j];
            r_y_j = y_old[j];
            r_z_j = z_old[j];

            m_j = m[j];

            x_ji = r_x_j - r_x_i;
            y_ji = r_y_j - r_y_i;
            z_ji = r_z_j - r_z_i;

            dist_ij = MAGNITUDE(x_ji, y_ji, z_ji);

            cnst = (G*m_j/(dist_ij*dist_ij*dist_ij));

            temp_a_x += x_ji*cnst;
            temp_a_y += y_ji*cnst;
            temp_a_z += z_ji*cnst;
        }

        a_x[i] = temp_a_x;
        a_y[i] = temp_a_y;
        a_z[i] = temp_a_z;

        temp_a_x = 0;
        temp_a_y = 0;
        temp_a_z = 0;

        x[i] += v_x_i*dt + a_x_i*0.5*dt*dt;
        y[i] += v_y_i*dt + a_y_i*0.5*dt*dt;
        z[i] += v_z_i*dt + a_z_i*0.5*dt*dt;

        v_x[i] += (a_x_i + a_x[i])*0.5*dt;
        v_y[i] += (a_y_i + a_y[i])*0.5*dt;
        v_z[i] += (a_z_i + a_z[i])*0.5*dt;

    }

    delete[] x_old;
    delete[] y_old;
    delete[] z_old;
}
