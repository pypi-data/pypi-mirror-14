#include <Python.h>
#include <numpy/arrayobject.h>
#define _USE_MATH_DEFINES
#include <math.h>


typedef void (*Sampler)(PyArrayObject* equirect, float* v, float* s);

static PyObject* cube_map_check(PyObject* self, PyObject* args);
static PyObject* equirect_check(PyObject* self, PyObject* args);

static PyObject* cube_map_assign(PyObject* self, PyObject* args);
static PyObject* equirect_assign(PyObject* self, PyObject* args);

static PyObject* cube_map_get_sampler(PyObject* self, PyObject* args);
static PyObject* equirect_get_sampler(PyObject* self, PyObject* args);

static PyMethodDef SphairaFunctions[] = {
  /* check */
  { "cube_map_check", cube_map_check, METH_VARARGS
  , "check if array has the shape of a cube map projection"
  }
, { "equirect_check", equirect_check, METH_VARARGS
  , "check if array has the shape for an equirectangular projection"
  }
  /* assign */
, { "cube_map_assign", cube_map_assign, METH_VARARGS
  , "assign the cube map from an image sphere"
  }
, { "equirect_assign", equirect_assign, METH_VARARGS
  , "assign the equirectangular map from an image sphere"
  }
  /* sample */
, { "cube_map_get_sampler", cube_map_get_sampler, METH_VARARGS
  , "get the sampler for cube maps"
  }
, { "equirect_get_sampler", equirect_get_sampler, METH_VARARGS
  , "get the sampler for equirectangular projections"
  }
, {NULL, NULL, 0, NULL}
};

static PyObject* cube_map_check(PyObject* self, PyObject* args)
{
  int ret = 0;
  PyArrayObject* cube_map;
  if (!PyArg_ParseTuple(args, "O", &cube_map)) {
    ret = 1; goto exit;
  }
  if (PyArray_Check(cube_map) == 0) {
    ret = 2; goto exit;
  }
  if (PyArray_TYPE(cube_map) != NPY_FLOAT32) {
    ret = 3; goto exit;
  }
  if (PyArray_NDIM(cube_map) != 4) {
    ret = 4; goto exit;
  }
  if (PyArray_DIM(cube_map, 3) != 4) {
    ret = 5; goto exit;
  }
  if (PyArray_DIM(cube_map, 0) != 6) {
    ret = 6; goto exit;
  }
  if (PyArray_DIM(cube_map, 1) != PyArray_DIM(cube_map, 2)) {
    ret = 7; goto exit;
  }
exit:
  return PyInt_FromLong(ret);
}

static PyObject* equirect_check(PyObject* self, PyObject* args)
{
  int ret = 0;
  PyArrayObject* equirect;
  if (!PyArg_ParseTuple(args, "O", &equirect)) {
    ret = 1; goto exit;
  }
  if (PyArray_Check(equirect) == 0) {
    ret = 2; goto exit;
  }
  if (PyArray_TYPE(equirect) != NPY_FLOAT32) {
    ret = 3; goto exit;
  }
  if (PyArray_NDIM(equirect) != 3) {
    ret = 4; goto exit;
  }
  if (PyArray_DIM(equirect, 2) != 4) {
    ret = 5; goto exit;
  }
  if (2*PyArray_DIM(equirect, 0) != PyArray_DIM(equirect, 1)) {
    ret = 6; goto exit;
  }
exit:
  return PyInt_FromLong(ret);
}

static PyObject* cube_map_assign(PyObject* self, PyObject* args)
{
  PyArrayObject* cube_map;
  PyArrayObject* data_sphere;
  PyObject* sampler_cobj;
  Sampler sampler;
  int size, sf, sy, sx, sd, f, y, x, d;
  char* data;
  float t, u, v[3], s[4];
  if (!PyArg_ParseTuple(args, "OOO", &cube_map, &data_sphere, &sampler_cobj)) {
    return NULL;
  }
  sampler = PyCObject_AsVoidPtr(sampler_cobj);
  size = PyArray_DIM(cube_map, 1);
  data = PyArray_DATA(cube_map);
  sf = PyArray_STRIDE(cube_map, 0);
  sy = PyArray_STRIDE(cube_map, 1);
  sx = PyArray_STRIDE(cube_map, 2);
  sd = PyArray_STRIDE(cube_map, 3);
  for (f = 0; f < 6; f++) {
    for (y = 0; y < size; y++) {
      for (x = 0; x <  size; x++) {
        t = 2.0*x / size - 1.0;
        u = 2.0*y / size - 1.0;
        switch (f) {
          case 0: v[0] = +1; v[1] = -u; v[2] = -t; break;
          case 1: v[0] = -1; v[1] = -u; v[2] = +t; break;
          case 2: v[0] = +t; v[1] = +1; v[2] = +u; break;
          case 3: v[0] = +t; v[1] = -1; v[2] = -u; break;
          case 4: v[0] = +t; v[1] = -u; v[2] = +1; break;
          case 5: v[0] = -t; v[1] = -u; v[2] = -1; break;
        }
        sampler(data_sphere, v, s);
        for (d = 0; d < 4; d++) {
          *(float*)(data + f*sf + y*sy + x*sx + d*sd) = s[d];
        }
      }
    }
  }
  return Py_None;
}

static PyObject* equirect_assign(PyObject* self, PyObject* args)
{
  PyArrayObject* equirect;
  PyArrayObject* data_sphere;
  PyObject* sampler_cobj;
  Sampler sampler;
  int height, width, sy, sx, sd, y, x, d;
  char* data;
  float phi, theta, v[3], s[4];
  if (!PyArg_ParseTuple(args, "OOO", &equirect, &data_sphere, &sampler_cobj)) {
    return NULL;
  }
  sampler = PyCObject_AsVoidPtr(sampler_cobj);
  height = PyArray_DIM(equirect, 0);
  width = 2*height;
  data = PyArray_DATA(equirect);
  sy = PyArray_STRIDE(equirect, 0);
  sx = PyArray_STRIDE(equirect, 1);
  sd = PyArray_STRIDE(equirect, 2);
  for (y = 0; y < height; y++) {
    for (x = 0; x < width; x++) {
      phi = M_PI*(2.0*x / width - 1.0);
      theta = M_PI*((float)y / height);
      v[0] = sin(theta)*cos(phi);
      v[1] = sin(theta)*sin(phi);
      v[2] = cos(theta);
      sampler(data_sphere, v, s);
      for (d = 0; d < 4; d++) {
        *(float*)(data + y*sy + x*sx + d*sd) = s[d];
      }
    }
  }
  return Py_None;
}

static void cube_map_sample(PyArrayObject* cube_map, float* v, float* s) {
  int size, sf, sy, sx, sd, f, y, x, d;
  char* data;
  float t, u, ax, ay, az;
  size = PyArray_DIM(cube_map, 1);
  sf = PyArray_STRIDE(cube_map, 0);
  sy = PyArray_STRIDE(cube_map, 1);
  sx = PyArray_STRIDE(cube_map, 2);
  sd = PyArray_STRIDE(cube_map, 3);
  ax = fabs(v[0]);
  ay = fabs(v[1]);
  az = fabs(v[2]);
  switch ((ax > ay) | (ay > az) << 1 | (az > ax) << 2) {
  case 1: case 3:
    f = 0 | (v[0] < 0); t = -v[2] / v[0]; u = -v[1] / ax; break;
  case 2: case 6:
    f = 2 | (v[1] < 0); t = +v[0] / ay; u = +v[2] / v[1]; break;
  case 4: case 5: case 0: case 7:
    f = 4 | (v[2] < 0); t = +v[0] / v[2]; u = -v[1] / az; break;
  }
  x = (0.5*t + 0.5)*(size - 1);
  y = (0.5*u + 0.5)*(size - 1);
  data = PyArray_DATA(cube_map);
  for (d = 0; d < 4; d++) {
    s[d] = *(float*)(data + f*sf + y*sy + x*sx + d*sd);
  }
}

static PyObject* cube_map_get_sampler(PyObject* self, PyObject* args) {
  return PyCObject_FromVoidPtr(cube_map_sample, NULL);
}

static void equirect_sample(PyArrayObject* equirect, float* v, float* s) {
  int width, height, sy, sx, sd, y, x, d;
  char* data;
  float phi, r, theta, t, u;
  height = PyArray_DIM(equirect, 0);
  width = PyArray_DIM(equirect, 1);
  sy = PyArray_STRIDE(equirect, 0);
  sx = PyArray_STRIDE(equirect, 1);
  sd = PyArray_STRIDE(equirect, 2);
  phi = atan2(v[1], v[0]);
  r = sqrt(v[0]*v[0] + v[1]*v[1] + v[2]*v[2]);
  theta = acos(v[2] / r);
  t = phi/(2*M_PI) + 0.5;
  u = theta/M_PI;
  x = t*(width - 1);
  y = u*(height - 1);
  data = PyArray_DATA(equirect);
  for (d = 0; d < 4; d++) {
    s[d] = *(float*)(data + y*sy + x*sx + d*sd);
  }
}

static PyObject* equirect_get_sampler(PyObject* self, PyObject* args) {
  return PyCObject_FromVoidPtr(equirect_sample, NULL);
}

/* This initiates the module using the above definitions. */
#if PY_VERSION_HEX >= 0x03000000
static struct PyModuleDef moduledef = {
    PyModuleDef_HEAD_INIT,
    "sphaira",
    NULL,
    -1,
    SphairaFunctions,
    NULL,
    NULL,
    NULL,
    NULL
};

PyMODINIT_FUNC PyInit_external(void)
{
    PyObject *m;
    m = PyModule_Create(&moduledef);
    if (!m) {
        return NULL;
    }
    import_array();
    return m;
}
#else
PyMODINIT_FUNC initexternal(void)
{
    PyObject *m;

    m = Py_InitModule("external", SphairaFunctions);
    if (m == NULL) {
        return;
    }
    import_array();
}
#endif
