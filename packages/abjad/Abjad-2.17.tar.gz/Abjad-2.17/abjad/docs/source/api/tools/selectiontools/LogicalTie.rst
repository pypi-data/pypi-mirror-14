.. currentmodule:: abjad.tools.selectiontools

LogicalTie
==========

.. autoclass:: LogicalTie

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
              "abjad.tools.selectiontools.LogicalTie.LogicalTie" [color=black,
                  fontcolor=white,
                  group=1,
                  label=<<B>LogicalTie</B>>,
                  shape=box,
                  style="filled, rounded"];
              "abjad.tools.selectiontools.Selection.Selection" [color=2,
                  group=1,
                  label=Selection,
                  shape=box];
              "abjad.tools.selectiontools.Selection.Selection" -> "abjad.tools.selectiontools.LogicalTie.LogicalTie";
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

- :py:class:`abjad.tools.selectiontools.Selection`

- :py:class:`builtins.object`

.. only:: html

   Attribute summary
   -----------------

   .. autosummary::

      ~abjad.tools.selectiontools.LogicalTie.LogicalTie.all_leaves_are_in_same_parent
      ~abjad.tools.selectiontools.LogicalTie.LogicalTie.get_duration
      ~abjad.tools.selectiontools.LogicalTie.LogicalTie.get_spanners
      ~abjad.tools.selectiontools.LogicalTie.LogicalTie.get_timespan
      ~abjad.tools.selectiontools.LogicalTie.LogicalTie.get_vertical_moment_at
      ~abjad.tools.selectiontools.LogicalTie.LogicalTie.group_by
      ~abjad.tools.selectiontools.LogicalTie.LogicalTie.head
      ~abjad.tools.selectiontools.LogicalTie.LogicalTie.is_pitched
      ~abjad.tools.selectiontools.LogicalTie.LogicalTie.is_trivial
      ~abjad.tools.selectiontools.LogicalTie.LogicalTie.leaves
      ~abjad.tools.selectiontools.LogicalTie.LogicalTie.leaves_grouped_by_immediate_parents
      ~abjad.tools.selectiontools.LogicalTie.LogicalTie.partition_by_durations
      ~abjad.tools.selectiontools.LogicalTie.LogicalTie.tail
      ~abjad.tools.selectiontools.LogicalTie.LogicalTie.tie_spanner
      ~abjad.tools.selectiontools.LogicalTie.LogicalTie.to_tuplet
      ~abjad.tools.selectiontools.LogicalTie.LogicalTie.written_duration
      ~abjad.tools.selectiontools.LogicalTie.LogicalTie.__add__
      ~abjad.tools.selectiontools.LogicalTie.LogicalTie.__contains__
      ~abjad.tools.selectiontools.LogicalTie.LogicalTie.__eq__
      ~abjad.tools.selectiontools.LogicalTie.LogicalTie.__format__
      ~abjad.tools.selectiontools.LogicalTie.LogicalTie.__getitem__
      ~abjad.tools.selectiontools.LogicalTie.LogicalTie.__hash__
      ~abjad.tools.selectiontools.LogicalTie.LogicalTie.__illustrate__
      ~abjad.tools.selectiontools.LogicalTie.LogicalTie.__len__
      ~abjad.tools.selectiontools.LogicalTie.LogicalTie.__ne__
      ~abjad.tools.selectiontools.LogicalTie.LogicalTie.__radd__
      ~abjad.tools.selectiontools.LogicalTie.LogicalTie.__repr__

Read-only properties
--------------------

.. autoattribute:: abjad.tools.selectiontools.LogicalTie.LogicalTie.all_leaves_are_in_same_parent

.. autoattribute:: abjad.tools.selectiontools.LogicalTie.LogicalTie.head

.. autoattribute:: abjad.tools.selectiontools.LogicalTie.LogicalTie.is_pitched

.. autoattribute:: abjad.tools.selectiontools.LogicalTie.LogicalTie.is_trivial

.. autoattribute:: abjad.tools.selectiontools.LogicalTie.LogicalTie.leaves

.. autoattribute:: abjad.tools.selectiontools.LogicalTie.LogicalTie.leaves_grouped_by_immediate_parents

.. autoattribute:: abjad.tools.selectiontools.LogicalTie.LogicalTie.tail

.. autoattribute:: abjad.tools.selectiontools.LogicalTie.LogicalTie.tie_spanner

.. autoattribute:: abjad.tools.selectiontools.LogicalTie.LogicalTie.written_duration

Methods
-------

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.selectiontools.LogicalTie.LogicalTie.get_duration

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.selectiontools.LogicalTie.LogicalTie.get_spanners

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.selectiontools.LogicalTie.LogicalTie.get_timespan

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.selectiontools.LogicalTie.LogicalTie.get_vertical_moment_at

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.selectiontools.LogicalTie.LogicalTie.group_by

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.selectiontools.LogicalTie.LogicalTie.partition_by_durations

.. automethod:: abjad.tools.selectiontools.LogicalTie.LogicalTie.to_tuplet

Special methods
---------------

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.selectiontools.LogicalTie.LogicalTie.__add__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.selectiontools.LogicalTie.LogicalTie.__contains__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.selectiontools.LogicalTie.LogicalTie.__eq__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.selectiontools.LogicalTie.LogicalTie.__format__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.selectiontools.LogicalTie.LogicalTie.__getitem__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.selectiontools.LogicalTie.LogicalTie.__hash__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.selectiontools.LogicalTie.LogicalTie.__illustrate__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.selectiontools.LogicalTie.LogicalTie.__len__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.selectiontools.LogicalTie.LogicalTie.__ne__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.selectiontools.LogicalTie.LogicalTie.__radd__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.selectiontools.LogicalTie.LogicalTie.__repr__
