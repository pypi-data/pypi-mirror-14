
#include <Python.h>
#include <stddef.h>

/* this block of #ifs should be kept exactly identical between
   c/_cffi_backend.c, cffi/vengine_cpy.py, cffi/vengine_gen.py */
#if defined(_MSC_VER)
# include <malloc.h>   /* for alloca() */
# if _MSC_VER < 1600   /* MSVC < 2010 */
   typedef __int8 int8_t;
   typedef __int16 int16_t;
   typedef __int32 int32_t;
   typedef __int64 int64_t;
   typedef unsigned __int8 uint8_t;
   typedef unsigned __int16 uint16_t;
   typedef unsigned __int32 uint32_t;
   typedef unsigned __int64 uint64_t;
   typedef __int8 int_least8_t;
   typedef __int16 int_least16_t;
   typedef __int32 int_least32_t;
   typedef __int64 int_least64_t;
   typedef unsigned __int8 uint_least8_t;
   typedef unsigned __int16 uint_least16_t;
   typedef unsigned __int32 uint_least32_t;
   typedef unsigned __int64 uint_least64_t;
   typedef __int8 int_fast8_t;
   typedef __int16 int_fast16_t;
   typedef __int32 int_fast32_t;
   typedef __int64 int_fast64_t;
   typedef unsigned __int8 uint_fast8_t;
   typedef unsigned __int16 uint_fast16_t;
   typedef unsigned __int32 uint_fast32_t;
   typedef unsigned __int64 uint_fast64_t;
   typedef __int64 intmax_t;
   typedef unsigned __int64 uintmax_t;
# else
#  include <stdint.h>
# endif
# if _MSC_VER < 1800   /* MSVC < 2013 */
   typedef unsigned char _Bool;
# endif
#else
# include <stdint.h>
# if (defined (__SVR4) && defined (__sun)) || defined(_AIX)
#  include <alloca.h>
# endif
#endif

#if PY_MAJOR_VERSION < 3
# undef PyCapsule_CheckExact
# undef PyCapsule_GetPointer
# define PyCapsule_CheckExact(capsule) (PyCObject_Check(capsule))
# define PyCapsule_GetPointer(capsule, name) \
    (PyCObject_AsVoidPtr(capsule))
#endif

#if PY_MAJOR_VERSION >= 3
# define PyInt_FromLong PyLong_FromLong
#endif

#define _cffi_from_c_double PyFloat_FromDouble
#define _cffi_from_c_float PyFloat_FromDouble
#define _cffi_from_c_long PyInt_FromLong
#define _cffi_from_c_ulong PyLong_FromUnsignedLong
#define _cffi_from_c_longlong PyLong_FromLongLong
#define _cffi_from_c_ulonglong PyLong_FromUnsignedLongLong

#define _cffi_to_c_double PyFloat_AsDouble
#define _cffi_to_c_float PyFloat_AsDouble

#define _cffi_from_c_int_const(x)                                        \
    (((x) > 0) ?                                                         \
        ((unsigned long long)(x) <= (unsigned long long)LONG_MAX) ?      \
            PyInt_FromLong((long)(x)) :                                  \
            PyLong_FromUnsignedLongLong((unsigned long long)(x)) :       \
        ((long long)(x) >= (long long)LONG_MIN) ?                        \
            PyInt_FromLong((long)(x)) :                                  \
            PyLong_FromLongLong((long long)(x)))

#define _cffi_from_c_int(x, type)                                        \
    (((type)-1) > 0 ? /* unsigned */                                     \
        (sizeof(type) < sizeof(long) ?                                   \
            PyInt_FromLong((long)x) :                                    \
         sizeof(type) == sizeof(long) ?                                  \
            PyLong_FromUnsignedLong((unsigned long)x) :                  \
            PyLong_FromUnsignedLongLong((unsigned long long)x)) :        \
        (sizeof(type) <= sizeof(long) ?                                  \
            PyInt_FromLong((long)x) :                                    \
            PyLong_FromLongLong((long long)x)))

#define _cffi_to_c_int(o, type)                                          \
    ((type)(                                                             \
     sizeof(type) == 1 ? (((type)-1) > 0 ? (type)_cffi_to_c_u8(o)        \
                                         : (type)_cffi_to_c_i8(o)) :     \
     sizeof(type) == 2 ? (((type)-1) > 0 ? (type)_cffi_to_c_u16(o)       \
                                         : (type)_cffi_to_c_i16(o)) :    \
     sizeof(type) == 4 ? (((type)-1) > 0 ? (type)_cffi_to_c_u32(o)       \
                                         : (type)_cffi_to_c_i32(o)) :    \
     sizeof(type) == 8 ? (((type)-1) > 0 ? (type)_cffi_to_c_u64(o)       \
                                         : (type)_cffi_to_c_i64(o)) :    \
     (Py_FatalError("unsupported size for type " #type), (type)0)))

#define _cffi_to_c_i8                                                    \
                 ((int(*)(PyObject *))_cffi_exports[1])
#define _cffi_to_c_u8                                                    \
                 ((int(*)(PyObject *))_cffi_exports[2])
#define _cffi_to_c_i16                                                   \
                 ((int(*)(PyObject *))_cffi_exports[3])
#define _cffi_to_c_u16                                                   \
                 ((int(*)(PyObject *))_cffi_exports[4])
#define _cffi_to_c_i32                                                   \
                 ((int(*)(PyObject *))_cffi_exports[5])
#define _cffi_to_c_u32                                                   \
                 ((unsigned int(*)(PyObject *))_cffi_exports[6])
#define _cffi_to_c_i64                                                   \
                 ((long long(*)(PyObject *))_cffi_exports[7])
#define _cffi_to_c_u64                                                   \
                 ((unsigned long long(*)(PyObject *))_cffi_exports[8])
#define _cffi_to_c_char                                                  \
                 ((int(*)(PyObject *))_cffi_exports[9])
#define _cffi_from_c_pointer                                             \
    ((PyObject *(*)(char *, CTypeDescrObject *))_cffi_exports[10])
#define _cffi_to_c_pointer                                               \
    ((char *(*)(PyObject *, CTypeDescrObject *))_cffi_exports[11])
#define _cffi_get_struct_layout                                          \
    ((PyObject *(*)(Py_ssize_t[]))_cffi_exports[12])
#define _cffi_restore_errno                                              \
    ((void(*)(void))_cffi_exports[13])
#define _cffi_save_errno                                                 \
    ((void(*)(void))_cffi_exports[14])
#define _cffi_from_c_char                                                \
    ((PyObject *(*)(char))_cffi_exports[15])
#define _cffi_from_c_deref                                               \
    ((PyObject *(*)(char *, CTypeDescrObject *))_cffi_exports[16])
#define _cffi_to_c                                                       \
    ((int(*)(char *, CTypeDescrObject *, PyObject *))_cffi_exports[17])
#define _cffi_from_c_struct                                              \
    ((PyObject *(*)(char *, CTypeDescrObject *))_cffi_exports[18])
#define _cffi_to_c_wchar_t                                               \
    ((wchar_t(*)(PyObject *))_cffi_exports[19])
#define _cffi_from_c_wchar_t                                             \
    ((PyObject *(*)(wchar_t))_cffi_exports[20])
#define _cffi_to_c_long_double                                           \
    ((long double(*)(PyObject *))_cffi_exports[21])
#define _cffi_to_c__Bool                                                 \
    ((_Bool(*)(PyObject *))_cffi_exports[22])
#define _cffi_prepare_pointer_call_argument                              \
    ((Py_ssize_t(*)(CTypeDescrObject *, PyObject *, char **))_cffi_exports[23])
#define _cffi_convert_array_from_object                                  \
    ((int(*)(char *, CTypeDescrObject *, PyObject *))_cffi_exports[24])
#define _CFFI_NUM_EXPORTS 25

typedef struct _ctypedescr CTypeDescrObject;

static void *_cffi_exports[_CFFI_NUM_EXPORTS];
static PyObject *_cffi_types, *_cffi_VerificationError;

static int _cffi_setup_custom(PyObject *lib);   /* forward */

static PyObject *_cffi_setup(PyObject *self, PyObject *args)
{
    PyObject *library;
    int was_alive = (_cffi_types != NULL);
    (void)self; /* unused */
    if (!PyArg_ParseTuple(args, "OOO", &_cffi_types, &_cffi_VerificationError,
                                       &library))
        return NULL;
    Py_INCREF(_cffi_types);
    Py_INCREF(_cffi_VerificationError);
    if (_cffi_setup_custom(library) < 0)
        return NULL;
    return PyBool_FromLong(was_alive);
}

static int _cffi_init(void)
{
    PyObject *module, *c_api_object = NULL;

    module = PyImport_ImportModule("_cffi_backend");
    if (module == NULL)
        goto failure;

    c_api_object = PyObject_GetAttrString(module, "_C_API");
    if (c_api_object == NULL)
        goto failure;
    if (!PyCapsule_CheckExact(c_api_object)) {
        PyErr_SetNone(PyExc_ImportError);
        goto failure;
    }
    memcpy(_cffi_exports, PyCapsule_GetPointer(c_api_object, "cffi"),
           _CFFI_NUM_EXPORTS * sizeof(void *));

    Py_DECREF(module);
    Py_DECREF(c_api_object);
    return 0;

  failure:
    Py_XDECREF(module);
    Py_XDECREF(c_api_object);
    return -1;
}

#define _cffi_type(num) ((CTypeDescrObject *)PyList_GET_ITEM(_cffi_types, num))

/**********/



#define XLIB_ILLEGAL_ACCESS
#include <X11/Xlib.h>
#include <X11/extensions/shape.h>
#include <X11/extensions/Xfixes.h>


static void _cffi_check__Screen(Screen *p)
{
  /* only to generate compile-time warnings or errors */
  (void)p;
  { XExtData * *tmp = &p->ext_data; (void)tmp; }
  { struct _XDisplay * *tmp = &p->display; (void)tmp; }
  (void)((p->root) << 1);
  (void)((p->width) << 1);
  (void)((p->height) << 1);
  (void)((p->mwidth) << 1);
  (void)((p->mheight) << 1);
  (void)((p->ndepths) << 1);
  { Depth * *tmp = &p->depths; (void)tmp; }
  (void)((p->root_depth) << 1);
  { Visual * *tmp = &p->root_visual; (void)tmp; }
  { struct _XGC * *tmp = &p->default_gc; (void)tmp; }
  (void)((p->cmap) << 1);
  (void)((p->white_pixel) << 1);
  (void)((p->black_pixel) << 1);
  (void)((p->max_maps) << 1);
  (void)((p->min_maps) << 1);
  (void)((p->backing_store) << 1);
  (void)((p->save_unders) << 1);
  (void)((p->root_input_mask) << 1);
}
static PyObject *
_cffi_layout__Screen(PyObject *self, PyObject *noarg)
{
  struct _cffi_aligncheck { char x; Screen y; };
  static Py_ssize_t nums[] = {
    sizeof(Screen),
    offsetof(struct _cffi_aligncheck, y),
    offsetof(Screen, ext_data),
    sizeof(((Screen *)0)->ext_data),
    offsetof(Screen, display),
    sizeof(((Screen *)0)->display),
    offsetof(Screen, root),
    sizeof(((Screen *)0)->root),
    offsetof(Screen, width),
    sizeof(((Screen *)0)->width),
    offsetof(Screen, height),
    sizeof(((Screen *)0)->height),
    offsetof(Screen, mwidth),
    sizeof(((Screen *)0)->mwidth),
    offsetof(Screen, mheight),
    sizeof(((Screen *)0)->mheight),
    offsetof(Screen, ndepths),
    sizeof(((Screen *)0)->ndepths),
    offsetof(Screen, depths),
    sizeof(((Screen *)0)->depths),
    offsetof(Screen, root_depth),
    sizeof(((Screen *)0)->root_depth),
    offsetof(Screen, root_visual),
    sizeof(((Screen *)0)->root_visual),
    offsetof(Screen, default_gc),
    sizeof(((Screen *)0)->default_gc),
    offsetof(Screen, cmap),
    sizeof(((Screen *)0)->cmap),
    offsetof(Screen, white_pixel),
    sizeof(((Screen *)0)->white_pixel),
    offsetof(Screen, black_pixel),
    sizeof(((Screen *)0)->black_pixel),
    offsetof(Screen, max_maps),
    sizeof(((Screen *)0)->max_maps),
    offsetof(Screen, min_maps),
    sizeof(((Screen *)0)->min_maps),
    offsetof(Screen, backing_store),
    sizeof(((Screen *)0)->backing_store),
    offsetof(Screen, save_unders),
    sizeof(((Screen *)0)->save_unders),
    offsetof(Screen, root_input_mask),
    sizeof(((Screen *)0)->root_input_mask),
    -1
  };
  (void)self; /* unused */
  (void)noarg; /* unused */
  return _cffi_get_struct_layout(nums);
  /* the next line is not executed, but compiled */
  _cffi_check__Screen(0);
}

static void _cffi_check__ScreenFormat(ScreenFormat *p)
{
  /* only to generate compile-time warnings or errors */
  (void)p;
  { XExtData * *tmp = &p->ext_data; (void)tmp; }
  (void)((p->depth) << 1);
  (void)((p->bits_per_pixel) << 1);
  (void)((p->scanline_pad) << 1);
}
static PyObject *
_cffi_layout__ScreenFormat(PyObject *self, PyObject *noarg)
{
  struct _cffi_aligncheck { char x; ScreenFormat y; };
  static Py_ssize_t nums[] = {
    sizeof(ScreenFormat),
    offsetof(struct _cffi_aligncheck, y),
    offsetof(ScreenFormat, ext_data),
    sizeof(((ScreenFormat *)0)->ext_data),
    offsetof(ScreenFormat, depth),
    sizeof(((ScreenFormat *)0)->depth),
    offsetof(ScreenFormat, bits_per_pixel),
    sizeof(((ScreenFormat *)0)->bits_per_pixel),
    offsetof(ScreenFormat, scanline_pad),
    sizeof(((ScreenFormat *)0)->scanline_pad),
    -1
  };
  (void)self; /* unused */
  (void)noarg; /* unused */
  return _cffi_get_struct_layout(nums);
  /* the next line is not executed, but compiled */
  _cffi_check__ScreenFormat(0);
}

static void _cffi_check__XClientMessageEvent(XClientMessageEvent *p)
{
  /* only to generate compile-time warnings or errors */
  (void)p;
  (void)((p->type) << 1);
  (void)((p->serial) << 1);
  (void)((p->send_event) << 1);
  { Display * *tmp = &p->display; (void)tmp; }
  (void)((p->window) << 1);
  (void)((p->message_type) << 1);
  (void)((p->format) << 1);
  /* cannot generate 'union $1' in field 'data': unknown type name */
}
static PyObject *
_cffi_layout__XClientMessageEvent(PyObject *self, PyObject *noarg)
{
  struct _cffi_aligncheck { char x; XClientMessageEvent y; };
  static Py_ssize_t nums[] = {
    sizeof(XClientMessageEvent),
    offsetof(struct _cffi_aligncheck, y),
    offsetof(XClientMessageEvent, type),
    sizeof(((XClientMessageEvent *)0)->type),
    offsetof(XClientMessageEvent, serial),
    sizeof(((XClientMessageEvent *)0)->serial),
    offsetof(XClientMessageEvent, send_event),
    sizeof(((XClientMessageEvent *)0)->send_event),
    offsetof(XClientMessageEvent, display),
    sizeof(((XClientMessageEvent *)0)->display),
    offsetof(XClientMessageEvent, window),
    sizeof(((XClientMessageEvent *)0)->window),
    offsetof(XClientMessageEvent, message_type),
    sizeof(((XClientMessageEvent *)0)->message_type),
    offsetof(XClientMessageEvent, format),
    sizeof(((XClientMessageEvent *)0)->format),
    offsetof(XClientMessageEvent, data),
    sizeof(((XClientMessageEvent *)0)->data),
    -1
  };
  (void)self; /* unused */
  (void)noarg; /* unused */
  return _cffi_get_struct_layout(nums);
  /* the next line is not executed, but compiled */
  _cffi_check__XClientMessageEvent(0);
}

static void _cffi_check__XRectangle(XRectangle *p)
{
  /* only to generate compile-time warnings or errors */
  (void)p;
  (void)((p->x) << 1);
  (void)((p->y) << 1);
  (void)((p->width) << 1);
  (void)((p->height) << 1);
}
static PyObject *
_cffi_layout__XRectangle(PyObject *self, PyObject *noarg)
{
  struct _cffi_aligncheck { char x; XRectangle y; };
  static Py_ssize_t nums[] = {
    sizeof(XRectangle),
    offsetof(struct _cffi_aligncheck, y),
    offsetof(XRectangle, x),
    sizeof(((XRectangle *)0)->x),
    offsetof(XRectangle, y),
    sizeof(((XRectangle *)0)->y),
    offsetof(XRectangle, width),
    sizeof(((XRectangle *)0)->width),
    offsetof(XRectangle, height),
    sizeof(((XRectangle *)0)->height),
    -1
  };
  (void)self; /* unused */
  (void)noarg; /* unused */
  return _cffi_get_struct_layout(nums);
  /* the next line is not executed, but compiled */
  _cffi_check__XRectangle(0);
}

static PyObject *
_cffi_f_XFixesCreateRegion(PyObject *self, PyObject *args)
{
  Display * x0;
  XRectangle * x1;
  int x2;
  Py_ssize_t datasize;
  unsigned long result;
  PyObject *arg0;
  PyObject *arg1;
  PyObject *arg2;

  if (!PyArg_ParseTuple(args, "OOO:XFixesCreateRegion", &arg0, &arg1, &arg2))
    return NULL;

  datasize = _cffi_prepare_pointer_call_argument(
      _cffi_type(0), arg0, (char **)&x0);
  if (datasize != 0) {
    if (datasize < 0)
      return NULL;
    x0 = alloca((size_t)datasize);
    memset((void *)x0, 0, (size_t)datasize);
    if (_cffi_convert_array_from_object((char *)x0, _cffi_type(0), arg0) < 0)
      return NULL;
  }

  datasize = _cffi_prepare_pointer_call_argument(
      _cffi_type(1), arg1, (char **)&x1);
  if (datasize != 0) {
    if (datasize < 0)
      return NULL;
    x1 = alloca((size_t)datasize);
    memset((void *)x1, 0, (size_t)datasize);
    if (_cffi_convert_array_from_object((char *)x1, _cffi_type(1), arg1) < 0)
      return NULL;
  }

  x2 = _cffi_to_c_int(arg2, int);
  if (x2 == (int)-1 && PyErr_Occurred())
    return NULL;

  Py_BEGIN_ALLOW_THREADS
  _cffi_restore_errno();
  { result = XFixesCreateRegion(x0, x1, x2); }
  _cffi_save_errno();
  Py_END_ALLOW_THREADS

  (void)self; /* unused */
  return _cffi_from_c_int(result, unsigned long);
}

static PyObject *
_cffi_f_XFixesDestroyRegion(PyObject *self, PyObject *args)
{
  Display * x0;
  unsigned long x1;
  Py_ssize_t datasize;
  PyObject *arg0;
  PyObject *arg1;

  if (!PyArg_ParseTuple(args, "OO:XFixesDestroyRegion", &arg0, &arg1))
    return NULL;

  datasize = _cffi_prepare_pointer_call_argument(
      _cffi_type(0), arg0, (char **)&x0);
  if (datasize != 0) {
    if (datasize < 0)
      return NULL;
    x0 = alloca((size_t)datasize);
    memset((void *)x0, 0, (size_t)datasize);
    if (_cffi_convert_array_from_object((char *)x0, _cffi_type(0), arg0) < 0)
      return NULL;
  }

  x1 = _cffi_to_c_int(arg1, unsigned long);
  if (x1 == (unsigned long)-1 && PyErr_Occurred())
    return NULL;

  Py_BEGIN_ALLOW_THREADS
  _cffi_restore_errno();
  { XFixesDestroyRegion(x0, x1); }
  _cffi_save_errno();
  Py_END_ALLOW_THREADS

  (void)self; /* unused */
  Py_INCREF(Py_None);
  return Py_None;
}

static PyObject *
_cffi_f_XFixesSetWindowShapeRegion(PyObject *self, PyObject *args)
{
  Display * x0;
  unsigned long x1;
  int x2;
  int x3;
  int x4;
  unsigned long x5;
  Py_ssize_t datasize;
  PyObject *arg0;
  PyObject *arg1;
  PyObject *arg2;
  PyObject *arg3;
  PyObject *arg4;
  PyObject *arg5;

  if (!PyArg_ParseTuple(args, "OOOOOO:XFixesSetWindowShapeRegion", &arg0, &arg1, &arg2, &arg3, &arg4, &arg5))
    return NULL;

  datasize = _cffi_prepare_pointer_call_argument(
      _cffi_type(0), arg0, (char **)&x0);
  if (datasize != 0) {
    if (datasize < 0)
      return NULL;
    x0 = alloca((size_t)datasize);
    memset((void *)x0, 0, (size_t)datasize);
    if (_cffi_convert_array_from_object((char *)x0, _cffi_type(0), arg0) < 0)
      return NULL;
  }

  x1 = _cffi_to_c_int(arg1, unsigned long);
  if (x1 == (unsigned long)-1 && PyErr_Occurred())
    return NULL;

  x2 = _cffi_to_c_int(arg2, int);
  if (x2 == (int)-1 && PyErr_Occurred())
    return NULL;

  x3 = _cffi_to_c_int(arg3, int);
  if (x3 == (int)-1 && PyErr_Occurred())
    return NULL;

  x4 = _cffi_to_c_int(arg4, int);
  if (x4 == (int)-1 && PyErr_Occurred())
    return NULL;

  x5 = _cffi_to_c_int(arg5, unsigned long);
  if (x5 == (unsigned long)-1 && PyErr_Occurred())
    return NULL;

  Py_BEGIN_ALLOW_THREADS
  _cffi_restore_errno();
  { XFixesSetWindowShapeRegion(x0, x1, x2, x3, x4, x5); }
  _cffi_save_errno();
  Py_END_ALLOW_THREADS

  (void)self; /* unused */
  Py_INCREF(Py_None);
  return Py_None;
}

static PyObject *
_cffi_f_XInternAtom(PyObject *self, PyObject *args)
{
  Display * x0;
  char const * x1;
  int x2;
  Py_ssize_t datasize;
  unsigned long result;
  PyObject *arg0;
  PyObject *arg1;
  PyObject *arg2;

  if (!PyArg_ParseTuple(args, "OOO:XInternAtom", &arg0, &arg1, &arg2))
    return NULL;

  datasize = _cffi_prepare_pointer_call_argument(
      _cffi_type(0), arg0, (char **)&x0);
  if (datasize != 0) {
    if (datasize < 0)
      return NULL;
    x0 = alloca((size_t)datasize);
    memset((void *)x0, 0, (size_t)datasize);
    if (_cffi_convert_array_from_object((char *)x0, _cffi_type(0), arg0) < 0)
      return NULL;
  }

  datasize = _cffi_prepare_pointer_call_argument(
      _cffi_type(3), arg1, (char **)&x1);
  if (datasize != 0) {
    if (datasize < 0)
      return NULL;
    x1 = alloca((size_t)datasize);
    memset((void *)x1, 0, (size_t)datasize);
    if (_cffi_convert_array_from_object((char *)x1, _cffi_type(3), arg1) < 0)
      return NULL;
  }

  x2 = _cffi_to_c_int(arg2, int);
  if (x2 == (int)-1 && PyErr_Occurred())
    return NULL;

  Py_BEGIN_ALLOW_THREADS
  _cffi_restore_errno();
  { result = XInternAtom(x0, x1, x2); }
  _cffi_save_errno();
  Py_END_ALLOW_THREADS

  (void)self; /* unused */
  return _cffi_from_c_int(result, unsigned long);
}

static PyObject *
_cffi_f_XSendEvent(PyObject *self, PyObject *args)
{
  Display * x0;
  unsigned long x1;
  int x2;
  long x3;
  XEvent * x4;
  Py_ssize_t datasize;
  int result;
  PyObject *arg0;
  PyObject *arg1;
  PyObject *arg2;
  PyObject *arg3;
  PyObject *arg4;

  if (!PyArg_ParseTuple(args, "OOOOO:XSendEvent", &arg0, &arg1, &arg2, &arg3, &arg4))
    return NULL;

  datasize = _cffi_prepare_pointer_call_argument(
      _cffi_type(0), arg0, (char **)&x0);
  if (datasize != 0) {
    if (datasize < 0)
      return NULL;
    x0 = alloca((size_t)datasize);
    memset((void *)x0, 0, (size_t)datasize);
    if (_cffi_convert_array_from_object((char *)x0, _cffi_type(0), arg0) < 0)
      return NULL;
  }

  x1 = _cffi_to_c_int(arg1, unsigned long);
  if (x1 == (unsigned long)-1 && PyErr_Occurred())
    return NULL;

  x2 = _cffi_to_c_int(arg2, int);
  if (x2 == (int)-1 && PyErr_Occurred())
    return NULL;

  x3 = _cffi_to_c_int(arg3, long);
  if (x3 == (long)-1 && PyErr_Occurred())
    return NULL;

  datasize = _cffi_prepare_pointer_call_argument(
      _cffi_type(4), arg4, (char **)&x4);
  if (datasize != 0) {
    if (datasize < 0)
      return NULL;
    x4 = alloca((size_t)datasize);
    memset((void *)x4, 0, (size_t)datasize);
    if (_cffi_convert_array_from_object((char *)x4, _cffi_type(4), arg4) < 0)
      return NULL;
  }

  Py_BEGIN_ALLOW_THREADS
  _cffi_restore_errno();
  { result = XSendEvent(x0, x1, x2, x3, x4); }
  _cffi_save_errno();
  Py_END_ALLOW_THREADS

  (void)self; /* unused */
  return _cffi_from_c_int(result, int);
}

static void _cffi_check_struct__XDisplay(struct _XDisplay *p)
{
  /* only to generate compile-time warnings or errors */
  (void)p;
  { XExtData * *tmp = &p->ext_data; (void)tmp; }
  { struct _XPrivate * *tmp = &p->private1; (void)tmp; }
  (void)((p->fd) << 1);
  (void)((p->private2) << 1);
  (void)((p->proto_major_version) << 1);
  (void)((p->proto_minor_version) << 1);
  { char * *tmp = &p->vendor; (void)tmp; }
  (void)((p->private3) << 1);
  (void)((p->private4) << 1);
  (void)((p->private5) << 1);
  (void)((p->private6) << 1);
  { unsigned long(* *tmp)(Display *) = &p->resource_alloc; (void)tmp; }
  (void)((p->byte_order) << 1);
  (void)((p->bitmap_unit) << 1);
  (void)((p->bitmap_pad) << 1);
  (void)((p->bitmap_bit_order) << 1);
  (void)((p->nformats) << 1);
  { ScreenFormat * *tmp = &p->pixmap_format; (void)tmp; }
  (void)((p->private8) << 1);
  (void)((p->release) << 1);
  { struct _XPrivate * *tmp = &p->private9; (void)tmp; }
  { struct _XPrivate * *tmp = &p->private10; (void)tmp; }
  (void)((p->qlen) << 1);
  (void)((p->last_request_read) << 1);
  (void)((p->request) << 1);
  { char * *tmp = &p->private11; (void)tmp; }
  { char * *tmp = &p->private12; (void)tmp; }
  { char * *tmp = &p->private13; (void)tmp; }
  { char * *tmp = &p->private14; (void)tmp; }
  (void)((p->max_request_size) << 1);
  { struct _XrmHashBucketRec * *tmp = &p->db; (void)tmp; }
  { int(* *tmp)(Display *) = &p->private15; (void)tmp; }
  { char * *tmp = &p->display_name; (void)tmp; }
  (void)((p->default_screen) << 1);
  (void)((p->nscreens) << 1);
  { Screen * *tmp = &p->screens; (void)tmp; }
  (void)((p->motion_buffer) << 1);
  (void)((p->private16) << 1);
  (void)((p->min_keycode) << 1);
  (void)((p->max_keycode) << 1);
  { char * *tmp = &p->private17; (void)tmp; }
  { char * *tmp = &p->private18; (void)tmp; }
  (void)((p->private19) << 1);
  { char * *tmp = &p->xdefaults; (void)tmp; }
}
static PyObject *
_cffi_layout_struct__XDisplay(PyObject *self, PyObject *noarg)
{
  struct _cffi_aligncheck { char x; struct _XDisplay y; };
  static Py_ssize_t nums[] = {
    sizeof(struct _XDisplay),
    offsetof(struct _cffi_aligncheck, y),
    offsetof(struct _XDisplay, ext_data),
    sizeof(((struct _XDisplay *)0)->ext_data),
    offsetof(struct _XDisplay, private1),
    sizeof(((struct _XDisplay *)0)->private1),
    offsetof(struct _XDisplay, fd),
    sizeof(((struct _XDisplay *)0)->fd),
    offsetof(struct _XDisplay, private2),
    sizeof(((struct _XDisplay *)0)->private2),
    offsetof(struct _XDisplay, proto_major_version),
    sizeof(((struct _XDisplay *)0)->proto_major_version),
    offsetof(struct _XDisplay, proto_minor_version),
    sizeof(((struct _XDisplay *)0)->proto_minor_version),
    offsetof(struct _XDisplay, vendor),
    sizeof(((struct _XDisplay *)0)->vendor),
    offsetof(struct _XDisplay, private3),
    sizeof(((struct _XDisplay *)0)->private3),
    offsetof(struct _XDisplay, private4),
    sizeof(((struct _XDisplay *)0)->private4),
    offsetof(struct _XDisplay, private5),
    sizeof(((struct _XDisplay *)0)->private5),
    offsetof(struct _XDisplay, private6),
    sizeof(((struct _XDisplay *)0)->private6),
    offsetof(struct _XDisplay, resource_alloc),
    sizeof(((struct _XDisplay *)0)->resource_alloc),
    offsetof(struct _XDisplay, byte_order),
    sizeof(((struct _XDisplay *)0)->byte_order),
    offsetof(struct _XDisplay, bitmap_unit),
    sizeof(((struct _XDisplay *)0)->bitmap_unit),
    offsetof(struct _XDisplay, bitmap_pad),
    sizeof(((struct _XDisplay *)0)->bitmap_pad),
    offsetof(struct _XDisplay, bitmap_bit_order),
    sizeof(((struct _XDisplay *)0)->bitmap_bit_order),
    offsetof(struct _XDisplay, nformats),
    sizeof(((struct _XDisplay *)0)->nformats),
    offsetof(struct _XDisplay, pixmap_format),
    sizeof(((struct _XDisplay *)0)->pixmap_format),
    offsetof(struct _XDisplay, private8),
    sizeof(((struct _XDisplay *)0)->private8),
    offsetof(struct _XDisplay, release),
    sizeof(((struct _XDisplay *)0)->release),
    offsetof(struct _XDisplay, private9),
    sizeof(((struct _XDisplay *)0)->private9),
    offsetof(struct _XDisplay, private10),
    sizeof(((struct _XDisplay *)0)->private10),
    offsetof(struct _XDisplay, qlen),
    sizeof(((struct _XDisplay *)0)->qlen),
    offsetof(struct _XDisplay, last_request_read),
    sizeof(((struct _XDisplay *)0)->last_request_read),
    offsetof(struct _XDisplay, request),
    sizeof(((struct _XDisplay *)0)->request),
    offsetof(struct _XDisplay, private11),
    sizeof(((struct _XDisplay *)0)->private11),
    offsetof(struct _XDisplay, private12),
    sizeof(((struct _XDisplay *)0)->private12),
    offsetof(struct _XDisplay, private13),
    sizeof(((struct _XDisplay *)0)->private13),
    offsetof(struct _XDisplay, private14),
    sizeof(((struct _XDisplay *)0)->private14),
    offsetof(struct _XDisplay, max_request_size),
    sizeof(((struct _XDisplay *)0)->max_request_size),
    offsetof(struct _XDisplay, db),
    sizeof(((struct _XDisplay *)0)->db),
    offsetof(struct _XDisplay, private15),
    sizeof(((struct _XDisplay *)0)->private15),
    offsetof(struct _XDisplay, display_name),
    sizeof(((struct _XDisplay *)0)->display_name),
    offsetof(struct _XDisplay, default_screen),
    sizeof(((struct _XDisplay *)0)->default_screen),
    offsetof(struct _XDisplay, nscreens),
    sizeof(((struct _XDisplay *)0)->nscreens),
    offsetof(struct _XDisplay, screens),
    sizeof(((struct _XDisplay *)0)->screens),
    offsetof(struct _XDisplay, motion_buffer),
    sizeof(((struct _XDisplay *)0)->motion_buffer),
    offsetof(struct _XDisplay, private16),
    sizeof(((struct _XDisplay *)0)->private16),
    offsetof(struct _XDisplay, min_keycode),
    sizeof(((struct _XDisplay *)0)->min_keycode),
    offsetof(struct _XDisplay, max_keycode),
    sizeof(((struct _XDisplay *)0)->max_keycode),
    offsetof(struct _XDisplay, private17),
    sizeof(((struct _XDisplay *)0)->private17),
    offsetof(struct _XDisplay, private18),
    sizeof(((struct _XDisplay *)0)->private18),
    offsetof(struct _XDisplay, private19),
    sizeof(((struct _XDisplay *)0)->private19),
    offsetof(struct _XDisplay, xdefaults),
    sizeof(((struct _XDisplay *)0)->xdefaults),
    -1
  };
  (void)self; /* unused */
  (void)noarg; /* unused */
  return _cffi_get_struct_layout(nums);
  /* the next line is not executed, but compiled */
  _cffi_check_struct__XDisplay(0);
}

static void _cffi_check_struct__XGC(struct _XGC *p)
{
  /* only to generate compile-time warnings or errors */
  (void)p;
  { XExtData * *tmp = &p->ext_data; (void)tmp; }
  (void)((p->gid) << 1);
}
static PyObject *
_cffi_layout_struct__XGC(PyObject *self, PyObject *noarg)
{
  struct _cffi_aligncheck { char x; struct _XGC y; };
  static Py_ssize_t nums[] = {
    sizeof(struct _XGC),
    offsetof(struct _cffi_aligncheck, y),
    offsetof(struct _XGC, ext_data),
    sizeof(((struct _XGC *)0)->ext_data),
    offsetof(struct _XGC, gid),
    sizeof(((struct _XGC *)0)->gid),
    -1
  };
  (void)self; /* unused */
  (void)noarg; /* unused */
  return _cffi_get_struct_layout(nums);
  /* the next line is not executed, but compiled */
  _cffi_check_struct__XGC(0);
}

static void _cffi_check_union__XEvent(union _XEvent *p)
{
  /* only to generate compile-time warnings or errors */
  (void)p;
  (void)((p->type) << 1);
  { XClientMessageEvent *tmp = &p->xclient; (void)tmp; }
  { long(*tmp)[24] = &p->pad; (void)tmp; }
}
static PyObject *
_cffi_layout_union__XEvent(PyObject *self, PyObject *noarg)
{
  struct _cffi_aligncheck { char x; union _XEvent y; };
  static Py_ssize_t nums[] = {
    sizeof(union _XEvent),
    offsetof(struct _cffi_aligncheck, y),
    offsetof(union _XEvent, type),
    sizeof(((union _XEvent *)0)->type),
    offsetof(union _XEvent, xclient),
    sizeof(((union _XEvent *)0)->xclient),
    offsetof(union _XEvent, pad),
    sizeof(((union _XEvent *)0)->pad),
    -1
  };
  (void)self; /* unused */
  (void)noarg; /* unused */
  return _cffi_get_struct_layout(nums);
  /* the next line is not executed, but compiled */
  _cffi_check_union__XEvent(0);
}

static int _cffi_setup_custom(PyObject *lib)
{
  return ((void)lib,0);
}

static PyMethodDef _cffi_methods[] = {
  {"_cffi_layout__Screen", _cffi_layout__Screen, METH_NOARGS, NULL},
  {"_cffi_layout__ScreenFormat", _cffi_layout__ScreenFormat, METH_NOARGS, NULL},
  {"_cffi_layout__XClientMessageEvent", _cffi_layout__XClientMessageEvent, METH_NOARGS, NULL},
  {"_cffi_layout__XRectangle", _cffi_layout__XRectangle, METH_NOARGS, NULL},
  {"XFixesCreateRegion", _cffi_f_XFixesCreateRegion, METH_VARARGS, NULL},
  {"XFixesDestroyRegion", _cffi_f_XFixesDestroyRegion, METH_VARARGS, NULL},
  {"XFixesSetWindowShapeRegion", _cffi_f_XFixesSetWindowShapeRegion, METH_VARARGS, NULL},
  {"XInternAtom", _cffi_f_XInternAtom, METH_VARARGS, NULL},
  {"XSendEvent", _cffi_f_XSendEvent, METH_VARARGS, NULL},
  {"_cffi_layout_struct__XDisplay", _cffi_layout_struct__XDisplay, METH_NOARGS, NULL},
  {"_cffi_layout_struct__XGC", _cffi_layout_struct__XGC, METH_NOARGS, NULL},
  {"_cffi_layout_union__XEvent", _cffi_layout_union__XEvent, METH_NOARGS, NULL},
  {"_cffi_setup", _cffi_setup, METH_VARARGS, NULL},
  {NULL, NULL, 0, NULL}    /* Sentinel */
};

#if PY_MAJOR_VERSION >= 3

static struct PyModuleDef _cffi_module_def = {
  PyModuleDef_HEAD_INIT,
  "_cffi__xa440ff13x7e5dac29",
  NULL,
  -1,
  _cffi_methods,
  NULL, NULL, NULL, NULL
};

PyMODINIT_FUNC
PyInit__cffi__xa440ff13x7e5dac29(void)
{
  PyObject *lib;
  lib = PyModule_Create(&_cffi_module_def);
  if (lib == NULL)
    return NULL;
  if (((void)lib,0) < 0 || _cffi_init() < 0) {
    Py_DECREF(lib);
    return NULL;
  }
  return lib;
}

#else

PyMODINIT_FUNC
init_cffi__xa440ff13x7e5dac29(void)
{
  PyObject *lib;
  lib = Py_InitModule("_cffi__xa440ff13x7e5dac29", _cffi_methods);
  if (lib == NULL)
    return;
  if (((void)lib,0) < 0 || _cffi_init() < 0)
    return;
  return;
}

#endif
