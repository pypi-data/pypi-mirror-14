/**
 * @author Andre Anjos <andre.anjos@idiap.ch>
 * @date Wed 14 May 14:00:33 2014 CEST
 *
 * @brief Binds configuration information available from bob
 */

#define BOB_IMPORT_VERSION
#include <bob.blitz/config.h>
#include <bob.blitz/cleanup.h>
#include <bob.core/config.h>
#include <bob.io.base/config.h>

#include <boost/preprocessor/stringize.hpp>

extern "C" {
  #include <jpeglib.h>

  #define PNG_SKIP_SETJMP_CHECK
  // #define requires because of the problematic pngconf.h.
  // Look at the thread here:
  // https://bugs.launchpad.net/ubuntu/+source/libpng/+bug/218409
  #include <png.h>
  #include <gif_lib.h>
  #include <tiffio.h>
}

/**
 * LibJPEG version
 */
static PyObject* libjpeg_version() {
  boost::format f("%d (compiled with %d bits depth)");
  f % LIBJPEG_VERSION % BITS_IN_JSAMPLE;
  return Py_BuildValue("s", f.str().c_str());
}

/**
 * Libpng version
 */
static PyObject* libpng_version() {
  return Py_BuildValue("s", PNG_LIBPNG_VER_STRING);
}

/**
 * Libtiff version
 */
static PyObject* libtiff_version() {
  static const std::string beg_str("LIBTIFF, Version ");
  static const size_t beg_len = beg_str.size();
  std::string vtiff(TIFFGetVersion());

  // Remove first part if it starts with "LIBTIFF, Version "
  if(vtiff.compare(0, beg_len, beg_str) == 0)
    vtiff = vtiff.substr(beg_len);

  // Remove multiple (copyright) lines if any
  size_t end_line = vtiff.find("\n");
  if(end_line != std::string::npos)
    vtiff = vtiff.substr(0,end_line);

  return Py_BuildValue("s", vtiff.c_str());
}

/**
 * Version of giflib support
 */
static PyObject* giflib_version() {
#ifdef GIF_LIB_VERSION
 return Py_BuildValue("s", GIF_LIB_VERSION);
#else
  boost::format f("%s.%s.%s");
  f % BOOST_PP_STRINGIZE(GIFLIB_MAJOR) % BOOST_PP_STRINGIZE(GIFLIB_MINOR) % BOOST_PP_STRINGIZE(GIFLIB_RELEASE);
  return Py_BuildValue("s", f.str().c_str());
#endif
}


static PyObject* build_version_dictionary() {

  PyObject* retval = PyDict_New();
  if (!retval) return 0;
  auto retval_ = make_safe(retval);

  if (!dict_steal(retval, "libjpeg", libjpeg_version())) return 0;
  if (!dict_steal(retval, "libpng", libpng_version())) return 0;
  if (!dict_steal(retval, "libtiff", libtiff_version())) return 0;
  if (!dict_steal(retval, "giflib", giflib_version())) return 0;
  if (!dict_steal(retval, "HDF5", hdf5_version())) return 0;
  if (!dict_steal(retval, "Boost", boost_version())) return 0;
  if (!dict_steal(retval, "Compiler", compiler_version())) return 0;
  if (!dict_steal(retval, "Python", python_version())) return 0;
  if (!dict_steal(retval, "NumPy", numpy_version())) return 0;
  if (!dict_steal(retval, "Blitz++", blitz_version())) return 0;
  if (!dict_steal(retval, "bob.blitz", bob_blitz_version())) return 0;
  if (!dict_steal(retval, "bob.core", bob_core_version())) return 0;
  if (!dict_steal(retval, "bob.io.base", bob_io_base_version())) return 0;

  return Py_BuildValue("O", retval);
}

static PyMethodDef module_methods[] = {
    {0}  /* Sentinel */
};

PyDoc_STRVAR(module_docstr,
"Information about software used to compile the C++ Bob API"
);

#if PY_VERSION_HEX >= 0x03000000
static PyModuleDef module_definition = {
  PyModuleDef_HEAD_INIT,
  BOB_EXT_MODULE_NAME,
  module_docstr,
  -1,
  module_methods,
  0, 0, 0, 0
};
#endif

static PyObject* create_module (void) {

# if PY_VERSION_HEX >= 0x03000000
  PyObject* m = PyModule_Create(&module_definition);
  auto m_ = make_xsafe(m);
  const char* ret = "O";
# else
  PyObject* m = Py_InitModule3(BOB_EXT_MODULE_NAME, module_methods, module_docstr);
  const char* ret = "N";
# endif
  if (!m) return 0;

  /* register version numbers and constants */
  if (PyModule_AddStringConstant(m, "module", BOB_EXT_MODULE_VERSION) < 0) return 0;
  if (PyModule_AddObject(m, "externals", build_version_dictionary()) < 0) return 0;

  return Py_BuildValue(ret, m);
}

PyMODINIT_FUNC BOB_EXT_ENTRY_NAME (void) {
# if PY_VERSION_HEX >= 0x03000000
  return
# endif
    create_module();
}
