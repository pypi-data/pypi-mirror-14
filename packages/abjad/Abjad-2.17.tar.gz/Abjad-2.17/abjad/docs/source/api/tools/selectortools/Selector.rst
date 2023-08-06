.. currentmodule:: abjad.tools.selectortools

Selector
========

.. autoclass:: Selector

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
              "abjad.tools.abctools.AbjadValueObject.AbjadValueObject" [color=1,
                  group=0,
                  label=AbjadValueObject,
                  shape=box];
              "abjad.tools.abctools.AbjadObject.AbjadObject" -> "abjad.tools.abctools.AbjadValueObject.AbjadValueObject";
              "abjad.tools.abctools.AbjadObject.AbstractBase" -> "abjad.tools.abctools.AbjadObject.AbjadObject";
          }
          subgraph cluster_selectortools {
              graph [label=selectortools];
              "abjad.tools.selectortools.Selector.Selector" [color=black,
                  fontcolor=white,
                  group=2,
                  label=<<B>Selector</B>>,
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
          "abjad.tools.abctools.AbjadValueObject.AbjadValueObject" -> "abjad.tools.selectortools.Selector.Selector";
          "builtins.object" -> "abjad.tools.abctools.AbjadObject.AbstractBase";
      }

Bases
-----

- :py:class:`abjad.tools.abctools.AbjadValueObject`

- :py:class:`abjad.tools.abctools.AbjadObject`

- :py:class:`abjad.tools.abctools.AbjadObject.AbstractBase`

- :py:class:`builtins.object`

.. only:: html

   Attribute summary
   -----------------

   .. autosummary::

      ~abjad.tools.selectortools.Selector.Selector.append_callback
      ~abjad.tools.selectortools.Selector.Selector.by_class
      ~abjad.tools.selectortools.Selector.Selector.by_contiguity
      ~abjad.tools.selectortools.Selector.Selector.by_counts
      ~abjad.tools.selectortools.Selector.Selector.by_duration
      ~abjad.tools.selectortools.Selector.Selector.by_leaves
      ~abjad.tools.selectortools.Selector.Selector.by_length
      ~abjad.tools.selectortools.Selector.Selector.by_logical_measure
      ~abjad.tools.selectortools.Selector.Selector.by_logical_tie
      ~abjad.tools.selectortools.Selector.Selector.by_pattern
      ~abjad.tools.selectortools.Selector.Selector.by_pitch
      ~abjad.tools.selectortools.Selector.Selector.by_run
      ~abjad.tools.selectortools.Selector.Selector.callbacks
      ~abjad.tools.selectortools.Selector.Selector.first
      ~abjad.tools.selectortools.Selector.Selector.flatten
      ~abjad.tools.selectortools.Selector.Selector.get_item
      ~abjad.tools.selectortools.Selector.Selector.get_slice
      ~abjad.tools.selectortools.Selector.Selector.last
      ~abjad.tools.selectortools.Selector.Selector.middle
      ~abjad.tools.selectortools.Selector.Selector.most
      ~abjad.tools.selectortools.Selector.Selector.partition_by_ratio
      ~abjad.tools.selectortools.Selector.Selector.rest
      ~abjad.tools.selectortools.Selector.Selector.run_selectors
      ~abjad.tools.selectortools.Selector.Selector.with_next_leaf
      ~abjad.tools.selectortools.Selector.Selector.with_previous_leaf
      ~abjad.tools.selectortools.Selector.Selector.__call__
      ~abjad.tools.selectortools.Selector.Selector.__copy__
      ~abjad.tools.selectortools.Selector.Selector.__eq__
      ~abjad.tools.selectortools.Selector.Selector.__format__
      ~abjad.tools.selectortools.Selector.Selector.__getitem__
      ~abjad.tools.selectortools.Selector.Selector.__hash__
      ~abjad.tools.selectortools.Selector.Selector.__ne__
      ~abjad.tools.selectortools.Selector.Selector.__repr__

Read-only properties
--------------------

.. autoattribute:: abjad.tools.selectortools.Selector.Selector.callbacks

Methods
-------

.. automethod:: abjad.tools.selectortools.Selector.Selector.append_callback

.. automethod:: abjad.tools.selectortools.Selector.Selector.by_class

.. automethod:: abjad.tools.selectortools.Selector.Selector.by_contiguity

.. automethod:: abjad.tools.selectortools.Selector.Selector.by_counts

.. automethod:: abjad.tools.selectortools.Selector.Selector.by_duration

.. automethod:: abjad.tools.selectortools.Selector.Selector.by_leaves

.. automethod:: abjad.tools.selectortools.Selector.Selector.by_length

.. automethod:: abjad.tools.selectortools.Selector.Selector.by_logical_measure

.. automethod:: abjad.tools.selectortools.Selector.Selector.by_logical_tie

.. automethod:: abjad.tools.selectortools.Selector.Selector.by_pattern

.. automethod:: abjad.tools.selectortools.Selector.Selector.by_pitch

.. automethod:: abjad.tools.selectortools.Selector.Selector.by_run

.. automethod:: abjad.tools.selectortools.Selector.Selector.first

.. automethod:: abjad.tools.selectortools.Selector.Selector.flatten

.. automethod:: abjad.tools.selectortools.Selector.Selector.get_item

.. automethod:: abjad.tools.selectortools.Selector.Selector.get_slice

.. automethod:: abjad.tools.selectortools.Selector.Selector.last

.. automethod:: abjad.tools.selectortools.Selector.Selector.middle

.. automethod:: abjad.tools.selectortools.Selector.Selector.most

.. automethod:: abjad.tools.selectortools.Selector.Selector.partition_by_ratio

.. automethod:: abjad.tools.selectortools.Selector.Selector.rest

.. automethod:: abjad.tools.selectortools.Selector.Selector.with_next_leaf

.. automethod:: abjad.tools.selectortools.Selector.Selector.with_previous_leaf

Class & static methods
----------------------

.. automethod:: abjad.tools.selectortools.Selector.Selector.run_selectors

Special methods
---------------

.. automethod:: abjad.tools.selectortools.Selector.Selector.__call__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.selectortools.Selector.Selector.__copy__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.selectortools.Selector.Selector.__eq__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.selectortools.Selector.Selector.__format__

.. automethod:: abjad.tools.selectortools.Selector.Selector.__getitem__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.selectortools.Selector.Selector.__hash__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.selectortools.Selector.Selector.__ne__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.selectortools.Selector.Selector.__repr__
