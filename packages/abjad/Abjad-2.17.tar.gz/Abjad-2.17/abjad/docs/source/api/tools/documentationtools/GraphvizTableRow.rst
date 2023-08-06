.. currentmodule:: abjad.tools.documentationtools

GraphvizTableRow
================

.. autoclass:: GraphvizTableRow

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
              "abjad.tools.documentationtools.GraphvizTableRow.GraphvizTableRow" [color=black,
                  fontcolor=white,
                  group=3,
                  label=<<B>GraphvizTableRow</B>>,
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
          "abjad.tools.datastructuretools.TreeContainer.TreeContainer" -> "abjad.tools.documentationtools.GraphvizTableRow.GraphvizTableRow";
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

      ~abjad.tools.documentationtools.GraphvizTableRow.GraphvizTableRow.append
      ~abjad.tools.documentationtools.GraphvizTableRow.GraphvizTableRow.children
      ~abjad.tools.documentationtools.GraphvizTableRow.GraphvizTableRow.depth
      ~abjad.tools.documentationtools.GraphvizTableRow.GraphvizTableRow.depthwise_inventory
      ~abjad.tools.documentationtools.GraphvizTableRow.GraphvizTableRow.extend
      ~abjad.tools.documentationtools.GraphvizTableRow.GraphvizTableRow.graph_order
      ~abjad.tools.documentationtools.GraphvizTableRow.GraphvizTableRow.improper_parentage
      ~abjad.tools.documentationtools.GraphvizTableRow.GraphvizTableRow.index
      ~abjad.tools.documentationtools.GraphvizTableRow.GraphvizTableRow.insert
      ~abjad.tools.documentationtools.GraphvizTableRow.GraphvizTableRow.leaves
      ~abjad.tools.documentationtools.GraphvizTableRow.GraphvizTableRow.name
      ~abjad.tools.documentationtools.GraphvizTableRow.GraphvizTableRow.nodes
      ~abjad.tools.documentationtools.GraphvizTableRow.GraphvizTableRow.parent
      ~abjad.tools.documentationtools.GraphvizTableRow.GraphvizTableRow.pop
      ~abjad.tools.documentationtools.GraphvizTableRow.GraphvizTableRow.proper_parentage
      ~abjad.tools.documentationtools.GraphvizTableRow.GraphvizTableRow.remove
      ~abjad.tools.documentationtools.GraphvizTableRow.GraphvizTableRow.root
      ~abjad.tools.documentationtools.GraphvizTableRow.GraphvizTableRow.__contains__
      ~abjad.tools.documentationtools.GraphvizTableRow.GraphvizTableRow.__copy__
      ~abjad.tools.documentationtools.GraphvizTableRow.GraphvizTableRow.__delitem__
      ~abjad.tools.documentationtools.GraphvizTableRow.GraphvizTableRow.__eq__
      ~abjad.tools.documentationtools.GraphvizTableRow.GraphvizTableRow.__format__
      ~abjad.tools.documentationtools.GraphvizTableRow.GraphvizTableRow.__getitem__
      ~abjad.tools.documentationtools.GraphvizTableRow.GraphvizTableRow.__hash__
      ~abjad.tools.documentationtools.GraphvizTableRow.GraphvizTableRow.__iter__
      ~abjad.tools.documentationtools.GraphvizTableRow.GraphvizTableRow.__len__
      ~abjad.tools.documentationtools.GraphvizTableRow.GraphvizTableRow.__ne__
      ~abjad.tools.documentationtools.GraphvizTableRow.GraphvizTableRow.__repr__
      ~abjad.tools.documentationtools.GraphvizTableRow.GraphvizTableRow.__setitem__
      ~abjad.tools.documentationtools.GraphvizTableRow.GraphvizTableRow.__str__

Read-only properties
--------------------

.. only:: html

   .. container:: inherited

      .. autoattribute:: abjad.tools.documentationtools.GraphvizTableRow.GraphvizTableRow.children

.. only:: html

   .. container:: inherited

      .. autoattribute:: abjad.tools.documentationtools.GraphvizTableRow.GraphvizTableRow.depth

.. only:: html

   .. container:: inherited

      .. autoattribute:: abjad.tools.documentationtools.GraphvizTableRow.GraphvizTableRow.depthwise_inventory

.. only:: html

   .. container:: inherited

      .. autoattribute:: abjad.tools.documentationtools.GraphvizTableRow.GraphvizTableRow.graph_order

.. only:: html

   .. container:: inherited

      .. autoattribute:: abjad.tools.documentationtools.GraphvizTableRow.GraphvizTableRow.improper_parentage

.. only:: html

   .. container:: inherited

      .. autoattribute:: abjad.tools.documentationtools.GraphvizTableRow.GraphvizTableRow.leaves

.. only:: html

   .. container:: inherited

      .. autoattribute:: abjad.tools.documentationtools.GraphvizTableRow.GraphvizTableRow.nodes

.. only:: html

   .. container:: inherited

      .. autoattribute:: abjad.tools.documentationtools.GraphvizTableRow.GraphvizTableRow.parent

.. only:: html

   .. container:: inherited

      .. autoattribute:: abjad.tools.documentationtools.GraphvizTableRow.GraphvizTableRow.proper_parentage

.. only:: html

   .. container:: inherited

      .. autoattribute:: abjad.tools.documentationtools.GraphvizTableRow.GraphvizTableRow.root

Read/write properties
---------------------

.. only:: html

   .. container:: inherited

      .. autoattribute:: abjad.tools.documentationtools.GraphvizTableRow.GraphvizTableRow.name

Methods
-------

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.documentationtools.GraphvizTableRow.GraphvizTableRow.append

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.documentationtools.GraphvizTableRow.GraphvizTableRow.extend

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.documentationtools.GraphvizTableRow.GraphvizTableRow.index

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.documentationtools.GraphvizTableRow.GraphvizTableRow.insert

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.documentationtools.GraphvizTableRow.GraphvizTableRow.pop

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.documentationtools.GraphvizTableRow.GraphvizTableRow.remove

Special methods
---------------

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.documentationtools.GraphvizTableRow.GraphvizTableRow.__contains__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.documentationtools.GraphvizTableRow.GraphvizTableRow.__copy__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.documentationtools.GraphvizTableRow.GraphvizTableRow.__delitem__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.documentationtools.GraphvizTableRow.GraphvizTableRow.__eq__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.documentationtools.GraphvizTableRow.GraphvizTableRow.__format__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.documentationtools.GraphvizTableRow.GraphvizTableRow.__getitem__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.documentationtools.GraphvizTableRow.GraphvizTableRow.__hash__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.documentationtools.GraphvizTableRow.GraphvizTableRow.__iter__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.documentationtools.GraphvizTableRow.GraphvizTableRow.__len__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.documentationtools.GraphvizTableRow.GraphvizTableRow.__ne__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.documentationtools.GraphvizTableRow.GraphvizTableRow.__repr__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.documentationtools.GraphvizTableRow.GraphvizTableRow.__setitem__

.. automethod:: abjad.tools.documentationtools.GraphvizTableRow.GraphvizTableRow.__str__
