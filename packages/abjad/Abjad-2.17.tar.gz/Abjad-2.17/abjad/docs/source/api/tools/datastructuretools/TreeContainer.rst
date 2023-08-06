.. currentmodule:: abjad.tools.datastructuretools

TreeContainer
=============

.. autoclass:: TreeContainer

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
              "abjad.tools.datastructuretools.TreeContainer.TreeContainer" [color=black,
                  fontcolor=white,
                  group=2,
                  label=<<B>TreeContainer</B>>,
                  shape=box,
                  style="filled, rounded"];
              "abjad.tools.datastructuretools.TreeNode.TreeNode" [color=3,
                  group=2,
                  label=TreeNode,
                  shape=box];
              "abjad.tools.datastructuretools.TreeNode.TreeNode" -> "abjad.tools.datastructuretools.TreeContainer.TreeContainer";
          }
          subgraph cluster_documentationtools {
              graph [label=documentationtools];
              "abjad.tools.documentationtools.GraphvizGraph.GraphvizGraph" [color=4,
                  group=3,
                  label=GraphvizGraph,
                  shape=box];
              "abjad.tools.documentationtools.GraphvizGroup.GraphvizGroup" [color=4,
                  group=3,
                  label=GraphvizGroup,
                  shape=box];
              "abjad.tools.documentationtools.GraphvizNode.GraphvizNode" [color=4,
                  group=3,
                  label=GraphvizNode,
                  shape=box];
              "abjad.tools.documentationtools.GraphvizSubgraph.GraphvizSubgraph" [color=4,
                  group=3,
                  label=GraphvizSubgraph,
                  shape=box];
              "abjad.tools.documentationtools.GraphvizTable.GraphvizTable" [color=4,
                  group=3,
                  label=GraphvizTable,
                  shape=box];
              "abjad.tools.documentationtools.GraphvizTableRow.GraphvizTableRow" [color=4,
                  group=3,
                  label=GraphvizTableRow,
                  shape=box];
              "abjad.tools.documentationtools.ReSTAutodocDirective.ReSTAutodocDirective" [color=4,
                  group=3,
                  label=ReSTAutodocDirective,
                  shape=box];
              "abjad.tools.documentationtools.ReSTAutosummaryDirective.ReSTAutosummaryDirective" [color=4,
                  group=3,
                  label=ReSTAutosummaryDirective,
                  shape=box];
              "abjad.tools.documentationtools.ReSTDirective.ReSTDirective" [color=4,
                  group=3,
                  label=ReSTDirective,
                  shape=box];
              "abjad.tools.documentationtools.ReSTDocument.ReSTDocument" [color=4,
                  group=3,
                  label=ReSTDocument,
                  shape=box];
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
              "abjad.tools.documentationtools.GraphvizGraph.GraphvizGraph" -> "abjad.tools.documentationtools.GraphvizSubgraph.GraphvizSubgraph";
              "abjad.tools.documentationtools.ReSTDirective.ReSTDirective" -> "abjad.tools.documentationtools.ReSTAutodocDirective.ReSTAutodocDirective";
              "abjad.tools.documentationtools.ReSTDirective.ReSTDirective" -> "abjad.tools.documentationtools.ReSTAutosummaryDirective.ReSTAutosummaryDirective";
              "abjad.tools.documentationtools.ReSTDirective.ReSTDirective" -> "abjad.tools.documentationtools.ReSTGraphvizDirective.ReSTGraphvizDirective";
              "abjad.tools.documentationtools.ReSTDirective.ReSTDirective" -> "abjad.tools.documentationtools.ReSTInheritanceDiagram.ReSTInheritanceDiagram";
              "abjad.tools.documentationtools.ReSTDirective.ReSTDirective" -> "abjad.tools.documentationtools.ReSTLineageDirective.ReSTLineageDirective";
              "abjad.tools.documentationtools.ReSTDirective.ReSTDirective" -> "abjad.tools.documentationtools.ReSTOnlyDirective.ReSTOnlyDirective";
              "abjad.tools.documentationtools.ReSTDirective.ReSTDirective" -> "abjad.tools.documentationtools.ReSTTOCDirective.ReSTTOCDirective";
          }
          subgraph cluster_quantizationtools {
              graph [label=quantizationtools];
              "abjad.tools.quantizationtools.QGridContainer.QGridContainer" [color=5,
                  group=4,
                  label=QGridContainer,
                  shape=box];
          }
          subgraph cluster_rhythmtreetools {
              graph [label=rhythmtreetools];
              "abjad.tools.rhythmtreetools.RhythmTreeContainer.RhythmTreeContainer" [color=6,
                  group=5,
                  label=RhythmTreeContainer,
                  shape=box];
          }
          subgraph cluster_builtins {
              graph [label=builtins];
              "builtins.object" [color=2,
                  group=1,
                  label=object,
                  shape=box];
          }
          "abjad.tools.abctools.AbjadObject.AbjadObject" -> "abjad.tools.datastructuretools.TreeNode.TreeNode";
          "abjad.tools.datastructuretools.TreeContainer.TreeContainer" -> "abjad.tools.documentationtools.GraphvizGraph.GraphvizGraph";
          "abjad.tools.datastructuretools.TreeContainer.TreeContainer" -> "abjad.tools.documentationtools.GraphvizGroup.GraphvizGroup";
          "abjad.tools.datastructuretools.TreeContainer.TreeContainer" -> "abjad.tools.documentationtools.GraphvizNode.GraphvizNode";
          "abjad.tools.datastructuretools.TreeContainer.TreeContainer" -> "abjad.tools.documentationtools.GraphvizTable.GraphvizTable";
          "abjad.tools.datastructuretools.TreeContainer.TreeContainer" -> "abjad.tools.documentationtools.GraphvizTableRow.GraphvizTableRow";
          "abjad.tools.datastructuretools.TreeContainer.TreeContainer" -> "abjad.tools.documentationtools.ReSTDirective.ReSTDirective";
          "abjad.tools.datastructuretools.TreeContainer.TreeContainer" -> "abjad.tools.documentationtools.ReSTDocument.ReSTDocument";
          "abjad.tools.datastructuretools.TreeContainer.TreeContainer" -> "abjad.tools.rhythmtreetools.RhythmTreeContainer.RhythmTreeContainer";
          "abjad.tools.rhythmtreetools.RhythmTreeContainer.RhythmTreeContainer" -> "abjad.tools.quantizationtools.QGridContainer.QGridContainer";
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

      ~abjad.tools.datastructuretools.TreeContainer.TreeContainer.append
      ~abjad.tools.datastructuretools.TreeContainer.TreeContainer.children
      ~abjad.tools.datastructuretools.TreeContainer.TreeContainer.depth
      ~abjad.tools.datastructuretools.TreeContainer.TreeContainer.depthwise_inventory
      ~abjad.tools.datastructuretools.TreeContainer.TreeContainer.extend
      ~abjad.tools.datastructuretools.TreeContainer.TreeContainer.graph_order
      ~abjad.tools.datastructuretools.TreeContainer.TreeContainer.improper_parentage
      ~abjad.tools.datastructuretools.TreeContainer.TreeContainer.index
      ~abjad.tools.datastructuretools.TreeContainer.TreeContainer.insert
      ~abjad.tools.datastructuretools.TreeContainer.TreeContainer.leaves
      ~abjad.tools.datastructuretools.TreeContainer.TreeContainer.name
      ~abjad.tools.datastructuretools.TreeContainer.TreeContainer.nodes
      ~abjad.tools.datastructuretools.TreeContainer.TreeContainer.parent
      ~abjad.tools.datastructuretools.TreeContainer.TreeContainer.pop
      ~abjad.tools.datastructuretools.TreeContainer.TreeContainer.proper_parentage
      ~abjad.tools.datastructuretools.TreeContainer.TreeContainer.remove
      ~abjad.tools.datastructuretools.TreeContainer.TreeContainer.root
      ~abjad.tools.datastructuretools.TreeContainer.TreeContainer.__contains__
      ~abjad.tools.datastructuretools.TreeContainer.TreeContainer.__copy__
      ~abjad.tools.datastructuretools.TreeContainer.TreeContainer.__delitem__
      ~abjad.tools.datastructuretools.TreeContainer.TreeContainer.__eq__
      ~abjad.tools.datastructuretools.TreeContainer.TreeContainer.__format__
      ~abjad.tools.datastructuretools.TreeContainer.TreeContainer.__getitem__
      ~abjad.tools.datastructuretools.TreeContainer.TreeContainer.__hash__
      ~abjad.tools.datastructuretools.TreeContainer.TreeContainer.__iter__
      ~abjad.tools.datastructuretools.TreeContainer.TreeContainer.__len__
      ~abjad.tools.datastructuretools.TreeContainer.TreeContainer.__ne__
      ~abjad.tools.datastructuretools.TreeContainer.TreeContainer.__repr__
      ~abjad.tools.datastructuretools.TreeContainer.TreeContainer.__setitem__

Read-only properties
--------------------

.. autoattribute:: abjad.tools.datastructuretools.TreeContainer.TreeContainer.children

.. only:: html

   .. container:: inherited

      .. autoattribute:: abjad.tools.datastructuretools.TreeContainer.TreeContainer.depth

.. only:: html

   .. container:: inherited

      .. autoattribute:: abjad.tools.datastructuretools.TreeContainer.TreeContainer.depthwise_inventory

.. only:: html

   .. container:: inherited

      .. autoattribute:: abjad.tools.datastructuretools.TreeContainer.TreeContainer.graph_order

.. only:: html

   .. container:: inherited

      .. autoattribute:: abjad.tools.datastructuretools.TreeContainer.TreeContainer.improper_parentage

.. autoattribute:: abjad.tools.datastructuretools.TreeContainer.TreeContainer.leaves

.. autoattribute:: abjad.tools.datastructuretools.TreeContainer.TreeContainer.nodes

.. only:: html

   .. container:: inherited

      .. autoattribute:: abjad.tools.datastructuretools.TreeContainer.TreeContainer.parent

.. only:: html

   .. container:: inherited

      .. autoattribute:: abjad.tools.datastructuretools.TreeContainer.TreeContainer.proper_parentage

.. only:: html

   .. container:: inherited

      .. autoattribute:: abjad.tools.datastructuretools.TreeContainer.TreeContainer.root

Read/write properties
---------------------

.. only:: html

   .. container:: inherited

      .. autoattribute:: abjad.tools.datastructuretools.TreeContainer.TreeContainer.name

Methods
-------

.. automethod:: abjad.tools.datastructuretools.TreeContainer.TreeContainer.append

.. automethod:: abjad.tools.datastructuretools.TreeContainer.TreeContainer.extend

.. automethod:: abjad.tools.datastructuretools.TreeContainer.TreeContainer.index

.. automethod:: abjad.tools.datastructuretools.TreeContainer.TreeContainer.insert

.. automethod:: abjad.tools.datastructuretools.TreeContainer.TreeContainer.pop

.. automethod:: abjad.tools.datastructuretools.TreeContainer.TreeContainer.remove

Special methods
---------------

.. automethod:: abjad.tools.datastructuretools.TreeContainer.TreeContainer.__contains__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.datastructuretools.TreeContainer.TreeContainer.__copy__

.. automethod:: abjad.tools.datastructuretools.TreeContainer.TreeContainer.__delitem__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.datastructuretools.TreeContainer.TreeContainer.__eq__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.datastructuretools.TreeContainer.TreeContainer.__format__

.. automethod:: abjad.tools.datastructuretools.TreeContainer.TreeContainer.__getitem__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.datastructuretools.TreeContainer.TreeContainer.__hash__

.. automethod:: abjad.tools.datastructuretools.TreeContainer.TreeContainer.__iter__

.. automethod:: abjad.tools.datastructuretools.TreeContainer.TreeContainer.__len__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.datastructuretools.TreeContainer.TreeContainer.__ne__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.datastructuretools.TreeContainer.TreeContainer.__repr__

.. automethod:: abjad.tools.datastructuretools.TreeContainer.TreeContainer.__setitem__
