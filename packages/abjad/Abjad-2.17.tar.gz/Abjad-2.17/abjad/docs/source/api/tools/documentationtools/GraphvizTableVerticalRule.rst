.. currentmodule:: abjad.tools.documentationtools

GraphvizTableVerticalRule
=========================

.. autoclass:: GraphvizTableVerticalRule

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
              "abjad.tools.documentationtools.GraphvizTableVerticalRule.GraphvizTableVerticalRule" [color=black,
                  fontcolor=white,
                  group=3,
                  label=<<B>GraphvizTableVerticalRule</B>>,
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
          "abjad.tools.datastructuretools.TreeNode.TreeNode" -> "abjad.tools.documentationtools.GraphvizTableVerticalRule.GraphvizTableVerticalRule";
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

      ~abjad.tools.documentationtools.GraphvizTableVerticalRule.GraphvizTableVerticalRule.depth
      ~abjad.tools.documentationtools.GraphvizTableVerticalRule.GraphvizTableVerticalRule.depthwise_inventory
      ~abjad.tools.documentationtools.GraphvizTableVerticalRule.GraphvizTableVerticalRule.graph_order
      ~abjad.tools.documentationtools.GraphvizTableVerticalRule.GraphvizTableVerticalRule.improper_parentage
      ~abjad.tools.documentationtools.GraphvizTableVerticalRule.GraphvizTableVerticalRule.name
      ~abjad.tools.documentationtools.GraphvizTableVerticalRule.GraphvizTableVerticalRule.parent
      ~abjad.tools.documentationtools.GraphvizTableVerticalRule.GraphvizTableVerticalRule.proper_parentage
      ~abjad.tools.documentationtools.GraphvizTableVerticalRule.GraphvizTableVerticalRule.root
      ~abjad.tools.documentationtools.GraphvizTableVerticalRule.GraphvizTableVerticalRule.__copy__
      ~abjad.tools.documentationtools.GraphvizTableVerticalRule.GraphvizTableVerticalRule.__eq__
      ~abjad.tools.documentationtools.GraphvizTableVerticalRule.GraphvizTableVerticalRule.__format__
      ~abjad.tools.documentationtools.GraphvizTableVerticalRule.GraphvizTableVerticalRule.__hash__
      ~abjad.tools.documentationtools.GraphvizTableVerticalRule.GraphvizTableVerticalRule.__ne__
      ~abjad.tools.documentationtools.GraphvizTableVerticalRule.GraphvizTableVerticalRule.__repr__
      ~abjad.tools.documentationtools.GraphvizTableVerticalRule.GraphvizTableVerticalRule.__str__

Read-only properties
--------------------

.. only:: html

   .. container:: inherited

      .. autoattribute:: abjad.tools.documentationtools.GraphvizTableVerticalRule.GraphvizTableVerticalRule.depth

.. only:: html

   .. container:: inherited

      .. autoattribute:: abjad.tools.documentationtools.GraphvizTableVerticalRule.GraphvizTableVerticalRule.depthwise_inventory

.. only:: html

   .. container:: inherited

      .. autoattribute:: abjad.tools.documentationtools.GraphvizTableVerticalRule.GraphvizTableVerticalRule.graph_order

.. only:: html

   .. container:: inherited

      .. autoattribute:: abjad.tools.documentationtools.GraphvizTableVerticalRule.GraphvizTableVerticalRule.improper_parentage

.. only:: html

   .. container:: inherited

      .. autoattribute:: abjad.tools.documentationtools.GraphvizTableVerticalRule.GraphvizTableVerticalRule.parent

.. only:: html

   .. container:: inherited

      .. autoattribute:: abjad.tools.documentationtools.GraphvizTableVerticalRule.GraphvizTableVerticalRule.proper_parentage

.. only:: html

   .. container:: inherited

      .. autoattribute:: abjad.tools.documentationtools.GraphvizTableVerticalRule.GraphvizTableVerticalRule.root

Read/write properties
---------------------

.. only:: html

   .. container:: inherited

      .. autoattribute:: abjad.tools.documentationtools.GraphvizTableVerticalRule.GraphvizTableVerticalRule.name

Special methods
---------------

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.documentationtools.GraphvizTableVerticalRule.GraphvizTableVerticalRule.__copy__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.documentationtools.GraphvizTableVerticalRule.GraphvizTableVerticalRule.__eq__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.documentationtools.GraphvizTableVerticalRule.GraphvizTableVerticalRule.__format__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.documentationtools.GraphvizTableVerticalRule.GraphvizTableVerticalRule.__hash__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.documentationtools.GraphvizTableVerticalRule.GraphvizTableVerticalRule.__ne__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.documentationtools.GraphvizTableVerticalRule.GraphvizTableVerticalRule.__repr__

.. automethod:: abjad.tools.documentationtools.GraphvizTableVerticalRule.GraphvizTableVerticalRule.__str__
