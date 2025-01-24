# Z80InsnClock - CMakeLists.txt
#  ________ ________ _________
# |____   /|   __   |   __   |\
#  \__/  / |  |\_|  |  |\_|  | |
#    /  / /|   __   |  | ||  | |
#   /  /_/_|  |\_|  |  |_||  | | Instruction Clock
#  /_______|________|________| | Copyright (C) 2021-2025 Sofía Ortega Sosa.
#  \________\________\________\| Released under the BSD Zero Clause License.

cmake_minimum_required(
	# 3.14: install(TARGETS ARCHIVE [DESTINATION])
	VERSION 3.14...${CMAKE_VERSION})

if(	CMAKE_CURRENT_SOURCE_DIR STREQUAL CMAKE_SOURCE_DIR AND
	NOT CMAKE_BUILD_TYPE AND NOT CMAKE_CONFIGURATION_TYPES
)
	set(CMAKE_BUILD_TYPE Release)
endif()

file(READ "${CMAKE_CURRENT_SOURCE_DIR}/API/Z80InsnClock.h" _)
string(REGEX MATCH ".*Z80_INSN_CLOCK_LIBRARY_VERSION_STRING \"([^\n]*)\".*" _ ${_})

project(Z80InsnClock
	VERSION ${CMAKE_MATCH_1}
	LANGUAGES C
	DESCRIPTION "Z80 instruction clock"
	HOMEPAGE_URL "https://zxe.io/software/Z80InsnClock")

unset(_)
message("${PROJECT_NAME} v${PROJECT_VERSION}")

set(${PROJECT_NAME}
"All" CACHE STRING
"${PROJECT_NAME}: \
Operation mode(s) to build.")

if(NOT ${PROJECT_NAME} MATCHES "^(All|Basic|Extra)$")
	message(FATAL_ERROR "Invalid value for option `${PROJECT_NAME}`.")
endif()

include(GNUInstallDirs)

set(${PROJECT_NAME}_INSTALL_CMAKEDIR
"${CMAKE_INSTALL_LIBDIR}/cmake/${PROJECT_NAME}" CACHE STRING
"${PROJECT_NAME}: \
Directory in which to install the CMake config-file package.")

set(${PROJECT_NAME}_INSTALL_PKGCONFIGDIR
"${CMAKE_INSTALL_LIBDIR}/pkgconfig" CACHE STRING
"${PROJECT_NAME}: \
Directory in which to install the pkg-config file.")

set(${PROJECT_NAME}_NOSTDLIB_FLAGS
"Auto" CACHE STRING
"${PROJECT_NAME}: \
Linker flags used to avoid linking against system libraries.")

option(${PROJECT_NAME}_OBJECT_LIBS
"${PROJECT_NAME}: \
Build ${PROJECT_NAME} as an object library."
NO)

set(${PROJECT_NAME}_SPHINX_HTML_THEME
"" CACHE STRING
"${PROJECT_NAME}: \
Sphinx theme for the documentation in HTML format.")

option(${PROJECT_NAME}_WITH_CMAKE_SUPPORT
"${PROJECT_NAME}: \
Generate and install the CMake config-file package."
NO)

option(${PROJECT_NAME}_WITH_HTML_DOCUMENTATION
"${PROJECT_NAME}: \
Build and install the documentation in HTML format."
NO)

option(${PROJECT_NAME}_WITH_PDF_DOCUMENTATION
"${PROJECT_NAME}: \
Build and install the documentation in PDF format."
NO)

option(${PROJECT_NAME}_WITH_PKGCONFIG_SUPPORT
"${PROJECT_NAME}: \
Generate and install the pkg-config file."
NO)

option(${PROJECT_NAME}_WITH_STANDARD_DOCUMENTS
"${PROJECT_NAME}: \
Install the standard text documents distributed with the package: \
AUTHORS, HISTORY, LICENSE-0BSD and README."
NO)

list(APPEND CMAKE_MODULE_PATH "${CMAKE_CURRENT_SOURCE_DIR}/CMake")

if(NOT TARGET Zeta)
	find_package(Zeta REQUIRED)
endif()

if(${PROJECT_NAME}_OBJECT_LIBS)
	add_library(${PROJECT_NAME} OBJECT)
else()
	if(DEFINED ${PROJECT_NAME}_SHARED_LIBS)
		set(BUILD_SHARED_LIBS ${${PROJECT_NAME}_SHARED_LIBS})
	endif()

	add_library(${PROJECT_NAME})
endif()

target_sources(
	${PROJECT_NAME} PRIVATE
	"${CMAKE_CURRENT_SOURCE_DIR}/API/Z80InsnClock.h"
	"${CMAKE_CURRENT_SOURCE_DIR}/sources/Z80InsnClock.c")

set_target_properties(
	${PROJECT_NAME} PROPERTIES
	C_STANDARD 99
	C_STANDARD_REQUIRED NO
	VERSION	${PROJECT_VERSION}
	SOVERSION ${PROJECT_VERSION_MAJOR}
	DEBUG_POSTFIX "-debug"
	PUBLIC_HEADER "${CMAKE_CURRENT_SOURCE_DIR}/API/Z80InsnClock.h")

target_link_libraries(${PROJECT_NAME} PUBLIC Zeta)

target_include_directories(
	${PROJECT_NAME} PUBLIC
	"$<BUILD_INTERFACE:${CMAKE_CURRENT_SOURCE_DIR}/API>"
	"$<INSTALL_INTERFACE:${CMAKE_INSTALL_INCLUDEDIR}>")

if(${PROJECT_NAME}_OBJECT_LIBS OR NOT BUILD_SHARED_LIBS)
	target_compile_definitions(${PROJECT_NAME} PUBLIC Z80_INSN_CLOCK_STATIC)
else()
	if(WIN32)
		if(PROJECT_VERSION_PATCH STREQUAL "")
			set(PROJECT_VERSION_PATCH 0)
		endif()

		configure_file(
			"${CMAKE_CURRENT_SOURCE_DIR}/sources/Z80InsnClock.rc.in"
			"${CMAKE_CURRENT_BINARY_DIR}/Z80InsnClock.rc"
			@ONLY)

		target_sources(${PROJECT_NAME} PRIVATE "${CMAKE_CURRENT_BINARY_DIR}/Z80InsnClock.rc")
	endif()

	if(${PROJECT_NAME}_NOSTDLIB_FLAGS STREQUAL "Auto")
		if(MSVC)
			target_compile_definitions(${PROJECT_NAME} PRIVATE Z80_INSN_CLOCK_WITH_DLL_MAIN_CRT_STARTUP)
			target_link_options(${PROJECT_NAME} PRIVATE "/NODEFAULTLIB")
		elseif(APPLE)
			if(CMAKE_C_COMPILER_ID MATCHES "^(AppleClang|Clang|GNU)$")
				target_link_options(${PROJECT_NAME} PRIVATE "LINKER:-dead_strip_dylibs")
			endif()
		elseif(CMAKE_C_COMPILER_ID MATCHES "^(ARMClang|Clang|GNU|Intel|TinyCC|XL|XLClang)$")
			target_link_options(${PROJECT_NAME} PRIVATE "-nostdlib")
		elseif(CMAKE_C_COMPILER_ID MATCHES "PGI")
			target_link_options(${PROJECT_NAME} PRIVATE "-Mnostdlib")
		elseif(CMAKE_C_COMPILER_ID MATCHES "SunPro")
			target_link_options(${PROJECT_NAME} PRIVATE "-xnolib")
		endif()
	elseif(NOT ${PROJECT_NAME}_NOSTDLIB_FLAGS STREQUAL "")
		target_link_options(${PROJECT_NAME} PRIVATE ${${PROJECT_NAME}_NOSTDLIB_FLAGS})
	endif()
endif()

if(${PROJECT_NAME} STREQUAL "Basic")
	target_compile_definitions(${PROJECT_NAME} PRIVATE Z80_INSN_CLOCK=1)
elseif(${PROJECT_NAME} STREQUAL "Extra")
	target_compile_definitions(${PROJECT_NAME} PRIVATE Z80_INSN_CLOCK=2)
endif()

install(TARGETS ${PROJECT_NAME}
	EXPORT  ${PROJECT_NAME}_Targets
	RUNTIME COMPONENT ${PROJECT_NAME}_Runtime
	LIBRARY DESTINATION "${CMAKE_INSTALL_LIBDIR}"
		COMPONENT ${PROJECT_NAME}_Runtime
		NAMELINK_COMPONENT ${PROJECT_NAME}_Development
	ARCHIVE COMPONENT ${PROJECT_NAME}_Development
	PUBLIC_HEADER
		DESTINATION "${CMAKE_INSTALL_INCLUDEDIR}"
		COMPONENT ${PROJECT_NAME}_Development)

if(	NOT ${PROJECT_NAME}_OBJECT_LIBS AND
	(${PROJECT_NAME}_WITH_CMAKE_SUPPORT OR ${PROJECT_NAME}_WITH_PKGCONFIG_SUPPORT)
)
	include(CMakePackageConfigHelpers)

	if(${PROJECT_NAME}_WITH_CMAKE_SUPPORT)
		if(BUILD_SHARED_LIBS)
			set(_type Shared)
		else()
			set(_type Static)
		endif()

		install(EXPORT ${PROJECT_NAME}_Targets
			DESTINATION "${${PROJECT_NAME}_INSTALL_CMAKEDIR}"
			FILE ${PROJECT_NAME}${_type}Targets.cmake
			COMPONENT ${PROJECT_NAME}_Development)

		unset(_type)

		write_basic_package_version_file(
			"${CMAKE_CURRENT_BINARY_DIR}/${PROJECT_NAME}ConfigVersion.cmake"
			VERSION ${PROJECT_VERSION}
			COMPATIBILITY SameMajorVersion)

		configure_package_config_file(
			"${CMAKE_CURRENT_SOURCE_DIR}/support/${PROJECT_NAME}Config.cmake.in"
			"${CMAKE_CURRENT_BINARY_DIR}/${PROJECT_NAME}Config.cmake"
			INSTALL_DESTINATION "${${PROJECT_NAME}_INSTALL_CMAKEDIR}")

		install(FILES
			"${CMAKE_CURRENT_BINARY_DIR}/${PROJECT_NAME}Config.cmake"
			"${CMAKE_CURRENT_BINARY_DIR}/${PROJECT_NAME}ConfigVersion.cmake"
			DESTINATION "${${PROJECT_NAME}_INSTALL_CMAKEDIR}"
			COMPONENT ${PROJECT_NAME}_Development)
	endif()

	if(${PROJECT_NAME}_WITH_PKGCONFIG_SUPPORT)
		configure_file(
			"${CMAKE_CURRENT_SOURCE_DIR}/support/${PROJECT_NAME}.pc.in"
			"${CMAKE_CURRENT_BINARY_DIR}/${PROJECT_NAME}.pc"
			@ONLY)

		install(FILES "${CMAKE_CURRENT_BINARY_DIR}/${PROJECT_NAME}.pc"
			DESTINATION "${${PROJECT_NAME}_INSTALL_PKGCONFIGDIR}"
			COMPONENT ${PROJECT_NAME}_Development)
	endif()
endif()

if(${PROJECT_NAME}_WITH_STANDARD_DOCUMENTS)
	install(FILES	"${CMAKE_CURRENT_SOURCE_DIR}/AUTHORS"
			#"${CMAKE_CURRENT_SOURCE_DIR}/HISTORY"
			"${CMAKE_CURRENT_SOURCE_DIR}/LICENSE-0BSD"
			"${CMAKE_CURRENT_SOURCE_DIR}/README"
		DESTINATION "${CMAKE_INSTALL_DOCDIR}"
		COMPONENT ${PROJECT_NAME}_Runtime)
endif()

if(${PROJECT_NAME}_WITH_HTML_DOCUMENTATION OR ${PROJECT_NAME}_WITH_PDF_DOCUMENTATION)
	add_subdirectory(documentation)
endif()

if(NOT CMAKE_CURRENT_SOURCE_DIR STREQUAL CMAKE_SOURCE_DIR)
	message("${PROJECT_NAME} END")
endif()

# CMakeLists.txt EOF
