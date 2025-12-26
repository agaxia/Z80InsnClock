# Z80 Instruction Clock

[![](https://zxe.io/software/Z80InsnClock/assets/images/documentation-badge.svg)](https://zxe.io/software/Z80InsnClock/documentation/latest)
[![](https://github.com/agaxia/Z80InsnClock/actions/workflows/build-library.yml/badge.svg)](https://github.com/agaxia/Z80InsnClock/actions/workflows/build-library.yml)
[![](https://github.com/agaxia/Z80InsnClock/actions/workflows/build-documentation.yml/badge.svg)](https://github.com/agaxia/Z80InsnClock/actions/workflows/build-documentation.yml)
[![](https://zxe.io/software/Z80InsnClock/assets/images/chat-badge.svg)](https://zxe.io/software/Z80InsnClock/chat)

[Z80InsnClock](https://zxe.io/software/Z80InsnClock) is a small library written in [ANSI C](https://en.wikipedia.org/wiki/ANSI_C) that provides T-state level precision to [Zilog Z80](https://en.wikipedia.org/wiki/Zilog_Z80) emulators. It allows to determine the exact clock cycle within an instruction at which the ongoing M-cycle starts, as well as its duration.

The library offers two modes of operation: Basic and Extra. Each mode increases the size of the library by 4 KiB of tables that contain patterns describing all Z80 instructions.

The Basic mode is the most simple, determining only the starting clock cycle of each M-cycle, and all related functions are inline.

The Extra mode allows knowing, in addition to the starting clock cycle, the number of extra clock cycles in the M-cycle and thus its duration, making it suitable for emulating systems such as the [ZX Spectrum](https://en.wikipedia.org/wiki/ZX_Spectrum). This mode is a bit more complex and requires calling a non-inline function during the opcode fetch.

Most users will integrate Z80InsnClock as a CMake subproject or copy its source code into their projects. In this case, if you do not need both operation modes, you can [disable](#cmake_option_z80insnclock) the compilation of the unused one.

## Installation

### <sub><img src="https://zxe.io/software/Z80InsnClock/assets/images/debian-icon.svg" height="24" width="20"></sub> Debian, <sub><img src="https://zxe.io/software/Z80InsnClock/assets/images/ubuntu-icon.svg" height="24" width="25"></sub> Ubuntu and other Debian-based Linux distributions

First, add the `zxe` repository and update the package index:

```shell
curl -L https://zxe.io/scripts/add-zxe-apt-repo.sh | sudo sh
sudo apt update
```

Next, install the library package:

```shell
sudo apt install libz80insnclock
```

In case you need to build software that requires the Z80InsnClock library, install the development package too:

```shell
sudo apt install libz80insnclock-dev
```

### <sub><img src="https://zxe.io/software/Z80InsnClock/assets/images/gentoo-icon.svg" height="24" width="24"></sub> Gentoo

First, add and sync the [`zxe`](https://github.com/redcode/zxe-gentoo-overlay) overlay:

```shell
eselect repository add zxe git https://github.com/redcode/zxe-gentoo-overlay.git
emaint sync --repo zxe
```

Then install the library:

```shell
emerge emulation-libs/z80insnclock
```

### <sub><img src="https://zxe.io/software/Z80InsnClock/assets/images/homebrew-icon.svg" height="24" width="16"></sub> Homebrew

```shell
brew install redcode/zxe/z80insnclock
```

### <sub><img src="https://zxe.io/software/Z80InsnClock/assets/images/windows-icon.png" height="24" width="24"></sub> Windows

Pre-built binaries for Windows are available on the [download](https://zxe.io/software/Z80InsnClock/download) page.

## Installation from sources

### Prerequisites

You will need [CMake](https://cmake.org) v3.14 or later to build the package and, optionally, recent versions of [Doxygen](https://www.doxygen.nl), [Sphinx](https://www.sphinx-doc.org) and [Breathe](https://www.breathe-doc.org) to compile the documentation. Also, make sure that you have [LaTeX](https://www.latex-project.org) with PDF support installed on your system if you want to generate the documentation in PDF format.

The Z80InsnClock library requires some types and macros included in [Zeta](https://zxe.io/software/Zeta), a [header-only](https://en.wikipedia.org/wiki/Header-only), dependency-free library used for portability reasons. Zeta is the sole dependency; Z80InsnClock does not depend on the [C standard library](https://en.wikipedia.org/wiki/C_standard_library).

### Configure

Once the prerequisites are met, create a directory and run `cmake` from there to prepare the build system:

```shell
mkdir build
cd build
cmake [options] <Z80InsnClock-project-directory>
```

The resulting build files can be configured by passing options to `cmake`. To show a complete list of those available along with their current settings, type the following:

```shell
cmake -LAH -N -B .
```

If in doubt, read the [CMake documentation](https://cmake.org/documentation/) for more information on configuration options. The following are some of the most relevant standard options of CMake:

* <span id="cmake_option_build_shared_libs">**<code>-D[BUILD_SHARED_LIBS](https://cmake.org/cmake/help/latest/variable/BUILD_SHARED_LIBS.html)=(YES|NO)</code>**</span>  
	Generate shared libraries rather than static libraries.  
	The default is `NO`.

* <span id="cmake_option_cmake_build_type">**<code>-D[CMAKE_BUILD_TYPE](https://cmake.org/cmake/help/latest/variable/CMAKE_BUILD_TYPE.html)=(Debug|Release|RelWithDebInfo|MinSizeRel)</code>**</span>  
	Choose the type of build (configuration) to generate.  
	The default is `Release`.

* <span id="cmake_option_cmake_install_name_dir">**<code>-D[CMAKE_INSTALL_NAME_DIR](https://cmake.org/cmake/help/latest/variable/CMAKE_INSTALL_NAME_DIR.html)="\<path\>"</code>**</span>  
	Specify the [directory portion](https://developer.apple.com/documentation/xcode/build-settings-reference#Dynamic-Library-Install-Name-Base) of the [dynamic library install name](https://developer.apple.com/documentation/xcode/build-settings-reference#Dynamic-Library-Install-Name) on Apple platforms (for installed shared libraries).  
	Not defined by default.

* <span id="cmake_option_cmake_install_prefix">**<code>-D[CMAKE_INSTALL_PREFIX](https://cmake.org/cmake/help/latest/variable/CMAKE_INSTALL_PREFIX.html)="\<path\>"</code>**</span>  
	Specify the installation prefix.  
	The default is `"/usr/local"` (on [UNIX](https://en.wikipedia.org/wiki/Unix) and [UNIX-like](https://en.wikipedia.org/wiki/Unix-like) operating systems).

<span id="cmake_package_options">Package-specific options</span> are as follows:

* <span id="cmake_option_z80insnclock">**`-DZ80InsnClock=(All|Basic|Extra)`**</span>  
	Specify which operation mode(s) to build.  
	`All` enables both `Basic` and `Extra`. `Basic` mode is the simplest and only determines the clock cycle at which the ongoing M-cycle begins, while `Extra` mode additionally provides information about the duration of the M-cycle.  
	The default is `All`.

* <span id="cmake_option_z80insnclock_install_cmakedir">**`-DZ80InsnClock_INSTALL_CMAKEDIR="<path>"`**</span>  
	Specify the directory in which to install the CMake [config-file package](https://cmake.org/cmake/help/latest/manual/cmake-packages.7.html#config-file-packages).  
	The default is <code>"${[CMAKE_INSTALL_LIBDIR](https://cmake.org/cmake/help/latest/module/GNUInstallDirs.html)}/cmake/Z80InsnClock"</code>.

* <span id="cmake_option_z80insnclock_install_pkgconfigdir">**`-DZ80InsnClock_INSTALL_PKGCONFIGDIR="<path>"`**</span>  
	Specify the directory in which to install the [pkg-config](https://www.freedesktop.org/wiki/Software/pkg-config) [file](https://people.freedesktop.org/~dbn/pkg-config-guide.html).  
	The default is <code>"${[CMAKE_INSTALL_LIBDIR](https://cmake.org/cmake/help/latest/module/GNUInstallDirs.html)}/pkgconfig"</code>.

* <span id="cmake_option_z80insnclock_nostdlib_flags">**`-DZ80InsnClock_NOSTDLIB_FLAGS=(Auto|"[<flag>[;<flag>...]]")`**</span>  
	Specify the linker flags used to avoid linking against system libraries.  
	The default is `Auto` (autoconfigure flags). If you get linker errors, set this option to `""`.

* <span id="cmake_option_z80insnclock_object_libs">**`-DZ80InsnClock_OBJECT_LIBS=(YES|NO)`**</span>  
	Build Z80InsnClock as an [object library](https://cmake.org/cmake/help/latest/manual/cmake-buildsystem.7.html#object-libraries).  
	This option takes precedence over [`BUILD_SHARED_LIBS`](#cmake_option_build_shared_libs) and [`Z80InsnClock_SHARED_LIBS`](#cmake_option_z80insnclock_shared_libs). If enabled, the build system will ignore [`Z80InsnClock_WITH_CMAKE_SUPPORT`](#cmake_option_z80insnclock_with_cmake_support) and [`Z80InsnClock_WITH_PKGCONFIG_SUPPORT`](#cmake_option_z80insnclock_with_pkgconfig_support), as no libraries or support files will be installed.  
	The default is `NO`.

* <span id="cmake_option_z80insnclock_shared_libs">**`-DZ80InsnClock_SHARED_LIBS=(YES|NO)`**</span>  
	Build Z80InsnClock as a shared library, rather than static.  
	This option takes precedence over [`BUILD_SHARED_LIBS`](#cmake_option_build_shared_libs).  
	Not defined by default.

* <span id="cmake_option_z80insnclock_sphinx_html_theme">**`-DZ80InsnClock_SPHINX_HTML_THEME="[<name>]"`**</span>  
	Specify the Sphinx theme for the documentation in HTML format.  
	The default is `""` (use the default theme).

* <span id="cmake_option_z80insnclock_with_cmake_support">**`-DZ80InsnClock_WITH_CMAKE_SUPPORT=(YES|NO)`**</span>  
	Generate and install the CMake [config-file package](https://cmake.org/cmake/help/latest/manual/cmake-packages.7.html#config-file-packages).  
	The default is `NO`.

* <span id="cmake_option_z80insnclock_with_html_documentation">**`-DZ80InsnClock_WITH_HTML_DOCUMENTATION=(YES|NO)`**</span>  
	Build and install the documentation in HTML format.  
	It requires Doxygen, Sphinx and Breathe.  
	The default is `NO`.

* <span id="cmake_option_z80insnclock_with_pdf_documentation">**`-DZ80InsnClock_WITH_PDF_DOCUMENTATION=(YES|NO)`**</span>  
	Build and install the documentation in PDF format.  
	It requires Doxygen, Sphinx, Breathe, and LaTeX with PDF support.  
	The default is `NO`.

* <span id="cmake_option_z80insnclock_with_pkgconfig_support">**`-DZ80InsnClock_WITH_PKGCONFIG_SUPPORT=(YES|NO)`**</span>  
	Generate and install the [pkg-config](https://www.freedesktop.org/wiki/Software/pkg-config) [file](https://people.freedesktop.org/~dbn/pkg-config-guide.html).  
	The default is `NO`.

* <span id="cmake_option_z80insnclock_with_standard_documents">**`-DZ80InsnClock_WITH_STANDARD_DOCUMENTS=(YES|NO)`**</span>  
	Install the standard text documents distributed with the package: [`AUTHORS`](AUTHORS), [`HISTORY`](HISTORY), [`LICENSE-0BSD`](LICENSE-0BSD) and [`README`](README).  
	The default is `NO`.

### Build and install

Finally, once the build system is configured according to your needs, build and install the package:

```shell
cmake --build . [--config (Debug|Release|RelWithDebInfo|MinSizeRel)]
cmake --install . [--config <configuration>] [--strip]
```

The [`--config`](https://cmake.org/cmake/help/latest/manual/cmake.1.html#cmdoption-cmake-build-config) option is only necessary for those [CMake generators](https://cmake.org/cmake/help/latest/manual/cmake-generators.7.html) that ignore [`CMAKE_BUILD_TYPE`](#cmake_option_cmake_build_type) (e.g., Xcode and Visual Studio). Use [`--strip`](https://cmake.org/cmake/help/latest/manual/cmake.1.html#cmdoption-cmake-install-strip) to remove debugging information and non-public symbols when installing non-debug builds of the shared library.

### TL;DR

Use the following to build Z80InsnClock as a shared library and install it along with the development files into `$HOME/.local`:

```shell
mkdir work && cd work
git clone https://github.com/agaxia/Z80InsnClock.git
cd Z80InsnClock
mkdir build && cd build
cmake \
	-DBUILD_SHARED_LIBS=YES \
	-DCMAKE_BUILD_TYPE=Release \
	-DCMAKE_INSTALL_NAME_DIR="$HOME/.local/lib" \
	-DCMAKE_INSTALL_PREFIX="$HOME/.local" \
	-DZ80InsnClock_WITH_CMAKE_SUPPORT=YES \
	-DZ80InsnClock_WITH_PKGCONFIG_SUPPORT=YES \
	..
cmake --build . --config Release
cmake --install . --config Release --strip
```

<sup>**[<sub><img src="https://zxe.io/software/Z80InsnClock/assets/images/sh.svg" height="14" width="19"></sub> build-and-install-Z80InsnClock.sh](https://zxe.io/software/Z80InsnClock/scripts/build-and-install-Z80InsnClock.sh)**</sup>

## License

<img src="https://zxe.io/software/Z80InsnClock/assets/images/0bsd.svg" width="150" height="70" align="right">

Copyright © 2021-2025 Sofía Ortega Sosa.

Permission to use, copy, modify, and/or distribute this software for any
purpose with or without fee is hereby granted.

THE SOFTWARE IS PROVIDED "AS IS" AND THE AUTHOR DISCLAIMS ALL WARRANTIES WITH REGARD TO THIS SOFTWARE INCLUDING ALL IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS. IN NO EVENT SHALL THE AUTHOR BE LIABLE FOR ANY SPECIAL, DIRECT, INDIRECT, OR CONSEQUENTIAL DAMAGES OR ANY DAMAGES WHATSOEVER RESULTING FROM LOSS OF USE, DATA OR PROFITS, WHETHER IN AN ACTION OF CONTRACT, NEGLIGENCE OR OTHER TORTIOUS ACTION, ARISING OUT OF OR IN CONNECTION WITH THE USE OR PERFORMANCE OF THIS SOFTWARE.
