/*
CalcEtaStar.cpp : This file is part bob-rheology (bob) 
bob-2.5 : rheology of Branch-On-Branch polymers
Copyright (C) 2006-2011, 2012 C. Das, D.J. Read, T.C.B. McLeish
 
  This program is free software; you can redistribute it and/or modify
  it under the terms of the GNU General Public License as published by
  the Free Software Foundation; either version 3 of the License, or
  (at your option) any later version.

  This program is distributed in the hope that it will be useful,
  but WITHOUT ANY WARRANTY; without even the implied warranty of
  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
  GNU General Public License for more details. You can find a copy
  of the license at <http://www.gnu.org/licenses/gpl.txt>
*/

#include <stdio.h>
#include <stdlib.h>
#include <math.h>
#include "../../RepTate/reptate_func.h"

double CalcEtaStar(double freq)
{
  // calculate complex viscosity at a particular frequency
  // use gtp.dat data to interpolate or omega, g_p, g_pp if reptate_flag
  extern double interp_logscale(int, double, double *, double *);
  extern bool reptate_flag;

  if (reptate_flag)
  {
    extern std::vector<double> omega, g_p, g_pp;
    double *ff, *competa;
    double eta;
    int ndata, i;
    ndata = omega.size();
    ff = new double[ndata];
    competa = new double[ndata];
    for (i = 0; i < ndata; i++)
    {
      ff[i] = omega[i];
      competa[i] = sqrt(g_p[i] * g_p[i] + g_pp[i] * g_pp[i]) / omega[i];
    }
    eta = interp_logscale(ndata, freq, ff, competa);
    delete[] ff;
    delete[] competa;
    return eta;
  }
  else
  {
    FILE *fid = fopen("gtp.dat", "r");
    extern FILE *infofl;
    double eta = 0.0;
    if (fid == 0)
    {
      fprintf(infofl, "In CalcEtaStar: Did not find gtp.dat \n");
      fprintf(infofl, "Something has gone quite wrong! \n\n");
    }
    else
    {
      int ndata = 0;
      int err = 0;
      double a1, a2, a3;
      while (err != -1)
      {
        err = fscanf(fid, "%lf %lf %lf", &a1, &a2, &a3);
        if (err == 3)
        {
          ndata++;
        }
      }
      fclose(fid);
      double *ff, *competa;
      ff = new double[ndata];
      competa = new double[ndata];

      fid = fopen("gtp.dat", "r");
      for (int i = 0; i < ndata; i++)
      {
        err = fscanf(fid, "%lf %lf %lf", &a1, &a2, &a3);
        ff[i] = a1;
        competa[i] = sqrt(a2 * a2 + a3 * a3) / a1;
      }
      fclose(fid);
      eta = interp_logscale(ndata, freq, ff, competa);
      delete[] ff;
      delete[] competa;
      return eta;
    }
  }
}

// y(x) over discrete nd points
// Do simple linear interpolation in log(y) vs. log (x) and return y(xx)

double interp_logscale(int nd, double xx, double *x, double *y)
{
  double val = 0.0;
  int k1 = 0, k2 = 0;
  if (x[0] < x[nd - 1])
  { // x increasing
    for (int i = 0; i < nd; i++)
    {
      if (k1 == 0)
      {
        if (xx < x[i])
        {
          k1 = 1;
          k2 = i;
        }
      }
    }
    if (k1 == 0)
    {
      k2 = nd - 1;
    }
    if (k2 == 0)
    {
      k2 = 1;
    }
    // xx between x[k2-1] and x[k2]
  }
  else
  { // x decreasing
    for (int i = 0; i < nd; i++)
    {
      if (k1 == 0)
      {
        if (xx > x[i])
        {
          k1 = 1;
          k2 = i;
        }
      }
    }
    if (k1 == 0)
    {
      k2 = nd - 1;
    }
    if (k2 == 0)
    {
      k2 = 1;
    }
  }

  double lx1 = log(x[k2 - 1]);
  double lx2 = log(x[k2]);
  double ly1 = log(y[k2 - 1]);
  double ly2 = log(y[k2]);
  val = exp(ly1 + ((ly2 - ly1) / (lx2 - lx1)) * (log(xx) - lx1));
  return val;
}
