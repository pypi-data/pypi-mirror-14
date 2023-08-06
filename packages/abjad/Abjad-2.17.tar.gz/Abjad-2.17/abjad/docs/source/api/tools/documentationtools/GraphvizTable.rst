.. currentmodule:: abjad.tools.documentationtools

GraphvizTable
=============

.. autoclass:: GraphvizTable

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
              "abjad.tools.documentationtools.GraphvizTable.GraphvizTable" [color=black,
                  fontcolor=white,
                  group=3,
                  label=<<B>GraphvizTable</B>>,
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
          "abjad.tools.abctools.AbjadObject.AbjadObject" -> "abjad.tools.datastructuretools.TreeNode.TreeNode";
          "abjad.tools.datastructuretools.TreeContainer.TreeContainer" -> "abjad.tools.documentationtools.GraphvizTable.GraphvizTable";
          "builtins.object" -> "abjad.tools.abctools.AbjadObject.AbstractBase";
      }

Bases
-----

- :py:class:`abjad.tools.datastructuretools.TreeContainer`

- :py:class:`abjad.tools.datastructuretools.TreeNode`

- :py:class:`abjad.tools.abctools.AbjadObject`

- :py:class:`abjad.tools.abctools.AbjadObject.AbstractBase`

- :py:class:`builtins.object`

.. only:: html

   Attribute summary
   -----------------

   .. autosummary::

      ~abjad.tools.documentationtools.GraphvizTable.GraphvizTable.append
      ~abjad.tools.documentationtools.GraphvizTable.GraphvizTable.attributes
      ~abjad.tools.documentationtools.GraphvizTable.GraphvizTable.children
      ~abjad.tools.documentationtools.GraphvizTable.GraphvizTable.depth
      ~abjad.tools.documentationtools.GraphvizTable.GraphvizTable.depthwise_inventory
      ~abjad.tools.documentationtools.GraphvizTable.GraphvizTable.extend
      ~abjad.tools.documentationtools.GraphvizTable.GraphvizTable.graph_order
      ~abjad.tools.documentationtools.GraphvizTable.GraphvizTable.improper_parentage
      ~abjad.tools.documentationtools.GraphvizTable.GraphvizTable.index
      ~abjad.tools.documentationtools.GraphvizTable.GraphvizTable.insert
      ~abjad.tools.documentationtools.GraphvizTable.GraphvizTable.leaves
      ~abjad.tools.documentationtools.GraphvizTable.GraphvizTable.name
      ~abjad.tools.documentationtools.GraphvizTable.GraphvizTable.nodes
      ~abjad.tools.documentationtools.GraphvizTable.GraphvizTable.parent
      ~abjad.tools.documentationtools.GraphvizTable.GraphvizTable.pop
      ~abjad.tools.documentationtools.GraphvizTable.GraphvizTable.proper_parentage
      ~abjad.tools.documentationtools.GraphvizTable.GraphvizTable.remove
      ~abjad.tools.documentationtools.GraphvizTable.GraphvizTable.root
      ~abjad.tools.documentationtools.GraphvizTable.GraphvizTable.__contains__
      ~abjad.tools.documentationtools.GraphvizTable.GraphvizTable.__copy__
      ~abjad.tools.documentationtools.GraphvizTable.GraphvizTable.__delitem__
      ~abjad.tools.documentationtools.GraphvizTable.GraphvizTable.__eq__
      ~abjad.tools.documentationtools.GraphvizTable.GraphvizTable.__format__
      ~abjad.tools.documentationtools.GraphvizTable.GraphvizTable.__getitem__
      ~abjad.tools.documentationtools.GraphvizTable.GraphvizTable.__hash__
      ~abjad.tools.documentationtools.GraphvizTable.GraphvizTable.__iter__
      ~abjad.tools.documentationtools.GraphvizTable.GraphvizTable.__len__
      ~abjad.tools.documentationtools.GraphvizTable.GraphvizTable.__ne__
      ~abjad.tools.documentationtools.GraphvizTable.GraphvizTable.__repr__
      ~abjad.tools.documentationtools.GraphvizTable.GraphvizTable.__setitem__
      ~abjad.tools.documentationtools.GraphvizTable.GraphvizTable.__str__

Read-only properties
--------------------

.. autoattribute:: abjad.tools.documentationtools.GraphvizTable.GraphvizTable.attributes

.. only:: html

   .. container:: inherited

      .. autoattribute:: abjad.tools.documentationtools.GraphvizTable.GraphvizTable.children

.. only:: html

   .. container:: inherited

      .. autoattribute:: abjad.tools.documentationtools.GraphvizTable.GraphvizTable.depth

.. only:: html

   .. container:: inherited

      .. autoattribute:: abjad.tools.documentationtools.GraphvizTable.GraphvizTable.depthwise_inventory

.. only:: html

   .. container:: inherited

      .. autoattribute:: abjad.tools.documentationtools.GraphvizTable.GraphvizTable.graph_order

.. only:: html

   .. container:: inherited

      .. autoattribute:: abjad.tools.documentationtools.GraphvizTable.GraphvizTable.improper_parentage

.. only:: html

   .. container:: inherited

      .. autoattribute:: abjad.tools.documentationtools.GraphvizTable.GraphvizTable.leaves

.. only:: html

   .. container:: inherited

      .. autoattribute:: abjad.tools.documentationtools.GraphvizTable.GraphvizTable.nodes

.. only:: html

   .. container:: inherited

      .. autoattribute:: abjad.tools.documentationtools.GraphvizTable.GraphvizTable.parent

.. only:: html

   .. container:: inherited

      .. autoattribute:: abjad.tools.documentationtools.GraphvizTable.GraphvizTable.proper_parentage

.. only:: html

   .. container:: inherited

      .. autoattribute:: abjad.tools.documentationtools.GraphvizTable.GraphvizTable.root

Read/write properties
---------------------

.. only:: html

   .. container:: inherited

      .. autoattribute:: abjad.tools.documentationtools.GraphvizTable.GraphvizTable.name

Methods
-------

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.documentationtools.GraphvizTable.GraphvizTable.append

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.documentationtools.GraphvizTable.GraphvizTable.extend

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.documentationtools.GraphvizTable.GraphvizTable.index

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.documentationtools.GraphvizTable.GraphvizTable.insert

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.documentationtools.GraphvizTable.GraphvizTable.pop

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.documentationtools.GraphvizTable.GraphvizTable.remove

Special methods
---------------

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.documentationtools.GraphvizTable.GraphvizTable.__contains__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.documentationtools.GraphvizTable.GraphvizTable.__copy__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.documentationtools.GraphvizTable.GraphvizTable.__delitem__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.documentationtools.GraphvizTable.GraphvizTable.__eq__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.documentationtools.GraphvizTable.GraphvizTable.__format__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.documentationtools.GraphvizTable.GraphvizTable.__getitem__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.documentationtools.GraphvizTable.GraphvizTable.__hash__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.documentationtools.GraphvizTable.GraphvizTable.__iter__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.documentationtools.GraphvizTable.GraphvizTable.__len__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.documentationtools.GraphvizTable.GraphvizTable.__ne__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.documentationtools.GraphvizTable.GraphvizTable.__repr__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.documentationtools.GraphvizTable.GraphvizTable.__setitem__

.. automethod:: abjad.tools.documentationtools.GraphvizTable.GraphvizTable.__str__
