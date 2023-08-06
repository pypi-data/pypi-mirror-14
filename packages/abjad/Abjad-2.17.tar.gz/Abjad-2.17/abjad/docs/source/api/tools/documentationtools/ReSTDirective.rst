.. currentmodule:: abjad.tools.documentationtools

ReSTDirective
=============

.. autoclass:: ReSTDirective

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
              "abjad.tools.documentationtools.ReSTAutodocDirective.ReSTAutodocDirective" [color=4,
                  group=3,
                  label=ReSTAutodocDirective,
                  shape=box];
              "abjad.tools.documentationtools.ReSTAutosummaryDirective.ReSTAutosummaryDirective" [color=4,
                  group=3,
                  label=ReSTAutosummaryDirective,
                  shape=box];
              "abjad.tools.documentationtools.ReSTDirective.ReSTDirective" [color=black,
                  fontcolor=white,
                  group=3,
                  label=<<B>ReSTDirective</B>>,
                  shape=box,
                  style="filled, rounded"];
              "abjad.tools.documentationtools.ReSTGraphvizDirective.ReSTGraphvizDirective" [color=4,
                  group=3,
                  label=ReSTGraphvizDirective,
                  shape=box];
              "abjad.tools.documentationtools.ReSTInheritanceDiagram.ReSTInheritanceDiagram" [color=4,
                  group=3,
                  label=ReSTInheritanceDiagram,
                  shape=box];
              "abjad.tools.documentationtools.ReSTLineageDirective.ReSTLineageDirective" [color=4,
                  group=3,
                  label=ReSTLineageDirective,
                  shape=box];
              "abjad.tools.documentationtools.ReSTOnlyDirective.ReSTOnlyDirective" [color=4,
                  group=3,
                  label=ReSTOnlyDirective,
                  shape=box];
              "abjad.tools.documentationtools.ReSTTOCDirective.ReSTTOCDirective" [color=4,
                  group=3,
                  label=ReSTTOCDirective,
                  shape=box];
              "abjad.tools.documentationtools.ReSTDirective.ReSTDirective" -> "abjad.tools.documentationtools.ReSTAutodocDirective.ReSTAutodocDirective";
              "abjad.tools.documentationtools.ReSTDirective.ReSTDirective" -> "abjad.tools.documentationtools.ReSTAutosummaryDirective.ReSTAutosummaryDirective";
              "abjad.tools.documentationtools.ReSTDirective.ReSTDirective" -> "abjad.tools.documentationtools.ReSTGraphvizDirective.ReSTGraphvizDirective";
              "abjad.tools.documentationtools.ReSTDirective.ReSTDirective" -> "abjad.tools.documentationtools.ReSTInheritanceDiagram.ReSTInheritanceDiagram";
              "abjad.tools.documentationtools.ReSTDirective.ReSTDirective" -> "abjad.tools.documentationtools.ReSTLineageDirective.ReSTLineageDirective";
              "abjad.tools.documentationtools.ReSTDirective.ReSTDirective" -> "abjad.tools.documentationtools.ReSTOnlyDirective.ReSTOnlyDirective";
              "abjad.tools.documentationtools.ReSTDirective.ReSTDirective" -> "abjad.tools.documentationtools.ReSTTOCDirective.ReSTTOCDirective";
          }
          subgraph cluster_builtins {
              graph [label=builtins];
              "builtins.object" [color=2,
                  group=1,
                  label=object,
                  shape=box];
          }
          "abjad.tools.abctools.AbjadObject.AbjadObject" -> "abjad.tools.datastructuretools.TreeNode.TreeNode";
          "abjad.tools.datastructuretools.TreeContainer.TreeContainer" -> "abjad.tools.documentationtools.ReSTDirective.ReSTDirective";
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

      ~abjad.tools.documentationtools.ReSTDirective.ReSTDirective.append
      ~abjad.tools.documentationtools.ReSTDirective.ReSTDirective.argument
      ~abjad.tools.documentationtools.ReSTDirective.ReSTDirective.children
      ~abjad.tools.documentationtools.ReSTDirective.ReSTDirective.depth
      ~abjad.tools.documentationtools.ReSTDirective.ReSTDirective.depthwise_inventory
      ~abjad.tools.documentationtools.ReSTDirective.ReSTDirective.directive
      ~abjad.tools.documentationtools.ReSTDirective.ReSTDirective.extend
      ~abjad.tools.documentationtools.ReSTDirective.ReSTDirective.graph_order
      ~abjad.tools.documentationtools.ReSTDirective.ReSTDirective.improper_parentage
      ~abjad.tools.documentationtools.ReSTDirective.ReSTDirective.index
      ~abjad.tools.documentationtools.ReSTDirective.ReSTDirective.insert
      ~abjad.tools.documentationtools.ReSTDirective.ReSTDirective.leaves
      ~abjad.tools.documentationtools.ReSTDirective.ReSTDirective.name
      ~abjad.tools.documentationtools.ReSTDirective.ReSTDirective.node_class
      ~abjad.tools.documentationtools.ReSTDirective.ReSTDirective.nodes
      ~abjad.tools.documentationtools.ReSTDirective.ReSTDirective.options
      ~abjad.tools.documentationtools.ReSTDirective.ReSTDirective.parent
      ~abjad.tools.documentationtools.ReSTDirective.ReSTDirective.pop
      ~abjad.tools.documentationtools.ReSTDirective.ReSTDirective.proper_parentage
      ~abjad.tools.documentationtools.ReSTDirective.ReSTDirective.remove
      ~abjad.tools.documentationtools.ReSTDirective.ReSTDirective.rest_format
      ~abjad.tools.documentationtools.ReSTDirective.ReSTDirective.root
      ~abjad.tools.documentationtools.ReSTDirective.ReSTDirective.__contains__
      ~abjad.tools.documentationtools.ReSTDirective.ReSTDirective.__copy__
      ~abjad.tools.documentationtools.ReSTDirective.ReSTDirective.__delitem__
      ~abjad.tools.documentationtools.ReSTDirective.ReSTDirective.__eq__
      ~abjad.tools.documentationtools.ReSTDirective.ReSTDirective.__format__
      ~abjad.tools.documentationtools.ReSTDirective.ReSTDirective.__getitem__
      ~abjad.tools.documentationtools.ReSTDirective.ReSTDirective.__hash__
      ~abjad.tools.documentationtools.ReSTDirective.ReSTDirective.__iter__
      ~abjad.tools.documentationtools.ReSTDirective.ReSTDirective.__len__
      ~abjad.tools.documentationtools.ReSTDirective.ReSTDirective.__ne__
      ~abjad.tools.documentationtools.ReSTDirective.ReSTDirective.__repr__
      ~abjad.tools.documentationtools.ReSTDirective.ReSTDirective.__setitem__

Read-only properties
--------------------

.. only:: html

   .. container:: inherited

      .. autoattribute:: abjad.tools.documentationtools.ReSTDirective.ReSTDirective.children

.. only:: html

   .. container:: inherited

      .. autoattribute:: abjad.tools.documentationtools.ReSTDirective.ReSTDirective.depth

.. only:: html

   .. container:: inherited

      .. autoattribute:: abjad.tools.documentationtools.ReSTDirective.ReSTDirective.depthwise_inventory

.. only:: html

   .. container:: inherited

      .. autoattribute:: abjad.tools.documentationtools.ReSTDirective.ReSTDirective.graph_order

.. only:: html

   .. container:: inherited

      .. autoattribute:: abjad.tools.documentationtools.ReSTDirective.ReSTDirective.improper_parentage

.. only:: html

   .. container:: inherited

      .. autoattribute:: abjad.tools.documentationtools.ReSTDirective.ReSTDirective.leaves

.. autoattribute:: abjad.tools.documentationtools.ReSTDirective.ReSTDirective.node_class

.. only:: html

   .. container:: inherited

      .. autoattribute:: abjad.tools.documentationtools.ReSTDirective.ReSTDirective.nodes

.. autoattribute:: abjad.tools.documentationtools.ReSTDirective.ReSTDirective.options

.. only:: html

   .. container:: inherited

      .. autoattribute:: abjad.tools.documentationtools.ReSTDirective.ReSTDirective.parent

.. only:: html

   .. container:: inherited

      .. autoattribute:: abjad.tools.documentationtools.ReSTDirective.ReSTDirective.proper_parentage

.. autoattribute:: abjad.tools.documentationtools.ReSTDirective.ReSTDirective.rest_format

.. only:: html

   .. container:: inherited

      .. autoattribute:: abjad.tools.documentationtools.ReSTDirective.ReSTDirective.root

Read/write properties
---------------------

.. autoattribute:: abjad.tools.documentationtools.ReSTDirective.ReSTDirective.argument

.. autoattribute:: abjad.tools.documentationtools.ReSTDirective.ReSTDirective.directive

.. only:: html

   .. container:: inherited

      .. autoattribute:: abjad.tools.documentationtools.ReSTDirective.ReSTDirective.name

Methods
-------

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.documentationtools.ReSTDirective.ReSTDirective.append

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.documentationtools.ReSTDirective.ReSTDirective.extend

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.documentationtools.ReSTDirective.ReSTDirective.index

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.documentationtools.ReSTDirective.ReSTDirective.insert

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.documentationtools.ReSTDirective.ReSTDirective.pop

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.documentationtools.ReSTDirective.ReSTDirective.remove

Special methods
---------------

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.documentationtools.ReSTDirective.ReSTDirective.__contains__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.documentationtools.ReSTDirective.ReSTDirective.__copy__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.documentationtools.ReSTDirective.ReSTDirective.__delitem__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.documentationtools.ReSTDirective.ReSTDirective.__eq__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.documentationtools.ReSTDirective.ReSTDirective.__format__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.documentationtools.ReSTDirective.ReSTDirective.__getitem__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.documentationtools.ReSTDirective.ReSTDirective.__hash__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.documentationtools.ReSTDirective.ReSTDirective.__iter__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.documentationtools.ReSTDirective.ReSTDirective.__len__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.documentationtools.ReSTDirective.ReSTDirective.__ne__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.documentationtools.ReSTDirective.ReSTDirective.__repr__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.documentationtools.ReSTDirective.ReSTDirective.__setitem__
