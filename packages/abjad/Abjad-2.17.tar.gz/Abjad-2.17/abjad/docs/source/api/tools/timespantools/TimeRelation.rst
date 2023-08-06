.. currentmodule:: abjad.tools.timespantools

TimeRelation
============

.. autoclass:: TimeRelation

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
              "abjad.tools.timespantools.OffsetTimespanTimeRelation.OffsetTimespanTimeRelation" [color=3,
                  group=2,
                  label=OffsetTimespanTimeRelation,
                  shape=box];
              "abjad.tools.timespantools.TimeRelation.TimeRelation" [color=black,
                  fontcolor=white,
                  group=2,
                  label=<<B>TimeRelation</B>>,
                  shape=oval,
                  style="filled, rounded"];
              "abjad.tools.timespantools.TimespanTimespanTimeRelation.TimespanTimespanTimeRelation" [color=3,
                  group=2,
                  label=TimespanTimespanTimeRelation,
                  shape=box];
              "abjad.tools.timespantools.TimeRelation.TimeRelation" -> "abjad.tools.timespantools.OffsetTimespanTimeRelation.OffsetTimespanTimeRelation";
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

- :py:class:`abjad.tools.abctools.AbjadObject`

- :py:class:`abjad.tools.abctools.AbjadObject.AbstractBase`

- :py:class:`builtins.object`

.. only:: html

   Attribute summary
   -----------------

   .. autosummary::

      ~abjad.tools.timespantools.TimeRelation.TimeRelation.inequality
      ~abjad.tools.timespantools.TimeRelation.TimeRelation.is_fully_loaded
      ~abjad.tools.timespantools.TimeRelation.TimeRelation.is_fully_unloaded
      ~abjad.tools.timespantools.TimeRelation.TimeRelation.__call__
      ~abjad.tools.timespantools.TimeRelation.TimeRelation.__eq__
      ~abjad.tools.timespantools.TimeRelation.TimeRelation.__format__
      ~abjad.tools.timespantools.TimeRelation.TimeRelation.__hash__
      ~abjad.tools.timespantools.TimeRelation.TimeRelation.__ne__
      ~abjad.tools.timespantools.TimeRelation.TimeRelation.__repr__

Read-only properties
--------------------

.. autoattribute:: abjad.tools.timespantools.TimeRelation.TimeRelation.inequality

.. autoattribute:: abjad.tools.timespantools.TimeRelation.TimeRelation.is_fully_loaded

.. autoattribute:: abjad.tools.timespantools.TimeRelation.TimeRelation.is_fully_unloaded

Special methods
---------------

.. automethod:: abjad.tools.timespantools.TimeRelation.TimeRelation.__call__

.. automethod:: abjad.tools.timespantools.TimeRelation.TimeRelation.__eq__

.. automethod:: abjad.tools.timespantools.TimeRelation.TimeRelation.__format__

.. automethod:: abjad.tools.timespantools.TimeRelation.TimeRelation.__hash__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.timespantools.TimeRelation.TimeRelation.__ne__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.timespantools.TimeRelation.TimeRelation.__repr__
