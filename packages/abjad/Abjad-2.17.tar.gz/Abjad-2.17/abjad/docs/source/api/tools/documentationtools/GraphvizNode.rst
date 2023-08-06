.. currentmodule:: abjad.tools.documentationtools

GraphvizNode
============

.. autoclass:: GraphvizNode

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
              "abjad.tools.documentationtools.GraphvizMixin.GraphvizMixin" [color=4,
                  group=3,
                  label=GraphvizMixin,
                  shape=oval,
                  style=bold];
              "abjad.tools.documentationtools.GraphvizNode.GraphvizNode" [color=black,
                  fontcolor=white,
                  group=3,
                  label=<<B>GraphvizNode</B>>,
                  shape=box,
                  style="filled, rounded"];
              "abjad.tools.documentationtools.GraphvizMixin.GraphvizMixin" -> "abjad.tools.documentationtools.GraphvizNode.GraphvizNode";
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
          "abjad.tools.datastructuretools.TreeContainer.TreeContainer" -> "abjad.tools.documentationtools.GraphvizNode.GraphvizNode";
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

      ~abjad.tools.documentationtools.GraphvizNode.GraphvizNode.all_edges
      ~abjad.tools.documentationtools.GraphvizNode.GraphvizNode.append
      ~abjad.tools.documentationtools.GraphvizNode.GraphvizNode.attributes
      ~abjad.tools.documentationtools.GraphvizNode.GraphvizNode.canonical_name
      ~abjad.tools.documentationtools.GraphvizNode.GraphvizNode.children
      ~abjad.tools.documentationtools.GraphvizNode.GraphvizNode.depth
      ~abjad.tools.documentationtools.GraphvizNode.GraphvizNode.depthwise_inventory
      ~abjad.tools.documentationtools.GraphvizNode.GraphvizNode.edges
      ~abjad.tools.documentationtools.GraphvizNode.GraphvizNode.extend
      ~abjad.tools.documentationtools.GraphvizNode.GraphvizNode.graph_order
      ~abjad.tools.documentationtools.GraphvizNode.GraphvizNode.improper_parentage
      ~abjad.tools.documentationtools.GraphvizNode.GraphvizNode.index
      ~abjad.tools.documentationtools.GraphvizNode.GraphvizNode.insert
      ~abjad.tools.documentationtools.GraphvizNode.GraphvizNode.leaves
      ~abjad.tools.documentationtools.GraphvizNode.GraphvizNode.name
      ~abjad.tools.documentationtools.GraphvizNode.GraphvizNode.nodes
      ~abjad.tools.documentationtools.GraphvizNode.GraphvizNode.parent
      ~abjad.tools.documentationtools.GraphvizNode.GraphvizNode.pop
      ~abjad.tools.documentationtools.GraphvizNode.GraphvizNode.proper_parentage
      ~abjad.tools.documentationtools.GraphvizNode.GraphvizNode.remove
      ~abjad.tools.documentationtools.GraphvizNode.GraphvizNode.root
      ~abjad.tools.documentationtools.GraphvizNode.GraphvizNode.__contains__
      ~abjad.tools.documentationtools.GraphvizNode.GraphvizNode.__copy__
      ~abjad.tools.documentationtools.GraphvizNode.GraphvizNode.__delitem__
      ~abjad.tools.documentationtools.GraphvizNode.GraphvizNode.__eq__
      ~abjad.tools.documentationtools.GraphvizNode.GraphvizNode.__format__
      ~abjad.tools.documentationtools.GraphvizNode.GraphvizNode.__getitem__
      ~abjad.tools.documentationtools.GraphvizNode.GraphvizNode.__hash__
      ~abjad.tools.documentationtools.GraphvizNode.GraphvizNode.__iter__
      ~abjad.tools.documentationtools.GraphvizNode.GraphvizNode.__len__
      ~abjad.tools.documentationtools.GraphvizNode.GraphvizNode.__ne__
      ~abjad.tools.documentationtools.GraphvizNode.GraphvizNode.__repr__
      ~abjad.tools.documentationtools.GraphvizNode.GraphvizNode.__setitem__
      ~abjad.tools.documentationtools.GraphvizNode.GraphvizNode.__str__

Read-only properties
--------------------

.. autoattribute:: abjad.tools.documentationtools.GraphvizNode.GraphvizNode.all_edges

.. only:: html

   .. container:: inherited

      .. autoattribute:: abjad.tools.documentationtools.GraphvizNode.GraphvizNode.attributes

.. autoattribute:: abjad.tools.documentationtools.GraphvizNode.GraphvizNode.canonical_name

.. only:: html

   .. container:: inherited

      .. autoattribute:: abjad.tools.documentationtools.GraphvizNode.GraphvizNode.children

.. only:: html

   .. container:: inherited

      .. autoattribute:: abjad.tools.documentationtools.GraphvizNode.GraphvizNode.depth

.. only:: html

   .. container:: inherited

      .. autoattribute:: abjad.tools.documentationtools.GraphvizNode.GraphvizNode.depthwise_inventory

.. autoattribute:: abjad.tools.documentationtools.GraphvizNode.GraphvizNode.edges

.. only:: html

   .. container:: inherited

      .. autoattribute:: abjad.tools.documentationtools.GraphvizNode.GraphvizNode.graph_order

.. only:: html

   .. container:: inherited

      .. autoattribute:: abjad.tools.documentationtools.GraphvizNode.GraphvizNode.improper_parentage

.. only:: html

   .. container:: inherited

      .. autoattribute:: abjad.tools.documentationtools.GraphvizNode.GraphvizNode.leaves

.. only:: html

   .. container:: inherited

      .. autoattribute:: abjad.tools.documentationtools.GraphvizNode.GraphvizNode.nodes

.. only:: html

   .. container:: inherited

      .. autoattribute:: abjad.tools.documentationtools.GraphvizNode.GraphvizNode.parent

.. only:: html

   .. container:: inherited

      .. autoattribute:: abjad.tools.documentationtools.GraphvizNode.GraphvizNode.proper_parentage

.. only:: html

   .. container:: inherited

      .. autoattribute:: abjad.tools.documentationtools.GraphvizNode.GraphvizNode.root

Read/write properties
---------------------

.. only:: html

   .. container:: inherited

      .. autoattribute:: abjad.tools.documentationtools.GraphvizNode.GraphvizNode.name

Methods
-------

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.documentationtools.GraphvizNode.GraphvizNode.append

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.documentationtools.GraphvizNode.GraphvizNode.extend

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.documentationtools.GraphvizNode.GraphvizNode.index

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.documentationtools.GraphvizNode.GraphvizNode.insert

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.documentationtools.GraphvizNode.GraphvizNode.pop

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.documentationtools.GraphvizNode.GraphvizNode.remove

Special methods
---------------

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.documentationtools.GraphvizNode.GraphvizNode.__contains__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.documentationtools.GraphvizNode.GraphvizNode.__copy__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.documentationtools.GraphvizNode.GraphvizNode.__delitem__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.documentationtools.GraphvizNode.GraphvizNode.__eq__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.documentationtools.GraphvizNode.GraphvizNode.__format__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.documentationtools.GraphvizNode.GraphvizNode.__getitem__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.documentationtools.GraphvizNode.GraphvizNode.__hash__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.documentationtools.GraphvizNode.GraphvizNode.__iter__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.documentationtools.GraphvizNode.GraphvizNode.__len__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.documentationtools.GraphvizNode.GraphvizNode.__ne__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.documentationtools.GraphvizNode.GraphvizNode.__repr__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.documentationtools.GraphvizNode.GraphvizNode.__setitem__

.. automethod:: abjad.tools.documentationtools.GraphvizNode.GraphvizNode.__str__
