.. currentmodule:: abjad.tools.selectiontools

Lineage
=======

.. autoclass:: Lineage

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
              "abjad.tools.selectiontools.Lineage.Lineage" [color=black,
                  fontcolor=white,
                  group=1,
                  label=<<B>Lineage</B>>,
                  shape=box,
                  style="filled, rounded"];
              "abjad.tools.selectiontools.Selection.Selection" [color=2,
                  group=1,
                  label=Selection,
                  shape=box];
              "abjad.tools.selectiontools.Selection.Selection" -> "abjad.tools.selectiontools.Lineage.Lineage";
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

      ~abjad.tools.selectiontools.Lineage.Lineage.component
      ~abjad.tools.selectiontools.Lineage.Lineage.get_duration
      ~abjad.tools.selectiontools.Lineage.Lineage.get_spanners
      ~abjad.tools.selectiontools.Lineage.Lineage.get_timespan
      ~abjad.tools.selectiontools.Lineage.Lineage.get_vertical_moment_at
      ~abjad.tools.selectiontools.Lineage.Lineage.group_by
      ~abjad.tools.selectiontools.Lineage.Lineage.partition_by_durations
      ~abjad.tools.selectiontools.Lineage.Lineage.__add__
      ~abjad.tools.selectiontools.Lineage.Lineage.__contains__
      ~abjad.tools.selectiontools.Lineage.Lineage.__eq__
      ~abjad.tools.selectiontools.Lineage.Lineage.__format__
      ~abjad.tools.selectiontools.Lineage.Lineage.__getitem__
      ~abjad.tools.selectiontools.Lineage.Lineage.__hash__
      ~abjad.tools.selectiontools.Lineage.Lineage.__illustrate__
      ~abjad.tools.selectiontools.Lineage.Lineage.__len__
      ~abjad.tools.selectiontools.Lineage.Lineage.__ne__
      ~abjad.tools.selectiontools.Lineage.Lineage.__radd__
      ~abjad.tools.selectiontools.Lineage.Lineage.__repr__

Read-only properties
--------------------

.. autoattribute:: abjad.tools.selectiontools.Lineage.Lineage.component

Methods
-------

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.selectiontools.Lineage.Lineage.get_duration

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.selectiontools.Lineage.Lineage.get_spanners

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.selectiontools.Lineage.Lineage.get_timespan

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.selectiontools.Lineage.Lineage.get_vertical_moment_at

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.selectiontools.Lineage.Lineage.group_by

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.selectiontools.Lineage.Lineage.partition_by_durations

Special methods
---------------

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.selectiontools.Lineage.Lineage.__add__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.selectiontools.Lineage.Lineage.__contains__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.selectiontools.Lineage.Lineage.__eq__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.selectiontools.Lineage.Lineage.__format__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.selectiontools.Lineage.Lineage.__getitem__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.selectiontools.Lineage.Lineage.__hash__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.selectiontools.Lineage.Lineage.__illustrate__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.selectiontools.Lineage.Lineage.__len__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.selectiontools.Lineage.Lineage.__ne__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.selectiontools.Lineage.Lineage.__radd__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.selectiontools.Lineage.Lineage.__repr__
