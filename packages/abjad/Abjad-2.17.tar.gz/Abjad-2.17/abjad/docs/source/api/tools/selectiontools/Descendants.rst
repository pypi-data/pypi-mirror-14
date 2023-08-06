.. currentmodule:: abjad.tools.selectiontools

Descendants
===========

.. autoclass:: Descendants

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
              "abjad.tools.selectiontools.Descendants.Descendants" [color=black,
                  fontcolor=white,
                  group=1,
                  label=<<B>Descendants</B>>,
                  shape=box,
                  style="filled, rounded"];
              "abjad.tools.selectiontools.Selection.Selection" [color=2,
                  group=1,
                  label=Selection,
                  shape=box];
              "abjad.tools.selectiontools.Selection.Selection" -> "abjad.tools.selectiontools.Descendants.Descendants";
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

      ~abjad.tools.selectiontools.Descendants.Descendants.component
      ~abjad.tools.selectiontools.Descendants.Descendants.get_duration
      ~abjad.tools.selectiontools.Descendants.Descendants.get_spanners
      ~abjad.tools.selectiontools.Descendants.Descendants.get_timespan
      ~abjad.tools.selectiontools.Descendants.Descendants.get_vertical_moment_at
      ~abjad.tools.selectiontools.Descendants.Descendants.group_by
      ~abjad.tools.selectiontools.Descendants.Descendants.partition_by_durations
      ~abjad.tools.selectiontools.Descendants.Descendants.__add__
      ~abjad.tools.selectiontools.Descendants.Descendants.__contains__
      ~abjad.tools.selectiontools.Descendants.Descendants.__eq__
      ~abjad.tools.selectiontools.Descendants.Descendants.__format__
      ~abjad.tools.selectiontools.Descendants.Descendants.__getitem__
      ~abjad.tools.selectiontools.Descendants.Descendants.__hash__
      ~abjad.tools.selectiontools.Descendants.Descendants.__illustrate__
      ~abjad.tools.selectiontools.Descendants.Descendants.__len__
      ~abjad.tools.selectiontools.Descendants.Descendants.__ne__
      ~abjad.tools.selectiontools.Descendants.Descendants.__radd__
      ~abjad.tools.selectiontools.Descendants.Descendants.__repr__

Read-only properties
--------------------

.. autoattribute:: abjad.tools.selectiontools.Descendants.Descendants.component

Methods
-------

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.selectiontools.Descendants.Descendants.get_duration

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.selectiontools.Descendants.Descendants.get_spanners

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.selectiontools.Descendants.Descendants.get_timespan

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.selectiontools.Descendants.Descendants.get_vertical_moment_at

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.selectiontools.Descendants.Descendants.group_by

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.selectiontools.Descendants.Descendants.partition_by_durations

Special methods
---------------

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.selectiontools.Descendants.Descendants.__add__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.selectiontools.Descendants.Descendants.__contains__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.selectiontools.Descendants.Descendants.__eq__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.selectiontools.Descendants.Descendants.__format__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.selectiontools.Descendants.Descendants.__getitem__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.selectiontools.Descendants.Descendants.__hash__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.selectiontools.Descendants.Descendants.__illustrate__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.selectiontools.Descendants.Descendants.__len__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.selectiontools.Descendants.Descendants.__ne__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.selectiontools.Descendants.Descendants.__radd__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.selectiontools.Descendants.Descendants.__repr__
