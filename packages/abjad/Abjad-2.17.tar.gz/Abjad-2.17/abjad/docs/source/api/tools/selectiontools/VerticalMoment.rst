.. currentmodule:: abjad.tools.selectiontools

VerticalMoment
==============

.. autoclass:: VerticalMoment

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
              "abjad.tools.selectiontools.Selection.Selection" [color=2,
                  group=1,
                  label=Selection,
                  shape=box];
              "abjad.tools.selectiontools.VerticalMoment.VerticalMoment" [color=black,
                  fontcolor=white,
                  group=1,
                  label=<<B>VerticalMoment</B>>,
                  shape=box,
                  style="filled, rounded"];
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

- :py:class:`abjad.tools.selectiontools.Selection`

- :py:class:`builtins.object`

.. only:: html

   Attribute summary
   -----------------

   .. autosummary::

      ~abjad.tools.selectiontools.VerticalMoment.VerticalMoment.attack_count
      ~abjad.tools.selectiontools.VerticalMoment.VerticalMoment.components
      ~abjad.tools.selectiontools.VerticalMoment.VerticalMoment.get_duration
      ~abjad.tools.selectiontools.VerticalMoment.VerticalMoment.get_spanners
      ~abjad.tools.selectiontools.VerticalMoment.VerticalMoment.get_timespan
      ~abjad.tools.selectiontools.VerticalMoment.VerticalMoment.get_vertical_moment_at
      ~abjad.tools.selectiontools.VerticalMoment.VerticalMoment.governors
      ~abjad.tools.selectiontools.VerticalMoment.VerticalMoment.group_by
      ~abjad.tools.selectiontools.VerticalMoment.VerticalMoment.leaves
      ~abjad.tools.selectiontools.VerticalMoment.VerticalMoment.measures
      ~abjad.tools.selectiontools.VerticalMoment.VerticalMoment.music
      ~abjad.tools.selectiontools.VerticalMoment.VerticalMoment.next_vertical_moment
      ~abjad.tools.selectiontools.VerticalMoment.VerticalMoment.notes
      ~abjad.tools.selectiontools.VerticalMoment.VerticalMoment.notes_and_chords
      ~abjad.tools.selectiontools.VerticalMoment.VerticalMoment.offset
      ~abjad.tools.selectiontools.VerticalMoment.VerticalMoment.overlap_components
      ~abjad.tools.selectiontools.VerticalMoment.VerticalMoment.overlap_leaves
      ~abjad.tools.selectiontools.VerticalMoment.VerticalMoment.overlap_measures
      ~abjad.tools.selectiontools.VerticalMoment.VerticalMoment.overlap_notes
      ~abjad.tools.selectiontools.VerticalMoment.VerticalMoment.partition_by_durations
      ~abjad.tools.selectiontools.VerticalMoment.VerticalMoment.previous_vertical_moment
      ~abjad.tools.selectiontools.VerticalMoment.VerticalMoment.start_components
      ~abjad.tools.selectiontools.VerticalMoment.VerticalMoment.start_leaves
      ~abjad.tools.selectiontools.VerticalMoment.VerticalMoment.start_notes
      ~abjad.tools.selectiontools.VerticalMoment.VerticalMoment.__add__
      ~abjad.tools.selectiontools.VerticalMoment.VerticalMoment.__contains__
      ~abjad.tools.selectiontools.VerticalMoment.VerticalMoment.__eq__
      ~abjad.tools.selectiontools.VerticalMoment.VerticalMoment.__format__
      ~abjad.tools.selectiontools.VerticalMoment.VerticalMoment.__getitem__
      ~abjad.tools.selectiontools.VerticalMoment.VerticalMoment.__hash__
      ~abjad.tools.selectiontools.VerticalMoment.VerticalMoment.__illustrate__
      ~abjad.tools.selectiontools.VerticalMoment.VerticalMoment.__len__
      ~abjad.tools.selectiontools.VerticalMoment.VerticalMoment.__ne__
      ~abjad.tools.selectiontools.VerticalMoment.VerticalMoment.__radd__
      ~abjad.tools.selectiontools.VerticalMoment.VerticalMoment.__repr__

Read-only properties
--------------------

.. autoattribute:: abjad.tools.selectiontools.VerticalMoment.VerticalMoment.attack_count

.. autoattribute:: abjad.tools.selectiontools.VerticalMoment.VerticalMoment.components

.. autoattribute:: abjad.tools.selectiontools.VerticalMoment.VerticalMoment.governors

.. autoattribute:: abjad.tools.selectiontools.VerticalMoment.VerticalMoment.leaves

.. autoattribute:: abjad.tools.selectiontools.VerticalMoment.VerticalMoment.measures

.. autoattribute:: abjad.tools.selectiontools.VerticalMoment.VerticalMoment.music

.. autoattribute:: abjad.tools.selectiontools.VerticalMoment.VerticalMoment.next_vertical_moment

.. autoattribute:: abjad.tools.selectiontools.VerticalMoment.VerticalMoment.notes

.. autoattribute:: abjad.tools.selectiontools.VerticalMoment.VerticalMoment.notes_and_chords

.. autoattribute:: abjad.tools.selectiontools.VerticalMoment.VerticalMoment.offset

.. autoattribute:: abjad.tools.selectiontools.VerticalMoment.VerticalMoment.overlap_components

.. autoattribute:: abjad.tools.selectiontools.VerticalMoment.VerticalMoment.overlap_leaves

.. autoattribute:: abjad.tools.selectiontools.VerticalMoment.VerticalMoment.overlap_measures

.. autoattribute:: abjad.tools.selectiontools.VerticalMoment.VerticalMoment.overlap_notes

.. autoattribute:: abjad.tools.selectiontools.VerticalMoment.VerticalMoment.previous_vertical_moment

.. autoattribute:: abjad.tools.selectiontools.VerticalMoment.VerticalMoment.start_components

.. autoattribute:: abjad.tools.selectiontools.VerticalMoment.VerticalMoment.start_leaves

.. autoattribute:: abjad.tools.selectiontools.VerticalMoment.VerticalMoment.start_notes

Methods
-------

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.selectiontools.VerticalMoment.VerticalMoment.get_duration

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.selectiontools.VerticalMoment.VerticalMoment.get_spanners

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.selectiontools.VerticalMoment.VerticalMoment.get_timespan

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.selectiontools.VerticalMoment.VerticalMoment.get_vertical_moment_at

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.selectiontools.VerticalMoment.VerticalMoment.group_by

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.selectiontools.VerticalMoment.VerticalMoment.partition_by_durations

Special methods
---------------

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.selectiontools.VerticalMoment.VerticalMoment.__add__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.selectiontools.VerticalMoment.VerticalMoment.__contains__

.. automethod:: abjad.tools.selectiontools.VerticalMoment.VerticalMoment.__eq__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.selectiontools.VerticalMoment.VerticalMoment.__format__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.selectiontools.VerticalMoment.VerticalMoment.__getitem__

.. automethod:: abjad.tools.selectiontools.VerticalMoment.VerticalMoment.__hash__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.selectiontools.VerticalMoment.VerticalMoment.__illustrate__

.. automethod:: abjad.tools.selectiontools.VerticalMoment.VerticalMoment.__len__

.. automethod:: abjad.tools.selectiontools.VerticalMoment.VerticalMoment.__ne__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.selectiontools.VerticalMoment.VerticalMoment.__radd__

.. automethod:: abjad.tools.selectiontools.VerticalMoment.VerticalMoment.__repr__
