documentationtools
==================

.. automodule:: abjad.tools.documentationtools

--------

Lineage
-------

.. container:: graphviz

   .. graphviz::

      digraph InheritanceGraph {
          graph [bgcolor=transparent,
              color=lightslategrey,
              dpi=72,
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
              "abjad.tools.documentationtools.DocumentationManager.DocumentationManager" [color=black,
                  fontcolor=white,
                  group=3,
                  label=DocumentationManager,
                  shape=box,
                  style="filled, rounded"];
              "abjad.tools.documentationtools.GraphvizEdge.GraphvizEdge" [color=black,
                  fontcolor=white,
                  group=3,
                  label=GraphvizEdge,
                  shape=box,
                  style="filled, rounded"];
              "abjad.tools.documentationtools.GraphvizField.GraphvizField" [color=black,
                  fontcolor=white,
                  group=3,
                  label=GraphvizField,
                  shape=box,
                  style="filled, rounded"];
              "abjad.tools.documentationtools.GraphvizGraph.GraphvizGraph" [color=black,
                  fontcolor=white,
                  group=3,
                  label=GraphvizGraph,
                  shape=box,
                  style="filled, rounded"];
              "abjad.tools.documentationtools.GraphvizGroup.GraphvizGroup" [color=black,
                  fontcolor=white,
                  group=3,
                  label=GraphvizGroup,
                  shape=box,
                  style="filled, rounded"];
              "abjad.tools.documentationtools.GraphvizMixin.GraphvizMixin" [color=black,
                  fontcolor=white,
                  group=3,
                  label=GraphvizMixin,
                  shape=oval,
                  style="filled, rounded"];
              "abjad.tools.documentationtools.GraphvizNode.GraphvizNode" [color=black,
                  fontcolor=white,
                  group=3,
                  label=GraphvizNode,
                  shape=box,
                  style="filled, rounded"];
              "abjad.tools.documentationtools.GraphvizSubgraph.GraphvizSubgraph" [color=black,
                  fontcolor=white,
                  group=3,
                  label=GraphvizSubgraph,
                  shape=box,
                  style="filled, rounded"];
              "abjad.tools.documentationtools.GraphvizTable.GraphvizTable" [color=black,
                  fontcolor=white,
                  group=3,
                  label=GraphvizTable,
                  shape=box,
                  style="filled, rounded"];
              "abjad.tools.documentationtools.GraphvizTableCell.GraphvizTableCell" [color=black,
                  fontcolor=white,
                  group=3,
                  label=GraphvizTableCell,
                  shape=box,
                  style="filled, rounded"];
              "abjad.tools.documentationtools.GraphvizTableHorizontalRule.GraphvizTableHorizontalRule" [color=black,
                  fontcolor=white,
                  group=3,
                  label=GraphvizTableHorizontalRule,
                  shape=box,
                  style="filled, rounded"];
              "abjad.tools.documentationtools.GraphvizTableRow.GraphvizTableRow" [color=black,
                  fontcolor=white,
                  group=3,
                  label=GraphvizTableRow,
                  shape=box,
                  style="filled, rounded"];
              "abjad.tools.documentationtools.GraphvizTableVerticalRule.GraphvizTableVerticalRule" [color=black,
                  fontcolor=white,
                  group=3,
                  label=GraphvizTableVerticalRule,
                  shape=box,
                  style="filled, rounded"];
              "abjad.tools.documentationtools.InheritanceGraph.InheritanceGraph" [color=black,
                  fontcolor=white,
                  group=3,
                  label=InheritanceGraph,
                  shape=box,
                  style="filled, rounded"];
              "abjad.tools.documentationtools.ReSTAutodocDirective.ReSTAutodocDirective" [color=black,
                  fontcolor=white,
                  group=3,
                  label=ReSTAutodocDirective,
                  shape=box,
                  style="filled, rounded"];
              "abjad.tools.documentationtools.ReSTAutosummaryDirective.ReSTAutosummaryDirective" [color=black,
                  fontcolor=white,
                  group=3,
                  label=ReSTAutosummaryDirective,
                  shape=box,
                  style="filled, rounded"];
              "abjad.tools.documentationtools.ReSTAutosummaryItem.ReSTAutosummaryItem" [color=black,
                  fontcolor=white,
                  group=3,
                  label=ReSTAutosummaryItem,
                  shape=box,
                  style="filled, rounded"];
              "abjad.tools.documentationtools.ReSTDirective.ReSTDirective" [color=black,
                  fontcolor=white,
                  group=3,
                  label=ReSTDirective,
                  shape=box,
                  style="filled, rounded"];
              "abjad.tools.documentationtools.ReSTDocument.ReSTDocument" [color=black,
                  fontcolor=white,
                  group=3,
                  label=ReSTDocument,
                  shape=box,
                  style="filled, rounded"];
              "abjad.tools.documentationtools.ReSTGraphvizDirective.ReSTGraphvizDirective" [color=black,
                  fontcolor=white,
                  group=3,
                  label=ReSTGraphvizDirective,
                  shape=box,
                  style="filled, rounded"];
              "abjad.tools.documentationtools.ReSTHeading.ReSTHeading" [color=black,
                  fontcolor=white,
                  group=3,
                  label=ReSTHeading,
                  shape=box,
                  style="filled, rounded"];
              "abjad.tools.documentationtools.ReSTHorizontalRule.ReSTHorizontalRule" [color=black,
                  fontcolor=white,
                  group=3,
                  label=ReSTHorizontalRule,
                  shape=box,
                  style="filled, rounded"];
              "abjad.tools.documentationtools.ReSTInheritanceDiagram.ReSTInheritanceDiagram" [color=black,
                  fontcolor=white,
                  group=3,
                  label=ReSTInheritanceDiagram,
                  shape=box,
                  style="filled, rounded"];
              "abjad.tools.documentationtools.ReSTLineageDirective.ReSTLineageDirective" [color=black,
                  fontcolor=white,
                  group=3,
                  label=ReSTLineageDirective,
                  shape=box,
                  style="filled, rounded"];
              "abjad.tools.documentationtools.ReSTOnlyDirective.ReSTOnlyDirective" [color=black,
                  fontcolor=white,
                  group=3,
                  label=ReSTOnlyDirective,
                  shape=box,
                  style="filled, rounded"];
              "abjad.tools.documentationtools.ReSTParagraph.ReSTParagraph" [color=black,
                  fontcolor=white,
                  group=3,
                  label=ReSTParagraph,
                  shape=box,
                  style="filled, rounded"];
              "abjad.tools.documentationtools.ReSTTOCDirective.ReSTTOCDirective" [color=black,
                  fontcolor=white,
                  group=3,
                  label=ReSTTOCDirective,
                  shape=box,
                  style="filled, rounded"];
              "abjad.tools.documentationtools.ReSTTOCItem.ReSTTOCItem" [color=black,
                  fontcolor=white,
                  group=3,
                  label=ReSTTOCItem,
                  shape=box,
                  style="filled, rounded"];
              "abjad.tools.documentationtools.GraphvizGraph.GraphvizGraph" -> "abjad.tools.documentationtools.GraphvizSubgraph.GraphvizSubgraph";
              "abjad.tools.documentationtools.GraphvizMixin.GraphvizMixin" -> "abjad.tools.documentationtools.GraphvizEdge.GraphvizEdge";
              "abjad.tools.documentationtools.GraphvizMixin.GraphvizMixin" -> "abjad.tools.documentationtools.GraphvizGraph.GraphvizGraph";
              "abjad.tools.documentationtools.GraphvizMixin.GraphvizMixin" -> "abjad.tools.documentationtools.GraphvizNode.GraphvizNode";
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
          "abjad.tools.abctools.AbjadObject.AbjadObject" -> "abjad.tools.documentationtools.DocumentationManager.DocumentationManager";
          "abjad.tools.abctools.AbjadObject.AbjadObject" -> "abjad.tools.documentationtools.GraphvizMixin.GraphvizMixin";
          "abjad.tools.abctools.AbjadObject.AbjadObject" -> "abjad.tools.documentationtools.InheritanceGraph.InheritanceGraph";
          "abjad.tools.datastructuretools.TreeContainer.TreeContainer" -> "abjad.tools.documentationtools.GraphvizGraph.GraphvizGraph";
          "abjad.tools.datastructuretools.TreeContainer.TreeContainer" -> "abjad.tools.documentationtools.GraphvizGroup.GraphvizGroup";
          "abjad.tools.datastructuretools.TreeContainer.TreeContainer" -> "abjad.tools.documentationtools.GraphvizNode.GraphvizNode";
          "abjad.tools.datastructuretools.TreeContainer.TreeContainer" -> "abjad.tools.documentationtools.GraphvizTable.GraphvizTable";
          "abjad.tools.datastructuretools.TreeContainer.TreeContainer" -> "abjad.tools.documentationtools.GraphvizTableRow.GraphvizTableRow";
          "abjad.tools.datastructuretools.TreeContainer.TreeContainer" -> "abjad.tools.documentationtools.ReSTDirective.ReSTDirective";
          "abjad.tools.datastructuretools.TreeContainer.TreeContainer" -> "abjad.tools.documentationtools.ReSTDocument.ReSTDocument";
          "abjad.tools.datastructuretools.TreeNode.TreeNode" -> "abjad.tools.documentationtools.GraphvizField.GraphvizField";
          "abjad.tools.datastructuretools.TreeNode.TreeNode" -> "abjad.tools.documentationtools.GraphvizTableCell.GraphvizTableCell";
          "abjad.tools.datastructuretools.TreeNode.TreeNode" -> "abjad.tools.documentationtools.GraphvizTableHorizontalRule.GraphvizTableHorizontalRule";
          "abjad.tools.datastructuretools.TreeNode.TreeNode" -> "abjad.tools.documentationtools.GraphvizTableVerticalRule.GraphvizTableVerticalRule";
          "abjad.tools.datastructuretools.TreeNode.TreeNode" -> "abjad.tools.documentationtools.ReSTAutosummaryItem.ReSTAutosummaryItem";
          "abjad.tools.datastructuretools.TreeNode.TreeNode" -> "abjad.tools.documentationtools.ReSTHeading.ReSTHeading";
          "abjad.tools.datastructuretools.TreeNode.TreeNode" -> "abjad.tools.documentationtools.ReSTHorizontalRule.ReSTHorizontalRule";
          "abjad.tools.datastructuretools.TreeNode.TreeNode" -> "abjad.tools.documentationtools.ReSTParagraph.ReSTParagraph";
          "abjad.tools.datastructuretools.TreeNode.TreeNode" -> "abjad.tools.documentationtools.ReSTTOCItem.ReSTTOCItem";
          "builtins.object" -> "abjad.tools.abctools.AbjadObject.AbstractBase";
      }

--------

Documenters
-----------

.. toctree::
   :hidden:

   DocumentationManager
   InheritanceGraph

.. autosummary::
   :nosignatures:

   DocumentationManager
   InheritanceGraph

--------

Graphviz
--------

.. toctree::
   :hidden:

   GraphvizEdge
   GraphvizField
   GraphvizGraph
   GraphvizGroup
   GraphvizMixin
   GraphvizNode
   GraphvizSubgraph
   GraphvizTable
   GraphvizTableCell
   GraphvizTableHorizontalRule
   GraphvizTableRow
   GraphvizTableVerticalRule

.. autosummary::
   :nosignatures:

   GraphvizEdge
   GraphvizField
   GraphvizGraph
   GraphvizGroup
   GraphvizMixin
   GraphvizNode
   GraphvizSubgraph
   GraphvizTable
   GraphvizTableCell
   GraphvizTableHorizontalRule
   GraphvizTableRow
   GraphvizTableVerticalRule

--------

reStructuredText
----------------

.. toctree::
   :hidden:

   ReSTAutodocDirective
   ReSTAutosummaryDirective
   ReSTAutosummaryItem
   ReSTDirective
   ReSTDocument
   ReSTGraphvizDirective
   ReSTHeading
   ReSTHorizontalRule
   ReSTInheritanceDiagram
   ReSTLineageDirective
   ReSTOnlyDirective
   ReSTParagraph
   ReSTTOCDirective
   ReSTTOCItem

.. autosummary::
   :nosignatures:

   ReSTAutodocDirective
   ReSTAutosummaryDirective
   ReSTAutosummaryItem
   ReSTDirective
   ReSTDocument
   ReSTGraphvizDirective
   ReSTHeading
   ReSTHorizontalRule
   ReSTInheritanceDiagram
   ReSTLineageDirective
   ReSTOnlyDirective
   ReSTParagraph
   ReSTTOCDirective
   ReSTTOCItem

--------

Functions
---------

.. toctree::
   :hidden:

   compare_images
   list_all_abjad_classes
   list_all_abjad_functions
   list_all_classes
   list_all_experimental_classes
   list_all_functions
   list_all_ide_classes
   list_all_ide_functions
   make_ligeti_example_lilypond_file
   make_reference_manual_graphviz_graph
   make_reference_manual_lilypond_file
   make_text_alignment_example_lilypond_file
   yield_all_classes
   yield_all_functions
   yield_all_modules

.. autosummary::
   :nosignatures:

   compare_images
   list_all_abjad_classes
   list_all_abjad_functions
   list_all_classes
   list_all_experimental_classes
   list_all_functions
   list_all_ide_classes
   list_all_ide_functions
   make_ligeti_example_lilypond_file
   make_reference_manual_graphviz_graph
   make_reference_manual_lilypond_file
   make_text_alignment_example_lilypond_file
   yield_all_classes
   yield_all_functions
   yield_all_modules
