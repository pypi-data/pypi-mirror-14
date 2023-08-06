.. currentmodule:: abjad.tools.timespantools

OffsetTimespanTimeRelation
==========================

.. autoclass:: OffsetTimespanTimeRelation

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
              "abjad.tools.timespantools.OffsetTimespanTimeRelation.OffsetTimespanTimeRelation" [color=black,
                  fontcolor=white,
                  group=2,
                  label=<<B>OffsetTimespanTimeRelation</B>>,
                  shape=box,
                  style="filled, rounded"];
              "abjad.tools.timespantools.TimeRelation.TimeRelation" [color=3,
                  group=2,
                  label=TimeRelation,
                  shape=oval,
                  style=bold];
              "abjad.tools.timespantools.TimeRelation.TimeRelation" -> "abjad.tools.timespantools.OffsetTimespanTimeRelation.OffsetTimespanTimeRelation";
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

      ~abjad.tools.timespantools.OffsetTimespanTimeRelation.OffsetTimespanTimeRelation.inequality
      ~abjad.tools.timespantools.OffsetTimespanTimeRelation.OffsetTimespanTimeRelation.is_fully_loaded
      ~abjad.tools.timespantools.OffsetTimespanTimeRelation.OffsetTimespanTimeRelation.is_fully_unloaded
      ~abjad.tools.timespantools.OffsetTimespanTimeRelation.OffsetTimespanTimeRelation.offset
      ~abjad.tools.timespantools.OffsetTimespanTimeRelation.OffsetTimespanTimeRelation.timespan
      ~abjad.tools.timespantools.OffsetTimespanTimeRelation.OffsetTimespanTimeRelation.__call__
      ~abjad.tools.timespantools.OffsetTimespanTimeRelation.OffsetTimespanTimeRelation.__eq__
      ~abjad.tools.timespantools.OffsetTimespanTimeRelation.OffsetTimespanTimeRelation.__format__
      ~abjad.tools.timespantools.OffsetTimespanTimeRelation.OffsetTimespanTimeRelation.__hash__
      ~abjad.tools.timespantools.OffsetTimespanTimeRelation.OffsetTimespanTimeRelation.__ne__
      ~abjad.tools.timespantools.OffsetTimespanTimeRelation.OffsetTimespanTimeRelation.__repr__

Read-only properties
--------------------

.. only:: html

   .. container:: inherited

      .. autoattribute:: abjad.tools.timespantools.OffsetTimespanTimeRelation.OffsetTimespanTimeRelation.inequality

.. autoattribute:: abjad.tools.timespantools.OffsetTimespanTimeRelation.OffsetTimespanTimeRelation.is_fully_loaded

.. autoattribute:: abjad.tools.timespantools.OffsetTimespanTimeRelation.OffsetTimespanTimeRelation.is_fully_unloaded

.. autoattribute:: abjad.tools.timespantools.OffsetTimespanTimeRelation.OffsetTimespanTimeRelation.offset

.. autoattribute:: abjad.tools.timespantools.OffsetTimespanTimeRelation.OffsetTimespanTimeRelation.timespan

Special methods
---------------

.. automethod:: abjad.tools.timespantools.OffsetTimespanTimeRelation.OffsetTimespanTimeRelation.__call__

.. automethod:: abjad.tools.timespantools.OffsetTimespanTimeRelation.OffsetTimespanTimeRelation.__eq__

.. automethod:: abjad.tools.timespantools.OffsetTimespanTimeRelation.OffsetTimespanTimeRelation.__format__

.. automethod:: abjad.tools.timespantools.OffsetTimespanTimeRelation.OffsetTimespanTimeRelation.__hash__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.timespantools.OffsetTimespanTimeRelation.OffsetTimespanTimeRelation.__ne__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.timespantools.OffsetTimespanTimeRelation.OffsetTimespanTimeRelation.__repr__
