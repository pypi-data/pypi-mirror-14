.. currentmodule:: abjad.tools.selectiontools

Parentage
=========

.. autoclass:: Parentage

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
              "abjad.tools.selectiontools.Parentage.Parentage" [color=black,
                  fontcolor=white,
                  group=1,
                  label=<<B>Parentage</B>>,
                  shape=box,
                  style="filled, rounded"];
              "abjad.tools.selectiontools.Selection.Selection" [color=2,
                  group=1,
                  label=Selection,
                  shape=box];
              "abjad.tools.selectiontools.Selection.Selection" -> "abjad.tools.selectiontools.Parentage.Parentage";
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

      ~abjad.tools.selectiontools.Parentage.Parentage.component
      ~abjad.tools.selectiontools.Parentage.Parentage.depth
      ~abjad.tools.selectiontools.Parentage.Parentage.get_duration
      ~abjad.tools.selectiontools.Parentage.Parentage.get_first
      ~abjad.tools.selectiontools.Parentage.Parentage.get_spanners
      ~abjad.tools.selectiontools.Parentage.Parentage.get_timespan
      ~abjad.tools.selectiontools.Parentage.Parentage.get_vertical_moment_at
      ~abjad.tools.selectiontools.Parentage.Parentage.group_by
      ~abjad.tools.selectiontools.Parentage.Parentage.is_orphan
      ~abjad.tools.selectiontools.Parentage.Parentage.logical_voice
      ~abjad.tools.selectiontools.Parentage.Parentage.parent
      ~abjad.tools.selectiontools.Parentage.Parentage.partition_by_durations
      ~abjad.tools.selectiontools.Parentage.Parentage.prolation
      ~abjad.tools.selectiontools.Parentage.Parentage.root
      ~abjad.tools.selectiontools.Parentage.Parentage.score_index
      ~abjad.tools.selectiontools.Parentage.Parentage.tuplet_depth
      ~abjad.tools.selectiontools.Parentage.Parentage.__add__
      ~abjad.tools.selectiontools.Parentage.Parentage.__contains__
      ~abjad.tools.selectiontools.Parentage.Parentage.__eq__
      ~abjad.tools.selectiontools.Parentage.Parentage.__format__
      ~abjad.tools.selectiontools.Parentage.Parentage.__getitem__
      ~abjad.tools.selectiontools.Parentage.Parentage.__hash__
      ~abjad.tools.selectiontools.Parentage.Parentage.__illustrate__
      ~abjad.tools.selectiontools.Parentage.Parentage.__len__
      ~abjad.tools.selectiontools.Parentage.Parentage.__ne__
      ~abjad.tools.selectiontools.Parentage.Parentage.__radd__
      ~abjad.tools.selectiontools.Parentage.Parentage.__repr__

Read-only properties
--------------------

.. autoattribute:: abjad.tools.selectiontools.Parentage.Parentage.component

.. autoattribute:: abjad.tools.selectiontools.Parentage.Parentage.depth

.. autoattribute:: abjad.tools.selectiontools.Parentage.Parentage.is_orphan

.. autoattribute:: abjad.tools.selectiontools.Parentage.Parentage.logical_voice

.. autoattribute:: abjad.tools.selectiontools.Parentage.Parentage.parent

.. autoattribute:: abjad.tools.selectiontools.Parentage.Parentage.prolation

.. autoattribute:: abjad.tools.selectiontools.Parentage.Parentage.root

.. autoattribute:: abjad.tools.selectiontools.Parentage.Parentage.score_index

.. autoattribute:: abjad.tools.selectiontools.Parentage.Parentage.tuplet_depth

Methods
-------

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.selectiontools.Parentage.Parentage.get_duration

.. automethod:: abjad.tools.selectiontools.Parentage.Parentage.get_first

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.selectiontools.Parentage.Parentage.get_spanners

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.selectiontools.Parentage.Parentage.get_timespan

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.selectiontools.Parentage.Parentage.get_vertical_moment_at

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.selectiontools.Parentage.Parentage.group_by

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.selectiontools.Parentage.Parentage.partition_by_durations

Special methods
---------------

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.selectiontools.Parentage.Parentage.__add__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.selectiontools.Parentage.Parentage.__contains__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.selectiontools.Parentage.Parentage.__eq__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.selectiontools.Parentage.Parentage.__format__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.selectiontools.Parentage.Parentage.__getitem__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.selectiontools.Parentage.Parentage.__hash__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.selectiontools.Parentage.Parentage.__illustrate__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.selectiontools.Parentage.Parentage.__len__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.selectiontools.Parentage.Parentage.__ne__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.selectiontools.Parentage.Parentage.__radd__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.selectiontools.Parentage.Parentage.__repr__
