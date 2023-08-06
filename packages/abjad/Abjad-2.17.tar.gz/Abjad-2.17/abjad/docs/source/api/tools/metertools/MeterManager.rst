.. currentmodule:: abjad.tools.metertools

MeterManager
============

.. autoclass:: MeterManager

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
              "abjad.tools.abctools.AbjadObject.AbstractBase" -> "abjad.tools.abctools.AbjadObject.AbjadObject";
          }
          subgraph cluster_metertools {
              graph [label=metertools];
              "abjad.tools.metertools.MeterManager.MeterManager" [color=black,
                  fontcolor=white,
                  group=2,
                  label=<<B>MeterManager</B>>,
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
          "abjad.tools.abctools.AbjadObject.AbjadObject" -> "abjad.tools.metertools.MeterManager.MeterManager";
          "builtins.object" -> "abjad.tools.abctools.AbjadObject.AbstractBase";
      }

Bases
-----

- :py:class:`abjad.tools.abctools.AbjadObject`

- :py:class:`abjad.tools.abctools.AbjadObject.AbstractBase`

- :py:class:`builtins.object`

.. only:: html

   Attribute summary
   -----------------

   .. autosummary::

      ~abjad.tools.metertools.MeterManager.MeterManager.get_offsets_at_depth
      ~abjad.tools.metertools.MeterManager.MeterManager.is_acceptable_logical_tie
      ~abjad.tools.metertools.MeterManager.MeterManager.is_boundary_crossing_logical_tie
      ~abjad.tools.metertools.MeterManager.MeterManager.iterate_rewrite_inputs
      ~abjad.tools.metertools.MeterManager.MeterManager.__eq__
      ~abjad.tools.metertools.MeterManager.MeterManager.__format__
      ~abjad.tools.metertools.MeterManager.MeterManager.__hash__
      ~abjad.tools.metertools.MeterManager.MeterManager.__ne__
      ~abjad.tools.metertools.MeterManager.MeterManager.__repr__

Class & static methods
----------------------

.. automethod:: abjad.tools.metertools.MeterManager.MeterManager.get_offsets_at_depth

.. automethod:: abjad.tools.metertools.MeterManager.MeterManager.is_acceptable_logical_tie

.. automethod:: abjad.tools.metertools.MeterManager.MeterManager.is_boundary_crossing_logical_tie

.. automethod:: abjad.tools.metertools.MeterManager.MeterManager.iterate_rewrite_inputs

Special methods
---------------

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.metertools.MeterManager.MeterManager.__eq__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.metertools.MeterManager.MeterManager.__format__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.metertools.MeterManager.MeterManager.__hash__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.metertools.MeterManager.MeterManager.__ne__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.metertools.MeterManager.MeterManager.__repr__
