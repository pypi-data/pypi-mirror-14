.. currentmodule:: abjad.tools.metertools

MeterFittingSession
===================

.. autoclass:: MeterFittingSession

Lineage
-------

.. container:: graphviz

   .. graphviz::

      digraph InheritanceGraph {
          graph [background=transparent,
              bgcolor=transparent,
              color=lightslategrey,
              fontname=Arial,
              outputorder=edgesfirst,
              overlap=prism,
              penwidth=2,
              rankdir=LR,
              root="__builtin__.object",
              splines=spline,
              style="dotted, rounded",
              truecolor=true];
          node [colorscheme=pastel19,
              fontname=Arial,
              fontsize=12,
              penwidth=2,
              style="filled, rounded"];
          edge [color=lightsteelblue2,
              penwidth=2];
          subgraph cluster_abctools {
              graph [label=abctools];
              "abjad.tools.abctools.AbjadObject.AbjadObject" [color=1,
                  group=0,
                  label=AbjadObject,
                  shape=box];
              "abjad.tools.abctools.AbjadObject.AbstractBase" [color=1,
                  group=0,
                  label=AbstractBase,
                  shape=box];
              "abjad.tools.abctools.AbjadValueObject.AbjadValueObject" [color=1,
                  group=0,
                  label=AbjadValueObject,
                  shape=box];
              "abjad.tools.abctools.AbjadObject.AbjadObject" -> "abjad.tools.abctools.AbjadValueObject.AbjadValueObject";
              "abjad.tools.abctools.AbjadObject.AbstractBase" -> "abjad.tools.abctools.AbjadObject.AbjadObject";
          }
          subgraph cluster_metertools {
              graph [label=metertools];
              "abjad.tools.metertools.MeterFittingSession.MeterFittingSession" [color=black,
                  fontcolor=white,
                  group=2,
                  label=<<B>MeterFittingSession</B>>,
                  shape=box,
                  style="filled, rounded"];
          }
          subgraph cluster_builtins {
              graph [label=builtins];
              "builtins.object" [color=2,
                  group=1,
                  label=object,
                  shape=box];
          }
          "abjad.tools.abctools.AbjadValueObject.AbjadValueObject" -> "abjad.tools.metertools.MeterFittingSession.MeterFittingSession";
          "builtins.object" -> "abjad.tools.abctools.AbjadObject.AbstractBase";
      }

Bases
-----

- :py:class:`abjad.tools.abctools.AbjadValueObject`

- :py:class:`abjad.tools.abctools.AbjadObject`

- :py:class:`abjad.tools.abctools.AbjadObject.AbstractBase`

- :py:class:`builtins.object`

.. only:: html

   Attribute summary
   -----------------

   .. autosummary::

      ~abjad.tools.metertools.MeterFittingSession.MeterFittingSession.cached_offset_counters
      ~abjad.tools.metertools.MeterFittingSession.MeterFittingSession.kernel_denominator
      ~abjad.tools.metertools.MeterFittingSession.MeterFittingSession.kernels
      ~abjad.tools.metertools.MeterFittingSession.MeterFittingSession.longest_kernel
      ~abjad.tools.metertools.MeterFittingSession.MeterFittingSession.maximum_run_length
      ~abjad.tools.metertools.MeterFittingSession.MeterFittingSession.meters
      ~abjad.tools.metertools.MeterFittingSession.MeterFittingSession.offset_counter
      ~abjad.tools.metertools.MeterFittingSession.MeterFittingSession.ordered_offsets
      ~abjad.tools.metertools.MeterFittingSession.MeterFittingSession.__call__
      ~abjad.tools.metertools.MeterFittingSession.MeterFittingSession.__copy__
      ~abjad.tools.metertools.MeterFittingSession.MeterFittingSession.__eq__
      ~abjad.tools.metertools.MeterFittingSession.MeterFittingSession.__format__
      ~abjad.tools.metertools.MeterFittingSession.MeterFittingSession.__hash__
      ~abjad.tools.metertools.MeterFittingSession.MeterFittingSession.__ne__
      ~abjad.tools.metertools.MeterFittingSession.MeterFittingSession.__repr__

Read-only properties
--------------------

.. autoattribute:: abjad.tools.metertools.MeterFittingSession.MeterFittingSession.cached_offset_counters

.. autoattribute:: abjad.tools.metertools.MeterFittingSession.MeterFittingSession.kernel_denominator

.. autoattribute:: abjad.tools.metertools.MeterFittingSession.MeterFittingSession.kernels

.. autoattribute:: abjad.tools.metertools.MeterFittingSession.MeterFittingSession.longest_kernel

.. autoattribute:: abjad.tools.metertools.MeterFittingSession.MeterFittingSession.maximum_run_length

.. autoattribute:: abjad.tools.metertools.MeterFittingSession.MeterFittingSession.meters

.. autoattribute:: abjad.tools.metertools.MeterFittingSession.MeterFittingSession.offset_counter

.. autoattribute:: abjad.tools.metertools.MeterFittingSession.MeterFittingSession.ordered_offsets

Special methods
---------------

.. automethod:: abjad.tools.metertools.MeterFittingSession.MeterFittingSession.__call__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.metertools.MeterFittingSession.MeterFittingSession.__copy__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.metertools.MeterFittingSession.MeterFittingSession.__eq__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.metertools.MeterFittingSession.MeterFittingSession.__format__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.metertools.MeterFittingSession.MeterFittingSession.__hash__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.metertools.MeterFittingSession.MeterFittingSession.__ne__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.metertools.MeterFittingSession.MeterFittingSession.__repr__
