.. currentmodule:: abjad.tools.documentationtools

ReSTAutosummaryItem
===================

.. autoclass:: ReSTAutosummaryItem

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
              "abjad.tools.documentationtools.ReSTAutosummaryItem.ReSTAutosummaryItem" [color=black,
                  fontcolor=white,
                  group=3,
                  label=<<B>ReSTAutosummaryItem</B>>,
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
          "abjad.tools.datastructuretools.TreeNode.TreeNode" -> "abjad.tools.documentationtools.ReSTAutosummaryItem.ReSTAutosummaryItem";
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

      ~abjad.tools.documentationtools.ReSTAutosummaryItem.ReSTAutosummaryItem.depth
      ~abjad.tools.documentationtools.ReSTAutosummaryItem.ReSTAutosummaryItem.depthwise_inventory
      ~abjad.tools.documentationtools.ReSTAutosummaryItem.ReSTAutosummaryItem.graph_order
      ~abjad.tools.documentationtools.ReSTAutosummaryItem.ReSTAutosummaryItem.improper_parentage
      ~abjad.tools.documentationtools.ReSTAutosummaryItem.ReSTAutosummaryItem.name
      ~abjad.tools.documentationtools.ReSTAutosummaryItem.ReSTAutosummaryItem.parent
      ~abjad.tools.documentationtools.ReSTAutosummaryItem.ReSTAutosummaryItem.proper_parentage
      ~abjad.tools.documentationtools.ReSTAutosummaryItem.ReSTAutosummaryItem.rest_format
      ~abjad.tools.documentationtools.ReSTAutosummaryItem.ReSTAutosummaryItem.root
      ~abjad.tools.documentationtools.ReSTAutosummaryItem.ReSTAutosummaryItem.text
      ~abjad.tools.documentationtools.ReSTAutosummaryItem.ReSTAutosummaryItem.__copy__
      ~abjad.tools.documentationtools.ReSTAutosummaryItem.ReSTAutosummaryItem.__eq__
      ~abjad.tools.documentationtools.ReSTAutosummaryItem.ReSTAutosummaryItem.__format__
      ~abjad.tools.documentationtools.ReSTAutosummaryItem.ReSTAutosummaryItem.__hash__
      ~abjad.tools.documentationtools.ReSTAutosummaryItem.ReSTAutosummaryItem.__ne__
      ~abjad.tools.documentationtools.ReSTAutosummaryItem.ReSTAutosummaryItem.__repr__

Read-only properties
--------------------

.. only:: html

   .. container:: inherited

      .. autoattribute:: abjad.tools.documentationtools.ReSTAutosummaryItem.ReSTAutosummaryItem.depth

.. only:: html

   .. container:: inherited

      .. autoattribute:: abjad.tools.documentationtools.ReSTAutosummaryItem.ReSTAutosummaryItem.depthwise_inventory

.. only:: html

   .. container:: inherited

      .. autoattribute:: abjad.tools.documentationtools.ReSTAutosummaryItem.ReSTAutosummaryItem.graph_order

.. only:: html

   .. container:: inherited

      .. autoattribute:: abjad.tools.documentationtools.ReSTAutosummaryItem.ReSTAutosummaryItem.improper_parentage

.. only:: html

   .. container:: inherited

      .. autoattribute:: abjad.tools.documentationtools.ReSTAutosummaryItem.ReSTAutosummaryItem.parent

.. only:: html

   .. container:: inherited

      .. autoattribute:: abjad.tools.documentationtools.ReSTAutosummaryItem.ReSTAutosummaryItem.proper_parentage

.. autoattribute:: abjad.tools.documentationtools.ReSTAutosummaryItem.ReSTAutosummaryItem.rest_format

.. only:: html

   .. container:: inherited

      .. autoattribute:: abjad.tools.documentationtools.ReSTAutosummaryItem.ReSTAutosummaryItem.root

Read/write properties
---------------------

.. only:: html

   .. container:: inherited

      .. autoattribute:: abjad.tools.documentationtools.ReSTAutosummaryItem.ReSTAutosummaryItem.name

.. autoattribute:: abjad.tools.documentationtools.ReSTAutosummaryItem.ReSTAutosummaryItem.text

Special methods
---------------

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.documentationtools.ReSTAutosummaryItem.ReSTAutosummaryItem.__copy__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.documentationtools.ReSTAutosummaryItem.ReSTAutosummaryItem.__eq__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.documentationtools.ReSTAutosummaryItem.ReSTAutosummaryItem.__format__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.documentationtools.ReSTAutosummaryItem.ReSTAutosummaryItem.__hash__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.documentationtools.ReSTAutosummaryItem.ReSTAutosummaryItem.__ne__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.documentationtools.ReSTAutosummaryItem.ReSTAutosummaryItem.__repr__
