.. currentmodule:: abjad.tools.timespantools

TimespanTimespanTimeRelation
============================

.. autoclass:: TimespanTimespanTimeRelation

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
          subgraph cluster_timespantools {
              graph [label=timespantools];
              "abjad.tools.timespantools.TimeRelation.TimeRelation" [color=3,
                  group=2,
                  label=TimeRelation,
                  shape=oval,
                  style=bold];
              "abjad.tools.timespantools.TimespanTimespanTimeRelation.TimespanTimespanTimeRelation" [color=black,
                  fontcolor=white,
                  group=2,
                  label=<<B>TimespanTimespanTimeRelation</B>>,
                  shape=box,
                  style="filled, rounded"];
              "abjad.tools.timespantools.TimeRelation.TimeRelation" -> "abjad.tools.timespantools.TimespanTimespanTimeRelation.TimespanTimespanTimeRelation";
          }
          subgraph cluster_builtins {
              graph [label=builtins];
              "builtins.object" [color=2,
                  group=1,
                  label=object,
                  shape=box];
          }
          "abjad.tools.abctools.AbjadObject.AbjadObject" -> "abjad.tools.timespantools.TimeRelation.TimeRelation";
          "builtins.object" -> "abjad.tools.abctools.AbjadObject.AbstractBase";
      }

Bases
-----

- :py:class:`abjad.tools.timespantools.TimeRelation`

- :py:class:`abjad.tools.abctools.AbjadObject`

- :py:class:`abjad.tools.abctools.AbjadObject.AbstractBase`

- :py:class:`builtins.object`

.. only:: html

   Attribute summary
   -----------------

   .. autosummary::

      ~abjad.tools.timespantools.TimespanTimespanTimeRelation.TimespanTimespanTimeRelation.get_counttime_components
      ~abjad.tools.timespantools.TimespanTimespanTimeRelation.TimespanTimespanTimeRelation.get_offset_indices
      ~abjad.tools.timespantools.TimespanTimespanTimeRelation.TimespanTimespanTimeRelation.inequality
      ~abjad.tools.timespantools.TimespanTimespanTimeRelation.TimespanTimespanTimeRelation.is_fully_loaded
      ~abjad.tools.timespantools.TimespanTimespanTimeRelation.TimespanTimespanTimeRelation.is_fully_unloaded
      ~abjad.tools.timespantools.TimespanTimespanTimeRelation.TimespanTimespanTimeRelation.timespan_1
      ~abjad.tools.timespantools.TimespanTimespanTimeRelation.TimespanTimespanTimeRelation.timespan_2
      ~abjad.tools.timespantools.TimespanTimespanTimeRelation.TimespanTimespanTimeRelation.__call__
      ~abjad.tools.timespantools.TimespanTimespanTimeRelation.TimespanTimespanTimeRelation.__eq__
      ~abjad.tools.timespantools.TimespanTimespanTimeRelation.TimespanTimespanTimeRelation.__format__
      ~abjad.tools.timespantools.TimespanTimespanTimeRelation.TimespanTimespanTimeRelation.__hash__
      ~abjad.tools.timespantools.TimespanTimespanTimeRelation.TimespanTimespanTimeRelation.__ne__
      ~abjad.tools.timespantools.TimespanTimespanTimeRelation.TimespanTimespanTimeRelation.__repr__

Read-only properties
--------------------

.. only:: html

   .. container:: inherited

      .. autoattribute:: abjad.tools.timespantools.TimespanTimespanTimeRelation.TimespanTimespanTimeRelation.inequality

.. autoattribute:: abjad.tools.timespantools.TimespanTimespanTimeRelation.TimespanTimespanTimeRelation.is_fully_loaded

.. autoattribute:: abjad.tools.timespantools.TimespanTimespanTimeRelation.TimespanTimespanTimeRelation.is_fully_unloaded

.. autoattribute:: abjad.tools.timespantools.TimespanTimespanTimeRelation.TimespanTimespanTimeRelation.timespan_1

.. autoattribute:: abjad.tools.timespantools.TimespanTimespanTimeRelation.TimespanTimespanTimeRelation.timespan_2

Methods
-------

.. automethod:: abjad.tools.timespantools.TimespanTimespanTimeRelation.TimespanTimespanTimeRelation.get_counttime_components

.. automethod:: abjad.tools.timespantools.TimespanTimespanTimeRelation.TimespanTimespanTimeRelation.get_offset_indices

Special methods
---------------

.. automethod:: abjad.tools.timespantools.TimespanTimespanTimeRelation.TimespanTimespanTimeRelation.__call__

.. automethod:: abjad.tools.timespantools.TimespanTimespanTimeRelation.TimespanTimespanTimeRelation.__eq__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.timespantools.TimespanTimespanTimeRelation.TimespanTimespanTimeRelation.__format__

.. automethod:: abjad.tools.timespantools.TimespanTimespanTimeRelation.TimespanTimespanTimeRelation.__hash__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.timespantools.TimespanTimespanTimeRelation.TimespanTimespanTimeRelation.__ne__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.timespantools.TimespanTimespanTimeRelation.TimespanTimespanTimeRelation.__repr__
