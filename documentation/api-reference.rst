=============
API reference
=============

.. code-block:: c

   #include <Z80InsnClock.h>

Types
=====

.. doxygenstruct:: Z80InsnClock
   :members:

Macros
======

Library version
---------------

.. doxygendefine:: Z80_INSN_CLOCK_LIBRARY_VERSION_MAJOR
.. doxygendefine:: Z80_INSN_CLOCK_LIBRARY_VERSION_MINOR
.. doxygendefine:: Z80_INSN_CLOCK_LIBRARY_VERSION_MICRO
.. doxygendefine:: Z80_INSN_CLOCK_LIBRARY_VERSION_STRING

Instruction prefix
------------------

.. doxygendefine:: Z80_INSN_CLOCK_PREFIX_NONE
.. doxygendefine:: Z80_INSN_CLOCK_PREFIX_CB
.. doxygendefine:: Z80_INSN_CLOCK_PREFIX_XY
.. doxygendefine:: Z80_INSN_CLOCK_PREFIX_ED

Variables
=========

.. doxygenvariable:: z80_insn_clock_table
.. doxygenvariable:: z80_insn_clock_extra_table

Functions
=========

.. doxygenfunction:: z80_insn_clock_initialize
.. doxygenfunction:: z80_insn_clock_start

.. doxygenfunction:: z80_insn_clock_m1
.. doxygenfunction:: z80_insn_clock_inta
.. doxygenfunction:: z80_insn_clock_nmia
.. doxygenfunction:: z80_insn_clock_m

.. doxygenfunction:: z80_insn_clock_extra_m1
.. doxygenfunction:: z80_insn_clock_extra_inta
.. doxygenfunction:: z80_insn_clock_extra_nmia_fast
.. doxygenfunction:: z80_insn_clock_extra_nmia
.. doxygenfunction:: z80_insn_clock_extra_m
.. doxygenfunction:: z80_insn_clock_extra_out

.. doxygenfunction:: z80_insn_clock_extra_add_m1
.. doxygenfunction:: z80_insn_clock_extra_add_inta
.. doxygenfunction:: z80_insn_clock_extra_add_nmia
.. doxygenfunction:: z80_insn_clock_extra_add_m
.. doxygenfunction:: z80_insn_clock_extra_add_in
