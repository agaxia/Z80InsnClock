=========================
Installation from sources
=========================

.. only:: html

   .. |br| raw:: html

      <br />

.. only:: latex

   .. |nl| raw:: latex

      \newline

.. |cmake_option_build_config| replace:: ``--config``
.. _cmake_option_build_config: https://cmake.org/cmake/help/latest/manual/cmake.1.html#cmdoption-cmake-build-config

.. |cmake_option_install_strip| replace:: ``--strip``
.. _cmake_option_install_strip: https://cmake.org/cmake/help/latest/manual/cmake.1.html#cmdoption-cmake-install-strip

.. |cmake_option_install_component| replace:: ``--component``
.. _cmake_option_install_component: https://cmake.org/cmake/help/latest/manual/cmake.1.html#cmdoption-cmake-install-component

Prerequisites
=============

You will need `CMake <https://cmake.org>`_ v3.14 or later to build the package and, optionally, recent versions of `Doxygen <https://www.doxygen.nl>`_, `Sphinx <https://www.sphinx-doc.org>`_ and `Breathe <https://www.breathe-doc.org>`_ to compile the documentation. Also, make sure that you have `LaTeX <https://www.latex-project.org>`_ with PDF support installed on your system if you want to generate the documentation in PDF format.

Z80InsnClock depends on `Z80 <https://zxe.io/software/Z80>`_ v0.2 or later. Although it does not need to be linked against Z80, it requires the :file:`Z80.h` header.

Configure
=========

Once the prerequisites are met, create a directory and run ``cmake`` from there to prepare the build system:

.. code-block:: sh

   mkdir build
   cd build
   cmake [options] <Z80InsnClock-project-directory>

The resulting build files can be configured by passing options to ``cmake``. To show a complete list of those available along with their current settings, type the following:

.. code-block:: sh

   cmake -LAH -N -B .

If in doubt, read the `CMake documentation <https://cmake.org/documentation/>`_ for more information on configuration options. The following are some of the most relevant standard options of CMake:

.. option:: -DBUILD_SHARED_LIBS=(YES|NO)

   Generate shared libraries rather than static libraries. |br| |nl|
   The default is ``NO``.

.. option:: -DCMAKE_BUILD_TYPE=(Debug|Release|RelWithDebInfo|MinSizeRel)

   Choose the type of build (configuration) to generate. |br| |nl|
   The default is ``Release``.

.. option:: -DCMAKE_INSTALL_NAME_DIR="<path>"

   Specify the `directory portion <https://developer.apple.com/documentation/xcode/build-settings-reference#Dynamic-Library-Install-Name-Base>`_ of the `dynamic library install name <https://developer.apple.com/documentation/xcode/build-settings-reference#Dynamic-Library-Install-Name>`_ on Apple platforms (for installed shared libraries). |br| |nl|
   Not defined by default.

.. option:: -DCMAKE_INSTALL_PREFIX="<path>"

   Specify the installation prefix. |br| |nl|
   The default is ``"/usr/local"`` (on `UNIX <https://en.wikipedia.org/wiki/Unix>`_ and `UNIX-like <https://en.wikipedia.org/wiki/Unix-like>`_ operating systems).

.. _cmake_package_options:

Package-specific options are as follows:

.. option:: -DZ80InsnClock=(All|Basic|Extra)

   Specify which operation mode(s) to build. |br| |nl|
   ``All`` enables both ``Basic`` and ``Extra``. ``Basic`` mode is the simplest and only determines the clock cycle at which the ongoing M-cycle begins, while ``Extra`` mode additionally provides information about the duration of the M-cycle. |br| |nl|
   The default is ``All``.

.. option:: -DZ80InsnClock_INSTALL_CMAKEDIR="<path>"

   Specify the directory in which to install the CMake `config-file package`_. |br| |nl|
   The default is ``"${CMAKE_INSTALL_LIBDIR}/cmake/Z80InsnClock"``.

.. option:: -DZ80InsnClock_INSTALL_PKGCONFIGDIR="<path>"

   Specify the directory in which to install the `pkg-config`_ `file`_. |br| |nl|
   The default is ``"${CMAKE_INSTALL_LIBDIR}/pkgconfig"``.

.. option:: -DZ80InsnClock_NOSTDLIB_FLAGS=(Auto|"[<flag>[;<flag>...]]")

   Specify the linker flags used to avoid linking against system libraries. |br| |nl|
   The default is ``Auto`` (autoconfigure flags). If you get linker errors, set this option to ``""``.

.. option:: -DZ80InsnClock_OBJECT_LIBS=(YES|NO)

   Build Z80InsnClock as an `object library <https://cmake.org/cmake/help/latest/manual/cmake-buildsystem.7.html#object-libraries>`_. |br| |nl|
   This option takes precedence over :option:`BUILD_SHARED_LIBS<-DBUILD_SHARED_LIBS>` and :option:`Z80InsnClock_SHARED_LIBS<-DZ80InsnClock_SHARED_LIBS>`. If enabled, the build system will ignore :option:`Z80InsnClock_WITH_CMAKE_SUPPORT<-DZ80InsnClock_WITH_CMAKE_SUPPORT>` and :option:`Z80InsnClock_WITH_PKGCONFIG_SUPPORT<-DZ80InsnClock_WITH_PKGCONFIG_SUPPORT>`, as no libraries or support files will be installed. |br| |nl|
   The default is ``NO``.

.. option:: -DZ80InsnClock_SHARED_LIBS=(YES|NO)

   Build Z80InsnClock as a shared library, rather than static. |br| |nl|
   This option takes precedence over :option:`BUILD_SHARED_LIBS<-DBUILD_SHARED_LIBS>`. |br| |nl|
   Not defined by default.

.. option:: -DZ80InsnClock_SPHINX_HTML_THEME="[<name>]"

   Specify the Sphinx theme for the documentation in HTML format. |br| |nl|
   The default is ``""`` (use the default theme).

.. option:: -DZ80InsnClock_WITH_CMAKE_SUPPORT=(YES|NO)

   Generate and install the CMake `config-file package`_. |br| |nl|
   The default is ``NO``.

.. option:: -DZ80InsnClock_WITH_HTML_DOCUMENTATION=(YES|NO)

   Build and install the documentation in HTML format. |br| |nl|
   It requires Doxygen, Sphinx and Breathe. |br| |nl|
   The default is ``NO``.

.. option:: -DZ80InsnClock_WITH_PDF_DOCUMENTATION=(YES|NO)

   Build and install the documentation in PDF format. |br| |nl|
   It requires Doxygen, Sphinx, Breathe, and LaTeX with PDF support. |br| |nl|
   The default is ``NO``.

.. option:: -DZ80InsnClock_WITH_PKGCONFIG_SUPPORT=(YES|NO)

   Generate and install the `pkg-config`_ `file`_. |br| |nl|
   The default is ``NO``.

.. option:: -DZ80InsnClock_WITH_STANDARD_DOCUMENTS=(YES|NO)

   Install the standard text documents distributed with the package: :file:`AUTHORS`, :file:`HISTORY`, :file:`LICENSE-0BSD` and :file:`README`. |br| |nl|
   The default is ``NO``.

Build and install
=================

Finally, once the build system is configured according to your needs, build and install the package:

.. code-block:: sh

   cmake --build . [--config (Debug|Release|RelWithDebInfo|MinSizeRel)]
   cmake --install . [--config <configuration>] [--strip] [--component <component>]

The |cmake_option_build_config|_ option is only necessary for those `CMake generators <https://cmake.org/cmake/help/latest/manual/cmake-generators.7.html>`_ that ignore :option:`CMAKE_BUILD_TYPE<-DCMAKE_BUILD_TYPE>` (e.g., Xcode and Visual Studio). Use |cmake_option_install_strip|_ to remove debugging information and non-public symbols when installing non-debug builds of the shared library. To install only a specific component of the package, use the |cmake_option_install_component|_ option. The project defines the following components:

.. option:: Z80InsnClock_Runtime

   * Shared library.
   * Symbolic link for the compatibility version of the shared library.
   * Standard text documents.

.. option:: Z80InsnClock_Development

   * Static library.
   * Unversioned symbolic link of the shared library.
   * Public header.
   * CMake config-file package.
   * pkg-config file.

.. option:: Z80InsnClock_Documentation

   * Documentation in HTML format.
   * Documentation in PDF format.

.. _config-file package: https://cmake.org/cmake/help/latest/manual/cmake-packages.7.html#config-file-packages
.. _file: https://people.freedesktop.org/~dbn/pkg-config-guide.html
.. _pkg-config: https://www.freedesktop.org/wiki/Software/pkg-config
