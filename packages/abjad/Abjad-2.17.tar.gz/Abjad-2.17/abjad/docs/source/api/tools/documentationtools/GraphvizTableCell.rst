.. currentmodule:: abjad.tools.documentationtools

GraphvizTableCell
=================

.. autoclass:: GraphvizTableCell

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
              "abjad.tools.datastructuretools.TreeNode.TreeNode" [color=3,
                  group=2,
                  label=TreeNode,
                  shape=box];
          }
          subgraph cluster_documentationtools {
              graph [label=documentationtools];
              "abjad.tools.documentationtools.GraphvizTableCell.GraphvizTableCell" [color=black,
                  fontcolor=white,
                  group=3,
                  label=<<B>GraphvizTableCell</B>>,
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
          "abjad.tools.datastructuretools.TreeNode.TreeNode" -> "abjad.tools.documentationtools.GraphvizTableCell.GraphvizTableCell";
          "builtins.object" -> "abjad.tools.abctools.AbjadObject.AbstractBase";
      }

Bases
-----

- :py:class:`abjad.tools.datastructuretools.TreeNode`

- :py:class:`abjad.tools.abctools.AbjadObject`

- :py:class:`abjad.tools.abctools.AbjadObject.AbstractBase`

- :py:class:`builtins.object`

.. only:: html

   Attribute summary
   -----------------

   .. autosummary::

      ~abjad.tools.documentationtools.GraphvizTableCell.GraphvizTableCell.attributes
      ~abjad.tools.documentationtools.GraphvizTableCell.GraphvizTableCell.depth
      ~abjad.tools.documentationtools.GraphvizTableCell.GraphvizTableCell.depthwise_inventory
      ~abjad.tools.documentationtools.GraphvizTableCell.GraphvizTableCell.graph_order
      ~abjad.tools.documentationtools.GraphvizTableCell.GraphvizTableCell.improper_parentage
      ~abjad.tools.documentationtools.GraphvizTableCell.GraphvizTableCell.label
      ~abjad.tools.documentationtools.GraphvizTableCell.GraphvizTableCell.name
      ~abjad.tools.documentationtools.GraphvizTableCell.GraphvizTableCell.parent
      ~abjad.tools.documentationtools.GraphvizTableCell.GraphvizTableCell.proper_parentage
      ~abjad.tools.documentationtools.GraphvizTableCell.GraphvizTableCell.root
      ~abjad.tools.documentationtools.GraphvizTableCell.GraphvizTableCell.__copy__
      ~abjad.tools.documentationtools.GraphvizTableCell.GraphvizTableCell.__eq__
      ~abjad.tools.documentationtools.GraphvizTableCell.GraphvizTableCell.__format__
      ~abjad.tools.documentationtools.GraphvizTableCell.GraphvizTableCell.__hash__
      ~abjad.tools.documentationtools.GraphvizTableCell.GraphvizTableCell.__ne__
      ~abjad.tools.documentationtools.GraphvizTableCell.GraphvizTableCell.__repr__
      ~abjad.tools.documentationtools.GraphvizTableCell.GraphvizTableCell.__str__

Read-only properties
--------------------

.. autoattribute:: abjad.tools.documentationtools.GraphvizTableCell.GraphvizTableCell.attributes

.. only:: html

   .. container:: inherited

      .. autoattribute:: abjad.tools.documentationtools.GraphvizTableCell.GraphvizTableCell.depth

.. only:: html

   .. container:: inherited

      .. autoattribute:: abjad.tools.documentationtools.GraphvizTableCell.GraphvizTableCell.depthwise_inventory

.. only:: html

   .. container:: inherited

      .. autoattribute:: abjad.tools.documentationtools.GraphvizTableCell.GraphvizTableCell.graph_order

.. only:: html

   .. container:: inherited

      .. autoattribute:: abjad.tools.documentationtools.GraphvizTableCell.GraphvizTableCell.improper_parentage

.. autoattribute:: abjad.tools.documentationtools.GraphvizTableCell.GraphvizTableCell.label

.. only:: html

   .. container:: inherited

      .. autoattribute:: abjad.tools.documentationtools.GraphvizTableCell.GraphvizTableCell.parent

.. only:: html

   .. container:: inherited

      .. autoattribute:: abjad.tools.documentationtools.GraphvizTableCell.GraphvizTableCell.proper_parentage

.. only:: html

   .. container:: inherited

      .. autoattribute:: abjad.tools.documentationtools.GraphvizTableCell.GraphvizTableCell.root

Read/write properties
---------------------

.. only:: html

   .. container:: inherited

      .. autoattribute:: abjad.tools.documentationtools.GraphvizTableCell.GraphvizTableCell.name

Special methods
---------------

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.documentationtools.GraphvizTableCell.GraphvizTableCell.__copy__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.documentationtools.GraphvizTableCell.GraphvizTableCell.__eq__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.documentationtools.GraphvizTableCell.GraphvizTableCell.__format__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.documentationtools.GraphvizTableCell.GraphvizTableCell.__hash__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.documentationtools.GraphvizTableCell.GraphvizTableCell.__ne__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.documentationtools.GraphvizTableCell.GraphvizTableCell.__repr__

.. automethod:: abjad.tools.documentationtools.GraphvizTableCell.GraphvizTableCell.__str__
