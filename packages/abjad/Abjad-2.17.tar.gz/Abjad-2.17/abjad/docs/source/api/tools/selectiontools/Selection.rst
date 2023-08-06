.. currentmodule:: abjad.tools.selectiontools

Selection
=========

.. autoclass:: Selection

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
          subgraph cluster_selectiontools {
              graph [label=selectiontools];
              "abjad.tools.selectiontools.Descendants.Descendants" [color=2,
                  group=1,
                  label=Descendants,
                  shape=box];
              "abjad.tools.selectiontools.Lineage.Lineage" [color=2,
                  group=1,
                  label=Lineage,
                  shape=box];
              "abjad.tools.selectiontools.LogicalTie.LogicalTie" [color=2,
                  group=1,
                  label=LogicalTie,
                  shape=box];
              "abjad.tools.selectiontools.Parentage.Parentage" [color=2,
                  group=1,
                  label=Parentage,
                  shape=box];
              "abjad.tools.selectiontools.Selection.Selection" [color=black,
                  fontcolor=white,
                  group=1,
                  label=<<B>Selection</B>>,
                  shape=box,
                  style="filled, rounded"];
              "abjad.tools.selectiontools.VerticalMoment.VerticalMoment" [color=2,
                  group=1,
                  label=VerticalMoment,
                  shape=box];
              "abjad.tools.selectiontools.Selection.Selection" -> "abjad.tools.selectiontools.Descendants.Descendants";
              "abjad.tools.selectiontools.Selection.Selection" -> "abjad.tools.selectiontools.Lineage.Lineage";
              "abjad.tools.selectiontools.Selection.Selection" -> "abjad.tools.selectiontools.LogicalTie.LogicalTie";
              "abjad.tools.selectiontools.Selection.Selection" -> "abjad.tools.selectiontools.Parentage.Parentage";
              "abjad.tools.selectiontools.Selection.Selection" -> "abjad.tools.selectiontools.VerticalMoment.VerticalMoment";
          }
          subgraph cluster_builtins {
              graph [label=builtins];
              "builtins.object" [color=1,
                  group=0,
                  label=object,
                  shape=box];
          }
          "builtins.object" -> "abjad.tools.selectiontools.Selection.Selection";
      }

Bases
-----

- :py:class:`builtins.object`

.. only:: html

   Attribute summary
   -----------------

   .. autosummary::

      ~abjad.tools.selectiontools.Selection.Selection.get_duration
      ~abjad.tools.selectiontools.Selection.Selection.get_spanners
      ~abjad.tools.selectiontools.Selection.Selection.get_timespan
      ~abjad.tools.selectiontools.Selection.Selection.get_vertical_moment_at
      ~abjad.tools.selectiontools.Selection.Selection.group_by
      ~abjad.tools.selectiontools.Selection.Selection.partition_by_durations
      ~abjad.tools.selectiontools.Selection.Selection.__add__
      ~abjad.tools.selectiontools.Selection.Selection.__contains__
      ~abjad.tools.selectiontools.Selection.Selection.__eq__
      ~abjad.tools.selectiontools.Selection.Selection.__format__
      ~abjad.tools.selectiontools.Selection.Selection.__getitem__
      ~abjad.tools.selectiontools.Selection.Selection.__hash__
      ~abjad.tools.selectiontools.Selection.Selection.__illustrate__
      ~abjad.tools.selectiontools.Selection.Selection.__len__
      ~abjad.tools.selectiontools.Selection.Selection.__ne__
      ~abjad.tools.selectiontools.Selection.Selection.__radd__
      ~abjad.tools.selectiontools.Selection.Selection.__repr__

Methods
-------

.. automethod:: abjad.tools.selectiontools.Selection.Selection.get_duration

.. automethod:: abjad.tools.selectiontools.Selection.Selection.get_spanners

.. automethod:: abjad.tools.selectiontools.Selection.Selection.get_timespan

.. automethod:: abjad.tools.selectiontools.Selection.Selection.get_vertical_moment_at

.. automethod:: abjad.tools.selectiontools.Selection.Selection.group_by

.. automethod:: abjad.tools.selectiontools.Selection.Selection.partition_by_durations

Special methods
---------------

.. automethod:: abjad.tools.selectiontools.Selection.Selection.__add__

.. automethod:: abjad.tools.selectiontools.Selection.Selection.__contains__

.. automethod:: abjad.tools.selectiontools.Selection.Selection.__eq__

.. automethod:: abjad.tools.selectiontools.Selection.Selection.__format__

.. automethod:: abjad.tools.selectiontools.Selection.Selection.__getitem__

.. automethod:: abjad.tools.selectiontools.Selection.Selection.__hash__

.. automethod:: abjad.tools.selectiontools.Selection.Selection.__illustrate__

.. automethod:: abjad.tools.selectiontools.Selection.Selection.__len__

.. automethod:: abjad.tools.selectiontools.Selection.Selection.__ne__

.. automethod:: abjad.tools.selectiontools.Selection.Selection.__radd__

.. automethod:: abjad.tools.selectiontools.Selection.Selection.__repr__
