quantizationtools
=================

.. automodule:: abjad.tools.quantizationtools

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
          subgraph cluster_quantizationtools {
              graph [label=quantizationtools];
              "abjad.tools.quantizationtools.AttackPointOptimizer.AttackPointOptimizer" [color=black,
                  fontcolor=white,
                  group=4,
                  label=AttackPointOptimizer,
                  shape=oval,
                  style="filled, rounded"];
              "abjad.tools.quantizationtools.BeatwiseQSchema.BeatwiseQSchema" [color=black,
                  fontcolor=white,
                  group=4,
                  label=BeatwiseQSchema,
                  shape=box,
                  style="filled, rounded"];
              "abjad.tools.quantizationtools.BeatwiseQSchemaItem.BeatwiseQSchemaItem" [color=black,
                  fontcolor=white,
                  group=4,
                  label=BeatwiseQSchemaItem,
                  shape=box,
                  style="filled, rounded"];
              "abjad.tools.quantizationtools.BeatwiseQTarget.BeatwiseQTarget" [color=black,
                  fontcolor=white,
                  group=4,
                  label=BeatwiseQTarget,
                  shape=box,
                  style="filled, rounded"];
              "abjad.tools.quantizationtools.CollapsingGraceHandler.CollapsingGraceHandler" [color=black,
                  fontcolor=white,
                  group=4,
                  label=CollapsingGraceHandler,
                  shape=box,
                  style="filled, rounded"];
              "abjad.tools.quantizationtools.ConcatenatingGraceHandler.ConcatenatingGraceHandler" [color=black,
                  fontcolor=white,
                  group=4,
                  label=ConcatenatingGraceHandler,
                  shape=box,
                  style="filled, rounded"];
              "abjad.tools.quantizationtools.DiscardingGraceHandler.DiscardingGraceHandler" [color=black,
                  fontcolor=white,
                  group=4,
                  label=DiscardingGraceHandler,
                  shape=box,
                  style="filled, rounded"];
              "abjad.tools.quantizationtools.DistanceHeuristic.DistanceHeuristic" [color=black,
                  fontcolor=white,
                  group=4,
                  label=DistanceHeuristic,
                  shape=box,
                  style="filled, rounded"];
              "abjad.tools.quantizationtools.GraceHandler.GraceHandler" [color=black,
                  fontcolor=white,
                  group=4,
                  label=GraceHandler,
                  shape=oval,
                  style="filled, rounded"];
              "abjad.tools.quantizationtools.Heuristic.Heuristic" [color=black,
                  fontcolor=white,
                  group=4,
                  label=Heuristic,
                  shape=oval,
                  style="filled, rounded"];
              "abjad.tools.quantizationtools.JobHandler.JobHandler" [color=black,
                  fontcolor=white,
                  group=4,
                  label=JobHandler,
                  shape=oval,
                  style="filled, rounded"];
              "abjad.tools.quantizationtools.MeasurewiseAttackPointOptimizer.MeasurewiseAttackPointOptimizer" [color=black,
                  fontcolor=white,
                  group=4,
                  label=MeasurewiseAttackPointOptimizer,
                  shape=box,
                  style="filled, rounded"];
              "abjad.tools.quantizationtools.MeasurewiseQSchema.MeasurewiseQSchema" [color=black,
                  fontcolor=white,
                  group=4,
                  label=MeasurewiseQSchema,
                  shape=box,
                  style="filled, rounded"];
              "abjad.tools.quantizationtools.MeasurewiseQSchemaItem.MeasurewiseQSchemaItem" [color=black,
                  fontcolor=white,
                  group=4,
                  label=MeasurewiseQSchemaItem,
                  shape=box,
                  style="filled, rounded"];
              "abjad.tools.quantizationtools.MeasurewiseQTarget.MeasurewiseQTarget" [color=black,
                  fontcolor=white,
                  group=4,
                  label=MeasurewiseQTarget,
                  shape=box,
                  style="filled, rounded"];
              "abjad.tools.quantizationtools.NaiveAttackPointOptimizer.NaiveAttackPointOptimizer" [color=black,
                  fontcolor=white,
                  group=4,
                  label=NaiveAttackPointOptimizer,
                  shape=box,
                  style="filled, rounded"];
              "abjad.tools.quantizationtools.NullAttackPointOptimizer.NullAttackPointOptimizer" [color=black,
                  fontcolor=white,
                  group=4,
                  label=NullAttackPointOptimizer,
                  shape=box,
                  style="filled, rounded"];
              "abjad.tools.quantizationtools.ParallelJobHandler.ParallelJobHandler" [color=black,
                  fontcolor=white,
                  group=4,
                  label=ParallelJobHandler,
                  shape=box,
                  style="filled, rounded"];
              "abjad.tools.quantizationtools.ParallelJobHandlerWorker.ParallelJobHandlerWorker" [color=black,
                  fontcolor=white,
                  group=4,
                  label=ParallelJobHandlerWorker,
                  shape=box,
                  style="filled, rounded"];
              "abjad.tools.quantizationtools.PitchedQEvent.PitchedQEvent" [color=black,
                  fontcolor=white,
                  group=4,
                  label=PitchedQEvent,
                  shape=box,
                  style="filled, rounded"];
              "abjad.tools.quantizationtools.QEvent.QEvent" [color=black,
                  fontcolor=white,
                  group=4,
                  label=QEvent,
                  shape=oval,
                  style="filled, rounded"];
              "abjad.tools.quantizationtools.QEventProxy.QEventProxy" [color=black,
                  fontcolor=white,
                  group=4,
                  label=QEventProxy,
                  shape=box,
                  style="filled, rounded"];
              "abjad.tools.quantizationtools.QEventSequence.QEventSequence" [color=black,
                  fontcolor=white,
                  group=4,
                  label=QEventSequence,
                  shape=box,
                  style="filled, rounded"];
              "abjad.tools.quantizationtools.QGrid.QGrid" [color=black,
                  fontcolor=white,
                  group=4,
                  label=QGrid,
                  shape=box,
                  style="filled, rounded"];
              "abjad.tools.quantizationtools.QGridContainer.QGridContainer" [color=black,
                  fontcolor=white,
                  group=4,
                  label=QGridContainer,
                  shape=box,
                  style="filled, rounded"];
              "abjad.tools.quantizationtools.QGridLeaf.QGridLeaf" [color=black,
                  fontcolor=white,
                  group=4,
                  label=QGridLeaf,
                  shape=box,
                  style="filled, rounded"];
              "abjad.tools.quantizationtools.QSchema.QSchema" [color=black,
                  fontcolor=white,
                  group=4,
                  label=QSchema,
                  shape=oval,
                  style="filled, rounded"];
              "abjad.tools.quantizationtools.QSchemaItem.QSchemaItem" [color=black,
                  fontcolor=white,
                  group=4,
                  label=QSchemaItem,
                  shape=oval,
                  style="filled, rounded"];
              "abjad.tools.quantizationtools.QTarget.QTarget" [color=black,
                  fontcolor=white,
                  group=4,
                  label=QTarget,
                  shape=oval,
                  style="filled, rounded"];
              "abjad.tools.quantizationtools.QTargetBeat.QTargetBeat" [color=black,
                  fontcolor=white,
                  group=4,
                  label=QTargetBeat,
                  shape=box,
                  style="filled, rounded"];
              "abjad.tools.quantizationtools.QTargetMeasure.QTargetMeasure" [color=black,
                  fontcolor=white,
                  group=4,
                  label=QTargetMeasure,
                  shape=box,
                  style="filled, rounded"];
              "abjad.tools.quantizationtools.QuantizationJob.QuantizationJob" [color=black,
                  fontcolor=white,
                  group=4,
                  label=QuantizationJob,
                  shape=box,
                  style="filled, rounded"];
              "abjad.tools.quantizationtools.Quantizer.Quantizer" [color=black,
                  fontcolor=white,
                  group=4,
                  label=Quantizer,
                  shape=box,
                  style="filled, rounded"];
              "abjad.tools.quantizationtools.SearchTree.SearchTree" [color=black,
                  fontcolor=white,
                  group=4,
                  label=SearchTree,
                  shape=oval,
                  style="filled, rounded"];
              "abjad.tools.quantizationtools.SerialJobHandler.SerialJobHandler" [color=black,
                  fontcolor=white,
                  group=4,
                  label=SerialJobHandler,
                  shape=box,
                  style="filled, rounded"];
              "abjad.tools.quantizationtools.SilentQEvent.SilentQEvent" [color=black,
                  fontcolor=white,
                  group=4,
                  label=SilentQEvent,
                  shape=box,
                  style="filled, rounded"];
              "abjad.tools.quantizationtools.TerminalQEvent.TerminalQEvent" [color=black,
                  fontcolor=white,
                  group=4,
                  label=TerminalQEvent,
                  shape=box,
                  style="filled, rounded"];
              "abjad.tools.quantizationtools.UnweightedSearchTree.UnweightedSearchTree" [color=black,
                  fontcolor=white,
                  group=4,
                  label=UnweightedSearchTree,
                  shape=box,
                  style="filled, rounded"];
              "abjad.tools.quantizationtools.WeightedSearchTree.WeightedSearchTree" [color=black,
                  fontcolor=white,
                  group=4,
                  label=WeightedSearchTree,
                  shape=box,
                  style="filled, rounded"];
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
          subgraph cluster_rhythmtreetools {
              graph [label=rhythmtreetools];
              "abjad.tools.rhythmtreetools.RhythmTreeContainer.RhythmTreeContainer" [color=6,
                  group=5,
                  label=RhythmTreeContainer,
                  shape=box];
              "abjad.tools.rhythmtreetools.RhythmTreeMixin.RhythmTreeMixin" [color=6,
                  group=5,
                  label=RhythmTreeMixin,
                  shape=oval,
                  style=bold];
              "abjad.tools.rhythmtreetools.RhythmTreeMixin.RhythmTreeMixin" -> "abjad.tools.rhythmtreetools.RhythmTreeContainer.RhythmTreeContainer";
          }
          subgraph cluster_builtins {
              graph [label=builtins];
              "builtins.object" [color=2,
                  group=1,
                  label=object,
                  shape=box];
          }
          subgraph cluster_multiprocessing {
              graph [label=multiprocessing];
              "multiprocessing.context.Process" [color=4,
                  group=3,
                  label=Process,
                  shape=box];
              "multiprocessing.process.BaseProcess" [color=4,
                  group=3,
                  label=BaseProcess,
                  shape=box];
              "multiprocessing.process.BaseProcess" -> "multiprocessing.context.Process";
          }
          "abjad.tools.abctools.AbjadObject.AbjadObject" -> "abjad.tools.datastructuretools.TreeNode.TreeNode";
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
          "abjad.tools.datastructuretools.TreeContainer.TreeContainer" -> "abjad.tools.rhythmtreetools.RhythmTreeContainer.RhythmTreeContainer";
          "abjad.tools.datastructuretools.TreeNode.TreeNode" -> "abjad.tools.quantizationtools.QGridLeaf.QGridLeaf";
          "abjad.tools.rhythmtreetools.RhythmTreeContainer.RhythmTreeContainer" -> "abjad.tools.quantizationtools.QGridContainer.QGridContainer";
          "abjad.tools.rhythmtreetools.RhythmTreeMixin.RhythmTreeMixin" -> "abjad.tools.quantizationtools.QGridLeaf.QGridLeaf";
          "builtins.object" -> "abjad.tools.abctools.AbjadObject.AbstractBase";
          "builtins.object" -> "multiprocessing.process.BaseProcess";
          "multiprocessing.context.Process" -> "abjad.tools.quantizationtools.ParallelJobHandlerWorker.ParallelJobHandlerWorker";
      }

--------

Abstract Classes
----------------

.. toctree::
   :hidden:

   AttackPointOptimizer
   GraceHandler
   Heuristic
   JobHandler
   QEvent
   QSchema
   QSchemaItem
   QTarget
   SearchTree

.. autosummary::
   :nosignatures:

   AttackPointOptimizer
   GraceHandler
   Heuristic
   JobHandler
   QEvent
   QSchema
   QSchemaItem
   QTarget
   SearchTree

--------

Classes
-------

.. toctree::
   :hidden:

   BeatwiseQSchema
   BeatwiseQSchemaItem
   BeatwiseQTarget
   CollapsingGraceHandler
   ConcatenatingGraceHandler
   DiscardingGraceHandler
   DistanceHeuristic
   MeasurewiseAttackPointOptimizer
   MeasurewiseQSchema
   MeasurewiseQSchemaItem
   MeasurewiseQTarget
   NaiveAttackPointOptimizer
   NullAttackPointOptimizer
   ParallelJobHandler
   ParallelJobHandlerWorker
   PitchedQEvent
   QEventProxy
   QEventSequence
   QGrid
   QGridContainer
   QGridLeaf
   QTargetBeat
   QTargetMeasure
   QuantizationJob
   Quantizer
   SerialJobHandler
   SilentQEvent
   TerminalQEvent
   UnweightedSearchTree
   WeightedSearchTree

.. autosummary::
   :nosignatures:

   BeatwiseQSchema
   BeatwiseQSchemaItem
   BeatwiseQTarget
   CollapsingGraceHandler
   ConcatenatingGraceHandler
   DiscardingGraceHandler
   DistanceHeuristic
   MeasurewiseAttackPointOptimizer
   MeasurewiseQSchema
   MeasurewiseQSchemaItem
   MeasurewiseQTarget
   NaiveAttackPointOptimizer
   NullAttackPointOptimizer
   ParallelJobHandler
   ParallelJobHandlerWorker
   PitchedQEvent
   QEventProxy
   QEventSequence
   QGrid
   QGridContainer
   QGridLeaf
   QTargetBeat
   QTargetMeasure
   QuantizationJob
   Quantizer
   SerialJobHandler
   SilentQEvent
   TerminalQEvent
   UnweightedSearchTree
   WeightedSearchTree

--------

Functions
---------

.. toctree::
   :hidden:

   make_test_time_segments

.. autosummary::
   :nosignatures:

   make_test_time_segments
