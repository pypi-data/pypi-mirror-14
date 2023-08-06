#include <Python.h>
#include <stdlib.h>
#include <stdio.h>
#include <math.h>
#include <string.h>

#define ndim 1

typedef struct {

	double OmegaM, OmegaL, OmegaG, OmegaK, H0, c;

} universe;

universe* LambdaCDM(void) {

	universe* LCDM = (universe*)malloc(sizeof(universe));
	LCDM->OmegaM = 0.3089;
	LCDM->OmegaL = 0.6911;
	LCDM->OmegaG = 0.0;
	LCDM->OmegaK = 0.0;
	LCDM->H0 = 67.74e3;
	LCDM->c = 299792458.0;
	
	return LCDM;
}

double FRW(universe* model, double a) {

	double result = pow(model->H0, 2)*(model->OmegaM/pow(a,3) + model->OmegaG/pow(a,4) + model->OmegaK/pow(a,2) + model->OmegaL);
	return result;
}

void dChi(double a, double f[], double rhsf[], universe* model) {

	rhsf[0] = 1.0/(sqrt(FRW(model, a)) * pow(a, 2))*model->c;
	
}

void RK4_step(double t, double dt, double f_t[], void(*rhs_function)(double t, double f[], double rhsf[], universe* model), universe *model ) {

	double f_f[ndim];
	double rhsf[ndim];
	double f_k[ndim];
	double k, h, s, z;
	int i, j;
	
	memcpy(f_k, f_t, sizeof(double)*ndim );
	memcpy(f_f, f_t, sizeof(double)*ndim );
	
	for (j=0; j<4; ++j) {
		h = ((j + 1) / 2)*0.5;
		s = ((j + 2) / 2)*0.5;
		z = -0.25*j*(j-3)+0.5;
		rhs_function(t + h * dt, f_k, rhsf, model);
		for (i=0; i<ndim; ++i) {
			k = dt * rhsf[i];
			f_k[i] = f_t[i] + s * k;
			f_f[i] += k*z/3.0;
		}
	}
	memcpy(f_t, f_f, sizeof(double)*ndim );
}



double LumDist(universe* model, double a0, double da) {

	double a;
	double chi[1];
	chi[0] = 0;
	for (a = a0; a < 1; a += da)
		RK4_step(a, da, chi, dChi, model);
	da = a0 - a;
	if (da > 0)
		RK4_step(1, da, chi, dChi, model);
	double result = chi[0]/a0;
	return result;
}	


static PyObject* PyLumDist(PyObject *self, PyObject *args, PyObject *keywds) {

	const char* model_str = "LCDM";
	double a0;
	double da = 0.01;
	double result;
	universe* model;

	static char* kwlist[] = {"a","da","model", NULL};
	
	if (!PyArg_ParseTupleAndKeywords(args, keywds, "d|ds", kwlist, &a0, &da, &model_str))
		return NULL;	
	if (strcmp(model_str,"LCDM") == 0)
		model = LambdaCDM();
	else 
		return NULL;
	result = LumDist(model, a0, da);

	return Py_BuildValue("f", result);
}

static PyMethodDef LumDistMethods[] = {
	{"LumDist",(PyCFunction)PyLumDist, METH_VARARGS | METH_KEYWORDS, "Calculate Luminosity Distance"},
	{NULL, NULL, 0, NULL}
};

PyMODINIT_FUNC initLumDist(void) {
	(void)Py_InitModule("LumDist", LumDistMethods);
}


int main(int argc, char* argv[]) {

	Py_SetProgramName(argv[0]);
	Py_Initialize();
	initLumDist();

	return 0;
}
/*
int main(void) {

	double* z = (double*)malloc(sizeof(double)*10);
	int i;
	universe* LCDM = LambdaCDM();
	for (i = 0; i < 10; ++i)
		z[i] = exp(i/sqrt(2));
	for (i = 0; i < 10; ++i)
		printf("%f %f\n", z[i], LumDist(LCDM, 1.0/(1+z[i]), 0.001));

	free(z);

	return 0;
}


*/
