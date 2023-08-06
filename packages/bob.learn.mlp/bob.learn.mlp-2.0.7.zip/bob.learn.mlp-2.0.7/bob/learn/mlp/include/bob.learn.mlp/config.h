/**
 * @author Andre Anjos <andre.anjos@idiap.ch>
 * @date Thu 24 Apr 17:31:59 2014 CEST
 *
 * @brief General directives for all modules in bob.learn.mlp
 */

#ifndef BOB_LEARN_MLP_CONFIG_H
#define BOB_LEARN_MLP_CONFIG_H

/* Macros that define versions and important names */
#define BOB_LEARN_MLP_API_VERSION 0x0200

#ifdef BOB_IMPORT_VERSION

  /***************************************
  * Here we define some functions that should be used to build version dictionaries in the version.cpp file
  * There will be a compiler warning, when these functions are not used, so use them!
  ***************************************/

  #include <Python.h>
  #include <boost/preprocessor/stringize.hpp>

  /**
   * bob.learn.mlp c/c++ api version
   */
  static PyObject* bob_learn_mlp_version() {
    return Py_BuildValue("{ss}", "api", BOOST_PP_STRINGIZE(BOB_LEARN_MLP_API_VERSION));
  }

#endif // BOB_IMPORT_VERSION

#endif /* BOB_LEARN_MLP_CONFIG_H */
