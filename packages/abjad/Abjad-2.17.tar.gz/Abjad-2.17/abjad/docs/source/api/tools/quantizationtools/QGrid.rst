.. currentmodule:: abjad.tools.quantizationtools

QGrid
=====

.. autoclass:: QGrid

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
          subgraph cluster_quantizationtools {
              graph [label=quantizationtools];
              "abjad.tools.quantizationtools.QGrid.QGrid" [color=black,
                  fontcolor=white,
                  group=2,
                  label=<<B>QGrid</B>>,
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
          "abjad.tools.abctools.AbjadObject.AbjadObject" -> "abjad.tools.quantizationtools.QGrid.QGrid";
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

      ~abjad.tools.quantizationtools.QGrid.QGrid.distance
      ~abjad.tools.quantizationtools.QGrid.QGrid.fit_q_events
      ~abjad.tools.quantizationtools.QGrid.QGrid.leaves
      ~abjad.tools.quantizationtools.QGrid.QGrid.next_downbeat
      ~abjad.tools.quantizationtools.QGrid.QGrid.offsets
      ~abjad.tools.quantizationtools.QGrid.QGrid.pretty_rtm_format
      ~abjad.tools.quantizationtools.QGrid.QGrid.root_node
      ~abjad.tools.quantizationtools.QGrid.QGrid.rtm_format
      ~abjad.tools.quantizationtools.QGrid.QGrid.sort_q_events_by_index
      ~abjad.tools.quantizationtools.QGrid.QGrid.subdivide_leaf
      ~abjad.tools.quantizationtools.QGrid.QGrid.subdivide_leaves
      ~abjad.tools.quantizationtools.QGrid.QGrid.__call__
      ~abjad.tools.quantizationtools.QGrid.QGrid.__copy__
      ~abjad.tools.quantizationtools.QGrid.QGrid.__eq__
      ~abjad.tools.quantizationtools.QGrid.QGrid.__format__
      ~abjad.tools.quantizationtools.QGrid.QGrid.__hash__
      ~abjad.tools.quantizationtools.QGrid.QGrid.__ne__
      ~abjad.tools.quantizationtools.QGrid.QGrid.__repr__

Read-only properties
--------------------

.. autoattribute:: abjad.tools.quantizationtools.QGrid.QGrid.distance

.. autoattribute:: abjad.tools.quantizationtools.QGrid.QGrid.leaves

.. autoattribute:: abjad.tools.quantizationtools.QGrid.QGrid.next_downbeat

.. autoattribute:: abjad.tools.quantizationtools.QGrid.QGrid.offsets

.. autoattribute:: abjad.tools.quantizationtools.QGrid.QGrid.pretty_rtm_format

.. autoattribute:: abjad.tools.quantizationtools.QGrid.QGrid.root_node

.. autoattribute:: abjad.tools.quantizationtools.QGrid.QGrid.rtm_format

Methods
-------

.. automethod:: abjad.tools.quantizationtools.QGrid.QGrid.fit_q_events

.. automethod:: abjad.tools.quantizationtools.QGrid.QGrid.sort_q_events_by_index

.. automethod:: abjad.tools.quantizationtools.QGrid.QGrid.subdivide_leaf

.. automethod:: abjad.tools.quantizationtools.QGrid.QGrid.subdivide_leaves

Special methods
---------------

.. automethod:: abjad.tools.quantizationtools.QGrid.QGrid.__call__

.. automethod:: abjad.tools.quantizationtools.QGrid.QGrid.__copy__

.. automethod:: abjad.tools.quantizationtools.QGrid.QGrid.__eq__

.. automethod:: abjad.tools.quantizationtools.QGrid.QGrid.__format__

.. automethod:: abjad.tools.quantizationtools.QGrid.QGrid.__hash__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.quantizationtools.QGrid.QGrid.__ne__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.quantizationtools.QGrid.QGrid.__repr__
