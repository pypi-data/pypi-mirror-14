datastructuretools
==================

.. automodule:: abjad.tools.datastructuretools

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
              "abjad.tools.datastructuretools.Cursor.Cursor" [color=black,
                  fontcolor=white,
                  group=2,
                  label=Cursor,
                  shape=box,
                  style="filled, rounded"];
              "abjad.tools.datastructuretools.CyclicMatrix.CyclicMatrix" [color=black,
                  fontcolor=white,
                  group=2,
                  label=CyclicMatrix,
                  shape=box,
                  style="filled, rounded"];
              "abjad.tools.datastructuretools.CyclicPayloadTree.CyclicPayloadTree" [color=black,
                  fontcolor=white,
                  group=2,
                  label=CyclicPayloadTree,
                  shape=box,
                  style="filled, rounded"];
              "abjad.tools.datastructuretools.CyclicTuple.CyclicTuple" [color=black,
                  fontcolor=white,
                  group=2,
                  label=CyclicTuple,
                  shape=box,
                  style="filled, rounded"];
              "abjad.tools.datastructuretools.Enumeration.Enumeration" [color=black,
                  fontcolor=white,
                  group=2,
                  label=Enumeration,
                  shape=box,
                  style="filled, rounded"];
              "abjad.tools.datastructuretools.Matrix.Matrix" [color=black,
                  fontcolor=white,
                  group=2,
                  label=Matrix,
                  shape=box,
                  style="filled, rounded"];
              "abjad.tools.datastructuretools.OrdinalConstant.OrdinalConstant" [color=black,
                  fontcolor=white,
                  group=2,
                  label=OrdinalConstant,
                  shape=box,
                  style="filled, rounded"];
              "abjad.tools.datastructuretools.PayloadTree.PayloadTree" [color=black,
                  fontcolor=white,
                  group=2,
                  label=PayloadTree,
                  shape=box,
                  style="filled, rounded"];
              "abjad.tools.datastructuretools.SortedCollection.SortedCollection" [color=black,
                  fontcolor=white,
                  group=2,
                  label=SortedCollection,
                  shape=box,
                  style="filled, rounded"];
              "abjad.tools.datastructuretools.TreeContainer.TreeContainer" [color=black,
                  fontcolor=white,
                  group=2,
                  label=TreeContainer,
                  shape=box,
                  style="filled, rounded"];
              "abjad.tools.datastructuretools.TreeNode.TreeNode" [color=black,
                  fontcolor=white,
                  group=2,
                  label=TreeNode,
                  shape=box,
                  style="filled, rounded"];
              "abjad.tools.datastructuretools.TypedCollection.TypedCollection" [color=black,
                  fontcolor=white,
                  group=2,
                  label=TypedCollection,
                  shape=oval,
                  style="filled, rounded"];
              "abjad.tools.datastructuretools.TypedCounter.TypedCounter" [color=black,
                  fontcolor=white,
                  group=2,
                  label=TypedCounter,
                  shape=box,
                  style="filled, rounded"];
              "abjad.tools.datastructuretools.TypedFrozenset.TypedFrozenset" [color=black,
                  fontcolor=white,
                  group=2,
                  label=TypedFrozenset,
                  shape=box,
                  style="filled, rounded"];
              "abjad.tools.datastructuretools.TypedList.TypedList" [color=black,
                  fontcolor=white,
                  group=2,
                  label=TypedList,
                  shape=box,
                  style="filled, rounded"];
              "abjad.tools.datastructuretools.TypedOrderedDict.TypedOrderedDict" [color=black,
                  fontcolor=white,
                  group=2,
                  label=TypedOrderedDict,
                  shape=box,
                  style="filled, rounded"];
              "abjad.tools.datastructuretools.TypedTuple.TypedTuple" [color=black,
                  fontcolor=white,
                  group=2,
                  label=TypedTuple,
                  shape=box,
                  style="filled, rounded"];
              "abjad.tools.datastructuretools.Matrix.Matrix" -> "abjad.tools.datastructuretools.CyclicMatrix.CyclicMatrix";
              "abjad.tools.datastructuretools.PayloadTree.PayloadTree" -> "abjad.tools.datastructuretools.CyclicPayloadTree.CyclicPayloadTree";
              "abjad.tools.datastructuretools.TreeNode.TreeNode" -> "abjad.tools.datastructuretools.TreeContainer.TreeContainer";
              "abjad.tools.datastructuretools.TypedCollection.TypedCollection" -> "abjad.tools.datastructuretools.TypedCounter.TypedCounter";
              "abjad.tools.datastructuretools.TypedCollection.TypedCollection" -> "abjad.tools.datastructuretools.TypedFrozenset.TypedFrozenset";
              "abjad.tools.datastructuretools.TypedCollection.TypedCollection" -> "abjad.tools.datastructuretools.TypedList.TypedList";
              "abjad.tools.datastructuretools.TypedCollection.TypedCollection" -> "abjad.tools.datastructuretools.TypedOrderedDict.TypedOrderedDict";
              "abjad.tools.datastructuretools.TypedCollection.TypedCollection" -> "abjad.tools.datastructuretools.TypedTuple.TypedTuple";
          }
          subgraph cluster_documentationtools {
              graph [label=documentationtools];
              "abjad.tools.documentationtools.GraphvizField.GraphvizField" [color=4,
                  group=3,
                  label=GraphvizField,
                  shape=box];
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
              "abjad.tools.documentationtools.GraphvizTableCell.GraphvizTableCell" [color=4,
                  group=3,
                  label=GraphvizTableCell,
                  shape=box];
              "abjad.tools.documentationtools.GraphvizTableHorizontalRule.GraphvizTableHorizontalRule" [color=4,
                  group=3,
                  label=GraphvizTableHorizontalRule,
                  shape=box];
              "abjad.tools.documentationtools.GraphvizTableRow.GraphvizTableRow" [color=4,
                  group=3,
                  label=GraphvizTableRow,
                  shape=box];
              "abjad.tools.documentationtools.GraphvizTableVerticalRule.GraphvizTableVerticalRule" [color=4,
                  group=3,
                  label=GraphvizTableVerticalRule,
                  shape=box];
              "abjad.tools.documentationtools.ReSTAutodocDirective.ReSTAutodocDirective" [color=4,
                  group=3,
                  label=ReSTAutodocDirective,
                  shape=box];
              "abjad.tools.documentationtools.ReSTAutosummaryDirective.ReSTAutosummaryDirective" [color=4,
                  group=3,
                  label=ReSTAutosummaryDirective,
                  shape=box];
              "abjad.tools.documentationtools.ReSTAutosummaryItem.ReSTAutosummaryItem" [color=4,
                  group=3,
                  label=ReSTAutosummaryItem,
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
              "abjad.tools.documentationtools.ReSTHeading.ReSTHeading" [color=4,
                  group=3,
                  label=ReSTHeading,
                  shape=box];
              "abjad.tools.documentationtools.ReSTHorizontalRule.ReSTHorizontalRule" [color=4,
                  group=3,
                  label=ReSTHorizontalRule,
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
              "abjad.tools.documentationtools.ReSTParagraph.ReSTParagraph" [color=4,
                  group=3,
                  label=ReSTParagraph,
                  shape=box];
              "abjad.tools.documentationtools.ReSTTOCDirective.ReSTTOCDirective" [color=4,
                  group=3,
                  label=ReSTTOCDirective,
                  shape=box];
              "abjad.tools.documentationtools.ReSTTOCItem.ReSTTOCItem" [color=4,
                  group=3,
                  label=ReSTTOCItem,
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
          subgraph cluster_indicatortools {
              graph [label=indicatortools];
              "abjad.tools.indicatortools.ClefInventory.ClefInventory" [color=6,
                  group=5,
                  label=ClefInventory,
                  shape=box];
              "abjad.tools.indicatortools.TempoInventory.TempoInventory" [color=6,
                  group=5,
                  label=TempoInventory,
                  shape=box];
              "abjad.tools.indicatortools.TimeSignatureInventory.TimeSignatureInventory" [color=6,
                  group=5,
                  label=TimeSignatureInventory,
                  shape=box];
          }
          subgraph cluster_instrumenttools {
              graph [label=instrumenttools];
              "abjad.tools.instrumenttools.InstrumentInventory.InstrumentInventory" [color=7,
                  group=6,
                  label=InstrumentInventory,
                  shape=box];
              "abjad.tools.instrumenttools.PerformerInventory.PerformerInventory" [color=7,
                  group=6,
                  label=PerformerInventory,
                  shape=box];
          }
          subgraph cluster_markuptools {
              graph [label=markuptools];
              "abjad.tools.markuptools.MarkupInventory.MarkupInventory" [color=8,
                  group=7,
                  label=MarkupInventory,
                  shape=box];
          }
          subgraph cluster_metertools {
              graph [label=metertools];
              "abjad.tools.metertools.MeterInventory.MeterInventory" [color=9,
                  group=8,
                  label=MeterInventory,
                  shape=box];
              "abjad.tools.metertools.OffsetCounter.OffsetCounter" [color=9,
                  group=8,
                  label=OffsetCounter,
                  shape=box];
          }
          subgraph cluster_patterntools {
              graph [label=patterntools];
              "abjad.tools.patterntools.CompoundPattern.CompoundPattern" [color=1,
                  group=9,
                  label=CompoundPattern,
                  shape=box];
              "abjad.tools.patterntools.PatternInventory.PatternInventory" [color=1,
                  group=9,
                  label=PatternInventory,
                  shape=box];
          }
          subgraph cluster_pitchtools {
              graph [label=pitchtools];
              "abjad.tools.pitchtools.IntervalClassSegment.IntervalClassSegment" [color=2,
                  group=10,
                  label=IntervalClassSegment,
                  shape=box];
              "abjad.tools.pitchtools.IntervalClassSet.IntervalClassSet" [color=2,
                  group=10,
                  label=IntervalClassSet,
                  shape=box];
              "abjad.tools.pitchtools.IntervalClassVector.IntervalClassVector" [color=2,
                  group=10,
                  label=IntervalClassVector,
                  shape=box];
              "abjad.tools.pitchtools.IntervalSegment.IntervalSegment" [color=2,
                  group=10,
                  label=IntervalSegment,
                  shape=box];
              "abjad.tools.pitchtools.IntervalSet.IntervalSet" [color=2,
                  group=10,
                  label=IntervalSet,
                  shape=box];
              "abjad.tools.pitchtools.IntervalVector.IntervalVector" [color=2,
                  group=10,
                  label=IntervalVector,
                  shape=box];
              "abjad.tools.pitchtools.PitchArrayInventory.PitchArrayInventory" [color=2,
                  group=10,
                  label=PitchArrayInventory,
                  shape=box];
              "abjad.tools.pitchtools.PitchClassSegment.PitchClassSegment" [color=2,
                  group=10,
                  label=PitchClassSegment,
                  shape=box];
              "abjad.tools.pitchtools.PitchClassSet.PitchClassSet" [color=2,
                  group=10,
                  label=PitchClassSet,
                  shape=box];
              "abjad.tools.pitchtools.PitchClassTree.PitchClassTree" [color=2,
                  group=10,
                  label=PitchClassTree,
                  shape=box];
              "abjad.tools.pitchtools.PitchClassVector.PitchClassVector" [color=2,
                  group=10,
                  label=PitchClassVector,
                  shape=box];
              "abjad.tools.pitchtools.PitchRangeInventory.PitchRangeInventory" [color=2,
                  group=10,
                  label=PitchRangeInventory,
                  shape=box];
              "abjad.tools.pitchtools.PitchSegment.PitchSegment" [color=2,
                  group=10,
                  label=PitchSegment,
                  shape=box];
              "abjad.tools.pitchtools.PitchSet.PitchSet" [color=2,
                  group=10,
                  label=PitchSet,
                  shape=box];
              "abjad.tools.pitchtools.PitchVector.PitchVector" [color=2,
                  group=10,
                  label=PitchVector,
                  shape=box];
              "abjad.tools.pitchtools.Registration.Registration" [color=2,
                  group=10,
                  label=Registration,
                  shape=box];
              "abjad.tools.pitchtools.RegistrationInventory.RegistrationInventory" [color=2,
                  group=10,
                  label=RegistrationInventory,
                  shape=box];
              "abjad.tools.pitchtools.Segment.Segment" [color=2,
                  group=10,
                  label=Segment,
                  shape=oval,
                  style=bold];
              "abjad.tools.pitchtools.Set.Set" [color=2,
                  group=10,
                  label=Set,
                  shape=oval,
                  style=bold];
              "abjad.tools.pitchtools.TwelveToneRow.TwelveToneRow" [color=2,
                  group=10,
                  label=TwelveToneRow,
                  shape=box];
              "abjad.tools.pitchtools.Vector.Vector" [color=2,
                  group=10,
                  label=Vector,
                  shape=oval,
                  style=bold];
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
              "abjad.tools.quantizationtools.QGridContainer.QGridContainer" [color=3,
                  group=11,
                  label=QGridContainer,
                  shape=box];
              "abjad.tools.quantizationtools.QGridLeaf.QGridLeaf" [color=3,
                  group=11,
                  label=QGridLeaf,
                  shape=box];
          }
          subgraph cluster_rhythmmakertools {
              graph [label=rhythmmakertools];
              "abjad.tools.rhythmmakertools.PartitionTable.PartitionTable" [color=4,
                  group=12,
                  label=PartitionTable,
                  shape=box];
              "abjad.tools.rhythmmakertools.RotationCounter.RotationCounter" [color=4,
                  group=12,
                  label=RotationCounter,
                  shape=box];
          }
          subgraph cluster_rhythmtreetools {
              graph [label=rhythmtreetools];
              "abjad.tools.rhythmtreetools.RhythmTreeContainer.RhythmTreeContainer" [color=5,
                  group=13,
                  label=RhythmTreeContainer,
                  shape=box];
              "abjad.tools.rhythmtreetools.RhythmTreeLeaf.RhythmTreeLeaf" [color=5,
                  group=13,
                  label=RhythmTreeLeaf,
                  shape=box];
          }
          subgraph cluster_scoretools {
              graph [label=scoretools];
              "abjad.tools.scoretools.NoteHeadInventory.NoteHeadInventory" [color=6,
                  group=14,
                  label=NoteHeadInventory,
                  shape=box];
          }
          subgraph cluster_selectiontools {
              graph [label=selectiontools];
              "abjad.tools.selectiontools.SelectionInventory.SelectionInventory" [color=7,
                  group=15,
                  label=SelectionInventory,
                  shape=box];
          }
          subgraph cluster_timespantools {
              graph [label=timespantools];
              "abjad.tools.timespantools.CompoundInequality.CompoundInequality" [color=8,
                  group=16,
                  label=CompoundInequality,
                  shape=box];
              "abjad.tools.timespantools.TimespanInventory.TimespanInventory" [color=8,
                  group=16,
                  label=TimespanInventory,
                  shape=box];
          }
          subgraph cluster_tonalanalysistools {
              graph [label=tonalanalysistools];
              "abjad.tools.tonalanalysistools.RootedChordClass.RootedChordClass" [color=9,
                  group=17,
                  label=RootedChordClass,
                  shape=box];
              "abjad.tools.tonalanalysistools.RootlessChordClass.RootlessChordClass" [color=9,
                  group=17,
                  label=RootlessChordClass,
                  shape=box];
              "abjad.tools.tonalanalysistools.Scale.Scale" [color=9,
                  group=17,
                  label=Scale,
                  shape=box];
          }
          subgraph cluster_builtins {
              graph [label=builtins];
              "builtins.int" [color=2,
                  group=1,
                  label=int,
                  shape=box];
              "builtins.object" [color=2,
                  group=1,
                  label=object,
                  shape=box];
              "builtins.tuple" [color=2,
                  group=1,
                  label=tuple,
                  shape=box];
              "builtins.object" -> "builtins.int";
              "builtins.object" -> "builtins.tuple";
          }
          subgraph cluster_enum {
              graph [label=enum];
              "enum.Enum" [color=5,
                  group=4,
                  label=Enum,
                  shape=box];
              "enum.IntEnum" [color=5,
                  group=4,
                  label=IntEnum,
                  shape=box];
              "enum.Enum" -> "enum.IntEnum";
          }
          "abjad.tools.abctools.AbjadObject.AbjadObject" -> "abjad.tools.datastructuretools.Cursor.Cursor";
          "abjad.tools.abctools.AbjadObject.AbjadObject" -> "abjad.tools.datastructuretools.CyclicTuple.CyclicTuple";
          "abjad.tools.abctools.AbjadObject.AbjadObject" -> "abjad.tools.datastructuretools.Matrix.Matrix";
          "abjad.tools.abctools.AbjadObject.AbjadObject" -> "abjad.tools.datastructuretools.OrdinalConstant.OrdinalConstant";
          "abjad.tools.abctools.AbjadObject.AbjadObject" -> "abjad.tools.datastructuretools.PayloadTree.PayloadTree";
          "abjad.tools.abctools.AbjadObject.AbjadObject" -> "abjad.tools.datastructuretools.TreeNode.TreeNode";
          "abjad.tools.abctools.AbjadObject.AbjadObject" -> "abjad.tools.datastructuretools.TypedCollection.TypedCollection";
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
          "abjad.tools.pitchtools.IntervalSegment.IntervalSegment" -> "abjad.tools.tonalanalysistools.RootlessChordClass.RootlessChordClass";
          "abjad.tools.pitchtools.PitchClassSegment.PitchClassSegment" -> "abjad.tools.tonalanalysistools.Scale.Scale";
          "abjad.tools.pitchtools.PitchClassSet.PitchClassSet" -> "abjad.tools.tonalanalysistools.RootedChordClass.RootedChordClass";
          "abjad.tools.rhythmtreetools.RhythmTreeContainer.RhythmTreeContainer" -> "abjad.tools.quantizationtools.QGridContainer.QGridContainer";
          "builtins.int" -> "enum.IntEnum";
          "builtins.object" -> "abjad.tools.abctools.AbjadObject.AbstractBase";
          "builtins.object" -> "abjad.tools.datastructuretools.SortedCollection.SortedCollection";
          "builtins.object" -> "enum.Enum";
          "builtins.tuple" -> "abjad.tools.datastructuretools.CyclicTuple.CyclicTuple";
          "enum.IntEnum" -> "abjad.tools.datastructuretools.Enumeration.Enumeration";
      }

--------

Abstract Classes
----------------

.. toctree::
   :hidden:

   TypedCollection

.. autosummary::
   :nosignatures:

   TypedCollection

--------

Classes
-------

.. toctree::
   :hidden:

   Cursor
   CyclicMatrix
   CyclicPayloadTree
   CyclicTuple
   Enumeration
   Matrix
   OrdinalConstant
   PayloadTree
   SortedCollection
   TreeContainer
   TreeNode
   TypedCounter
   TypedFrozenset
   TypedList
   TypedOrderedDict
   TypedTuple

.. autosummary::
   :nosignatures:

   Cursor
   CyclicMatrix
   CyclicPayloadTree
   CyclicTuple
   Enumeration
   Matrix
   OrdinalConstant
   PayloadTree
   SortedCollection
   TreeContainer
   TreeNode
   TypedCounter
   TypedFrozenset
   TypedList
   TypedOrderedDict
   TypedTuple
