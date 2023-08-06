.. currentmodule:: abjad.tools.documentationtools

GraphvizGraph
=============

.. autoclass:: GraphvizGraph

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
          subgraph cluster_datastructuretools {
              graph [label=datastructuretools];
              "abjad.tools.datastructuretools.TreeContainer.TreeContainer" [color=3,
                  group=2,
                  label=TreeContainer,
                  shape=box];
              "abjad.tools.datastructuretools.TreeNode.TreeNode" [color=3,
                  group=2,
                  label=TreeNode,
                  shape=box];
              "abjad.tools.datastructuretools.TreeNode.TreeNode" -> "abjad.tools.datastructuretools.TreeContainer.TreeContainer";
          }
          subgraph cluster_documentationtools {
              graph [label=documentationtools];
              "abjad.tools.documentationtools.GraphvizGraph.GraphvizGraph" [color=black,
                  fontcolor=white,
                  group=3,
                  label=<<B>GraphvizGraph</B>>,
                  shape=box,
                  style="filled, rounded"];
              "abjad.tools.documentationtools.GraphvizMixin.GraphvizMixin" [color=4,
                  group=3,
                  label=GraphvizMixin,
                  shape=oval,
                  style=bold];
              "abjad.tools.documentationtools.GraphvizSubgraph.GraphvizSubgraph" [color=4,
                  group=3,
                  label=GraphvizSubgraph,
                  shape=box];
              "abjad.tools.documentationtools.GraphvizGraph.GraphvizGraph" -> "abjad.tools.documentationtools.GraphvizSubgraph.GraphvizSubgraph";
              "abjad.tools.documentationtools.GraphvizMixin.GraphvizMixin" -> "abjad.tools.documentationtools.GraphvizGraph.GraphvizGraph";
          }
          subgraph cluster_builtins {
              graph [label=builtins];
              "builtins.object" [color=2,
                  group=1,
                  label=object,
                  shape=box];
          }
          "abjad.tools.abctools.AbjadObject.AbjadObject" -> "abjad.tools.datastructuretools.TreeNode.TreeNode";
          "abjad.tools.abctools.AbjadObject.AbjadObject" -> "abjad.tools.documentationtools.GraphvizMixin.GraphvizMixin";
          "abjad.tools.datastructuretools.TreeContainer.TreeContainer" -> "abjad.tools.documentationtools.GraphvizGraph.GraphvizGraph";
          "builtins.object" -> "abjad.tools.abctools.AbjadObject.AbstractBase";
      }

Bases
-----

- :py:class:`abjad.tools.documentationtools.GraphvizMixin`

- :py:class:`abjad.tools.datastructuretools.TreeContainer`

- :py:class:`abjad.tools.datastructuretools.TreeNode`

- :py:class:`abjad.tools.abctools.AbjadObject`

- :py:class:`abjad.tools.abctools.AbjadObject.AbstractBase`

- :py:class:`builtins.object`

.. only:: html

   Attribute summary
   -----------------

   .. autosummary::

      ~abjad.tools.documentationtools.GraphvizGraph.GraphvizGraph.append
      ~abjad.tools.documentationtools.GraphvizGraph.GraphvizGraph.attributes
      ~abjad.tools.documentationtools.GraphvizGraph.GraphvizGraph.canonical_name
      ~abjad.tools.documentationtools.GraphvizGraph.GraphvizGraph.children
      ~abjad.tools.documentationtools.GraphvizGraph.GraphvizGraph.depth
      ~abjad.tools.documentationtools.GraphvizGraph.GraphvizGraph.depthwise_inventory
      ~abjad.tools.documentationtools.GraphvizGraph.GraphvizGraph.edge_attributes
      ~abjad.tools.documentationtools.GraphvizGraph.GraphvizGraph.extend
      ~abjad.tools.documentationtools.GraphvizGraph.GraphvizGraph.graph_order
      ~abjad.tools.documentationtools.GraphvizGraph.GraphvizGraph.improper_parentage
      ~abjad.tools.documentationtools.GraphvizGraph.GraphvizGraph.index
      ~abjad.tools.documentationtools.GraphvizGraph.GraphvizGraph.insert
      ~abjad.tools.documentationtools.GraphvizGraph.GraphvizGraph.is_digraph
      ~abjad.tools.documentationtools.GraphvizGraph.GraphvizGraph.leaves
      ~abjad.tools.documentationtools.GraphvizGraph.GraphvizGraph.name
      ~abjad.tools.documentationtools.GraphvizGraph.GraphvizGraph.node_attributes
      ~abjad.tools.documentationtools.GraphvizGraph.GraphvizGraph.nodes
      ~abjad.tools.documentationtools.GraphvizGraph.GraphvizGraph.parent
      ~abjad.tools.documentationtools.GraphvizGraph.GraphvizGraph.pop
      ~abjad.tools.documentationtools.GraphvizGraph.GraphvizGraph.proper_parentage
      ~abjad.tools.documentationtools.GraphvizGraph.GraphvizGraph.remove
      ~abjad.tools.documentationtools.GraphvizGraph.GraphvizGraph.root
      ~abjad.tools.documentationtools.GraphvizGraph.GraphvizGraph.unflattened_graphviz_format
      ~abjad.tools.documentationtools.GraphvizGraph.GraphvizGraph.__contains__
      ~abjad.tools.documentationtools.GraphvizGraph.GraphvizGraph.__copy__
      ~abjad.tools.documentationtools.GraphvizGraph.GraphvizGraph.__delitem__
      ~abjad.tools.documentationtools.GraphvizGraph.GraphvizGraph.__eq__
      ~abjad.tools.documentationtools.GraphvizGraph.GraphvizGraph.__format__
      ~abjad.tools.documentationtools.GraphvizGraph.GraphvizGraph.__getitem__
      ~abjad.tools.documentationtools.GraphvizGraph.GraphvizGraph.__graph__
      ~abjad.tools.documentationtools.GraphvizGraph.GraphvizGraph.__hash__
      ~abjad.tools.documentationtools.GraphvizGraph.GraphvizGraph.__iter__
      ~abjad.tools.documentationtools.GraphvizGraph.GraphvizGraph.__len__
      ~abjad.tools.documentationtools.GraphvizGraph.GraphvizGraph.__ne__
      ~abjad.tools.documentationtools.GraphvizGraph.GraphvizGraph.__repr__
      ~abjad.tools.documentationtools.GraphvizGraph.GraphvizGraph.__setitem__
      ~abjad.tools.documentationtools.GraphvizGraph.GraphvizGraph.__str__

Read-only properties
--------------------

.. only:: html

   .. container:: inherited

      .. autoattribute:: abjad.tools.documentationtools.GraphvizGraph.GraphvizGraph.attributes

.. autoattribute:: abjad.tools.documentationtools.GraphvizGraph.GraphvizGraph.canonical_name

.. only:: html

   .. container:: inherited

      .. autoattribute:: abjad.tools.documentationtools.GraphvizGraph.GraphvizGraph.children

.. only:: html

   .. container:: inherited

      .. autoattribute:: abjad.tools.documentationtools.GraphvizGraph.GraphvizGraph.depth

.. only:: html

   .. container:: inherited

      .. autoattribute:: abjad.tools.documentationtools.GraphvizGraph.GraphvizGraph.depthwise_inventory

.. autoattribute:: abjad.tools.documentationtools.GraphvizGraph.GraphvizGraph.edge_attributes

.. only:: html

   .. container:: inherited

      .. autoattribute:: abjad.tools.documentationtools.GraphvizGraph.GraphvizGraph.graph_order

.. only:: html

   .. container:: inherited

      .. autoattribute:: abjad.tools.documentationtools.GraphvizGraph.GraphvizGraph.improper_parentage

.. only:: html

   .. container:: inherited

      .. autoattribute:: abjad.tools.documentationtools.GraphvizGraph.GraphvizGraph.leaves

.. autoattribute:: abjad.tools.documentationtools.GraphvizGraph.GraphvizGraph.node_attributes

.. only:: html

   .. container:: inherited

      .. autoattribute:: abjad.tools.documentationtools.GraphvizGraph.GraphvizGraph.nodes

.. only:: html

   .. container:: inherited

      .. autoattribute:: abjad.tools.documentationtools.GraphvizGraph.GraphvizGraph.parent

.. only:: html

   .. container:: inherited

      .. autoattribute:: abjad.tools.documentationtools.GraphvizGraph.GraphvizGraph.proper_parentage

.. only:: html

   .. container:: inherited

      .. autoattribute:: abjad.tools.documentationtools.GraphvizGraph.GraphvizGraph.root

.. autoattribute:: abjad.tools.documentationtools.GraphvizGraph.GraphvizGraph.unflattened_graphviz_format

Read/write properties
---------------------

.. autoattribute:: abjad.tools.documentationtools.GraphvizGraph.GraphvizGraph.is_digraph

.. only:: html

   .. container:: inherited

      .. autoattribute:: abjad.tools.documentationtools.GraphvizGraph.GraphvizGraph.name

Methods
-------

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.documentationtools.GraphvizGraph.GraphvizGraph.append

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.documentationtools.GraphvizGraph.GraphvizGraph.extend

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.documentationtools.GraphvizGraph.GraphvizGraph.index

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.documentationtools.GraphvizGraph.GraphvizGraph.insert

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.documentationtools.GraphvizGraph.GraphvizGraph.pop

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.documentationtools.GraphvizGraph.GraphvizGraph.remove

Special methods
---------------

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.documentationtools.GraphvizGraph.GraphvizGraph.__contains__

.. automethod:: abjad.tools.documentationtools.GraphvizGraph.GraphvizGraph.__copy__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.documentationtools.GraphvizGraph.GraphvizGraph.__delitem__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.documentationtools.GraphvizGraph.GraphvizGraph.__eq__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.documentationtools.GraphvizGraph.GraphvizGraph.__format__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.documentationtools.GraphvizGraph.GraphvizGraph.__getitem__

.. automethod:: abjad.tools.documentationtools.GraphvizGraph.GraphvizGraph.__graph__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.documentationtools.GraphvizGraph.GraphvizGraph.__hash__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.documentationtools.GraphvizGraph.GraphvizGraph.__iter__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.documentationtools.GraphvizGraph.GraphvizGraph.__len__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.documentationtools.GraphvizGraph.GraphvizGraph.__ne__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.documentationtools.GraphvizGraph.GraphvizGraph.__repr__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.documentationtools.GraphvizGraph.GraphvizGraph.__setitem__

.. automethod:: abjad.tools.documentationtools.GraphvizGraph.GraphvizGraph.__str__
