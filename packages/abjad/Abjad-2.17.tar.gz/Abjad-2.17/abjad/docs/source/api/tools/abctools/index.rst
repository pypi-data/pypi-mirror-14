abctools
========

.. automodule:: abjad.tools.abctools

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
          subgraph cluster_part {
              graph [label=part];
              "abjad.demos.part.PartCantusScoreTemplate.PartCantusScoreTemplate" [color=4,
                  group=21,
                  label=PartCantusScoreTemplate,
                  shape=box];
          }
          subgraph cluster_abctools {
              graph [label=abctools];
              "abjad.tools.abctools.AbjadObject.AbjadObject" [color=black,
                  fontcolor=white,
                  group=0,
                  label=AbjadObject,
                  shape=box,
                  style="filled, rounded"];
              "abjad.tools.abctools.AbjadObject.AbstractBase" [color=1,
                  group=0,
                  label=AbstractBase,
                  shape=box];
              "abjad.tools.abctools.AbjadValueObject.AbjadValueObject" [color=black,
                  fontcolor=white,
                  group=0,
                  label=AbjadValueObject,
                  shape=box,
                  style="filled, rounded"];
              "abjad.tools.abctools.ContextManager.ContextManager" [color=black,
                  fontcolor=white,
                  group=0,
                  label=ContextManager,
                  shape=oval,
                  style="filled, rounded"];
              "abjad.tools.abctools.Parser.Parser" [color=black,
                  fontcolor=white,
                  group=0,
                  label=Parser,
                  shape=oval,
                  style="filled, rounded"];
              "abjad.tools.abctools.AbjadObject.AbjadObject" -> "abjad.tools.abctools.AbjadValueObject.AbjadValueObject";
              "abjad.tools.abctools.AbjadObject.AbjadObject" -> "abjad.tools.abctools.ContextManager.ContextManager";
              "abjad.tools.abctools.AbjadObject.AbjadObject" -> "abjad.tools.abctools.Parser.Parser";
              "abjad.tools.abctools.AbjadObject.AbstractBase" -> "abjad.tools.abctools.AbjadObject.AbjadObject";
          }
          subgraph cluster_abjadbooktools {
              graph [label=abjadbooktools];
              "abjad.tools.abjadbooktools.AbjadBookScript.AbjadBookScript" [color=2,
                  group=1,
                  label=AbjadBookScript,
                  shape=box];
              "abjad.tools.abjadbooktools.CodeBlock.CodeBlock" [color=2,
                  group=1,
                  label=CodeBlock,
                  shape=box];
              "abjad.tools.abjadbooktools.CodeBlockSpecifier.CodeBlockSpecifier" [color=2,
                  group=1,
                  label=CodeBlockSpecifier,
                  shape=box];
              "abjad.tools.abjadbooktools.CodeOutputProxy.CodeOutputProxy" [color=2,
                  group=1,
                  label=CodeOutputProxy,
                  shape=box];
              "abjad.tools.abjadbooktools.GraphvizOutputProxy.GraphvizOutputProxy" [color=2,
                  group=1,
                  label=GraphvizOutputProxy,
                  shape=box];
              "abjad.tools.abjadbooktools.ImageLayoutSpecifier.ImageLayoutSpecifier" [color=2,
                  group=1,
                  label=ImageLayoutSpecifier,
                  shape=box];
              "abjad.tools.abjadbooktools.ImageOutputProxy.ImageOutputProxy" [color=2,
                  group=1,
                  label=ImageOutputProxy,
                  shape=oval,
                  style=bold];
              "abjad.tools.abjadbooktools.ImageRenderSpecifier.ImageRenderSpecifier" [color=2,
                  group=1,
                  label=ImageRenderSpecifier,
                  shape=box];
              "abjad.tools.abjadbooktools.LaTeXDocumentHandler.LaTeXDocumentHandler" [color=2,
                  group=1,
                  label=LaTeXDocumentHandler,
                  shape=box];
              "abjad.tools.abjadbooktools.LilyPondOutputProxy.LilyPondOutputProxy" [color=2,
                  group=1,
                  label=LilyPondOutputProxy,
                  shape=box];
              "abjad.tools.abjadbooktools.SphinxDocumentHandler.SphinxDocumentHandler" [color=2,
                  group=1,
                  label=SphinxDocumentHandler,
                  shape=box];
              "abjad.tools.abjadbooktools.ImageOutputProxy.ImageOutputProxy" -> "abjad.tools.abjadbooktools.GraphvizOutputProxy.GraphvizOutputProxy";
              "abjad.tools.abjadbooktools.ImageOutputProxy.ImageOutputProxy" -> "abjad.tools.abjadbooktools.LilyPondOutputProxy.LilyPondOutputProxy";
          }
          subgraph cluster_agenttools {
              graph [label=agenttools];
              "abjad.tools.agenttools.InspectionAgent.InspectionAgent" [color=3,
                  group=2,
                  label=InspectionAgent,
                  shape=box];
              "abjad.tools.agenttools.IterationAgent.IterationAgent" [color=3,
                  group=2,
                  label=IterationAgent,
                  shape=box];
              "abjad.tools.agenttools.LabelAgent.LabelAgent" [color=3,
                  group=2,
                  label=LabelAgent,
                  shape=box];
              "abjad.tools.agenttools.MutationAgent.MutationAgent" [color=3,
                  group=2,
                  label=MutationAgent,
                  shape=box];
              "abjad.tools.agenttools.PersistenceAgent.PersistenceAgent" [color=3,
                  group=2,
                  label=PersistenceAgent,
                  shape=box];
          }
          subgraph cluster_datastructuretools {
              graph [label=datastructuretools];
              "abjad.tools.datastructuretools.Cursor.Cursor" [color=6,
                  group=5,
                  label=Cursor,
                  shape=box];
              "abjad.tools.datastructuretools.CyclicMatrix.CyclicMatrix" [color=6,
                  group=5,
                  label=CyclicMatrix,
                  shape=box];
              "abjad.tools.datastructuretools.CyclicPayloadTree.CyclicPayloadTree" [color=6,
                  group=5,
                  label=CyclicPayloadTree,
                  shape=box];
              "abjad.tools.datastructuretools.CyclicTuple.CyclicTuple" [color=6,
                  group=5,
                  label=CyclicTuple,
                  shape=box];
              "abjad.tools.datastructuretools.Matrix.Matrix" [color=6,
                  group=5,
                  label=Matrix,
                  shape=box];
              "abjad.tools.datastructuretools.OrdinalConstant.OrdinalConstant" [color=6,
                  group=5,
                  label=OrdinalConstant,
                  shape=box];
              "abjad.tools.datastructuretools.PayloadTree.PayloadTree" [color=6,
                  group=5,
                  label=PayloadTree,
                  shape=box];
              "abjad.tools.datastructuretools.TreeContainer.TreeContainer" [color=6,
                  group=5,
                  label=TreeContainer,
                  shape=box];
              "abjad.tools.datastructuretools.TreeNode.TreeNode" [color=6,
                  group=5,
                  label=TreeNode,
                  shape=box];
              "abjad.tools.datastructuretools.TypedCollection.TypedCollection" [color=6,
                  group=5,
                  label=TypedCollection,
                  shape=oval,
                  style=bold];
              "abjad.tools.datastructuretools.TypedCounter.TypedCounter" [color=6,
                  group=5,
                  label=TypedCounter,
                  shape=box];
              "abjad.tools.datastructuretools.TypedFrozenset.TypedFrozenset" [color=6,
                  group=5,
                  label=TypedFrozenset,
                  shape=box];
              "abjad.tools.datastructuretools.TypedList.TypedList" [color=6,
                  group=5,
                  label=TypedList,
                  shape=box];
              "abjad.tools.datastructuretools.TypedOrderedDict.TypedOrderedDict" [color=6,
                  group=5,
                  label=TypedOrderedDict,
                  shape=box];
              "abjad.tools.datastructuretools.TypedTuple.TypedTuple" [color=6,
                  group=5,
                  label=TypedTuple,
                  shape=box];
              "abjad.tools.datastructuretools.Matrix.Matrix" -> "abjad.tools.datastructuretools.CyclicMatrix.CyclicMatrix";
              "abjad.tools.datastructuretools.PayloadTree.PayloadTree" -> "abjad.tools.datastructuretools.CyclicPayloadTree.CyclicPayloadTree";
              "abjad.tools.datastructuretools.TreeNode.TreeNode" -> "abjad.tools.datastructuretools.TreeContainer.TreeContainer";
              "abjad.tools.datastructuretools.TypedCollection.TypedCollection" -> "abjad.tools.datastructuretools.TypedCounter.TypedCounter";
              "abjad.tools.datastructuretools.TypedCollection.TypedCollection" -> "abjad.tools.datastructuretools.TypedFrozenset.TypedFrozenset";
              "abjad.tools.datastructuretools.TypedCollection.TypedCollection" -> "abjad.tools.datastructuretools.TypedList.TypedList";
              "abjad.tools.datastructuretools.TypedCollection.TypedCollection" -> "abjad.tools.datastructuretools.TypedOrderedDict.TypedOrderedDict";
              "abjad.tools.datastructuretools.TypedCollection.TypedCollection" -> "abjad.tools.datastructuretools.TypedTuple.TypedTuple";
          }
          subgraph cluster_developerscripttools {
              graph [label=developerscripttools];
              "abjad.tools.developerscripttools.AbjDevScript.AbjDevScript" [color=7,
                  group=6,
                  label=AbjDevScript,
                  shape=box];
              "abjad.tools.developerscripttools.AbjGrepScript.AbjGrepScript" [color=7,
                  group=6,
                  label=AbjGrepScript,
                  shape=box];
              "abjad.tools.developerscripttools.BuildAPIScript.BuildAPIScript" [color=7,
                  group=6,
                  label=BuildAPIScript,
                  shape=box];
              "abjad.tools.developerscripttools.CleanScript.CleanScript" [color=7,
                  group=6,
                  label=CleanScript,
                  shape=box];
              "abjad.tools.developerscripttools.CountLinewidthsScript.CountLinewidthsScript" [color=7,
                  group=6,
                  label=CountLinewidthsScript,
                  shape=box];
              "abjad.tools.developerscripttools.CountToolsScript.CountToolsScript" [color=7,
                  group=6,
                  label=CountToolsScript,
                  shape=box];
              "abjad.tools.developerscripttools.DeveloperScript.DeveloperScript" [color=7,
                  group=6,
                  label=DeveloperScript,
                  shape=oval,
                  style=bold];
              "abjad.tools.developerscripttools.DirectoryScript.DirectoryScript" [color=7,
                  group=6,
                  label=DirectoryScript,
                  shape=oval,
                  style=bold];
              "abjad.tools.developerscripttools.NewScoreScript.NewScoreScript" [color=7,
                  group=6,
                  label=NewScoreScript,
                  shape=box];
              "abjad.tools.developerscripttools.PyTestScript.PyTestScript" [color=7,
                  group=6,
                  label=PyTestScript,
                  shape=box];
              "abjad.tools.developerscripttools.RenameModulesScript.RenameModulesScript" [color=7,
                  group=6,
                  label=RenameModulesScript,
                  shape=box];
              "abjad.tools.developerscripttools.ReplaceInFilesScript.ReplaceInFilesScript" [color=7,
                  group=6,
                  label=ReplaceInFilesScript,
                  shape=box];
              "abjad.tools.developerscripttools.RunDoctestsScript.RunDoctestsScript" [color=7,
                  group=6,
                  label=RunDoctestsScript,
                  shape=box];
              "abjad.tools.developerscripttools.StatsScript.StatsScript" [color=7,
                  group=6,
                  label=StatsScript,
                  shape=box];
              "abjad.tools.developerscripttools.TestAndRebuildScript.TestAndRebuildScript" [color=7,
                  group=6,
                  label=TestAndRebuildScript,
                  shape=box];
              "abjad.tools.developerscripttools.DeveloperScript.DeveloperScript" -> "abjad.tools.developerscripttools.AbjDevScript.AbjDevScript";
              "abjad.tools.developerscripttools.DeveloperScript.DeveloperScript" -> "abjad.tools.developerscripttools.BuildAPIScript.BuildAPIScript";
              "abjad.tools.developerscripttools.DeveloperScript.DeveloperScript" -> "abjad.tools.developerscripttools.DirectoryScript.DirectoryScript";
              "abjad.tools.developerscripttools.DeveloperScript.DeveloperScript" -> "abjad.tools.developerscripttools.RenameModulesScript.RenameModulesScript";
              "abjad.tools.developerscripttools.DeveloperScript.DeveloperScript" -> "abjad.tools.developerscripttools.TestAndRebuildScript.TestAndRebuildScript";
              "abjad.tools.developerscripttools.DirectoryScript.DirectoryScript" -> "abjad.tools.developerscripttools.AbjGrepScript.AbjGrepScript";
              "abjad.tools.developerscripttools.DirectoryScript.DirectoryScript" -> "abjad.tools.developerscripttools.CleanScript.CleanScript";
              "abjad.tools.developerscripttools.DirectoryScript.DirectoryScript" -> "abjad.tools.developerscripttools.CountLinewidthsScript.CountLinewidthsScript";
              "abjad.tools.developerscripttools.DirectoryScript.DirectoryScript" -> "abjad.tools.developerscripttools.CountToolsScript.CountToolsScript";
              "abjad.tools.developerscripttools.DirectoryScript.DirectoryScript" -> "abjad.tools.developerscripttools.NewScoreScript.NewScoreScript";
              "abjad.tools.developerscripttools.DirectoryScript.DirectoryScript" -> "abjad.tools.developerscripttools.PyTestScript.PyTestScript";
              "abjad.tools.developerscripttools.DirectoryScript.DirectoryScript" -> "abjad.tools.developerscripttools.ReplaceInFilesScript.ReplaceInFilesScript";
              "abjad.tools.developerscripttools.DirectoryScript.DirectoryScript" -> "abjad.tools.developerscripttools.RunDoctestsScript.RunDoctestsScript";
              "abjad.tools.developerscripttools.DirectoryScript.DirectoryScript" -> "abjad.tools.developerscripttools.StatsScript.StatsScript";
          }
          subgraph cluster_documentationtools {
              graph [label=documentationtools];
              "abjad.tools.documentationtools.DocumentationManager.DocumentationManager" [color=8,
                  group=7,
                  label=DocumentationManager,
                  shape=box];
              "abjad.tools.documentationtools.GraphvizEdge.GraphvizEdge" [color=8,
                  group=7,
                  label=GraphvizEdge,
                  shape=box];
              "abjad.tools.documentationtools.GraphvizField.GraphvizField" [color=8,
                  group=7,
                  label=GraphvizField,
                  shape=box];
              "abjad.tools.documentationtools.GraphvizGraph.GraphvizGraph" [color=8,
                  group=7,
                  label=GraphvizGraph,
                  shape=box];
              "abjad.tools.documentationtools.GraphvizGroup.GraphvizGroup" [color=8,
                  group=7,
                  label=GraphvizGroup,
                  shape=box];
              "abjad.tools.documentationtools.GraphvizMixin.GraphvizMixin" [color=8,
                  group=7,
                  label=GraphvizMixin,
                  shape=oval,
                  style=bold];
              "abjad.tools.documentationtools.GraphvizNode.GraphvizNode" [color=8,
                  group=7,
                  label=GraphvizNode,
                  shape=box];
              "abjad.tools.documentationtools.GraphvizSubgraph.GraphvizSubgraph" [color=8,
                  group=7,
                  label=GraphvizSubgraph,
                  shape=box];
              "abjad.tools.documentationtools.GraphvizTable.GraphvizTable" [color=8,
                  group=7,
                  label=GraphvizTable,
                  shape=box];
              "abjad.tools.documentationtools.GraphvizTableCell.GraphvizTableCell" [color=8,
                  group=7,
                  label=GraphvizTableCell,
                  shape=box];
              "abjad.tools.documentationtools.GraphvizTableHorizontalRule.GraphvizTableHorizontalRule" [color=8,
                  group=7,
                  label=GraphvizTableHorizontalRule,
                  shape=box];
              "abjad.tools.documentationtools.GraphvizTableRow.GraphvizTableRow" [color=8,
                  group=7,
                  label=GraphvizTableRow,
                  shape=box];
              "abjad.tools.documentationtools.GraphvizTableVerticalRule.GraphvizTableVerticalRule" [color=8,
                  group=7,
                  label=GraphvizTableVerticalRule,
                  shape=box];
              "abjad.tools.documentationtools.InheritanceGraph.InheritanceGraph" [color=8,
                  group=7,
                  label=InheritanceGraph,
                  shape=box];
              "abjad.tools.documentationtools.ReSTAutodocDirective.ReSTAutodocDirective" [color=8,
                  group=7,
                  label=ReSTAutodocDirective,
                  shape=box];
              "abjad.tools.documentationtools.ReSTAutosummaryDirective.ReSTAutosummaryDirective" [color=8,
                  group=7,
                  label=ReSTAutosummaryDirective,
                  shape=box];
              "abjad.tools.documentationtools.ReSTAutosummaryItem.ReSTAutosummaryItem" [color=8,
                  group=7,
                  label=ReSTAutosummaryItem,
                  shape=box];
              "abjad.tools.documentationtools.ReSTDirective.ReSTDirective" [color=8,
                  group=7,
                  label=ReSTDirective,
                  shape=box];
              "abjad.tools.documentationtools.ReSTDocument.ReSTDocument" [color=8,
                  group=7,
                  label=ReSTDocument,
                  shape=box];
              "abjad.tools.documentationtools.ReSTGraphvizDirective.ReSTGraphvizDirective" [color=8,
                  group=7,
                  label=ReSTGraphvizDirective,
                  shape=box];
              "abjad.tools.documentationtools.ReSTHeading.ReSTHeading" [color=8,
                  group=7,
                  label=ReSTHeading,
                  shape=box];
              "abjad.tools.documentationtools.ReSTHorizontalRule.ReSTHorizontalRule" [color=8,
                  group=7,
                  label=ReSTHorizontalRule,
                  shape=box];
              "abjad.tools.documentationtools.ReSTInheritanceDiagram.ReSTInheritanceDiagram" [color=8,
                  group=7,
                  label=ReSTInheritanceDiagram,
                  shape=box];
              "abjad.tools.documentationtools.ReSTLineageDirective.ReSTLineageDirective" [color=8,
                  group=7,
                  label=ReSTLineageDirective,
                  shape=box];
              "abjad.tools.documentationtools.ReSTOnlyDirective.ReSTOnlyDirective" [color=8,
                  group=7,
                  label=ReSTOnlyDirective,
                  shape=box];
              "abjad.tools.documentationtools.ReSTParagraph.ReSTParagraph" [color=8,
                  group=7,
                  label=ReSTParagraph,
                  shape=box];
              "abjad.tools.documentationtools.ReSTTOCDirective.ReSTTOCDirective" [color=8,
                  group=7,
                  label=ReSTTOCDirective,
                  shape=box];
              "abjad.tools.documentationtools.ReSTTOCItem.ReSTTOCItem" [color=8,
                  group=7,
                  label=ReSTTOCItem,
                  shape=box];
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
          subgraph cluster_durationtools {
              graph [label=durationtools];
              "abjad.tools.durationtools.Division.Division" [color=9,
                  group=8,
                  label=Division,
                  shape=box];
              "abjad.tools.durationtools.Duration.Duration" [color=9,
                  group=8,
                  label=Duration,
                  shape=box];
              "abjad.tools.durationtools.Multiplier.Multiplier" [color=9,
                  group=8,
                  label=Multiplier,
                  shape=box];
              "abjad.tools.durationtools.Offset.Offset" [color=9,
                  group=8,
                  label=Offset,
                  shape=box];
              "abjad.tools.durationtools.Duration.Duration" -> "abjad.tools.durationtools.Multiplier.Multiplier";
              "abjad.tools.durationtools.Duration.Duration" -> "abjad.tools.durationtools.Offset.Offset";
          }
          subgraph cluster_expressiontools {
              graph [label=expressiontools];
              "abjad.tools.expressiontools.Callback.Callback" [color=1,
                  group=9,
                  label=Callback,
                  shape=box];
              "abjad.tools.expressiontools.Expression.Expression" [color=1,
                  group=9,
                  label=Expression,
                  shape=box];
              "abjad.tools.expressiontools.LabelExpression.LabelExpression" [color=1,
                  group=9,
                  label=LabelExpression,
                  shape=box];
              "abjad.tools.expressiontools.SequenceExpression.SequenceExpression" [color=1,
                  group=9,
                  label=SequenceExpression,
                  shape=box];
              "abjad.tools.expressiontools.Expression.Expression" -> "abjad.tools.expressiontools.LabelExpression.LabelExpression";
              "abjad.tools.expressiontools.Expression.Expression" -> "abjad.tools.expressiontools.SequenceExpression.SequenceExpression";
          }
          subgraph cluster_indicatortools {
              graph [label=indicatortools];
              "abjad.tools.indicatortools.Accelerando.Accelerando" [color=3,
                  group=11,
                  label=Accelerando,
                  shape=box];
              "abjad.tools.indicatortools.Annotation.Annotation" [color=3,
                  group=11,
                  label=Annotation,
                  shape=box];
              "abjad.tools.indicatortools.Arpeggio.Arpeggio" [color=3,
                  group=11,
                  label=Arpeggio,
                  shape=box];
              "abjad.tools.indicatortools.Arrow.Arrow" [color=3,
                  group=11,
                  label=Arrow,
                  shape=box];
              "abjad.tools.indicatortools.Articulation.Articulation" [color=3,
                  group=11,
                  label=Articulation,
                  shape=box];
              "abjad.tools.indicatortools.BarLine.BarLine" [color=3,
                  group=11,
                  label=BarLine,
                  shape=box];
              "abjad.tools.indicatortools.BendAfter.BendAfter" [color=3,
                  group=11,
                  label=BendAfter,
                  shape=box];
              "abjad.tools.indicatortools.BowContactPoint.BowContactPoint" [color=3,
                  group=11,
                  label=BowContactPoint,
                  shape=box];
              "abjad.tools.indicatortools.BowMotionTechnique.BowMotionTechnique" [color=3,
                  group=11,
                  label=BowMotionTechnique,
                  shape=box];
              "abjad.tools.indicatortools.BowPressure.BowPressure" [color=3,
                  group=11,
                  label=BowPressure,
                  shape=box];
              "abjad.tools.indicatortools.BreathMark.BreathMark" [color=3,
                  group=11,
                  label=BreathMark,
                  shape=box];
              "abjad.tools.indicatortools.Clef.Clef" [color=3,
                  group=11,
                  label=Clef,
                  shape=box];
              "abjad.tools.indicatortools.ClefInventory.ClefInventory" [color=3,
                  group=11,
                  label=ClefInventory,
                  shape=box];
              "abjad.tools.indicatortools.ColorFingering.ColorFingering" [color=3,
                  group=11,
                  label=ColorFingering,
                  shape=box];
              "abjad.tools.indicatortools.Dynamic.Dynamic" [color=3,
                  group=11,
                  label=Dynamic,
                  shape=box];
              "abjad.tools.indicatortools.Fermata.Fermata" [color=3,
                  group=11,
                  label=Fermata,
                  shape=box];
              "abjad.tools.indicatortools.IndicatorExpression.IndicatorExpression" [color=3,
                  group=11,
                  label=IndicatorExpression,
                  shape=box];
              "abjad.tools.indicatortools.IsAtSoundingPitch.IsAtSoundingPitch" [color=3,
                  group=11,
                  label=IsAtSoundingPitch,
                  shape=box];
              "abjad.tools.indicatortools.IsUnpitched.IsUnpitched" [color=3,
                  group=11,
                  label=IsUnpitched,
                  shape=box];
              "abjad.tools.indicatortools.KeyCluster.KeyCluster" [color=3,
                  group=11,
                  label=KeyCluster,
                  shape=box];
              "abjad.tools.indicatortools.KeySignature.KeySignature" [color=3,
                  group=11,
                  label=KeySignature,
                  shape=box];
              "abjad.tools.indicatortools.LaissezVibrer.LaissezVibrer" [color=3,
                  group=11,
                  label=LaissezVibrer,
                  shape=box];
              "abjad.tools.indicatortools.LilyPondCommand.LilyPondCommand" [color=3,
                  group=11,
                  label=LilyPondCommand,
                  shape=box];
              "abjad.tools.indicatortools.LilyPondComment.LilyPondComment" [color=3,
                  group=11,
                  label=LilyPondComment,
                  shape=box];
              "abjad.tools.indicatortools.LineSegment.LineSegment" [color=3,
                  group=11,
                  label=LineSegment,
                  shape=box];
              "abjad.tools.indicatortools.MetricModulation.MetricModulation" [color=3,
                  group=11,
                  label=MetricModulation,
                  shape=box];
              "abjad.tools.indicatortools.PageBreak.PageBreak" [color=3,
                  group=11,
                  label=PageBreak,
                  shape=box];
              "abjad.tools.indicatortools.RehearsalMark.RehearsalMark" [color=3,
                  group=11,
                  label=RehearsalMark,
                  shape=box];
              "abjad.tools.indicatortools.Repeat.Repeat" [color=3,
                  group=11,
                  label=Repeat,
                  shape=box];
              "abjad.tools.indicatortools.Ritardando.Ritardando" [color=3,
                  group=11,
                  label=Ritardando,
                  shape=box];
              "abjad.tools.indicatortools.SpacingIndication.SpacingIndication" [color=3,
                  group=11,
                  label=SpacingIndication,
                  shape=box];
              "abjad.tools.indicatortools.StaffChange.StaffChange" [color=3,
                  group=11,
                  label=StaffChange,
                  shape=box];
              "abjad.tools.indicatortools.StemTremolo.StemTremolo" [color=3,
                  group=11,
                  label=StemTremolo,
                  shape=box];
              "abjad.tools.indicatortools.StringContactPoint.StringContactPoint" [color=3,
                  group=11,
                  label=StringContactPoint,
                  shape=box];
              "abjad.tools.indicatortools.StringNumber.StringNumber" [color=3,
                  group=11,
                  label=StringNumber,
                  shape=box];
              "abjad.tools.indicatortools.SystemBreak.SystemBreak" [color=3,
                  group=11,
                  label=SystemBreak,
                  shape=box];
              "abjad.tools.indicatortools.Tempo.Tempo" [color=3,
                  group=11,
                  label=Tempo,
                  shape=box];
              "abjad.tools.indicatortools.TempoInventory.TempoInventory" [color=3,
                  group=11,
                  label=TempoInventory,
                  shape=box];
              "abjad.tools.indicatortools.TimeSignature.TimeSignature" [color=3,
                  group=11,
                  label=TimeSignature,
                  shape=box];
              "abjad.tools.indicatortools.TimeSignatureInventory.TimeSignatureInventory" [color=3,
                  group=11,
                  label=TimeSignatureInventory,
                  shape=box];
              "abjad.tools.indicatortools.Tremolo.Tremolo" [color=3,
                  group=11,
                  label=Tremolo,
                  shape=box];
              "abjad.tools.indicatortools.Tuning.Tuning" [color=3,
                  group=11,
                  label=Tuning,
                  shape=box];
              "abjad.tools.indicatortools.LineSegment.LineSegment" -> "abjad.tools.indicatortools.Arrow.Arrow";
          }
          subgraph cluster_instrumenttools {
              graph [label=instrumenttools];
              "abjad.tools.instrumenttools.Accordion.Accordion" [color=4,
                  group=12,
                  label=Accordion,
                  shape=box];
              "abjad.tools.instrumenttools.AltoFlute.AltoFlute" [color=4,
                  group=12,
                  label=AltoFlute,
                  shape=box];
              "abjad.tools.instrumenttools.AltoSaxophone.AltoSaxophone" [color=4,
                  group=12,
                  label=AltoSaxophone,
                  shape=box];
              "abjad.tools.instrumenttools.AltoTrombone.AltoTrombone" [color=4,
                  group=12,
                  label=AltoTrombone,
                  shape=box];
              "abjad.tools.instrumenttools.AltoVoice.AltoVoice" [color=4,
                  group=12,
                  label=AltoVoice,
                  shape=box];
              "abjad.tools.instrumenttools.BaritoneSaxophone.BaritoneSaxophone" [color=4,
                  group=12,
                  label=BaritoneSaxophone,
                  shape=box];
              "abjad.tools.instrumenttools.BaritoneVoice.BaritoneVoice" [color=4,
                  group=12,
                  label=BaritoneVoice,
                  shape=box];
              "abjad.tools.instrumenttools.BassClarinet.BassClarinet" [color=4,
                  group=12,
                  label=BassClarinet,
                  shape=box];
              "abjad.tools.instrumenttools.BassFlute.BassFlute" [color=4,
                  group=12,
                  label=BassFlute,
                  shape=box];
              "abjad.tools.instrumenttools.BassSaxophone.BassSaxophone" [color=4,
                  group=12,
                  label=BassSaxophone,
                  shape=box];
              "abjad.tools.instrumenttools.BassTrombone.BassTrombone" [color=4,
                  group=12,
                  label=BassTrombone,
                  shape=box];
              "abjad.tools.instrumenttools.BassVoice.BassVoice" [color=4,
                  group=12,
                  label=BassVoice,
                  shape=box];
              "abjad.tools.instrumenttools.Bassoon.Bassoon" [color=4,
                  group=12,
                  label=Bassoon,
                  shape=box];
              "abjad.tools.instrumenttools.Cello.Cello" [color=4,
                  group=12,
                  label=Cello,
                  shape=box];
              "abjad.tools.instrumenttools.ClarinetInA.ClarinetInA" [color=4,
                  group=12,
                  label=ClarinetInA,
                  shape=box];
              "abjad.tools.instrumenttools.ClarinetInBFlat.ClarinetInBFlat" [color=4,
                  group=12,
                  label=ClarinetInBFlat,
                  shape=box];
              "abjad.tools.instrumenttools.ClarinetInEFlat.ClarinetInEFlat" [color=4,
                  group=12,
                  label=ClarinetInEFlat,
                  shape=box];
              "abjad.tools.instrumenttools.Contrabass.Contrabass" [color=4,
                  group=12,
                  label=Contrabass,
                  shape=box];
              "abjad.tools.instrumenttools.ContrabassClarinet.ContrabassClarinet" [color=4,
                  group=12,
                  label=ContrabassClarinet,
                  shape=box];
              "abjad.tools.instrumenttools.ContrabassFlute.ContrabassFlute" [color=4,
                  group=12,
                  label=ContrabassFlute,
                  shape=box];
              "abjad.tools.instrumenttools.ContrabassSaxophone.ContrabassSaxophone" [color=4,
                  group=12,
                  label=ContrabassSaxophone,
                  shape=box];
              "abjad.tools.instrumenttools.Contrabassoon.Contrabassoon" [color=4,
                  group=12,
                  label=Contrabassoon,
                  shape=box];
              "abjad.tools.instrumenttools.EnglishHorn.EnglishHorn" [color=4,
                  group=12,
                  label=EnglishHorn,
                  shape=box];
              "abjad.tools.instrumenttools.Flute.Flute" [color=4,
                  group=12,
                  label=Flute,
                  shape=box];
              "abjad.tools.instrumenttools.FrenchHorn.FrenchHorn" [color=4,
                  group=12,
                  label=FrenchHorn,
                  shape=box];
              "abjad.tools.instrumenttools.Glockenspiel.Glockenspiel" [color=4,
                  group=12,
                  label=Glockenspiel,
                  shape=box];
              "abjad.tools.instrumenttools.Guitar.Guitar" [color=4,
                  group=12,
                  label=Guitar,
                  shape=box];
              "abjad.tools.instrumenttools.Harp.Harp" [color=4,
                  group=12,
                  label=Harp,
                  shape=box];
              "abjad.tools.instrumenttools.Harpsichord.Harpsichord" [color=4,
                  group=12,
                  label=Harpsichord,
                  shape=box];
              "abjad.tools.instrumenttools.Instrument.Instrument" [color=4,
                  group=12,
                  label=Instrument,
                  shape=box];
              "abjad.tools.instrumenttools.InstrumentInventory.InstrumentInventory" [color=4,
                  group=12,
                  label=InstrumentInventory,
                  shape=box];
              "abjad.tools.instrumenttools.Marimba.Marimba" [color=4,
                  group=12,
                  label=Marimba,
                  shape=box];
              "abjad.tools.instrumenttools.MezzoSopranoVoice.MezzoSopranoVoice" [color=4,
                  group=12,
                  label=MezzoSopranoVoice,
                  shape=box];
              "abjad.tools.instrumenttools.Oboe.Oboe" [color=4,
                  group=12,
                  label=Oboe,
                  shape=box];
              "abjad.tools.instrumenttools.Percussion.Percussion" [color=4,
                  group=12,
                  label=Percussion,
                  shape=box];
              "abjad.tools.instrumenttools.Performer.Performer" [color=4,
                  group=12,
                  label=Performer,
                  shape=box];
              "abjad.tools.instrumenttools.PerformerInventory.PerformerInventory" [color=4,
                  group=12,
                  label=PerformerInventory,
                  shape=box];
              "abjad.tools.instrumenttools.Piano.Piano" [color=4,
                  group=12,
                  label=Piano,
                  shape=box];
              "abjad.tools.instrumenttools.Piccolo.Piccolo" [color=4,
                  group=12,
                  label=Piccolo,
                  shape=box];
              "abjad.tools.instrumenttools.SopraninoSaxophone.SopraninoSaxophone" [color=4,
                  group=12,
                  label=SopraninoSaxophone,
                  shape=box];
              "abjad.tools.instrumenttools.SopranoSaxophone.SopranoSaxophone" [color=4,
                  group=12,
                  label=SopranoSaxophone,
                  shape=box];
              "abjad.tools.instrumenttools.SopranoVoice.SopranoVoice" [color=4,
                  group=12,
                  label=SopranoVoice,
                  shape=box];
              "abjad.tools.instrumenttools.TenorSaxophone.TenorSaxophone" [color=4,
                  group=12,
                  label=TenorSaxophone,
                  shape=box];
              "abjad.tools.instrumenttools.TenorTrombone.TenorTrombone" [color=4,
                  group=12,
                  label=TenorTrombone,
                  shape=box];
              "abjad.tools.instrumenttools.TenorVoice.TenorVoice" [color=4,
                  group=12,
                  label=TenorVoice,
                  shape=box];
              "abjad.tools.instrumenttools.Trumpet.Trumpet" [color=4,
                  group=12,
                  label=Trumpet,
                  shape=box];
              "abjad.tools.instrumenttools.Tuba.Tuba" [color=4,
                  group=12,
                  label=Tuba,
                  shape=box];
              "abjad.tools.instrumenttools.Vibraphone.Vibraphone" [color=4,
                  group=12,
                  label=Vibraphone,
                  shape=box];
              "abjad.tools.instrumenttools.Viola.Viola" [color=4,
                  group=12,
                  label=Viola,
                  shape=box];
              "abjad.tools.instrumenttools.Violin.Violin" [color=4,
                  group=12,
                  label=Violin,
                  shape=box];
              "abjad.tools.instrumenttools.WoodwindFingering.WoodwindFingering" [color=4,
                  group=12,
                  label=WoodwindFingering,
                  shape=box];
              "abjad.tools.instrumenttools.Xylophone.Xylophone" [color=4,
                  group=12,
                  label=Xylophone,
                  shape=box];
              "abjad.tools.instrumenttools.Instrument.Instrument" -> "abjad.tools.instrumenttools.Accordion.Accordion";
              "abjad.tools.instrumenttools.Instrument.Instrument" -> "abjad.tools.instrumenttools.AltoFlute.AltoFlute";
              "abjad.tools.instrumenttools.Instrument.Instrument" -> "abjad.tools.instrumenttools.AltoSaxophone.AltoSaxophone";
              "abjad.tools.instrumenttools.Instrument.Instrument" -> "abjad.tools.instrumenttools.AltoTrombone.AltoTrombone";
              "abjad.tools.instrumenttools.Instrument.Instrument" -> "abjad.tools.instrumenttools.AltoVoice.AltoVoice";
              "abjad.tools.instrumenttools.Instrument.Instrument" -> "abjad.tools.instrumenttools.BaritoneSaxophone.BaritoneSaxophone";
              "abjad.tools.instrumenttools.Instrument.Instrument" -> "abjad.tools.instrumenttools.BaritoneVoice.BaritoneVoice";
              "abjad.tools.instrumenttools.Instrument.Instrument" -> "abjad.tools.instrumenttools.BassClarinet.BassClarinet";
              "abjad.tools.instrumenttools.Instrument.Instrument" -> "abjad.tools.instrumenttools.BassFlute.BassFlute";
              "abjad.tools.instrumenttools.Instrument.Instrument" -> "abjad.tools.instrumenttools.BassSaxophone.BassSaxophone";
              "abjad.tools.instrumenttools.Instrument.Instrument" -> "abjad.tools.instrumenttools.BassTrombone.BassTrombone";
              "abjad.tools.instrumenttools.Instrument.Instrument" -> "abjad.tools.instrumenttools.BassVoice.BassVoice";
              "abjad.tools.instrumenttools.Instrument.Instrument" -> "abjad.tools.instrumenttools.Bassoon.Bassoon";
              "abjad.tools.instrumenttools.Instrument.Instrument" -> "abjad.tools.instrumenttools.Cello.Cello";
              "abjad.tools.instrumenttools.Instrument.Instrument" -> "abjad.tools.instrumenttools.ClarinetInA.ClarinetInA";
              "abjad.tools.instrumenttools.Instrument.Instrument" -> "abjad.tools.instrumenttools.ClarinetInBFlat.ClarinetInBFlat";
              "abjad.tools.instrumenttools.Instrument.Instrument" -> "abjad.tools.instrumenttools.ClarinetInEFlat.ClarinetInEFlat";
              "abjad.tools.instrumenttools.Instrument.Instrument" -> "abjad.tools.instrumenttools.Contrabass.Contrabass";
              "abjad.tools.instrumenttools.Instrument.Instrument" -> "abjad.tools.instrumenttools.ContrabassClarinet.ContrabassClarinet";
              "abjad.tools.instrumenttools.Instrument.Instrument" -> "abjad.tools.instrumenttools.ContrabassFlute.ContrabassFlute";
              "abjad.tools.instrumenttools.Instrument.Instrument" -> "abjad.tools.instrumenttools.ContrabassSaxophone.ContrabassSaxophone";
              "abjad.tools.instrumenttools.Instrument.Instrument" -> "abjad.tools.instrumenttools.Contrabassoon.Contrabassoon";
              "abjad.tools.instrumenttools.Instrument.Instrument" -> "abjad.tools.instrumenttools.EnglishHorn.EnglishHorn";
              "abjad.tools.instrumenttools.Instrument.Instrument" -> "abjad.tools.instrumenttools.Flute.Flute";
              "abjad.tools.instrumenttools.Instrument.Instrument" -> "abjad.tools.instrumenttools.FrenchHorn.FrenchHorn";
              "abjad.tools.instrumenttools.Instrument.Instrument" -> "abjad.tools.instrumenttools.Glockenspiel.Glockenspiel";
              "abjad.tools.instrumenttools.Instrument.Instrument" -> "abjad.tools.instrumenttools.Guitar.Guitar";
              "abjad.tools.instrumenttools.Instrument.Instrument" -> "abjad.tools.instrumenttools.Harp.Harp";
              "abjad.tools.instrumenttools.Instrument.Instrument" -> "abjad.tools.instrumenttools.Harpsichord.Harpsichord";
              "abjad.tools.instrumenttools.Instrument.Instrument" -> "abjad.tools.instrumenttools.Marimba.Marimba";
              "abjad.tools.instrumenttools.Instrument.Instrument" -> "abjad.tools.instrumenttools.MezzoSopranoVoice.MezzoSopranoVoice";
              "abjad.tools.instrumenttools.Instrument.Instrument" -> "abjad.tools.instrumenttools.Oboe.Oboe";
              "abjad.tools.instrumenttools.Instrument.Instrument" -> "abjad.tools.instrumenttools.Percussion.Percussion";
              "abjad.tools.instrumenttools.Instrument.Instrument" -> "abjad.tools.instrumenttools.Piano.Piano";
              "abjad.tools.instrumenttools.Instrument.Instrument" -> "abjad.tools.instrumenttools.Piccolo.Piccolo";
              "abjad.tools.instrumenttools.Instrument.Instrument" -> "abjad.tools.instrumenttools.SopraninoSaxophone.SopraninoSaxophone";
              "abjad.tools.instrumenttools.Instrument.Instrument" -> "abjad.tools.instrumenttools.SopranoSaxophone.SopranoSaxophone";
              "abjad.tools.instrumenttools.Instrument.Instrument" -> "abjad.tools.instrumenttools.SopranoVoice.SopranoVoice";
              "abjad.tools.instrumenttools.Instrument.Instrument" -> "abjad.tools.instrumenttools.TenorSaxophone.TenorSaxophone";
              "abjad.tools.instrumenttools.Instrument.Instrument" -> "abjad.tools.instrumenttools.TenorTrombone.TenorTrombone";
              "abjad.tools.instrumenttools.Instrument.Instrument" -> "abjad.tools.instrumenttools.TenorVoice.TenorVoice";
              "abjad.tools.instrumenttools.Instrument.Instrument" -> "abjad.tools.instrumenttools.Trumpet.Trumpet";
              "abjad.tools.instrumenttools.Instrument.Instrument" -> "abjad.tools.instrumenttools.Tuba.Tuba";
              "abjad.tools.instrumenttools.Instrument.Instrument" -> "abjad.tools.instrumenttools.Vibraphone.Vibraphone";
              "abjad.tools.instrumenttools.Instrument.Instrument" -> "abjad.tools.instrumenttools.Viola.Viola";
              "abjad.tools.instrumenttools.Instrument.Instrument" -> "abjad.tools.instrumenttools.Violin.Violin";
              "abjad.tools.instrumenttools.Instrument.Instrument" -> "abjad.tools.instrumenttools.Xylophone.Xylophone";
          }
          subgraph cluster_lilypondfiletools {
              graph [label=lilypondfiletools];
              "abjad.tools.lilypondfiletools.Block.Block" [color=6,
                  group=14,
                  label=Block,
                  shape=box];
              "abjad.tools.lilypondfiletools.ContextBlock.ContextBlock" [color=6,
                  group=14,
                  label=ContextBlock,
                  shape=box];
              "abjad.tools.lilypondfiletools.DateTimeToken.DateTimeToken" [color=6,
                  group=14,
                  label=DateTimeToken,
                  shape=box];
              "abjad.tools.lilypondfiletools.LilyPondDimension.LilyPondDimension" [color=6,
                  group=14,
                  label=LilyPondDimension,
                  shape=box];
              "abjad.tools.lilypondfiletools.LilyPondFile.LilyPondFile" [color=6,
                  group=14,
                  label=LilyPondFile,
                  shape=box];
              "abjad.tools.lilypondfiletools.LilyPondLanguageToken.LilyPondLanguageToken" [color=6,
                  group=14,
                  label=LilyPondLanguageToken,
                  shape=box];
              "abjad.tools.lilypondfiletools.LilyPondVersionToken.LilyPondVersionToken" [color=6,
                  group=14,
                  label=LilyPondVersionToken,
                  shape=box];
              "abjad.tools.lilypondfiletools.PackageGitCommitToken.PackageGitCommitToken" [color=6,
                  group=14,
                  label=PackageGitCommitToken,
                  shape=box];
              "abjad.tools.lilypondfiletools.Block.Block" -> "abjad.tools.lilypondfiletools.ContextBlock.ContextBlock";
          }
          subgraph cluster_lilypondnametools {
              graph [label=lilypondnametools];
              "abjad.tools.lilypondnametools.LilyPondContext.LilyPondContext" [color=7,
                  group=15,
                  label=LilyPondContext,
                  shape=box];
              "abjad.tools.lilypondnametools.LilyPondContextSetting.LilyPondContextSetting" [color=7,
                  group=15,
                  label=LilyPondContextSetting,
                  shape=box];
              "abjad.tools.lilypondnametools.LilyPondEngraver.LilyPondEngraver" [color=7,
                  group=15,
                  label=LilyPondEngraver,
                  shape=box];
              "abjad.tools.lilypondnametools.LilyPondGrob.LilyPondGrob" [color=7,
                  group=15,
                  label=LilyPondGrob,
                  shape=box];
              "abjad.tools.lilypondnametools.LilyPondGrobInterface.LilyPondGrobInterface" [color=7,
                  group=15,
                  label=LilyPondGrobInterface,
                  shape=box];
              "abjad.tools.lilypondnametools.LilyPondGrobNameManager.LilyPondGrobNameManager" [color=7,
                  group=15,
                  label=LilyPondGrobNameManager,
                  shape=box];
              "abjad.tools.lilypondnametools.LilyPondGrobOverride.LilyPondGrobOverride" [color=7,
                  group=15,
                  label=LilyPondGrobOverride,
                  shape=box];
              "abjad.tools.lilypondnametools.LilyPondNameManager.LilyPondNameManager" [color=7,
                  group=15,
                  label=LilyPondNameManager,
                  shape=box];
              "abjad.tools.lilypondnametools.LilyPondSettingNameManager.LilyPondSettingNameManager" [color=7,
                  group=15,
                  label=LilyPondSettingNameManager,
                  shape=box];
              "abjad.tools.lilypondnametools.LilyPondNameManager.LilyPondNameManager" -> "abjad.tools.lilypondnametools.LilyPondGrobNameManager.LilyPondGrobNameManager";
              "abjad.tools.lilypondnametools.LilyPondNameManager.LilyPondNameManager" -> "abjad.tools.lilypondnametools.LilyPondSettingNameManager.LilyPondSettingNameManager";
          }
          subgraph cluster_lilypondparsertools {
              graph [label=lilypondparsertools];
              "abjad.tools.lilypondparsertools.ContextSpeccedMusic.ContextSpeccedMusic" [color=8,
                  group=16,
                  label=ContextSpeccedMusic,
                  shape=box];
              "abjad.tools.lilypondparsertools.GuileProxy.GuileProxy" [color=8,
                  group=16,
                  label=GuileProxy,
                  shape=box];
              "abjad.tools.lilypondparsertools.LilyPondDuration.LilyPondDuration" [color=8,
                  group=16,
                  label=LilyPondDuration,
                  shape=box];
              "abjad.tools.lilypondparsertools.LilyPondEvent.LilyPondEvent" [color=8,
                  group=16,
                  label=LilyPondEvent,
                  shape=box];
              "abjad.tools.lilypondparsertools.LilyPondFraction.LilyPondFraction" [color=8,
                  group=16,
                  label=LilyPondFraction,
                  shape=box];
              "abjad.tools.lilypondparsertools.LilyPondGrammarGenerator.LilyPondGrammarGenerator" [color=8,
                  group=16,
                  label=LilyPondGrammarGenerator,
                  shape=box];
              "abjad.tools.lilypondparsertools.LilyPondLexicalDefinition.LilyPondLexicalDefinition" [color=8,
                  group=16,
                  label=LilyPondLexicalDefinition,
                  shape=box];
              "abjad.tools.lilypondparsertools.LilyPondParser.LilyPondParser" [color=8,
                  group=16,
                  label=LilyPondParser,
                  shape=box];
              "abjad.tools.lilypondparsertools.LilyPondSyntacticalDefinition.LilyPondSyntacticalDefinition" [color=8,
                  group=16,
                  label=LilyPondSyntacticalDefinition,
                  shape=box];
              "abjad.tools.lilypondparsertools.Music.Music" [color=8,
                  group=16,
                  label=Music,
                  shape=oval,
                  style=bold];
              "abjad.tools.lilypondparsertools.ReducedLyParser.ReducedLyParser" [color=8,
                  group=16,
                  label=ReducedLyParser,
                  shape=box];
              "abjad.tools.lilypondparsertools.SchemeParser.SchemeParser" [color=8,
                  group=16,
                  label=SchemeParser,
                  shape=box];
              "abjad.tools.lilypondparsertools.SequentialMusic.SequentialMusic" [color=8,
                  group=16,
                  label=SequentialMusic,
                  shape=box];
              "abjad.tools.lilypondparsertools.SimultaneousMusic.SimultaneousMusic" [color=8,
                  group=16,
                  label=SimultaneousMusic,
                  shape=oval,
                  style=bold];
              "abjad.tools.lilypondparsertools.SyntaxNode.SyntaxNode" [color=8,
                  group=16,
                  label=SyntaxNode,
                  shape=box];
              "abjad.tools.lilypondparsertools.Music.Music" -> "abjad.tools.lilypondparsertools.ContextSpeccedMusic.ContextSpeccedMusic";
              "abjad.tools.lilypondparsertools.Music.Music" -> "abjad.tools.lilypondparsertools.SequentialMusic.SequentialMusic";
              "abjad.tools.lilypondparsertools.Music.Music" -> "abjad.tools.lilypondparsertools.SimultaneousMusic.SimultaneousMusic";
          }
          subgraph cluster_markuptools {
              graph [label=markuptools];
              "abjad.tools.markuptools.Markup.Markup" [color=1,
                  group=18,
                  label=Markup,
                  shape=box];
              "abjad.tools.markuptools.MarkupCommand.MarkupCommand" [color=1,
                  group=18,
                  label=MarkupCommand,
                  shape=box];
              "abjad.tools.markuptools.MarkupInventory.MarkupInventory" [color=1,
                  group=18,
                  label=MarkupInventory,
                  shape=box];
              "abjad.tools.markuptools.Postscript.Postscript" [color=1,
                  group=18,
                  label=Postscript,
                  shape=box];
              "abjad.tools.markuptools.PostscriptOperator.PostscriptOperator" [color=1,
                  group=18,
                  label=PostscriptOperator,
                  shape=box];
          }
          subgraph cluster_mathtools {
              graph [label=mathtools];
              "abjad.tools.mathtools.BoundedObject.BoundedObject" [color=2,
                  group=19,
                  label=BoundedObject,
                  shape=box];
              "abjad.tools.mathtools.Infinity.Infinity" [color=2,
                  group=19,
                  label=Infinity,
                  shape=box];
              "abjad.tools.mathtools.NegativeInfinity.NegativeInfinity" [color=2,
                  group=19,
                  label=NegativeInfinity,
                  shape=box];
              "abjad.tools.mathtools.NonreducedFraction.NonreducedFraction" [color=2,
                  group=19,
                  label=NonreducedFraction,
                  shape=box];
              "abjad.tools.mathtools.NonreducedRatio.NonreducedRatio" [color=2,
                  group=19,
                  label=NonreducedRatio,
                  shape=box];
              "abjad.tools.mathtools.Ratio.Ratio" [color=2,
                  group=19,
                  label=Ratio,
                  shape=box];
              "abjad.tools.mathtools.Infinity.Infinity" -> "abjad.tools.mathtools.NegativeInfinity.NegativeInfinity";
              "abjad.tools.mathtools.NonreducedRatio.NonreducedRatio" -> "abjad.tools.mathtools.Ratio.Ratio";
          }
          subgraph cluster_metertools {
              graph [label=metertools];
              "abjad.tools.metertools.Meter.Meter" [color=3,
                  group=20,
                  label=Meter,
                  shape=box];
              "abjad.tools.metertools.MeterFittingSession.MeterFittingSession" [color=3,
                  group=20,
                  label=MeterFittingSession,
                  shape=box];
              "abjad.tools.metertools.MeterInventory.MeterInventory" [color=3,
                  group=20,
                  label=MeterInventory,
                  shape=box];
              "abjad.tools.metertools.MeterManager.MeterManager" [color=3,
                  group=20,
                  label=MeterManager,
                  shape=box];
              "abjad.tools.metertools.MetricAccentKernel.MetricAccentKernel" [color=3,
                  group=20,
                  label=MetricAccentKernel,
                  shape=box];
              "abjad.tools.metertools.OffsetCounter.OffsetCounter" [color=3,
                  group=20,
                  label=OffsetCounter,
                  shape=box];
          }
          subgraph cluster_patterntools {
              graph [label=patterntools];
              "abjad.tools.patterntools.CompoundPattern.CompoundPattern" [color=5,
                  group=22,
                  label=CompoundPattern,
                  shape=box];
              "abjad.tools.patterntools.Pattern.Pattern" [color=5,
                  group=22,
                  label=Pattern,
                  shape=box];
              "abjad.tools.patterntools.PatternInventory.PatternInventory" [color=5,
                  group=22,
                  label=PatternInventory,
                  shape=box];
          }
          subgraph cluster_pitchtools {
              graph [label=pitchtools];
              "abjad.tools.pitchtools.Accidental.Accidental" [color=6,
                  group=23,
                  label=Accidental,
                  shape=box];
              "abjad.tools.pitchtools.Interval.Interval" [color=6,
                  group=23,
                  label=Interval,
                  shape=oval,
                  style=bold];
              "abjad.tools.pitchtools.IntervalClass.IntervalClass" [color=6,
                  group=23,
                  label=IntervalClass,
                  shape=oval,
                  style=bold];
              "abjad.tools.pitchtools.IntervalClassSegment.IntervalClassSegment" [color=6,
                  group=23,
                  label=IntervalClassSegment,
                  shape=box];
              "abjad.tools.pitchtools.IntervalClassSet.IntervalClassSet" [color=6,
                  group=23,
                  label=IntervalClassSet,
                  shape=box];
              "abjad.tools.pitchtools.IntervalClassVector.IntervalClassVector" [color=6,
                  group=23,
                  label=IntervalClassVector,
                  shape=box];
              "abjad.tools.pitchtools.IntervalSegment.IntervalSegment" [color=6,
                  group=23,
                  label=IntervalSegment,
                  shape=box];
              "abjad.tools.pitchtools.IntervalSet.IntervalSet" [color=6,
                  group=23,
                  label=IntervalSet,
                  shape=box];
              "abjad.tools.pitchtools.IntervalVector.IntervalVector" [color=6,
                  group=23,
                  label=IntervalVector,
                  shape=box];
              "abjad.tools.pitchtools.Inversion.Inversion" [color=6,
                  group=23,
                  label=Inversion,
                  shape=box];
              "abjad.tools.pitchtools.Multiplication.Multiplication" [color=6,
                  group=23,
                  label=Multiplication,
                  shape=box];
              "abjad.tools.pitchtools.NamedInterval.NamedInterval" [color=6,
                  group=23,
                  label=NamedInterval,
                  shape=box];
              "abjad.tools.pitchtools.NamedIntervalClass.NamedIntervalClass" [color=6,
                  group=23,
                  label=NamedIntervalClass,
                  shape=box];
              "abjad.tools.pitchtools.NamedInversionEquivalentIntervalClass.NamedInversionEquivalentIntervalClass" [color=6,
                  group=23,
                  label=NamedInversionEquivalentIntervalClass,
                  shape=box];
              "abjad.tools.pitchtools.NamedPitch.NamedPitch" [color=6,
                  group=23,
                  label=NamedPitch,
                  shape=box];
              "abjad.tools.pitchtools.NamedPitchClass.NamedPitchClass" [color=6,
                  group=23,
                  label=NamedPitchClass,
                  shape=box];
              "abjad.tools.pitchtools.NumberedInterval.NumberedInterval" [color=6,
                  group=23,
                  label=NumberedInterval,
                  shape=box];
              "abjad.tools.pitchtools.NumberedIntervalClass.NumberedIntervalClass" [color=6,
                  group=23,
                  label=NumberedIntervalClass,
                  shape=box];
              "abjad.tools.pitchtools.NumberedInversionEquivalentIntervalClass.NumberedInversionEquivalentIntervalClass" [color=6,
                  group=23,
                  label=NumberedInversionEquivalentIntervalClass,
                  shape=box];
              "abjad.tools.pitchtools.NumberedPitch.NumberedPitch" [color=6,
                  group=23,
                  label=NumberedPitch,
                  shape=box];
              "abjad.tools.pitchtools.NumberedPitchClass.NumberedPitchClass" [color=6,
                  group=23,
                  label=NumberedPitchClass,
                  shape=box];
              "abjad.tools.pitchtools.NumberedPitchClassColorMap.NumberedPitchClassColorMap" [color=6,
                  group=23,
                  label=NumberedPitchClassColorMap,
                  shape=box];
              "abjad.tools.pitchtools.Octave.Octave" [color=6,
                  group=23,
                  label=Octave,
                  shape=box];
              "abjad.tools.pitchtools.Pitch.Pitch" [color=6,
                  group=23,
                  label=Pitch,
                  shape=oval,
                  style=bold];
              "abjad.tools.pitchtools.PitchArray.PitchArray" [color=6,
                  group=23,
                  label=PitchArray,
                  shape=box];
              "abjad.tools.pitchtools.PitchArrayCell.PitchArrayCell" [color=6,
                  group=23,
                  label=PitchArrayCell,
                  shape=box];
              "abjad.tools.pitchtools.PitchArrayColumn.PitchArrayColumn" [color=6,
                  group=23,
                  label=PitchArrayColumn,
                  shape=box];
              "abjad.tools.pitchtools.PitchArrayInventory.PitchArrayInventory" [color=6,
                  group=23,
                  label=PitchArrayInventory,
                  shape=box];
              "abjad.tools.pitchtools.PitchArrayRow.PitchArrayRow" [color=6,
                  group=23,
                  label=PitchArrayRow,
                  shape=box];
              "abjad.tools.pitchtools.PitchClass.PitchClass" [color=6,
                  group=23,
                  label=PitchClass,
                  shape=oval,
                  style=bold];
              "abjad.tools.pitchtools.PitchClassSegment.PitchClassSegment" [color=6,
                  group=23,
                  label=PitchClassSegment,
                  shape=box];
              "abjad.tools.pitchtools.PitchClassSet.PitchClassSet" [color=6,
                  group=23,
                  label=PitchClassSet,
                  shape=box];
              "abjad.tools.pitchtools.PitchClassTree.PitchClassTree" [color=6,
                  group=23,
                  label=PitchClassTree,
                  shape=box];
              "abjad.tools.pitchtools.PitchClassVector.PitchClassVector" [color=6,
                  group=23,
                  label=PitchClassVector,
                  shape=box];
              "abjad.tools.pitchtools.PitchOperation.PitchOperation" [color=6,
                  group=23,
                  label=PitchOperation,
                  shape=box];
              "abjad.tools.pitchtools.PitchRange.PitchRange" [color=6,
                  group=23,
                  label=PitchRange,
                  shape=box];
              "abjad.tools.pitchtools.PitchRangeInventory.PitchRangeInventory" [color=6,
                  group=23,
                  label=PitchRangeInventory,
                  shape=box];
              "abjad.tools.pitchtools.PitchSegment.PitchSegment" [color=6,
                  group=23,
                  label=PitchSegment,
                  shape=box];
              "abjad.tools.pitchtools.PitchSet.PitchSet" [color=6,
                  group=23,
                  label=PitchSet,
                  shape=box];
              "abjad.tools.pitchtools.PitchVector.PitchVector" [color=6,
                  group=23,
                  label=PitchVector,
                  shape=box];
              "abjad.tools.pitchtools.Registration.Registration" [color=6,
                  group=23,
                  label=Registration,
                  shape=box];
              "abjad.tools.pitchtools.RegistrationComponent.RegistrationComponent" [color=6,
                  group=23,
                  label=RegistrationComponent,
                  shape=box];
              "abjad.tools.pitchtools.RegistrationInventory.RegistrationInventory" [color=6,
                  group=23,
                  label=RegistrationInventory,
                  shape=box];
              "abjad.tools.pitchtools.Retrogression.Retrogression" [color=6,
                  group=23,
                  label=Retrogression,
                  shape=box];
              "abjad.tools.pitchtools.Rotation.Rotation" [color=6,
                  group=23,
                  label=Rotation,
                  shape=box];
              "abjad.tools.pitchtools.Segment.Segment" [color=6,
                  group=23,
                  label=Segment,
                  shape=oval,
                  style=bold];
              "abjad.tools.pitchtools.Set.Set" [color=6,
                  group=23,
                  label=Set,
                  shape=oval,
                  style=bold];
              "abjad.tools.pitchtools.StaffPosition.StaffPosition" [color=6,
                  group=23,
                  label=StaffPosition,
                  shape=box];
              "abjad.tools.pitchtools.Transposition.Transposition" [color=6,
                  group=23,
                  label=Transposition,
                  shape=box];
              "abjad.tools.pitchtools.TwelveToneRow.TwelveToneRow" [color=6,
                  group=23,
                  label=TwelveToneRow,
                  shape=box];
              "abjad.tools.pitchtools.Vector.Vector" [color=6,
                  group=23,
                  label=Vector,
                  shape=oval,
                  style=bold];
              "abjad.tools.pitchtools.Interval.Interval" -> "abjad.tools.pitchtools.NamedInterval.NamedInterval";
              "abjad.tools.pitchtools.Interval.Interval" -> "abjad.tools.pitchtools.NumberedInterval.NumberedInterval";
              "abjad.tools.pitchtools.IntervalClass.IntervalClass" -> "abjad.tools.pitchtools.NamedIntervalClass.NamedIntervalClass";
              "abjad.tools.pitchtools.IntervalClass.IntervalClass" -> "abjad.tools.pitchtools.NumberedIntervalClass.NumberedIntervalClass";
              "abjad.tools.pitchtools.NamedIntervalClass.NamedIntervalClass" -> "abjad.tools.pitchtools.NamedInversionEquivalentIntervalClass.NamedInversionEquivalentIntervalClass";
              "abjad.tools.pitchtools.NumberedIntervalClass.NumberedIntervalClass" -> "abjad.tools.pitchtools.NumberedInversionEquivalentIntervalClass.NumberedInversionEquivalentIntervalClass";
              "abjad.tools.pitchtools.Pitch.Pitch" -> "abjad.tools.pitchtools.NamedPitch.NamedPitch";
              "abjad.tools.pitchtools.Pitch.Pitch" -> "abjad.tools.pitchtools.NumberedPitch.NumberedPitch";
              "abjad.tools.pitchtools.PitchClass.PitchClass" -> "abjad.tools.pitchtools.NamedPitchClass.NamedPitchClass";
              "abjad.tools.pitchtools.PitchClass.PitchClass" -> "abjad.tools.pitchtools.NumberedPitchClass.NumberedPitchClass";
              "abjad.tools.pitchtools.PitchClassSegment.PitchClassSegment" -> "abjad.tools.pitchtools.TwelveToneRow.TwelveToneRow";
              "abjad.tools.pitchtools.Segment.Segment" -> "abjad.tools.pitchtools.IntervalClassSegment.IntervalClassSegment";
              "abjad.tools.pitchtools.Segment.Segment" -> "abjad.tools.pitchtools.IntervalSegment.IntervalSegment";
              "abjad.tools.pitchtools.Segment.Segment" -> "abjad.tools.pitchtools.PitchClassSegment.PitchClassSegment";
              "abjad.tools.pitchtools.Segment.Segment" -> "abjad.tools.pitchtools.PitchSegment.PitchSegment";
              "abjad.tools.pitchtools.Set.Set" -> "abjad.tools.pitchtools.IntervalClassSet.IntervalClassSet";
              "abjad.tools.pitchtools.Set.Set" -> "abjad.tools.pitchtools.IntervalSet.IntervalSet";
              "abjad.tools.pitchtools.Set.Set" -> "abjad.tools.pitchtools.PitchClassSet.PitchClassSet";
              "abjad.tools.pitchtools.Set.Set" -> "abjad.tools.pitchtools.PitchSet.PitchSet";
              "abjad.tools.pitchtools.Vector.Vector" -> "abjad.tools.pitchtools.IntervalClassVector.IntervalClassVector";
              "abjad.tools.pitchtools.Vector.Vector" -> "abjad.tools.pitchtools.IntervalVector.IntervalVector";
              "abjad.tools.pitchtools.Vector.Vector" -> "abjad.tools.pitchtools.PitchClassVector.PitchClassVector";
              "abjad.tools.pitchtools.Vector.Vector" -> "abjad.tools.pitchtools.PitchVector.PitchVector";
          }
          subgraph cluster_quantizationtools {
              graph [label=quantizationtools];
              "abjad.tools.quantizationtools.AttackPointOptimizer.AttackPointOptimizer" [color=7,
                  group=24,
                  label=AttackPointOptimizer,
                  shape=oval,
                  style=bold];
              "abjad.tools.quantizationtools.BeatwiseQSchema.BeatwiseQSchema" [color=7,
                  group=24,
                  label=BeatwiseQSchema,
                  shape=box];
              "abjad.tools.quantizationtools.BeatwiseQSchemaItem.BeatwiseQSchemaItem" [color=7,
                  group=24,
                  label=BeatwiseQSchemaItem,
                  shape=box];
              "abjad.tools.quantizationtools.BeatwiseQTarget.BeatwiseQTarget" [color=7,
                  group=24,
                  label=BeatwiseQTarget,
                  shape=box];
              "abjad.tools.quantizationtools.CollapsingGraceHandler.CollapsingGraceHandler" [color=7,
                  group=24,
                  label=CollapsingGraceHandler,
                  shape=box];
              "abjad.tools.quantizationtools.ConcatenatingGraceHandler.ConcatenatingGraceHandler" [color=7,
                  group=24,
                  label=ConcatenatingGraceHandler,
                  shape=box];
              "abjad.tools.quantizationtools.DiscardingGraceHandler.DiscardingGraceHandler" [color=7,
                  group=24,
                  label=DiscardingGraceHandler,
                  shape=box];
              "abjad.tools.quantizationtools.DistanceHeuristic.DistanceHeuristic" [color=7,
                  group=24,
                  label=DistanceHeuristic,
                  shape=box];
              "abjad.tools.quantizationtools.GraceHandler.GraceHandler" [color=7,
                  group=24,
                  label=GraceHandler,
                  shape=oval,
                  style=bold];
              "abjad.tools.quantizationtools.Heuristic.Heuristic" [color=7,
                  group=24,
                  label=Heuristic,
                  shape=oval,
                  style=bold];
              "abjad.tools.quantizationtools.JobHandler.JobHandler" [color=7,
                  group=24,
                  label=JobHandler,
                  shape=oval,
                  style=bold];
              "abjad.tools.quantizationtools.MeasurewiseAttackPointOptimizer.MeasurewiseAttackPointOptimizer" [color=7,
                  group=24,
                  label=MeasurewiseAttackPointOptimizer,
                  shape=box];
              "abjad.tools.quantizationtools.MeasurewiseQSchema.MeasurewiseQSchema" [color=7,
                  group=24,
                  label=MeasurewiseQSchema,
                  shape=box];
              "abjad.tools.quantizationtools.MeasurewiseQSchemaItem.MeasurewiseQSchemaItem" [color=7,
                  group=24,
                  label=MeasurewiseQSchemaItem,
                  shape=box];
              "abjad.tools.quantizationtools.MeasurewiseQTarget.MeasurewiseQTarget" [color=7,
                  group=24,
                  label=MeasurewiseQTarget,
                  shape=box];
              "abjad.tools.quantizationtools.NaiveAttackPointOptimizer.NaiveAttackPointOptimizer" [color=7,
                  group=24,
                  label=NaiveAttackPointOptimizer,
                  shape=box];
              "abjad.tools.quantizationtools.NullAttackPointOptimizer.NullAttackPointOptimizer" [color=7,
                  group=24,
                  label=NullAttackPointOptimizer,
                  shape=box];
              "abjad.tools.quantizationtools.ParallelJobHandler.ParallelJobHandler" [color=7,
                  group=24,
                  label=ParallelJobHandler,
                  shape=box];
              "abjad.tools.quantizationtools.ParallelJobHandlerWorker.ParallelJobHandlerWorker" [color=7,
                  group=24,
                  label=ParallelJobHandlerWorker,
                  shape=box];
              "abjad.tools.quantizationtools.PitchedQEvent.PitchedQEvent" [color=7,
                  group=24,
                  label=PitchedQEvent,
                  shape=box];
              "abjad.tools.quantizationtools.QEvent.QEvent" [color=7,
                  group=24,
                  label=QEvent,
                  shape=oval,
                  style=bold];
              "abjad.tools.quantizationtools.QEventProxy.QEventProxy" [color=7,
                  group=24,
                  label=QEventProxy,
                  shape=box];
              "abjad.tools.quantizationtools.QEventSequence.QEventSequence" [color=7,
                  group=24,
                  label=QEventSequence,
                  shape=box];
              "abjad.tools.quantizationtools.QGrid.QGrid" [color=7,
                  group=24,
                  label=QGrid,
                  shape=box];
              "abjad.tools.quantizationtools.QGridContainer.QGridContainer" [color=7,
                  group=24,
                  label=QGridContainer,
                  shape=box];
              "abjad.tools.quantizationtools.QGridLeaf.QGridLeaf" [color=7,
                  group=24,
                  label=QGridLeaf,
                  shape=box];
              "abjad.tools.quantizationtools.QSchema.QSchema" [color=7,
                  group=24,
                  label=QSchema,
                  shape=oval,
                  style=bold];
              "abjad.tools.quantizationtools.QSchemaItem.QSchemaItem" [color=7,
                  group=24,
                  label=QSchemaItem,
                  shape=oval,
                  style=bold];
              "abjad.tools.quantizationtools.QTarget.QTarget" [color=7,
                  group=24,
                  label=QTarget,
                  shape=oval,
                  style=bold];
              "abjad.tools.quantizationtools.QTargetBeat.QTargetBeat" [color=7,
                  group=24,
                  label=QTargetBeat,
                  shape=box];
              "abjad.tools.quantizationtools.QTargetMeasure.QTargetMeasure" [color=7,
                  group=24,
                  label=QTargetMeasure,
                  shape=box];
              "abjad.tools.quantizationtools.QuantizationJob.QuantizationJob" [color=7,
                  group=24,
                  label=QuantizationJob,
                  shape=box];
              "abjad.tools.quantizationtools.Quantizer.Quantizer" [color=7,
                  group=24,
                  label=Quantizer,
                  shape=box];
              "abjad.tools.quantizationtools.SearchTree.SearchTree" [color=7,
                  group=24,
                  label=SearchTree,
                  shape=oval,
                  style=bold];
              "abjad.tools.quantizationtools.SerialJobHandler.SerialJobHandler" [color=7,
                  group=24,
                  label=SerialJobHandler,
                  shape=box];
              "abjad.tools.quantizationtools.SilentQEvent.SilentQEvent" [color=7,
                  group=24,
                  label=SilentQEvent,
                  shape=box];
              "abjad.tools.quantizationtools.TerminalQEvent.TerminalQEvent" [color=7,
                  group=24,
                  label=TerminalQEvent,
                  shape=box];
              "abjad.tools.quantizationtools.UnweightedSearchTree.UnweightedSearchTree" [color=7,
                  group=24,
                  label=UnweightedSearchTree,
                  shape=box];
              "abjad.tools.quantizationtools.WeightedSearchTree.WeightedSearchTree" [color=7,
                  group=24,
                  label=WeightedSearchTree,
                  shape=box];
              "abjad.tools.quantizationtools.AttackPointOptimizer.AttackPointOptimizer" -> "abjad.tools.quantizationtools.MeasurewiseAttackPointOptimizer.MeasurewiseAttackPointOptimizer";
              "abjad.tools.quantizationtools.AttackPointOptimizer.AttackPointOptimizer" -> "abjad.tools.quantizationtools.NaiveAttackPointOptimizer.NaiveAttackPointOptimizer";
              "abjad.tools.quantizationtools.AttackPointOptimizer.AttackPointOptimizer" -> "abjad.tools.quantizationtools.NullAttackPointOptimizer.NullAttackPointOptimizer";
              "abjad.tools.quantizationtools.GraceHandler.GraceHandler" -> "abjad.tools.quantizationtools.CollapsingGraceHandler.CollapsingGraceHandler";
              "abjad.tools.quantizationtools.GraceHandler.GraceHandler" -> "abjad.tools.quantizationtools.ConcatenatingGraceHandler.ConcatenatingGraceHandler";
              "abjad.tools.quantizationtools.GraceHandler.GraceHandler" -> "abjad.tools.quantizationtools.DiscardingGraceHandler.DiscardingGraceHandler";
              "abjad.tools.quantizationtools.Heuristic.Heuristic" -> "abjad.tools.quantizationtools.DistanceHeuristic.DistanceHeuristic";
              "abjad.tools.quantizationtools.JobHandler.JobHandler" -> "abjad.tools.quantizationtools.ParallelJobHandler.ParallelJobHandler";
              "abjad.tools.quantizationtools.JobHandler.JobHandler" -> "abjad.tools.quantizationtools.SerialJobHandler.SerialJobHandler";
              "abjad.tools.quantizationtools.QEvent.QEvent" -> "abjad.tools.quantizationtools.PitchedQEvent.PitchedQEvent";
              "abjad.tools.quantizationtools.QEvent.QEvent" -> "abjad.tools.quantizationtools.SilentQEvent.SilentQEvent";
              "abjad.tools.quantizationtools.QEvent.QEvent" -> "abjad.tools.quantizationtools.TerminalQEvent.TerminalQEvent";
              "abjad.tools.quantizationtools.QSchema.QSchema" -> "abjad.tools.quantizationtools.BeatwiseQSchema.BeatwiseQSchema";
              "abjad.tools.quantizationtools.QSchema.QSchema" -> "abjad.tools.quantizationtools.MeasurewiseQSchema.MeasurewiseQSchema";
              "abjad.tools.quantizationtools.QSchemaItem.QSchemaItem" -> "abjad.tools.quantizationtools.BeatwiseQSchemaItem.BeatwiseQSchemaItem";
              "abjad.tools.quantizationtools.QSchemaItem.QSchemaItem" -> "abjad.tools.quantizationtools.MeasurewiseQSchemaItem.MeasurewiseQSchemaItem";
              "abjad.tools.quantizationtools.QTarget.QTarget" -> "abjad.tools.quantizationtools.BeatwiseQTarget.BeatwiseQTarget";
              "abjad.tools.quantizationtools.QTarget.QTarget" -> "abjad.tools.quantizationtools.MeasurewiseQTarget.MeasurewiseQTarget";
              "abjad.tools.quantizationtools.SearchTree.SearchTree" -> "abjad.tools.quantizationtools.UnweightedSearchTree.UnweightedSearchTree";
              "abjad.tools.quantizationtools.SearchTree.SearchTree" -> "abjad.tools.quantizationtools.WeightedSearchTree.WeightedSearchTree";
          }
          subgraph cluster_rhythmmakertools {
              graph [label=rhythmmakertools];
              "abjad.tools.rhythmmakertools.AccelerandoRhythmMaker.AccelerandoRhythmMaker" [color=8,
                  group=25,
                  label=AccelerandoRhythmMaker,
                  shape=box];
              "abjad.tools.rhythmmakertools.BeamSpecifier.BeamSpecifier" [color=8,
                  group=25,
                  label=BeamSpecifier,
                  shape=box];
              "abjad.tools.rhythmmakertools.BurnishSpecifier.BurnishSpecifier" [color=8,
                  group=25,
                  label=BurnishSpecifier,
                  shape=box];
              "abjad.tools.rhythmmakertools.DurationSpellingSpecifier.DurationSpellingSpecifier" [color=8,
                  group=25,
                  label=DurationSpellingSpecifier,
                  shape=box];
              "abjad.tools.rhythmmakertools.EvenDivisionRhythmMaker.EvenDivisionRhythmMaker" [color=8,
                  group=25,
                  label=EvenDivisionRhythmMaker,
                  shape=box];
              "abjad.tools.rhythmmakertools.EvenRunRhythmMaker.EvenRunRhythmMaker" [color=8,
                  group=25,
                  label=EvenRunRhythmMaker,
                  shape=box];
              "abjad.tools.rhythmmakertools.ExampleWrapper.ExampleWrapper" [color=8,
                  group=25,
                  label=ExampleWrapper,
                  shape=box];
              "abjad.tools.rhythmmakertools.GalleryMaker.GalleryMaker" [color=8,
                  group=25,
                  label=GalleryMaker,
                  shape=box];
              "abjad.tools.rhythmmakertools.InciseSpecifier.InciseSpecifier" [color=8,
                  group=25,
                  label=InciseSpecifier,
                  shape=box];
              "abjad.tools.rhythmmakertools.IncisedRhythmMaker.IncisedRhythmMaker" [color=8,
                  group=25,
                  label=IncisedRhythmMaker,
                  shape=box];
              "abjad.tools.rhythmmakertools.InterpolationSpecifier.InterpolationSpecifier" [color=8,
                  group=25,
                  label=InterpolationSpecifier,
                  shape=box];
              "abjad.tools.rhythmmakertools.NoteRhythmMaker.NoteRhythmMaker" [color=8,
                  group=25,
                  label=NoteRhythmMaker,
                  shape=box];
              "abjad.tools.rhythmmakertools.PartitionTable.PartitionTable" [color=8,
                  group=25,
                  label=PartitionTable,
                  shape=box];
              "abjad.tools.rhythmmakertools.RhythmMaker.RhythmMaker" [color=8,
                  group=25,
                  label=RhythmMaker,
                  shape=box];
              "abjad.tools.rhythmmakertools.RotationCounter.RotationCounter" [color=8,
                  group=25,
                  label=RotationCounter,
                  shape=box];
              "abjad.tools.rhythmmakertools.SilenceMask.SilenceMask" [color=8,
                  group=25,
                  label=SilenceMask,
                  shape=box];
              "abjad.tools.rhythmmakertools.SkipRhythmMaker.SkipRhythmMaker" [color=8,
                  group=25,
                  label=SkipRhythmMaker,
                  shape=box];
              "abjad.tools.rhythmmakertools.SustainMask.SustainMask" [color=8,
                  group=25,
                  label=SustainMask,
                  shape=box];
              "abjad.tools.rhythmmakertools.Talea.Talea" [color=8,
                  group=25,
                  label=Talea,
                  shape=box];
              "abjad.tools.rhythmmakertools.TaleaRhythmMaker.TaleaRhythmMaker" [color=8,
                  group=25,
                  label=TaleaRhythmMaker,
                  shape=box];
              "abjad.tools.rhythmmakertools.TieSpecifier.TieSpecifier" [color=8,
                  group=25,
                  label=TieSpecifier,
                  shape=box];
              "abjad.tools.rhythmmakertools.TupletRhythmMaker.TupletRhythmMaker" [color=8,
                  group=25,
                  label=TupletRhythmMaker,
                  shape=box];
              "abjad.tools.rhythmmakertools.TupletSpellingSpecifier.TupletSpellingSpecifier" [color=8,
                  group=25,
                  label=TupletSpellingSpecifier,
                  shape=box];
              "abjad.tools.rhythmmakertools.RhythmMaker.RhythmMaker" -> "abjad.tools.rhythmmakertools.AccelerandoRhythmMaker.AccelerandoRhythmMaker";
              "abjad.tools.rhythmmakertools.RhythmMaker.RhythmMaker" -> "abjad.tools.rhythmmakertools.EvenDivisionRhythmMaker.EvenDivisionRhythmMaker";
              "abjad.tools.rhythmmakertools.RhythmMaker.RhythmMaker" -> "abjad.tools.rhythmmakertools.EvenRunRhythmMaker.EvenRunRhythmMaker";
              "abjad.tools.rhythmmakertools.RhythmMaker.RhythmMaker" -> "abjad.tools.rhythmmakertools.IncisedRhythmMaker.IncisedRhythmMaker";
              "abjad.tools.rhythmmakertools.RhythmMaker.RhythmMaker" -> "abjad.tools.rhythmmakertools.NoteRhythmMaker.NoteRhythmMaker";
              "abjad.tools.rhythmmakertools.RhythmMaker.RhythmMaker" -> "abjad.tools.rhythmmakertools.SkipRhythmMaker.SkipRhythmMaker";
              "abjad.tools.rhythmmakertools.RhythmMaker.RhythmMaker" -> "abjad.tools.rhythmmakertools.TaleaRhythmMaker.TaleaRhythmMaker";
              "abjad.tools.rhythmmakertools.RhythmMaker.RhythmMaker" -> "abjad.tools.rhythmmakertools.TupletRhythmMaker.TupletRhythmMaker";
          }
          subgraph cluster_rhythmtreetools {
              graph [label=rhythmtreetools];
              "abjad.tools.rhythmtreetools.RhythmTreeContainer.RhythmTreeContainer" [color=9,
                  group=26,
                  label=RhythmTreeContainer,
                  shape=box];
              "abjad.tools.rhythmtreetools.RhythmTreeLeaf.RhythmTreeLeaf" [color=9,
                  group=26,
                  label=RhythmTreeLeaf,
                  shape=box];
              "abjad.tools.rhythmtreetools.RhythmTreeMixin.RhythmTreeMixin" [color=9,
                  group=26,
                  label=RhythmTreeMixin,
                  shape=oval,
                  style=bold];
              "abjad.tools.rhythmtreetools.RhythmTreeParser.RhythmTreeParser" [color=9,
                  group=26,
                  label=RhythmTreeParser,
                  shape=box];
              "abjad.tools.rhythmtreetools.RhythmTreeMixin.RhythmTreeMixin" -> "abjad.tools.rhythmtreetools.RhythmTreeContainer.RhythmTreeContainer";
              "abjad.tools.rhythmtreetools.RhythmTreeMixin.RhythmTreeMixin" -> "abjad.tools.rhythmtreetools.RhythmTreeLeaf.RhythmTreeLeaf";
          }
          subgraph cluster_schemetools {
              graph [label=schemetools];
              "abjad.tools.schemetools.Scheme.Scheme" [color=1,
                  group=27,
                  label=Scheme,
                  shape=box];
              "abjad.tools.schemetools.SchemeAssociativeList.SchemeAssociativeList" [color=1,
                  group=27,
                  label=SchemeAssociativeList,
                  shape=box];
              "abjad.tools.schemetools.SchemeColor.SchemeColor" [color=1,
                  group=27,
                  label=SchemeColor,
                  shape=box];
              "abjad.tools.schemetools.SchemeMoment.SchemeMoment" [color=1,
                  group=27,
                  label=SchemeMoment,
                  shape=box];
              "abjad.tools.schemetools.SchemePair.SchemePair" [color=1,
                  group=27,
                  label=SchemePair,
                  shape=box];
              "abjad.tools.schemetools.SchemeSymbol.SchemeSymbol" [color=1,
                  group=27,
                  label=SchemeSymbol,
                  shape=box];
              "abjad.tools.schemetools.SchemeVector.SchemeVector" [color=1,
                  group=27,
                  label=SchemeVector,
                  shape=box];
              "abjad.tools.schemetools.SchemeVectorConstant.SchemeVectorConstant" [color=1,
                  group=27,
                  label=SchemeVectorConstant,
                  shape=box];
              "abjad.tools.schemetools.Scheme.Scheme" -> "abjad.tools.schemetools.SchemeAssociativeList.SchemeAssociativeList";
              "abjad.tools.schemetools.Scheme.Scheme" -> "abjad.tools.schemetools.SchemeColor.SchemeColor";
              "abjad.tools.schemetools.Scheme.Scheme" -> "abjad.tools.schemetools.SchemeMoment.SchemeMoment";
              "abjad.tools.schemetools.Scheme.Scheme" -> "abjad.tools.schemetools.SchemePair.SchemePair";
              "abjad.tools.schemetools.Scheme.Scheme" -> "abjad.tools.schemetools.SchemeSymbol.SchemeSymbol";
              "abjad.tools.schemetools.Scheme.Scheme" -> "abjad.tools.schemetools.SchemeVector.SchemeVector";
              "abjad.tools.schemetools.Scheme.Scheme" -> "abjad.tools.schemetools.SchemeVectorConstant.SchemeVectorConstant";
          }
          subgraph cluster_scoretools {
              graph [label=scoretools];
              "abjad.tools.scoretools.Chord.Chord" [color=2,
                  group=28,
                  label=Chord,
                  shape=box];
              "abjad.tools.scoretools.Cluster.Cluster" [color=2,
                  group=28,
                  label=Cluster,
                  shape=box];
              "abjad.tools.scoretools.Component.Component" [color=2,
                  group=28,
                  label=Component,
                  shape=oval,
                  style=bold];
              "abjad.tools.scoretools.Container.Container" [color=2,
                  group=28,
                  label=Container,
                  shape=box];
              "abjad.tools.scoretools.Context.Context" [color=2,
                  group=28,
                  label=Context,
                  shape=box];
              "abjad.tools.scoretools.DrumNoteHead.DrumNoteHead" [color=2,
                  group=28,
                  label=DrumNoteHead,
                  shape=box];
              "abjad.tools.scoretools.FixedDurationContainer.FixedDurationContainer" [color=2,
                  group=28,
                  label=FixedDurationContainer,
                  shape=box];
              "abjad.tools.scoretools.FixedDurationTuplet.FixedDurationTuplet" [color=2,
                  group=28,
                  label=FixedDurationTuplet,
                  shape=box];
              "abjad.tools.scoretools.GraceContainer.GraceContainer" [color=2,
                  group=28,
                  label=GraceContainer,
                  shape=box];
              "abjad.tools.scoretools.Leaf.Leaf" [color=2,
                  group=28,
                  label=Leaf,
                  shape=oval,
                  style=bold];
              "abjad.tools.scoretools.Measure.Measure" [color=2,
                  group=28,
                  label=Measure,
                  shape=box];
              "abjad.tools.scoretools.MultimeasureRest.MultimeasureRest" [color=2,
                  group=28,
                  label=MultimeasureRest,
                  shape=box];
              "abjad.tools.scoretools.Note.Note" [color=2,
                  group=28,
                  label=Note,
                  shape=box];
              "abjad.tools.scoretools.NoteHead.NoteHead" [color=2,
                  group=28,
                  label=NoteHead,
                  shape=box];
              "abjad.tools.scoretools.NoteHeadInventory.NoteHeadInventory" [color=2,
                  group=28,
                  label=NoteHeadInventory,
                  shape=box];
              "abjad.tools.scoretools.Rest.Rest" [color=2,
                  group=28,
                  label=Rest,
                  shape=box];
              "abjad.tools.scoretools.Score.Score" [color=2,
                  group=28,
                  label=Score,
                  shape=box];
              "abjad.tools.scoretools.Skip.Skip" [color=2,
                  group=28,
                  label=Skip,
                  shape=box];
              "abjad.tools.scoretools.Staff.Staff" [color=2,
                  group=28,
                  label=Staff,
                  shape=box];
              "abjad.tools.scoretools.StaffGroup.StaffGroup" [color=2,
                  group=28,
                  label=StaffGroup,
                  shape=box];
              "abjad.tools.scoretools.Tuplet.Tuplet" [color=2,
                  group=28,
                  label=Tuplet,
                  shape=box];
              "abjad.tools.scoretools.Voice.Voice" [color=2,
                  group=28,
                  label=Voice,
                  shape=box];
              "abjad.tools.scoretools.Component.Component" -> "abjad.tools.scoretools.Container.Container";
              "abjad.tools.scoretools.Component.Component" -> "abjad.tools.scoretools.Leaf.Leaf";
              "abjad.tools.scoretools.Container.Container" -> "abjad.tools.scoretools.Cluster.Cluster";
              "abjad.tools.scoretools.Container.Container" -> "abjad.tools.scoretools.Context.Context";
              "abjad.tools.scoretools.Container.Container" -> "abjad.tools.scoretools.FixedDurationContainer.FixedDurationContainer";
              "abjad.tools.scoretools.Container.Container" -> "abjad.tools.scoretools.GraceContainer.GraceContainer";
              "abjad.tools.scoretools.Container.Container" -> "abjad.tools.scoretools.Tuplet.Tuplet";
              "abjad.tools.scoretools.Context.Context" -> "abjad.tools.scoretools.Score.Score";
              "abjad.tools.scoretools.Context.Context" -> "abjad.tools.scoretools.Staff.Staff";
              "abjad.tools.scoretools.Context.Context" -> "abjad.tools.scoretools.StaffGroup.StaffGroup";
              "abjad.tools.scoretools.Context.Context" -> "abjad.tools.scoretools.Voice.Voice";
              "abjad.tools.scoretools.FixedDurationContainer.FixedDurationContainer" -> "abjad.tools.scoretools.Measure.Measure";
              "abjad.tools.scoretools.Leaf.Leaf" -> "abjad.tools.scoretools.Chord.Chord";
              "abjad.tools.scoretools.Leaf.Leaf" -> "abjad.tools.scoretools.MultimeasureRest.MultimeasureRest";
              "abjad.tools.scoretools.Leaf.Leaf" -> "abjad.tools.scoretools.Note.Note";
              "abjad.tools.scoretools.Leaf.Leaf" -> "abjad.tools.scoretools.Rest.Rest";
              "abjad.tools.scoretools.Leaf.Leaf" -> "abjad.tools.scoretools.Skip.Skip";
              "abjad.tools.scoretools.NoteHead.NoteHead" -> "abjad.tools.scoretools.DrumNoteHead.DrumNoteHead";
              "abjad.tools.scoretools.Tuplet.Tuplet" -> "abjad.tools.scoretools.FixedDurationTuplet.FixedDurationTuplet";
          }
          subgraph cluster_selectiontools {
              graph [label=selectiontools];
              "abjad.tools.selectiontools.SelectionInventory.SelectionInventory" [color=3,
                  group=29,
                  label=SelectionInventory,
                  shape=box];
          }
          subgraph cluster_selectortools {
              graph [label=selectortools];
              "abjad.tools.selectortools.ContiguitySelectorCallback.ContiguitySelectorCallback" [color=4,
                  group=30,
                  label=ContiguitySelectorCallback,
                  shape=box];
              "abjad.tools.selectortools.CountsSelectorCallback.CountsSelectorCallback" [color=4,
                  group=30,
                  label=CountsSelectorCallback,
                  shape=box];
              "abjad.tools.selectortools.DurationInequality.DurationInequality" [color=4,
                  group=30,
                  label=DurationInequality,
                  shape=box];
              "abjad.tools.selectortools.DurationSelectorCallback.DurationSelectorCallback" [color=4,
                  group=30,
                  label=DurationSelectorCallback,
                  shape=box];
              "abjad.tools.selectortools.ExtraLeafSelectorCallback.ExtraLeafSelectorCallback" [color=4,
                  group=30,
                  label=ExtraLeafSelectorCallback,
                  shape=box];
              "abjad.tools.selectortools.FlattenSelectorCallback.FlattenSelectorCallback" [color=4,
                  group=30,
                  label=FlattenSelectorCallback,
                  shape=box];
              "abjad.tools.selectortools.Inequality.Inequality" [color=4,
                  group=30,
                  label=Inequality,
                  shape=oval,
                  style=bold];
              "abjad.tools.selectortools.ItemSelectorCallback.ItemSelectorCallback" [color=4,
                  group=30,
                  label=ItemSelectorCallback,
                  shape=box];
              "abjad.tools.selectortools.LengthInequality.LengthInequality" [color=4,
                  group=30,
                  label=LengthInequality,
                  shape=box];
              "abjad.tools.selectortools.LengthSelectorCallback.LengthSelectorCallback" [color=4,
                  group=30,
                  label=LengthSelectorCallback,
                  shape=box];
              "abjad.tools.selectortools.LogicalMeasureSelectorCallback.LogicalMeasureSelectorCallback" [color=4,
                  group=30,
                  label=LogicalMeasureSelectorCallback,
                  shape=box];
              "abjad.tools.selectortools.LogicalTieSelectorCallback.LogicalTieSelectorCallback" [color=4,
                  group=30,
                  label=LogicalTieSelectorCallback,
                  shape=box];
              "abjad.tools.selectortools.PartitionByRatioCallback.PartitionByRatioCallback" [color=4,
                  group=30,
                  label=PartitionByRatioCallback,
                  shape=box];
              "abjad.tools.selectortools.PatternedSelectorCallback.PatternedSelectorCallback" [color=4,
                  group=30,
                  label=PatternedSelectorCallback,
                  shape=box];
              "abjad.tools.selectortools.PitchSelectorCallback.PitchSelectorCallback" [color=4,
                  group=30,
                  label=PitchSelectorCallback,
                  shape=box];
              "abjad.tools.selectortools.PrototypeSelectorCallback.PrototypeSelectorCallback" [color=4,
                  group=30,
                  label=PrototypeSelectorCallback,
                  shape=box];
              "abjad.tools.selectortools.RunSelectorCallback.RunSelectorCallback" [color=4,
                  group=30,
                  label=RunSelectorCallback,
                  shape=box];
              "abjad.tools.selectortools.Selector.Selector" [color=4,
                  group=30,
                  label=Selector,
                  shape=box];
              "abjad.tools.selectortools.SliceSelectorCallback.SliceSelectorCallback" [color=4,
                  group=30,
                  label=SliceSelectorCallback,
                  shape=box];
              "abjad.tools.selectortools.Inequality.Inequality" -> "abjad.tools.selectortools.DurationInequality.DurationInequality";
              "abjad.tools.selectortools.Inequality.Inequality" -> "abjad.tools.selectortools.LengthInequality.LengthInequality";
          }
          subgraph cluster_sequencetools {
              graph [label=sequencetools];
              "abjad.tools.sequencetools.Duplication.Duplication" [color=5,
                  group=31,
                  label=Duplication,
                  shape=box];
              "abjad.tools.sequencetools.Sequence.Sequence" [color=5,
                  group=31,
                  label=Sequence,
                  shape=box];
          }
          subgraph cluster_spannertools {
              graph [label=spannertools];
              "abjad.tools.spannertools.Beam.Beam" [color=6,
                  group=32,
                  label=Beam,
                  shape=box];
              "abjad.tools.spannertools.BowContactSpanner.BowContactSpanner" [color=6,
                  group=32,
                  label=BowContactSpanner,
                  shape=box];
              "abjad.tools.spannertools.ClefSpanner.ClefSpanner" [color=6,
                  group=32,
                  label=ClefSpanner,
                  shape=box];
              "abjad.tools.spannertools.ComplexBeam.ComplexBeam" [color=6,
                  group=32,
                  label=ComplexBeam,
                  shape=box];
              "abjad.tools.spannertools.ComplexTrillSpanner.ComplexTrillSpanner" [color=6,
                  group=32,
                  label=ComplexTrillSpanner,
                  shape=box];
              "abjad.tools.spannertools.Crescendo.Crescendo" [color=6,
                  group=32,
                  label=Crescendo,
                  shape=box];
              "abjad.tools.spannertools.Decrescendo.Decrescendo" [color=6,
                  group=32,
                  label=Decrescendo,
                  shape=box];
              "abjad.tools.spannertools.DuratedComplexBeam.DuratedComplexBeam" [color=6,
                  group=32,
                  label=DuratedComplexBeam,
                  shape=box];
              "abjad.tools.spannertools.GeneralizedBeam.GeneralizedBeam" [color=6,
                  group=32,
                  label=GeneralizedBeam,
                  shape=box];
              "abjad.tools.spannertools.Glissando.Glissando" [color=6,
                  group=32,
                  label=Glissando,
                  shape=box];
              "abjad.tools.spannertools.Hairpin.Hairpin" [color=6,
                  group=32,
                  label=Hairpin,
                  shape=box];
              "abjad.tools.spannertools.HiddenStaffSpanner.HiddenStaffSpanner" [color=6,
                  group=32,
                  label=HiddenStaffSpanner,
                  shape=box];
              "abjad.tools.spannertools.HorizontalBracketSpanner.HorizontalBracketSpanner" [color=6,
                  group=32,
                  label=HorizontalBracketSpanner,
                  shape=box];
              "abjad.tools.spannertools.MeasuredComplexBeam.MeasuredComplexBeam" [color=6,
                  group=32,
                  label=MeasuredComplexBeam,
                  shape=box];
              "abjad.tools.spannertools.MultipartBeam.MultipartBeam" [color=6,
                  group=32,
                  label=MultipartBeam,
                  shape=box];
              "abjad.tools.spannertools.OctavationSpanner.OctavationSpanner" [color=6,
                  group=32,
                  label=OctavationSpanner,
                  shape=box];
              "abjad.tools.spannertools.PhrasingSlur.PhrasingSlur" [color=6,
                  group=32,
                  label=PhrasingSlur,
                  shape=box];
              "abjad.tools.spannertools.PianoPedalSpanner.PianoPedalSpanner" [color=6,
                  group=32,
                  label=PianoPedalSpanner,
                  shape=box];
              "abjad.tools.spannertools.Slur.Slur" [color=6,
                  group=32,
                  label=Slur,
                  shape=box];
              "abjad.tools.spannertools.Spanner.Spanner" [color=6,
                  group=32,
                  label=Spanner,
                  shape=box];
              "abjad.tools.spannertools.StaffLinesSpanner.StaffLinesSpanner" [color=6,
                  group=32,
                  label=StaffLinesSpanner,
                  shape=box];
              "abjad.tools.spannertools.StemTremoloSpanner.StemTremoloSpanner" [color=6,
                  group=32,
                  label=StemTremoloSpanner,
                  shape=box];
              "abjad.tools.spannertools.TempoSpanner.TempoSpanner" [color=6,
                  group=32,
                  label=TempoSpanner,
                  shape=box];
              "abjad.tools.spannertools.TextSpanner.TextSpanner" [color=6,
                  group=32,
                  label=TextSpanner,
                  shape=box];
              "abjad.tools.spannertools.Tie.Tie" [color=6,
                  group=32,
                  label=Tie,
                  shape=box];
              "abjad.tools.spannertools.TrillSpanner.TrillSpanner" [color=6,
                  group=32,
                  label=TrillSpanner,
                  shape=box];
              "abjad.tools.spannertools.Beam.Beam" -> "abjad.tools.spannertools.ComplexBeam.ComplexBeam";
              "abjad.tools.spannertools.Beam.Beam" -> "abjad.tools.spannertools.MultipartBeam.MultipartBeam";
              "abjad.tools.spannertools.ComplexBeam.ComplexBeam" -> "abjad.tools.spannertools.DuratedComplexBeam.DuratedComplexBeam";
              "abjad.tools.spannertools.ComplexBeam.ComplexBeam" -> "abjad.tools.spannertools.MeasuredComplexBeam.MeasuredComplexBeam";
              "abjad.tools.spannertools.Hairpin.Hairpin" -> "abjad.tools.spannertools.Crescendo.Crescendo";
              "abjad.tools.spannertools.Hairpin.Hairpin" -> "abjad.tools.spannertools.Decrescendo.Decrescendo";
              "abjad.tools.spannertools.Spanner.Spanner" -> "abjad.tools.spannertools.Beam.Beam";
              "abjad.tools.spannertools.Spanner.Spanner" -> "abjad.tools.spannertools.BowContactSpanner.BowContactSpanner";
              "abjad.tools.spannertools.Spanner.Spanner" -> "abjad.tools.spannertools.ClefSpanner.ClefSpanner";
              "abjad.tools.spannertools.Spanner.Spanner" -> "abjad.tools.spannertools.ComplexTrillSpanner.ComplexTrillSpanner";
              "abjad.tools.spannertools.Spanner.Spanner" -> "abjad.tools.spannertools.GeneralizedBeam.GeneralizedBeam";
              "abjad.tools.spannertools.Spanner.Spanner" -> "abjad.tools.spannertools.Glissando.Glissando";
              "abjad.tools.spannertools.Spanner.Spanner" -> "abjad.tools.spannertools.Hairpin.Hairpin";
              "abjad.tools.spannertools.Spanner.Spanner" -> "abjad.tools.spannertools.HiddenStaffSpanner.HiddenStaffSpanner";
              "abjad.tools.spannertools.Spanner.Spanner" -> "abjad.tools.spannertools.HorizontalBracketSpanner.HorizontalBracketSpanner";
              "abjad.tools.spannertools.Spanner.Spanner" -> "abjad.tools.spannertools.OctavationSpanner.OctavationSpanner";
              "abjad.tools.spannertools.Spanner.Spanner" -> "abjad.tools.spannertools.PhrasingSlur.PhrasingSlur";
              "abjad.tools.spannertools.Spanner.Spanner" -> "abjad.tools.spannertools.PianoPedalSpanner.PianoPedalSpanner";
              "abjad.tools.spannertools.Spanner.Spanner" -> "abjad.tools.spannertools.Slur.Slur";
              "abjad.tools.spannertools.Spanner.Spanner" -> "abjad.tools.spannertools.StaffLinesSpanner.StaffLinesSpanner";
              "abjad.tools.spannertools.Spanner.Spanner" -> "abjad.tools.spannertools.StemTremoloSpanner.StemTremoloSpanner";
              "abjad.tools.spannertools.Spanner.Spanner" -> "abjad.tools.spannertools.TempoSpanner.TempoSpanner";
              "abjad.tools.spannertools.Spanner.Spanner" -> "abjad.tools.spannertools.TextSpanner.TextSpanner";
              "abjad.tools.spannertools.Spanner.Spanner" -> "abjad.tools.spannertools.Tie.Tie";
              "abjad.tools.spannertools.Spanner.Spanner" -> "abjad.tools.spannertools.TrillSpanner.TrillSpanner";
          }
          subgraph cluster_systemtools {
              graph [label=systemtools];
              "abjad.tools.systemtools.AbjadConfiguration.AbjadConfiguration" [color=7,
                  group=33,
                  label=AbjadConfiguration,
                  shape=box];
              "abjad.tools.systemtools.BenchmarkScoreMaker.BenchmarkScoreMaker" [color=7,
                  group=33,
                  label=BenchmarkScoreMaker,
                  shape=box];
              "abjad.tools.systemtools.Configuration.Configuration" [color=7,
                  group=33,
                  label=Configuration,
                  shape=oval,
                  style=bold];
              "abjad.tools.systemtools.FilesystemState.FilesystemState" [color=7,
                  group=33,
                  label=FilesystemState,
                  shape=box];
              "abjad.tools.systemtools.ForbidUpdate.ForbidUpdate" [color=7,
                  group=33,
                  label=ForbidUpdate,
                  shape=box];
              "abjad.tools.systemtools.IOManager.IOManager" [color=7,
                  group=33,
                  label=IOManager,
                  shape=box];
              "abjad.tools.systemtools.ImportManager.ImportManager" [color=7,
                  group=33,
                  label=ImportManager,
                  shape=box];
              "abjad.tools.systemtools.LilyPondFormatBundle.LilyPondFormatBundle" [color=7,
                  group=33,
                  label=LilyPondFormatBundle,
                  shape=box];
              "abjad.tools.systemtools.LilyPondFormatManager.LilyPondFormatManager" [color=7,
                  group=33,
                  label=LilyPondFormatManager,
                  shape=box];
              "abjad.tools.systemtools.NullContextManager.NullContextManager" [color=7,
                  group=33,
                  label=NullContextManager,
                  shape=box];
              "abjad.tools.systemtools.ProgressIndicator.ProgressIndicator" [color=7,
                  group=33,
                  label=ProgressIndicator,
                  shape=box];
              "abjad.tools.systemtools.RedirectedStreams.RedirectedStreams" [color=7,
                  group=33,
                  label=RedirectedStreams,
                  shape=box];
              "abjad.tools.systemtools.StorageFormatManager.StorageFormatManager" [color=7,
                  group=33,
                  label=StorageFormatManager,
                  shape=box];
              "abjad.tools.systemtools.StorageFormatSpecification.StorageFormatSpecification" [color=7,
                  group=33,
                  label=StorageFormatSpecification,
                  shape=box];
              "abjad.tools.systemtools.TemporaryDirectory.TemporaryDirectory" [color=7,
                  group=33,
                  label=TemporaryDirectory,
                  shape=box];
              "abjad.tools.systemtools.TemporaryDirectoryChange.TemporaryDirectoryChange" [color=7,
                  group=33,
                  label=TemporaryDirectoryChange,
                  shape=box];
              "abjad.tools.systemtools.TestManager.TestManager" [color=7,
                  group=33,
                  label=TestManager,
                  shape=box];
              "abjad.tools.systemtools.Timer.Timer" [color=7,
                  group=33,
                  label=Timer,
                  shape=box];
              "abjad.tools.systemtools.UpdateManager.UpdateManager" [color=7,
                  group=33,
                  label=UpdateManager,
                  shape=box];
              "abjad.tools.systemtools.WellformednessManager.WellformednessManager" [color=7,
                  group=33,
                  label=WellformednessManager,
                  shape=box];
              "abjad.tools.systemtools.Configuration.Configuration" -> "abjad.tools.systemtools.AbjadConfiguration.AbjadConfiguration";
          }
          subgraph cluster_templatetools {
              graph [label=templatetools];
              "abjad.tools.templatetools.GroupedRhythmicStavesScoreTemplate.GroupedRhythmicStavesScoreTemplate" [color=8,
                  group=34,
                  label=GroupedRhythmicStavesScoreTemplate,
                  shape=box];
              "abjad.tools.templatetools.GroupedStavesScoreTemplate.GroupedStavesScoreTemplate" [color=8,
                  group=34,
                  label=GroupedStavesScoreTemplate,
                  shape=box];
              "abjad.tools.templatetools.StringOrchestraScoreTemplate.StringOrchestraScoreTemplate" [color=8,
                  group=34,
                  label=StringOrchestraScoreTemplate,
                  shape=box];
              "abjad.tools.templatetools.StringQuartetScoreTemplate.StringQuartetScoreTemplate" [color=8,
                  group=34,
                  label=StringQuartetScoreTemplate,
                  shape=box];
              "abjad.tools.templatetools.TwoStaffPianoScoreTemplate.TwoStaffPianoScoreTemplate" [color=8,
                  group=34,
                  label=TwoStaffPianoScoreTemplate,
                  shape=box];
          }
          subgraph cluster_timespantools {
              graph [label=timespantools];
              "abjad.tools.timespantools.AnnotatedTimespan.AnnotatedTimespan" [color=9,
                  group=35,
                  label=AnnotatedTimespan,
                  shape=box];
              "abjad.tools.timespantools.CompoundInequality.CompoundInequality" [color=9,
                  group=35,
                  label=CompoundInequality,
                  shape=box];
              "abjad.tools.timespantools.Inequality.Inequality" [color=9,
                  group=35,
                  label=Inequality,
                  shape=box];
              "abjad.tools.timespantools.OffsetTimespanTimeRelation.OffsetTimespanTimeRelation" [color=9,
                  group=35,
                  label=OffsetTimespanTimeRelation,
                  shape=box];
              "abjad.tools.timespantools.TimeRelation.TimeRelation" [color=9,
                  group=35,
                  label=TimeRelation,
                  shape=oval,
                  style=bold];
              "abjad.tools.timespantools.Timespan.Timespan" [color=9,
                  group=35,
                  label=Timespan,
                  shape=box];
              "abjad.tools.timespantools.TimespanInventory.TimespanInventory" [color=9,
                  group=35,
                  label=TimespanInventory,
                  shape=box];
              "abjad.tools.timespantools.TimespanTimespanTimeRelation.TimespanTimespanTimeRelation" [color=9,
                  group=35,
                  label=TimespanTimespanTimeRelation,
                  shape=box];
              "abjad.tools.timespantools.TimeRelation.TimeRelation" -> "abjad.tools.timespantools.OffsetTimespanTimeRelation.OffsetTimespanTimeRelation";
              "abjad.tools.timespantools.TimeRelation.TimeRelation" -> "abjad.tools.timespantools.TimespanTimespanTimeRelation.TimespanTimespanTimeRelation";
              "abjad.tools.timespantools.Timespan.Timespan" -> "abjad.tools.timespantools.AnnotatedTimespan.AnnotatedTimespan";
          }
          subgraph cluster_tonalanalysistools {
              graph [label=tonalanalysistools];
              "abjad.tools.tonalanalysistools.ChordExtent.ChordExtent" [color=1,
                  group=36,
                  label=ChordExtent,
                  shape=box];
              "abjad.tools.tonalanalysistools.ChordInversion.ChordInversion" [color=1,
                  group=36,
                  label=ChordInversion,
                  shape=box];
              "abjad.tools.tonalanalysistools.ChordOmission.ChordOmission" [color=1,
                  group=36,
                  label=ChordOmission,
                  shape=box];
              "abjad.tools.tonalanalysistools.ChordQuality.ChordQuality" [color=1,
                  group=36,
                  label=ChordQuality,
                  shape=box];
              "abjad.tools.tonalanalysistools.ChordSuspension.ChordSuspension" [color=1,
                  group=36,
                  label=ChordSuspension,
                  shape=box];
              "abjad.tools.tonalanalysistools.Mode.Mode" [color=1,
                  group=36,
                  label=Mode,
                  shape=box];
              "abjad.tools.tonalanalysistools.RomanNumeral.RomanNumeral" [color=1,
                  group=36,
                  label=RomanNumeral,
                  shape=box];
              "abjad.tools.tonalanalysistools.RootedChordClass.RootedChordClass" [color=1,
                  group=36,
                  label=RootedChordClass,
                  shape=box];
              "abjad.tools.tonalanalysistools.RootlessChordClass.RootlessChordClass" [color=1,
                  group=36,
                  label=RootlessChordClass,
                  shape=box];
              "abjad.tools.tonalanalysistools.Scale.Scale" [color=1,
                  group=36,
                  label=Scale,
                  shape=box];
              "abjad.tools.tonalanalysistools.ScaleDegree.ScaleDegree" [color=1,
                  group=36,
                  label=ScaleDegree,
                  shape=box];
              "abjad.tools.tonalanalysistools.TonalAnalysisAgent.TonalAnalysisAgent" [color=1,
                  group=36,
                  label=TonalAnalysisAgent,
                  shape=box];
          }
          subgraph cluster_builtins {
              graph [label=builtins];
              "builtins.object" [color=4,
                  group=3,
                  label=object,
                  shape=box];
          }
          subgraph cluster_constrainttools {
              graph [label=constrainttools];
              "experimental.tools.constrainttools.AbsoluteIndexConstraint.AbsoluteIndexConstraint" [color=5,
                  group=4,
                  label=AbsoluteIndexConstraint,
                  shape=box];
              "experimental.tools.constrainttools.Domain.Domain" [color=5,
                  group=4,
                  label=Domain,
                  shape=box];
              "experimental.tools.constrainttools.FixedLengthStreamSolver.FixedLengthStreamSolver" [color=5,
                  group=4,
                  label=FixedLengthStreamSolver,
                  shape=box];
              "experimental.tools.constrainttools.GlobalConstraint.GlobalConstraint" [color=5,
                  group=4,
                  label=GlobalConstraint,
                  shape=box];
              "experimental.tools.constrainttools.GlobalCountsConstraint.GlobalCountsConstraint" [color=5,
                  group=4,
                  label=GlobalCountsConstraint,
                  shape=box];
              "experimental.tools.constrainttools.GlobalReferenceConstraint.GlobalReferenceConstraint" [color=5,
                  group=4,
                  label=GlobalReferenceConstraint,
                  shape=box];
              "experimental.tools.constrainttools.RelativeCountsConstraint.RelativeCountsConstraint" [color=5,
                  group=4,
                  label=RelativeCountsConstraint,
                  shape=box];
              "experimental.tools.constrainttools.RelativeIndexConstraint.RelativeIndexConstraint" [color=5,
                  group=4,
                  label=RelativeIndexConstraint,
                  shape=box];
              "experimental.tools.constrainttools.VariableLengthStreamSolver.VariableLengthStreamSolver" [color=5,
                  group=4,
                  label=VariableLengthStreamSolver,
                  shape=box];
              "experimental.tools.constrainttools._AbsoluteConstraint._AbsoluteConstraint._AbsoluteConstraint" [color=5,
                  group=4,
                  label=_AbsoluteConstraint,
                  shape=box];
              "experimental.tools.constrainttools._Constraint._Constraint._Constraint" [color=5,
                  group=4,
                  label=_Constraint,
                  shape=box];
              "experimental.tools.constrainttools._GlobalConstraint._GlobalConstraint._GlobalConstraint" [color=5,
                  group=4,
                  label=_GlobalConstraint,
                  shape=box];
              "experimental.tools.constrainttools._RelativeConstraint._RelativeConstraint._RelativeConstraint" [color=5,
                  group=4,
                  label=_RelativeConstraint,
                  shape=box];
              "experimental.tools.constrainttools._SolutionNode._SolutionNode._SolutionNode" [color=5,
                  group=4,
                  label=_SolutionNode,
                  shape=box];
              "experimental.tools.constrainttools._Solver._Solver._Solver" [color=5,
                  group=4,
                  label=_Solver,
                  shape=box];
              "experimental.tools.constrainttools._AbsoluteConstraint._AbsoluteConstraint._AbsoluteConstraint" -> "experimental.tools.constrainttools.AbsoluteIndexConstraint.AbsoluteIndexConstraint";
              "experimental.tools.constrainttools._Constraint._Constraint._Constraint" -> "experimental.tools.constrainttools._AbsoluteConstraint._AbsoluteConstraint._AbsoluteConstraint";
              "experimental.tools.constrainttools._Constraint._Constraint._Constraint" -> "experimental.tools.constrainttools._GlobalConstraint._GlobalConstraint._GlobalConstraint";
              "experimental.tools.constrainttools._Constraint._Constraint._Constraint" -> "experimental.tools.constrainttools._RelativeConstraint._RelativeConstraint._RelativeConstraint";
              "experimental.tools.constrainttools._GlobalConstraint._GlobalConstraint._GlobalConstraint" -> "experimental.tools.constrainttools.GlobalConstraint.GlobalConstraint";
              "experimental.tools.constrainttools._GlobalConstraint._GlobalConstraint._GlobalConstraint" -> "experimental.tools.constrainttools.GlobalCountsConstraint.GlobalCountsConstraint";
              "experimental.tools.constrainttools._GlobalConstraint._GlobalConstraint._GlobalConstraint" -> "experimental.tools.constrainttools.GlobalReferenceConstraint.GlobalReferenceConstraint";
              "experimental.tools.constrainttools._RelativeConstraint._RelativeConstraint._RelativeConstraint" -> "experimental.tools.constrainttools.RelativeCountsConstraint.RelativeCountsConstraint";
              "experimental.tools.constrainttools._RelativeConstraint._RelativeConstraint._RelativeConstraint" -> "experimental.tools.constrainttools.RelativeIndexConstraint.RelativeIndexConstraint";
              "experimental.tools.constrainttools._Solver._Solver._Solver" -> "experimental.tools.constrainttools.FixedLengthStreamSolver.FixedLengthStreamSolver";
              "experimental.tools.constrainttools._Solver._Solver._Solver" -> "experimental.tools.constrainttools.VariableLengthStreamSolver.VariableLengthStreamSolver";
          }
          subgraph cluster_interpolationtools {
              graph [label=interpolationtools];
              "experimental.tools.interpolationtools.BreakPointFunction.BreakPointFunction" [color=5,
                  group=13,
                  label=BreakPointFunction,
                  shape=box];
          }
          subgraph cluster_makertools {
              graph [label=makertools];
              "experimental.tools.makertools.PianoStaffSegmentMaker.PianoStaffSegmentMaker" [color=9,
                  group=17,
                  label=PianoStaffSegmentMaker,
                  shape=box];
              "experimental.tools.makertools.SegmentMaker.SegmentMaker" [color=9,
                  group=17,
                  label=SegmentMaker,
                  shape=box];
              "experimental.tools.makertools.SegmentMaker.SegmentMaker" -> "experimental.tools.makertools.PianoStaffSegmentMaker.PianoStaffSegmentMaker";
          }
          subgraph cluster_idetools {
              graph [label=idetools];
              "ide.tools.idetools.AbjadIDEConfiguration.AbjadIDEConfiguration" [color=2,
                  group=10,
                  label=AbjadIDEConfiguration,
                  shape=box];
              "ide.tools.idetools.IOManager.IOManager" [color=2,
                  group=10,
                  label=IOManager,
                  shape=box];
              "ide.tools.idetools.Interaction.Interaction" [color=2,
                  group=10,
                  label=Interaction,
                  shape=box];
              "ide.tools.idetools.MenuEntry.MenuEntry" [color=2,
                  group=10,
                  label=MenuEntry,
                  shape=box];
              "ide.tools.idetools.MenuSection.MenuSection" [color=2,
                  group=10,
                  label=MenuSection,
                  shape=box];
              "ide.tools.idetools.Prompt.Prompt" [color=2,
                  group=10,
                  label=Prompt,
                  shape=box];
              "ide.tools.idetools.Transcript.Transcript" [color=2,
                  group=10,
                  label=Transcript,
                  shape=box];
              "ide.tools.idetools.TranscriptEntry.TranscriptEntry" [color=2,
                  group=10,
                  label=TranscriptEntry,
                  shape=box];
          }
          "abjad.tools.abctools.AbjadObject.AbjadObject" -> "abjad.demos.part.PartCantusScoreTemplate.PartCantusScoreTemplate";
          "abjad.tools.abctools.AbjadObject.AbjadObject" -> "abjad.tools.abjadbooktools.LaTeXDocumentHandler.LaTeXDocumentHandler";
          "abjad.tools.abctools.AbjadObject.AbjadObject" -> "abjad.tools.abjadbooktools.SphinxDocumentHandler.SphinxDocumentHandler";
          "abjad.tools.abctools.AbjadObject.AbjadObject" -> "abjad.tools.agenttools.InspectionAgent.InspectionAgent";
          "abjad.tools.abctools.AbjadObject.AbjadObject" -> "abjad.tools.agenttools.IterationAgent.IterationAgent";
          "abjad.tools.abctools.AbjadObject.AbjadObject" -> "abjad.tools.agenttools.LabelAgent.LabelAgent";
          "abjad.tools.abctools.AbjadObject.AbjadObject" -> "abjad.tools.agenttools.MutationAgent.MutationAgent";
          "abjad.tools.abctools.AbjadObject.AbjadObject" -> "abjad.tools.agenttools.PersistenceAgent.PersistenceAgent";
          "abjad.tools.abctools.AbjadObject.AbjadObject" -> "abjad.tools.datastructuretools.Cursor.Cursor";
          "abjad.tools.abctools.AbjadObject.AbjadObject" -> "abjad.tools.datastructuretools.CyclicTuple.CyclicTuple";
          "abjad.tools.abctools.AbjadObject.AbjadObject" -> "abjad.tools.datastructuretools.Matrix.Matrix";
          "abjad.tools.abctools.AbjadObject.AbjadObject" -> "abjad.tools.datastructuretools.OrdinalConstant.OrdinalConstant";
          "abjad.tools.abctools.AbjadObject.AbjadObject" -> "abjad.tools.datastructuretools.PayloadTree.PayloadTree";
          "abjad.tools.abctools.AbjadObject.AbjadObject" -> "abjad.tools.datastructuretools.TreeNode.TreeNode";
          "abjad.tools.abctools.AbjadObject.AbjadObject" -> "abjad.tools.datastructuretools.TypedCollection.TypedCollection";
          "abjad.tools.abctools.AbjadObject.AbjadObject" -> "abjad.tools.developerscripttools.DeveloperScript.DeveloperScript";
          "abjad.tools.abctools.AbjadObject.AbjadObject" -> "abjad.tools.documentationtools.DocumentationManager.DocumentationManager";
          "abjad.tools.abctools.AbjadObject.AbjadObject" -> "abjad.tools.documentationtools.GraphvizMixin.GraphvizMixin";
          "abjad.tools.abctools.AbjadObject.AbjadObject" -> "abjad.tools.documentationtools.InheritanceGraph.InheritanceGraph";
          "abjad.tools.abctools.AbjadObject.AbjadObject" -> "abjad.tools.durationtools.Duration.Duration";
          "abjad.tools.abctools.AbjadObject.AbjadObject" -> "abjad.tools.expressiontools.Callback.Callback";
          "abjad.tools.abctools.AbjadObject.AbjadObject" -> "abjad.tools.expressiontools.Expression.Expression";
          "abjad.tools.abctools.AbjadObject.AbjadObject" -> "abjad.tools.indicatortools.MetricModulation.MetricModulation";
          "abjad.tools.abctools.AbjadObject.AbjadObject" -> "abjad.tools.indicatortools.SpacingIndication.SpacingIndication";
          "abjad.tools.abctools.AbjadObject.AbjadObject" -> "abjad.tools.instrumenttools.Instrument.Instrument";
          "abjad.tools.abctools.AbjadObject.AbjadObject" -> "abjad.tools.instrumenttools.Performer.Performer";
          "abjad.tools.abctools.AbjadObject.AbjadObject" -> "abjad.tools.instrumenttools.WoodwindFingering.WoodwindFingering";
          "abjad.tools.abctools.AbjadObject.AbjadObject" -> "abjad.tools.lilypondfiletools.Block.Block";
          "abjad.tools.abctools.AbjadObject.AbjadObject" -> "abjad.tools.lilypondfiletools.DateTimeToken.DateTimeToken";
          "abjad.tools.abctools.AbjadObject.AbjadObject" -> "abjad.tools.lilypondfiletools.LilyPondDimension.LilyPondDimension";
          "abjad.tools.abctools.AbjadObject.AbjadObject" -> "abjad.tools.lilypondfiletools.LilyPondFile.LilyPondFile";
          "abjad.tools.abctools.AbjadObject.AbjadObject" -> "abjad.tools.lilypondfiletools.LilyPondVersionToken.LilyPondVersionToken";
          "abjad.tools.abctools.AbjadObject.AbjadObject" -> "abjad.tools.lilypondnametools.LilyPondContextSetting.LilyPondContextSetting";
          "abjad.tools.abctools.AbjadObject.AbjadObject" -> "abjad.tools.lilypondnametools.LilyPondGrobOverride.LilyPondGrobOverride";
          "abjad.tools.abctools.AbjadObject.AbjadObject" -> "abjad.tools.lilypondnametools.LilyPondNameManager.LilyPondNameManager";
          "abjad.tools.abctools.AbjadObject.AbjadObject" -> "abjad.tools.lilypondparsertools.GuileProxy.GuileProxy";
          "abjad.tools.abctools.AbjadObject.AbjadObject" -> "abjad.tools.lilypondparsertools.LilyPondDuration.LilyPondDuration";
          "abjad.tools.abctools.AbjadObject.AbjadObject" -> "abjad.tools.lilypondparsertools.LilyPondEvent.LilyPondEvent";
          "abjad.tools.abctools.AbjadObject.AbjadObject" -> "abjad.tools.lilypondparsertools.LilyPondFraction.LilyPondFraction";
          "abjad.tools.abctools.AbjadObject.AbjadObject" -> "abjad.tools.lilypondparsertools.LilyPondGrammarGenerator.LilyPondGrammarGenerator";
          "abjad.tools.abctools.AbjadObject.AbjadObject" -> "abjad.tools.lilypondparsertools.LilyPondLexicalDefinition.LilyPondLexicalDefinition";
          "abjad.tools.abctools.AbjadObject.AbjadObject" -> "abjad.tools.lilypondparsertools.LilyPondSyntacticalDefinition.LilyPondSyntacticalDefinition";
          "abjad.tools.abctools.AbjadObject.AbjadObject" -> "abjad.tools.lilypondparsertools.Music.Music";
          "abjad.tools.abctools.AbjadObject.AbjadObject" -> "abjad.tools.lilypondparsertools.SyntaxNode.SyntaxNode";
          "abjad.tools.abctools.AbjadObject.AbjadObject" -> "abjad.tools.mathtools.BoundedObject.BoundedObject";
          "abjad.tools.abctools.AbjadObject.AbjadObject" -> "abjad.tools.mathtools.Infinity.Infinity";
          "abjad.tools.abctools.AbjadObject.AbjadObject" -> "abjad.tools.mathtools.NonreducedFraction.NonreducedFraction";
          "abjad.tools.abctools.AbjadObject.AbjadObject" -> "abjad.tools.metertools.Meter.Meter";
          "abjad.tools.abctools.AbjadObject.AbjadObject" -> "abjad.tools.metertools.MeterManager.MeterManager";
          "abjad.tools.abctools.AbjadObject.AbjadObject" -> "abjad.tools.pitchtools.Accidental.Accidental";
          "abjad.tools.abctools.AbjadObject.AbjadObject" -> "abjad.tools.pitchtools.Interval.Interval";
          "abjad.tools.abctools.AbjadObject.AbjadObject" -> "abjad.tools.pitchtools.IntervalClass.IntervalClass";
          "abjad.tools.abctools.AbjadObject.AbjadObject" -> "abjad.tools.pitchtools.NumberedPitchClassColorMap.NumberedPitchClassColorMap";
          "abjad.tools.abctools.AbjadObject.AbjadObject" -> "abjad.tools.pitchtools.Octave.Octave";
          "abjad.tools.abctools.AbjadObject.AbjadObject" -> "abjad.tools.pitchtools.Pitch.Pitch";
          "abjad.tools.abctools.AbjadObject.AbjadObject" -> "abjad.tools.pitchtools.PitchArray.PitchArray";
          "abjad.tools.abctools.AbjadObject.AbjadObject" -> "abjad.tools.pitchtools.PitchArrayCell.PitchArrayCell";
          "abjad.tools.abctools.AbjadObject.AbjadObject" -> "abjad.tools.pitchtools.PitchArrayColumn.PitchArrayColumn";
          "abjad.tools.abctools.AbjadObject.AbjadObject" -> "abjad.tools.pitchtools.PitchArrayRow.PitchArrayRow";
          "abjad.tools.abctools.AbjadObject.AbjadObject" -> "abjad.tools.pitchtools.PitchClass.PitchClass";
          "abjad.tools.abctools.AbjadObject.AbjadObject" -> "abjad.tools.pitchtools.PitchRange.PitchRange";
          "abjad.tools.abctools.AbjadObject.AbjadObject" -> "abjad.tools.pitchtools.RegistrationComponent.RegistrationComponent";
          "abjad.tools.abctools.AbjadObject.AbjadObject" -> "abjad.tools.pitchtools.StaffPosition.StaffPosition";
          "abjad.tools.abctools.AbjadObject.AbjadObject" -> "abjad.tools.quantizationtools.AttackPointOptimizer.AttackPointOptimizer";
          "abjad.tools.abctools.AbjadObject.AbjadObject" -> "abjad.tools.quantizationtools.GraceHandler.GraceHandler";
          "abjad.tools.abctools.AbjadObject.AbjadObject" -> "abjad.tools.quantizationtools.Heuristic.Heuristic";
          "abjad.tools.abctools.AbjadObject.AbjadObject" -> "abjad.tools.quantizationtools.JobHandler.JobHandler";
          "abjad.tools.abctools.AbjadObject.AbjadObject" -> "abjad.tools.quantizationtools.ParallelJobHandlerWorker.ParallelJobHandlerWorker";
          "abjad.tools.abctools.AbjadObject.AbjadObject" -> "abjad.tools.quantizationtools.QEvent.QEvent";
          "abjad.tools.abctools.AbjadObject.AbjadObject" -> "abjad.tools.quantizationtools.QEventProxy.QEventProxy";
          "abjad.tools.abctools.AbjadObject.AbjadObject" -> "abjad.tools.quantizationtools.QEventSequence.QEventSequence";
          "abjad.tools.abctools.AbjadObject.AbjadObject" -> "abjad.tools.quantizationtools.QGrid.QGrid";
          "abjad.tools.abctools.AbjadObject.AbjadObject" -> "abjad.tools.quantizationtools.QSchema.QSchema";
          "abjad.tools.abctools.AbjadObject.AbjadObject" -> "abjad.tools.quantizationtools.QSchemaItem.QSchemaItem";
          "abjad.tools.abctools.AbjadObject.AbjadObject" -> "abjad.tools.quantizationtools.QTarget.QTarget";
          "abjad.tools.abctools.AbjadObject.AbjadObject" -> "abjad.tools.quantizationtools.QTargetBeat.QTargetBeat";
          "abjad.tools.abctools.AbjadObject.AbjadObject" -> "abjad.tools.quantizationtools.QTargetMeasure.QTargetMeasure";
          "abjad.tools.abctools.AbjadObject.AbjadObject" -> "abjad.tools.quantizationtools.QuantizationJob.QuantizationJob";
          "abjad.tools.abctools.AbjadObject.AbjadObject" -> "abjad.tools.quantizationtools.Quantizer.Quantizer";
          "abjad.tools.abctools.AbjadObject.AbjadObject" -> "abjad.tools.quantizationtools.SearchTree.SearchTree";
          "abjad.tools.abctools.AbjadObject.AbjadObject" -> "abjad.tools.rhythmtreetools.RhythmTreeMixin.RhythmTreeMixin";
          "abjad.tools.abctools.AbjadObject.AbjadObject" -> "abjad.tools.scoretools.Component.Component";
          "abjad.tools.abctools.AbjadObject.AbjadObject" -> "abjad.tools.scoretools.NoteHead.NoteHead";
          "abjad.tools.abctools.AbjadObject.AbjadObject" -> "abjad.tools.sequencetools.Sequence.Sequence";
          "abjad.tools.abctools.AbjadObject.AbjadObject" -> "abjad.tools.spannertools.Spanner.Spanner";
          "abjad.tools.abctools.AbjadObject.AbjadObject" -> "abjad.tools.systemtools.BenchmarkScoreMaker.BenchmarkScoreMaker";
          "abjad.tools.abctools.AbjadObject.AbjadObject" -> "abjad.tools.systemtools.Configuration.Configuration";
          "abjad.tools.abctools.AbjadObject.AbjadObject" -> "abjad.tools.systemtools.IOManager.IOManager";
          "abjad.tools.abctools.AbjadObject.AbjadObject" -> "abjad.tools.systemtools.ImportManager.ImportManager";
          "abjad.tools.abctools.AbjadObject.AbjadObject" -> "abjad.tools.systemtools.LilyPondFormatBundle.LilyPondFormatBundle";
          "abjad.tools.abctools.AbjadObject.AbjadObject" -> "abjad.tools.systemtools.LilyPondFormatManager.LilyPondFormatManager";
          "abjad.tools.abctools.AbjadObject.AbjadObject" -> "abjad.tools.systemtools.StorageFormatManager.StorageFormatManager";
          "abjad.tools.abctools.AbjadObject.AbjadObject" -> "abjad.tools.systemtools.StorageFormatSpecification.StorageFormatSpecification";
          "abjad.tools.abctools.AbjadObject.AbjadObject" -> "abjad.tools.systemtools.TestManager.TestManager";
          "abjad.tools.abctools.AbjadObject.AbjadObject" -> "abjad.tools.systemtools.UpdateManager.UpdateManager";
          "abjad.tools.abctools.AbjadObject.AbjadObject" -> "abjad.tools.systemtools.WellformednessManager.WellformednessManager";
          "abjad.tools.abctools.AbjadObject.AbjadObject" -> "abjad.tools.templatetools.GroupedRhythmicStavesScoreTemplate.GroupedRhythmicStavesScoreTemplate";
          "abjad.tools.abctools.AbjadObject.AbjadObject" -> "abjad.tools.templatetools.GroupedStavesScoreTemplate.GroupedStavesScoreTemplate";
          "abjad.tools.abctools.AbjadObject.AbjadObject" -> "abjad.tools.templatetools.StringQuartetScoreTemplate.StringQuartetScoreTemplate";
          "abjad.tools.abctools.AbjadObject.AbjadObject" -> "abjad.tools.templatetools.TwoStaffPianoScoreTemplate.TwoStaffPianoScoreTemplate";
          "abjad.tools.abctools.AbjadObject.AbjadObject" -> "abjad.tools.timespantools.Inequality.Inequality";
          "abjad.tools.abctools.AbjadObject.AbjadObject" -> "abjad.tools.timespantools.TimeRelation.TimeRelation";
          "abjad.tools.abctools.AbjadObject.AbjadObject" -> "abjad.tools.tonalanalysistools.ChordExtent.ChordExtent";
          "abjad.tools.abctools.AbjadObject.AbjadObject" -> "abjad.tools.tonalanalysistools.ChordInversion.ChordInversion";
          "abjad.tools.abctools.AbjadObject.AbjadObject" -> "abjad.tools.tonalanalysistools.ChordOmission.ChordOmission";
          "abjad.tools.abctools.AbjadObject.AbjadObject" -> "abjad.tools.tonalanalysistools.ChordQuality.ChordQuality";
          "abjad.tools.abctools.AbjadObject.AbjadObject" -> "abjad.tools.tonalanalysistools.ChordSuspension.ChordSuspension";
          "abjad.tools.abctools.AbjadObject.AbjadObject" -> "abjad.tools.tonalanalysistools.Mode.Mode";
          "abjad.tools.abctools.AbjadObject.AbjadObject" -> "abjad.tools.tonalanalysistools.RomanNumeral.RomanNumeral";
          "abjad.tools.abctools.AbjadObject.AbjadObject" -> "abjad.tools.tonalanalysistools.ScaleDegree.ScaleDegree";
          "abjad.tools.abctools.AbjadObject.AbjadObject" -> "abjad.tools.tonalanalysistools.TonalAnalysisAgent.TonalAnalysisAgent";
          "abjad.tools.abctools.AbjadObject.AbjadObject" -> "experimental.tools.constrainttools.Domain.Domain";
          "abjad.tools.abctools.AbjadObject.AbjadObject" -> "experimental.tools.constrainttools._Constraint._Constraint._Constraint";
          "abjad.tools.abctools.AbjadObject.AbjadObject" -> "experimental.tools.constrainttools._SolutionNode._SolutionNode._SolutionNode";
          "abjad.tools.abctools.AbjadObject.AbjadObject" -> "experimental.tools.constrainttools._Solver._Solver._Solver";
          "abjad.tools.abctools.AbjadObject.AbjadObject" -> "experimental.tools.interpolationtools.BreakPointFunction.BreakPointFunction";
          "abjad.tools.abctools.AbjadObject.AbjadObject" -> "experimental.tools.makertools.SegmentMaker.SegmentMaker";
          "abjad.tools.abctools.AbjadObject.AbjadObject" -> "ide.tools.idetools.MenuEntry.MenuEntry";
          "abjad.tools.abctools.AbjadObject.AbjadObject" -> "ide.tools.idetools.MenuSection.MenuSection";
          "abjad.tools.abctools.AbjadObject.AbjadObject" -> "ide.tools.idetools.Prompt.Prompt";
          "abjad.tools.abctools.AbjadObject.AbjadObject" -> "ide.tools.idetools.Transcript.Transcript";
          "abjad.tools.abctools.AbjadObject.AbjadObject" -> "ide.tools.idetools.TranscriptEntry.TranscriptEntry";
          "abjad.tools.abctools.AbjadValueObject.AbjadValueObject" -> "abjad.tools.abjadbooktools.CodeBlock.CodeBlock";
          "abjad.tools.abctools.AbjadValueObject.AbjadValueObject" -> "abjad.tools.abjadbooktools.CodeBlockSpecifier.CodeBlockSpecifier";
          "abjad.tools.abctools.AbjadValueObject.AbjadValueObject" -> "abjad.tools.abjadbooktools.CodeOutputProxy.CodeOutputProxy";
          "abjad.tools.abctools.AbjadValueObject.AbjadValueObject" -> "abjad.tools.abjadbooktools.ImageLayoutSpecifier.ImageLayoutSpecifier";
          "abjad.tools.abctools.AbjadValueObject.AbjadValueObject" -> "abjad.tools.abjadbooktools.ImageOutputProxy.ImageOutputProxy";
          "abjad.tools.abctools.AbjadValueObject.AbjadValueObject" -> "abjad.tools.abjadbooktools.ImageRenderSpecifier.ImageRenderSpecifier";
          "abjad.tools.abctools.AbjadValueObject.AbjadValueObject" -> "abjad.tools.indicatortools.Accelerando.Accelerando";
          "abjad.tools.abctools.AbjadValueObject.AbjadValueObject" -> "abjad.tools.indicatortools.Annotation.Annotation";
          "abjad.tools.abctools.AbjadValueObject.AbjadValueObject" -> "abjad.tools.indicatortools.Arpeggio.Arpeggio";
          "abjad.tools.abctools.AbjadValueObject.AbjadValueObject" -> "abjad.tools.indicatortools.Articulation.Articulation";
          "abjad.tools.abctools.AbjadValueObject.AbjadValueObject" -> "abjad.tools.indicatortools.BarLine.BarLine";
          "abjad.tools.abctools.AbjadValueObject.AbjadValueObject" -> "abjad.tools.indicatortools.BendAfter.BendAfter";
          "abjad.tools.abctools.AbjadValueObject.AbjadValueObject" -> "abjad.tools.indicatortools.BowContactPoint.BowContactPoint";
          "abjad.tools.abctools.AbjadValueObject.AbjadValueObject" -> "abjad.tools.indicatortools.BowMotionTechnique.BowMotionTechnique";
          "abjad.tools.abctools.AbjadValueObject.AbjadValueObject" -> "abjad.tools.indicatortools.BowPressure.BowPressure";
          "abjad.tools.abctools.AbjadValueObject.AbjadValueObject" -> "abjad.tools.indicatortools.BreathMark.BreathMark";
          "abjad.tools.abctools.AbjadValueObject.AbjadValueObject" -> "abjad.tools.indicatortools.Clef.Clef";
          "abjad.tools.abctools.AbjadValueObject.AbjadValueObject" -> "abjad.tools.indicatortools.ColorFingering.ColorFingering";
          "abjad.tools.abctools.AbjadValueObject.AbjadValueObject" -> "abjad.tools.indicatortools.Dynamic.Dynamic";
          "abjad.tools.abctools.AbjadValueObject.AbjadValueObject" -> "abjad.tools.indicatortools.Fermata.Fermata";
          "abjad.tools.abctools.AbjadValueObject.AbjadValueObject" -> "abjad.tools.indicatortools.IndicatorExpression.IndicatorExpression";
          "abjad.tools.abctools.AbjadValueObject.AbjadValueObject" -> "abjad.tools.indicatortools.IsAtSoundingPitch.IsAtSoundingPitch";
          "abjad.tools.abctools.AbjadValueObject.AbjadValueObject" -> "abjad.tools.indicatortools.IsUnpitched.IsUnpitched";
          "abjad.tools.abctools.AbjadValueObject.AbjadValueObject" -> "abjad.tools.indicatortools.KeyCluster.KeyCluster";
          "abjad.tools.abctools.AbjadValueObject.AbjadValueObject" -> "abjad.tools.indicatortools.KeySignature.KeySignature";
          "abjad.tools.abctools.AbjadValueObject.AbjadValueObject" -> "abjad.tools.indicatortools.LaissezVibrer.LaissezVibrer";
          "abjad.tools.abctools.AbjadValueObject.AbjadValueObject" -> "abjad.tools.indicatortools.LilyPondCommand.LilyPondCommand";
          "abjad.tools.abctools.AbjadValueObject.AbjadValueObject" -> "abjad.tools.indicatortools.LilyPondComment.LilyPondComment";
          "abjad.tools.abctools.AbjadValueObject.AbjadValueObject" -> "abjad.tools.indicatortools.LineSegment.LineSegment";
          "abjad.tools.abctools.AbjadValueObject.AbjadValueObject" -> "abjad.tools.indicatortools.PageBreak.PageBreak";
          "abjad.tools.abctools.AbjadValueObject.AbjadValueObject" -> "abjad.tools.indicatortools.RehearsalMark.RehearsalMark";
          "abjad.tools.abctools.AbjadValueObject.AbjadValueObject" -> "abjad.tools.indicatortools.Repeat.Repeat";
          "abjad.tools.abctools.AbjadValueObject.AbjadValueObject" -> "abjad.tools.indicatortools.Ritardando.Ritardando";
          "abjad.tools.abctools.AbjadValueObject.AbjadValueObject" -> "abjad.tools.indicatortools.StaffChange.StaffChange";
          "abjad.tools.abctools.AbjadValueObject.AbjadValueObject" -> "abjad.tools.indicatortools.StemTremolo.StemTremolo";
          "abjad.tools.abctools.AbjadValueObject.AbjadValueObject" -> "abjad.tools.indicatortools.StringContactPoint.StringContactPoint";
          "abjad.tools.abctools.AbjadValueObject.AbjadValueObject" -> "abjad.tools.indicatortools.StringNumber.StringNumber";
          "abjad.tools.abctools.AbjadValueObject.AbjadValueObject" -> "abjad.tools.indicatortools.SystemBreak.SystemBreak";
          "abjad.tools.abctools.AbjadValueObject.AbjadValueObject" -> "abjad.tools.indicatortools.Tempo.Tempo";
          "abjad.tools.abctools.AbjadValueObject.AbjadValueObject" -> "abjad.tools.indicatortools.TimeSignature.TimeSignature";
          "abjad.tools.abctools.AbjadValueObject.AbjadValueObject" -> "abjad.tools.indicatortools.Tremolo.Tremolo";
          "abjad.tools.abctools.AbjadValueObject.AbjadValueObject" -> "abjad.tools.indicatortools.Tuning.Tuning";
          "abjad.tools.abctools.AbjadValueObject.AbjadValueObject" -> "abjad.tools.lilypondfiletools.LilyPondLanguageToken.LilyPondLanguageToken";
          "abjad.tools.abctools.AbjadValueObject.AbjadValueObject" -> "abjad.tools.lilypondfiletools.PackageGitCommitToken.PackageGitCommitToken";
          "abjad.tools.abctools.AbjadValueObject.AbjadValueObject" -> "abjad.tools.lilypondnametools.LilyPondContext.LilyPondContext";
          "abjad.tools.abctools.AbjadValueObject.AbjadValueObject" -> "abjad.tools.lilypondnametools.LilyPondEngraver.LilyPondEngraver";
          "abjad.tools.abctools.AbjadValueObject.AbjadValueObject" -> "abjad.tools.lilypondnametools.LilyPondGrob.LilyPondGrob";
          "abjad.tools.abctools.AbjadValueObject.AbjadValueObject" -> "abjad.tools.lilypondnametools.LilyPondGrobInterface.LilyPondGrobInterface";
          "abjad.tools.abctools.AbjadValueObject.AbjadValueObject" -> "abjad.tools.markuptools.Markup.Markup";
          "abjad.tools.abctools.AbjadValueObject.AbjadValueObject" -> "abjad.tools.markuptools.MarkupCommand.MarkupCommand";
          "abjad.tools.abctools.AbjadValueObject.AbjadValueObject" -> "abjad.tools.markuptools.Postscript.Postscript";
          "abjad.tools.abctools.AbjadValueObject.AbjadValueObject" -> "abjad.tools.markuptools.PostscriptOperator.PostscriptOperator";
          "abjad.tools.abctools.AbjadValueObject.AbjadValueObject" -> "abjad.tools.mathtools.NonreducedRatio.NonreducedRatio";
          "abjad.tools.abctools.AbjadValueObject.AbjadValueObject" -> "abjad.tools.metertools.MeterFittingSession.MeterFittingSession";
          "abjad.tools.abctools.AbjadValueObject.AbjadValueObject" -> "abjad.tools.metertools.MetricAccentKernel.MetricAccentKernel";
          "abjad.tools.abctools.AbjadValueObject.AbjadValueObject" -> "abjad.tools.patterntools.Pattern.Pattern";
          "abjad.tools.abctools.AbjadValueObject.AbjadValueObject" -> "abjad.tools.pitchtools.Inversion.Inversion";
          "abjad.tools.abctools.AbjadValueObject.AbjadValueObject" -> "abjad.tools.pitchtools.Multiplication.Multiplication";
          "abjad.tools.abctools.AbjadValueObject.AbjadValueObject" -> "abjad.tools.pitchtools.PitchOperation.PitchOperation";
          "abjad.tools.abctools.AbjadValueObject.AbjadValueObject" -> "abjad.tools.pitchtools.Retrogression.Retrogression";
          "abjad.tools.abctools.AbjadValueObject.AbjadValueObject" -> "abjad.tools.pitchtools.Rotation.Rotation";
          "abjad.tools.abctools.AbjadValueObject.AbjadValueObject" -> "abjad.tools.pitchtools.Transposition.Transposition";
          "abjad.tools.abctools.AbjadValueObject.AbjadValueObject" -> "abjad.tools.rhythmmakertools.BeamSpecifier.BeamSpecifier";
          "abjad.tools.abctools.AbjadValueObject.AbjadValueObject" -> "abjad.tools.rhythmmakertools.BurnishSpecifier.BurnishSpecifier";
          "abjad.tools.abctools.AbjadValueObject.AbjadValueObject" -> "abjad.tools.rhythmmakertools.DurationSpellingSpecifier.DurationSpellingSpecifier";
          "abjad.tools.abctools.AbjadValueObject.AbjadValueObject" -> "abjad.tools.rhythmmakertools.ExampleWrapper.ExampleWrapper";
          "abjad.tools.abctools.AbjadValueObject.AbjadValueObject" -> "abjad.tools.rhythmmakertools.GalleryMaker.GalleryMaker";
          "abjad.tools.abctools.AbjadValueObject.AbjadValueObject" -> "abjad.tools.rhythmmakertools.InciseSpecifier.InciseSpecifier";
          "abjad.tools.abctools.AbjadValueObject.AbjadValueObject" -> "abjad.tools.rhythmmakertools.InterpolationSpecifier.InterpolationSpecifier";
          "abjad.tools.abctools.AbjadValueObject.AbjadValueObject" -> "abjad.tools.rhythmmakertools.RhythmMaker.RhythmMaker";
          "abjad.tools.abctools.AbjadValueObject.AbjadValueObject" -> "abjad.tools.rhythmmakertools.SilenceMask.SilenceMask";
          "abjad.tools.abctools.AbjadValueObject.AbjadValueObject" -> "abjad.tools.rhythmmakertools.SustainMask.SustainMask";
          "abjad.tools.abctools.AbjadValueObject.AbjadValueObject" -> "abjad.tools.rhythmmakertools.Talea.Talea";
          "abjad.tools.abctools.AbjadValueObject.AbjadValueObject" -> "abjad.tools.rhythmmakertools.TieSpecifier.TieSpecifier";
          "abjad.tools.abctools.AbjadValueObject.AbjadValueObject" -> "abjad.tools.rhythmmakertools.TupletSpellingSpecifier.TupletSpellingSpecifier";
          "abjad.tools.abctools.AbjadValueObject.AbjadValueObject" -> "abjad.tools.schemetools.Scheme.Scheme";
          "abjad.tools.abctools.AbjadValueObject.AbjadValueObject" -> "abjad.tools.selectortools.ContiguitySelectorCallback.ContiguitySelectorCallback";
          "abjad.tools.abctools.AbjadValueObject.AbjadValueObject" -> "abjad.tools.selectortools.CountsSelectorCallback.CountsSelectorCallback";
          "abjad.tools.abctools.AbjadValueObject.AbjadValueObject" -> "abjad.tools.selectortools.DurationSelectorCallback.DurationSelectorCallback";
          "abjad.tools.abctools.AbjadValueObject.AbjadValueObject" -> "abjad.tools.selectortools.ExtraLeafSelectorCallback.ExtraLeafSelectorCallback";
          "abjad.tools.abctools.AbjadValueObject.AbjadValueObject" -> "abjad.tools.selectortools.FlattenSelectorCallback.FlattenSelectorCallback";
          "abjad.tools.abctools.AbjadValueObject.AbjadValueObject" -> "abjad.tools.selectortools.Inequality.Inequality";
          "abjad.tools.abctools.AbjadValueObject.AbjadValueObject" -> "abjad.tools.selectortools.ItemSelectorCallback.ItemSelectorCallback";
          "abjad.tools.abctools.AbjadValueObject.AbjadValueObject" -> "abjad.tools.selectortools.LengthSelectorCallback.LengthSelectorCallback";
          "abjad.tools.abctools.AbjadValueObject.AbjadValueObject" -> "abjad.tools.selectortools.LogicalMeasureSelectorCallback.LogicalMeasureSelectorCallback";
          "abjad.tools.abctools.AbjadValueObject.AbjadValueObject" -> "abjad.tools.selectortools.LogicalTieSelectorCallback.LogicalTieSelectorCallback";
          "abjad.tools.abctools.AbjadValueObject.AbjadValueObject" -> "abjad.tools.selectortools.PartitionByRatioCallback.PartitionByRatioCallback";
          "abjad.tools.abctools.AbjadValueObject.AbjadValueObject" -> "abjad.tools.selectortools.PatternedSelectorCallback.PatternedSelectorCallback";
          "abjad.tools.abctools.AbjadValueObject.AbjadValueObject" -> "abjad.tools.selectortools.PitchSelectorCallback.PitchSelectorCallback";
          "abjad.tools.abctools.AbjadValueObject.AbjadValueObject" -> "abjad.tools.selectortools.PrototypeSelectorCallback.PrototypeSelectorCallback";
          "abjad.tools.abctools.AbjadValueObject.AbjadValueObject" -> "abjad.tools.selectortools.RunSelectorCallback.RunSelectorCallback";
          "abjad.tools.abctools.AbjadValueObject.AbjadValueObject" -> "abjad.tools.selectortools.Selector.Selector";
          "abjad.tools.abctools.AbjadValueObject.AbjadValueObject" -> "abjad.tools.selectortools.SliceSelectorCallback.SliceSelectorCallback";
          "abjad.tools.abctools.AbjadValueObject.AbjadValueObject" -> "abjad.tools.sequencetools.Duplication.Duplication";
          "abjad.tools.abctools.AbjadValueObject.AbjadValueObject" -> "abjad.tools.templatetools.StringOrchestraScoreTemplate.StringOrchestraScoreTemplate";
          "abjad.tools.abctools.ContextManager.ContextManager" -> "abjad.tools.systemtools.FilesystemState.FilesystemState";
          "abjad.tools.abctools.ContextManager.ContextManager" -> "abjad.tools.systemtools.ForbidUpdate.ForbidUpdate";
          "abjad.tools.abctools.ContextManager.ContextManager" -> "abjad.tools.systemtools.NullContextManager.NullContextManager";
          "abjad.tools.abctools.ContextManager.ContextManager" -> "abjad.tools.systemtools.ProgressIndicator.ProgressIndicator";
          "abjad.tools.abctools.ContextManager.ContextManager" -> "abjad.tools.systemtools.RedirectedStreams.RedirectedStreams";
          "abjad.tools.abctools.ContextManager.ContextManager" -> "abjad.tools.systemtools.TemporaryDirectory.TemporaryDirectory";
          "abjad.tools.abctools.ContextManager.ContextManager" -> "abjad.tools.systemtools.TemporaryDirectoryChange.TemporaryDirectoryChange";
          "abjad.tools.abctools.ContextManager.ContextManager" -> "abjad.tools.systemtools.Timer.Timer";
          "abjad.tools.abctools.ContextManager.ContextManager" -> "ide.tools.idetools.Interaction.Interaction";
          "abjad.tools.abctools.Parser.Parser" -> "abjad.tools.lilypondparsertools.LilyPondParser.LilyPondParser";
          "abjad.tools.abctools.Parser.Parser" -> "abjad.tools.lilypondparsertools.ReducedLyParser.ReducedLyParser";
          "abjad.tools.abctools.Parser.Parser" -> "abjad.tools.lilypondparsertools.SchemeParser.SchemeParser";
          "abjad.tools.abctools.Parser.Parser" -> "abjad.tools.rhythmtreetools.RhythmTreeParser.RhythmTreeParser";
          "abjad.tools.datastructuretools.PayloadTree.PayloadTree" -> "abjad.tools.pitchtools.PitchClassTree.PitchClassTree";
          "abjad.tools.datastructuretools.TreeContainer.TreeContainer" -> "abjad.tools.documentationtools.GraphvizGraph.GraphvizGraph";
          "abjad.tools.datastructuretools.TreeContainer.TreeContainer" -> "abjad.tools.documentationtools.GraphvizGroup.GraphvizGroup";
          "abjad.tools.datastructuretools.TreeContainer.TreeContainer" -> "abjad.tools.documentationtools.GraphvizNode.GraphvizNode";
          "abjad.tools.datastructuretools.TreeContainer.TreeContainer" -> "abjad.tools.documentationtools.GraphvizTable.GraphvizTable";
          "abjad.tools.datastructuretools.TreeContainer.TreeContainer" -> "abjad.tools.documentationtools.GraphvizTableRow.GraphvizTableRow";
          "abjad.tools.datastructuretools.TreeContainer.TreeContainer" -> "abjad.tools.documentationtools.ReSTDirective.ReSTDirective";
          "abjad.tools.datastructuretools.TreeContainer.TreeContainer" -> "abjad.tools.documentationtools.ReSTDocument.ReSTDocument";
          "abjad.tools.datastructuretools.TreeContainer.TreeContainer" -> "abjad.tools.rhythmtreetools.RhythmTreeContainer.RhythmTreeContainer";
          "abjad.tools.datastructuretools.TreeNode.TreeNode" -> "abjad.tools.documentationtools.GraphvizField.GraphvizField";
          "abjad.tools.datastructuretools.TreeNode.TreeNode" -> "abjad.tools.documentationtools.GraphvizTableCell.GraphvizTableCell";
          "abjad.tools.datastructuretools.TreeNode.TreeNode" -> "abjad.tools.documentationtools.GraphvizTableHorizontalRule.GraphvizTableHorizontalRule";
          "abjad.tools.datastructuretools.TreeNode.TreeNode" -> "abjad.tools.documentationtools.GraphvizTableVerticalRule.GraphvizTableVerticalRule";
          "abjad.tools.datastructuretools.TreeNode.TreeNode" -> "abjad.tools.documentationtools.ReSTAutosummaryItem.ReSTAutosummaryItem";
          "abjad.tools.datastructuretools.TreeNode.TreeNode" -> "abjad.tools.documentationtools.ReSTHeading.ReSTHeading";
          "abjad.tools.datastructuretools.TreeNode.TreeNode" -> "abjad.tools.documentationtools.ReSTHorizontalRule.ReSTHorizontalRule";
          "abjad.tools.datastructuretools.TreeNode.TreeNode" -> "abjad.tools.documentationtools.ReSTParagraph.ReSTParagraph";
          "abjad.tools.datastructuretools.TreeNode.TreeNode" -> "abjad.tools.documentationtools.ReSTTOCItem.ReSTTOCItem";
          "abjad.tools.datastructuretools.TreeNode.TreeNode" -> "abjad.tools.quantizationtools.QGridLeaf.QGridLeaf";
          "abjad.tools.datastructuretools.TreeNode.TreeNode" -> "abjad.tools.rhythmtreetools.RhythmTreeLeaf.RhythmTreeLeaf";
          "abjad.tools.datastructuretools.TypedCounter.TypedCounter" -> "abjad.tools.metertools.OffsetCounter.OffsetCounter";
          "abjad.tools.datastructuretools.TypedCounter.TypedCounter" -> "abjad.tools.pitchtools.Vector.Vector";
          "abjad.tools.datastructuretools.TypedCounter.TypedCounter" -> "abjad.tools.rhythmmakertools.RotationCounter.RotationCounter";
          "abjad.tools.datastructuretools.TypedFrozenset.TypedFrozenset" -> "abjad.tools.pitchtools.Set.Set";
          "abjad.tools.datastructuretools.TypedList.TypedList" -> "abjad.tools.indicatortools.ClefInventory.ClefInventory";
          "abjad.tools.datastructuretools.TypedList.TypedList" -> "abjad.tools.indicatortools.TempoInventory.TempoInventory";
          "abjad.tools.datastructuretools.TypedList.TypedList" -> "abjad.tools.indicatortools.TimeSignatureInventory.TimeSignatureInventory";
          "abjad.tools.datastructuretools.TypedList.TypedList" -> "abjad.tools.instrumenttools.InstrumentInventory.InstrumentInventory";
          "abjad.tools.datastructuretools.TypedList.TypedList" -> "abjad.tools.instrumenttools.PerformerInventory.PerformerInventory";
          "abjad.tools.datastructuretools.TypedList.TypedList" -> "abjad.tools.markuptools.MarkupInventory.MarkupInventory";
          "abjad.tools.datastructuretools.TypedList.TypedList" -> "abjad.tools.metertools.MeterInventory.MeterInventory";
          "abjad.tools.datastructuretools.TypedList.TypedList" -> "abjad.tools.pitchtools.PitchArrayInventory.PitchArrayInventory";
          "abjad.tools.datastructuretools.TypedList.TypedList" -> "abjad.tools.pitchtools.PitchRangeInventory.PitchRangeInventory";
          "abjad.tools.datastructuretools.TypedList.TypedList" -> "abjad.tools.pitchtools.Registration.Registration";
          "abjad.tools.datastructuretools.TypedList.TypedList" -> "abjad.tools.pitchtools.RegistrationInventory.RegistrationInventory";
          "abjad.tools.datastructuretools.TypedList.TypedList" -> "abjad.tools.scoretools.NoteHeadInventory.NoteHeadInventory";
          "abjad.tools.datastructuretools.TypedList.TypedList" -> "abjad.tools.selectiontools.SelectionInventory.SelectionInventory";
          "abjad.tools.datastructuretools.TypedList.TypedList" -> "abjad.tools.timespantools.CompoundInequality.CompoundInequality";
          "abjad.tools.datastructuretools.TypedList.TypedList" -> "abjad.tools.timespantools.TimespanInventory.TimespanInventory";
          "abjad.tools.datastructuretools.TypedOrderedDict.TypedOrderedDict" -> "abjad.tools.rhythmmakertools.PartitionTable.PartitionTable";
          "abjad.tools.datastructuretools.TypedTuple.TypedTuple" -> "abjad.tools.patterntools.CompoundPattern.CompoundPattern";
          "abjad.tools.datastructuretools.TypedTuple.TypedTuple" -> "abjad.tools.patterntools.PatternInventory.PatternInventory";
          "abjad.tools.datastructuretools.TypedTuple.TypedTuple" -> "abjad.tools.pitchtools.Segment.Segment";
          "abjad.tools.developerscripttools.DeveloperScript.DeveloperScript" -> "abjad.tools.abjadbooktools.AbjadBookScript.AbjadBookScript";
          "abjad.tools.mathtools.BoundedObject.BoundedObject" -> "abjad.tools.timespantools.Timespan.Timespan";
          "abjad.tools.mathtools.NonreducedFraction.NonreducedFraction" -> "abjad.tools.durationtools.Division.Division";
          "abjad.tools.pitchtools.IntervalSegment.IntervalSegment" -> "abjad.tools.tonalanalysistools.RootlessChordClass.RootlessChordClass";
          "abjad.tools.pitchtools.PitchClassSegment.PitchClassSegment" -> "abjad.tools.tonalanalysistools.Scale.Scale";
          "abjad.tools.pitchtools.PitchClassSet.PitchClassSet" -> "abjad.tools.tonalanalysistools.RootedChordClass.RootedChordClass";
          "abjad.tools.rhythmtreetools.RhythmTreeContainer.RhythmTreeContainer" -> "abjad.tools.quantizationtools.QGridContainer.QGridContainer";
          "abjad.tools.rhythmtreetools.RhythmTreeMixin.RhythmTreeMixin" -> "abjad.tools.quantizationtools.QGridLeaf.QGridLeaf";
          "abjad.tools.systemtools.Configuration.Configuration" -> "ide.tools.idetools.AbjadIDEConfiguration.AbjadIDEConfiguration";
          "abjad.tools.systemtools.IOManager.IOManager" -> "ide.tools.idetools.IOManager.IOManager";
          "builtins.object" -> "abjad.tools.abctools.AbjadObject.AbstractBase";
      }

--------

Abstract Classes
----------------

.. toctree::
   :hidden:

   ContextManager
   Parser

.. autosummary::
   :nosignatures:

   ContextManager
   Parser

--------

Classes
-------

.. toctree::
   :hidden:

   AbjadObject
   AbjadValueObject

.. autosummary::
   :nosignatures:

   AbjadObject
   AbjadValueObject
