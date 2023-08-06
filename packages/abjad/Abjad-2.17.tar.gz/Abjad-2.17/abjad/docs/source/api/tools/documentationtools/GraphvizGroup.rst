.. currentmodule:: abjad.tools.documentationtools

GraphvizGroup
=============

.. autoclass:: GraphvizGroup

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
              "abjad.tools.documentationtools.GraphvizGroup.GraphvizGroup" [color=black,
                  fontcolor=white,
                  group=3,
                  label=<<B>GraphvizGroup</B>>,
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
          "abjad.tools.datastructuretools.TreeContainer.TreeContainer" -> "abjad.tools.documentationtools.GraphvizGroup.GraphvizGroup";
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

      ~abjad.tools.documentationtools.GraphvizGroup.GraphvizGroup.append
      ~abjad.tools.documentationtools.GraphvizGroup.GraphvizGroup.children
      ~abjad.tools.documentationtools.GraphvizGroup.GraphvizGroup.depth
      ~abjad.tools.documentationtools.GraphvizGroup.GraphvizGroup.depthwise_inventory
      ~abjad.tools.documentationtools.GraphvizGroup.GraphvizGroup.extend
      ~abjad.tools.documentationtools.GraphvizGroup.GraphvizGroup.graph_order
      ~abjad.tools.documentationtools.GraphvizGroup.GraphvizGroup.improper_parentage
      ~abjad.tools.documentationtools.GraphvizGroup.GraphvizGroup.index
      ~abjad.tools.documentationtools.GraphvizGroup.GraphvizGroup.insert
      ~abjad.tools.documentationtools.GraphvizGroup.GraphvizGroup.leaves
      ~abjad.tools.documentationtools.GraphvizGroup.GraphvizGroup.name
      ~abjad.tools.documentationtools.GraphvizGroup.GraphvizGroup.nodes
      ~abjad.tools.documentationtools.GraphvizGroup.GraphvizGroup.parent
      ~abjad.tools.documentationtools.GraphvizGroup.GraphvizGroup.pop
      ~abjad.tools.documentationtools.GraphvizGroup.GraphvizGroup.proper_parentage
      ~abjad.tools.documentationtools.GraphvizGroup.GraphvizGroup.remove
      ~abjad.tools.documentationtools.GraphvizGroup.GraphvizGroup.root
      ~abjad.tools.documentationtools.GraphvizGroup.GraphvizGroup.__contains__
      ~abjad.tools.documentationtools.GraphvizGroup.GraphvizGroup.__copy__
      ~abjad.tools.documentationtools.GraphvizGroup.GraphvizGroup.__delitem__
      ~abjad.tools.documentationtools.GraphvizGroup.GraphvizGroup.__eq__
      ~abjad.tools.documentationtools.GraphvizGroup.GraphvizGroup.__format__
      ~abjad.tools.documentationtools.GraphvizGroup.GraphvizGroup.__getitem__
      ~abjad.tools.documentationtools.GraphvizGroup.GraphvizGroup.__hash__
      ~abjad.tools.documentationtools.GraphvizGroup.GraphvizGroup.__iter__
      ~abjad.tools.documentationtools.GraphvizGroup.GraphvizGroup.__len__
      ~abjad.tools.documentationtools.GraphvizGroup.GraphvizGroup.__ne__
      ~abjad.tools.documentationtools.GraphvizGroup.GraphvizGroup.__repr__
      ~abjad.tools.documentationtools.GraphvizGroup.GraphvizGroup.__setitem__

Read-only properties
--------------------

.. only:: html

   .. container:: inherited

      .. autoattribute:: abjad.tools.documentationtools.GraphvizGroup.GraphvizGroup.children

.. only:: html

   .. container:: inherited

      .. autoattribute:: abjad.tools.documentationtools.GraphvizGroup.GraphvizGroup.depth

.. only:: html

   .. container:: inherited

      .. autoattribute:: abjad.tools.documentationtools.GraphvizGroup.GraphvizGroup.depthwise_inventory

.. only:: html

   .. container:: inherited

      .. autoattribute:: abjad.tools.documentationtools.GraphvizGroup.GraphvizGroup.graph_order

.. only:: html

   .. container:: inherited

      .. autoattribute:: abjad.tools.documentationtools.GraphvizGroup.GraphvizGroup.improper_parentage

.. only:: html

   .. container:: inherited

      .. autoattribute:: abjad.tools.documentationtools.GraphvizGroup.GraphvizGroup.leaves

.. only:: html

   .. container:: inherited

      .. autoattribute:: abjad.tools.documentationtools.GraphvizGroup.GraphvizGroup.nodes

.. only:: html

   .. container:: inherited

      .. autoattribute:: abjad.tools.documentationtools.GraphvizGroup.GraphvizGroup.parent

.. only:: html

   .. container:: inherited

      .. autoattribute:: abjad.tools.documentationtools.GraphvizGroup.GraphvizGroup.proper_parentage

.. only:: html

   .. container:: inherited

      .. autoattribute:: abjad.tools.documentationtools.GraphvizGroup.GraphvizGroup.root

Read/write properties
---------------------

.. only:: html

   .. container:: inherited

      .. autoattribute:: abjad.tools.documentationtools.GraphvizGroup.GraphvizGroup.name

Methods
-------

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.documentationtools.GraphvizGroup.GraphvizGroup.append

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.documentationtools.GraphvizGroup.GraphvizGroup.extend

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.documentationtools.GraphvizGroup.GraphvizGroup.index

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.documentationtools.GraphvizGroup.GraphvizGroup.insert

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.documentationtools.GraphvizGroup.GraphvizGroup.pop

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.documentationtools.GraphvizGroup.GraphvizGroup.remove

Special methods
---------------

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.documentationtools.GraphvizGroup.GraphvizGroup.__contains__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.documentationtools.GraphvizGroup.GraphvizGroup.__copy__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.documentationtools.GraphvizGroup.GraphvizGroup.__delitem__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.documentationtools.GraphvizGroup.GraphvizGroup.__eq__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.documentationtools.GraphvizGroup.GraphvizGroup.__format__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.documentationtools.GraphvizGroup.GraphvizGroup.__getitem__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.documentationtools.GraphvizGroup.GraphvizGroup.__hash__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.documentationtools.GraphvizGroup.GraphvizGroup.__iter__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.documentationtools.GraphvizGroup.GraphvizGroup.__len__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.documentationtools.GraphvizGroup.GraphvizGroup.__ne__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.documentationtools.GraphvizGroup.GraphvizGroup.__repr__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.documentationtools.GraphvizGroup.GraphvizGroup.__setitem__
