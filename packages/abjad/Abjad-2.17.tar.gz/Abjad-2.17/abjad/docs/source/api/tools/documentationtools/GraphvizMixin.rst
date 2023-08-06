.. currentmodule:: abjad.tools.documentationtools

GraphvizMixin
=============

.. autoclass:: GraphvizMixin

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
          subgraph cluster_documentationtools {
              graph [label=documentationtools];
              "abjad.tools.documentationtools.GraphvizEdge.GraphvizEdge" [color=3,
                  group=2,
                  label=GraphvizEdge,
                  shape=box];
              "abjad.tools.documentationtools.GraphvizGraph.GraphvizGraph" [color=3,
                  group=2,
                  label=GraphvizGraph,
                  shape=box];
              "abjad.tools.documentationtools.GraphvizMixin.GraphvizMixin" [color=black,
                  fontcolor=white,
                  group=2,
                  label=<<B>GraphvizMixin</B>>,
                  shape=oval,
                  style="filled, rounded"];
              "abjad.tools.documentationtools.GraphvizNode.GraphvizNode" [color=3,
                  group=2,
                  label=GraphvizNode,
                  shape=box];
              "abjad.tools.documentationtools.GraphvizSubgraph.GraphvizSubgraph" [color=3,
                  group=2,
                  label=GraphvizSubgraph,
                  shape=box];
              "abjad.tools.documentationtools.GraphvizGraph.GraphvizGraph" -> "abjad.tools.documentationtools.GraphvizSubgraph.GraphvizSubgraph";
              "abjad.tools.documentationtools.GraphvizMixin.GraphvizMixin" -> "abjad.tools.documentationtools.GraphvizEdge.GraphvizEdge";
              "abjad.tools.documentationtools.GraphvizMixin.GraphvizMixin" -> "abjad.tools.documentationtools.GraphvizGraph.GraphvizGraph";
              "abjad.tools.documentationtools.GraphvizMixin.GraphvizMixin" -> "abjad.tools.documentationtools.GraphvizNode.GraphvizNode";
          }
          subgraph cluster_builtins {
              graph [label=builtins];
              "builtins.object" [color=2,
                  group=1,
                  label=object,
                  shape=box];
          }
          "abjad.tools.abctools.AbjadObject.AbjadObject" -> "abjad.tools.documentationtools.GraphvizMixin.GraphvizMixin";
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

      ~abjad.tools.documentationtools.GraphvizMixin.GraphvizMixin.attributes
      ~abjad.tools.documentationtools.GraphvizMixin.GraphvizMixin.__eq__
      ~abjad.tools.documentationtools.GraphvizMixin.GraphvizMixin.__format__
      ~abjad.tools.documentationtools.GraphvizMixin.GraphvizMixin.__hash__
      ~abjad.tools.documentationtools.GraphvizMixin.GraphvizMixin.__ne__
      ~abjad.tools.documentationtools.GraphvizMixin.GraphvizMixin.__repr__

Read-only properties
--------------------

.. autoattribute:: abjad.tools.documentationtools.GraphvizMixin.GraphvizMixin.attributes

Special methods
---------------

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.documentationtools.GraphvizMixin.GraphvizMixin.__eq__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.documentationtools.GraphvizMixin.GraphvizMixin.__format__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.documentationtools.GraphvizMixin.GraphvizMixin.__hash__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.documentationtools.GraphvizMixin.GraphvizMixin.__ne__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.documentationtools.GraphvizMixin.GraphvizMixin.__repr__
