tonalanalysistools
==================

.. automodule:: abjad.tools.tonalanalysistools

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
              "abjad.tools.datastructuretools.TypedCollection.TypedCollection" [color=3,
                  group=2,
                  label=TypedCollection,
                  shape=oval,
                  style=bold];
              "abjad.tools.datastructuretools.TypedFrozenset.TypedFrozenset" [color=3,
                  group=2,
                  label=TypedFrozenset,
                  shape=box];
              "abjad.tools.datastructuretools.TypedTuple.TypedTuple" [color=3,
                  group=2,
                  label=TypedTuple,
                  shape=box];
              "abjad.tools.datastructuretools.TypedCollection.TypedCollection" -> "abjad.tools.datastructuretools.TypedFrozenset.TypedFrozenset";
              "abjad.tools.datastructuretools.TypedCollection.TypedCollection" -> "abjad.tools.datastructuretools.TypedTuple.TypedTuple";
          }
          subgraph cluster_pitchtools {
              graph [label=pitchtools];
              "abjad.tools.pitchtools.IntervalSegment.IntervalSegment" [color=4,
                  group=3,
                  label=IntervalSegment,
                  shape=box];
              "abjad.tools.pitchtools.PitchClassSegment.PitchClassSegment" [color=4,
                  group=3,
                  label=PitchClassSegment,
                  shape=box];
              "abjad.tools.pitchtools.PitchClassSet.PitchClassSet" [color=4,
                  group=3,
                  label=PitchClassSet,
                  shape=box];
              "abjad.tools.pitchtools.Segment.Segment" [color=4,
                  group=3,
                  label=Segment,
                  shape=oval,
                  style=bold];
              "abjad.tools.pitchtools.Set.Set" [color=4,
                  group=3,
                  label=Set,
                  shape=oval,
                  style=bold];
              "abjad.tools.pitchtools.Segment.Segment" -> "abjad.tools.pitchtools.IntervalSegment.IntervalSegment";
              "abjad.tools.pitchtools.Segment.Segment" -> "abjad.tools.pitchtools.PitchClassSegment.PitchClassSegment";
              "abjad.tools.pitchtools.Set.Set" -> "abjad.tools.pitchtools.PitchClassSet.PitchClassSet";
          }
          subgraph cluster_tonalanalysistools {
              graph [label=tonalanalysistools];
              "abjad.tools.tonalanalysistools.ChordExtent.ChordExtent" [color=black,
                  fontcolor=white,
                  group=4,
                  label=ChordExtent,
                  shape=box,
                  style="filled, rounded"];
              "abjad.tools.tonalanalysistools.ChordInversion.ChordInversion" [color=black,
                  fontcolor=white,
                  group=4,
                  label=ChordInversion,
                  shape=box,
                  style="filled, rounded"];
              "abjad.tools.tonalanalysistools.ChordOmission.ChordOmission" [color=black,
                  fontcolor=white,
                  group=4,
                  label=ChordOmission,
                  shape=box,
                  style="filled, rounded"];
              "abjad.tools.tonalanalysistools.ChordQuality.ChordQuality" [color=black,
                  fontcolor=white,
                  group=4,
                  label=ChordQuality,
                  shape=box,
                  style="filled, rounded"];
              "abjad.tools.tonalanalysistools.ChordSuspension.ChordSuspension" [color=black,
                  fontcolor=white,
                  group=4,
                  label=ChordSuspension,
                  shape=box,
                  style="filled, rounded"];
              "abjad.tools.tonalanalysistools.Mode.Mode" [color=black,
                  fontcolor=white,
                  group=4,
                  label=Mode,
                  shape=box,
                  style="filled, rounded"];
              "abjad.tools.tonalanalysistools.RomanNumeral.RomanNumeral" [color=black,
                  fontcolor=white,
                  group=4,
                  label=RomanNumeral,
                  shape=box,
                  style="filled, rounded"];
              "abjad.tools.tonalanalysistools.RootedChordClass.RootedChordClass" [color=black,
                  fontcolor=white,
                  group=4,
                  label=RootedChordClass,
                  shape=box,
                  style="filled, rounded"];
              "abjad.tools.tonalanalysistools.RootlessChordClass.RootlessChordClass" [color=black,
                  fontcolor=white,
                  group=4,
                  label=RootlessChordClass,
                  shape=box,
                  style="filled, rounded"];
              "abjad.tools.tonalanalysistools.Scale.Scale" [color=black,
                  fontcolor=white,
                  group=4,
                  label=Scale,
                  shape=box,
                  style="filled, rounded"];
              "abjad.tools.tonalanalysistools.ScaleDegree.ScaleDegree" [color=black,
                  fontcolor=white,
                  group=4,
                  label=ScaleDegree,
                  shape=box,
                  style="filled, rounded"];
              "abjad.tools.tonalanalysistools.TonalAnalysisAgent.TonalAnalysisAgent" [color=black,
                  fontcolor=white,
                  group=4,
                  label=TonalAnalysisAgent,
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
          "abjad.tools.abctools.AbjadObject.AbjadObject" -> "abjad.tools.datastructuretools.TypedCollection.TypedCollection";
          "abjad.tools.abctools.AbjadObject.AbjadObject" -> "abjad.tools.tonalanalysistools.ChordExtent.ChordExtent";
          "abjad.tools.abctools.AbjadObject.AbjadObject" -> "abjad.tools.tonalanalysistools.ChordInversion.ChordInversion";
          "abjad.tools.abctools.AbjadObject.AbjadObject" -> "abjad.tools.tonalanalysistools.ChordOmission.ChordOmission";
          "abjad.tools.abctools.AbjadObject.AbjadObject" -> "abjad.tools.tonalanalysistools.ChordQuality.ChordQuality";
          "abjad.tools.abctools.AbjadObject.AbjadObject" -> "abjad.tools.tonalanalysistools.ChordSuspension.ChordSuspension";
          "abjad.tools.abctools.AbjadObject.AbjadObject" -> "abjad.tools.tonalanalysistools.Mode.Mode";
          "abjad.tools.abctools.AbjadObject.AbjadObject" -> "abjad.tools.tonalanalysistools.RomanNumeral.RomanNumeral";
          "abjad.tools.abctools.AbjadObject.AbjadObject" -> "abjad.tools.tonalanalysistools.ScaleDegree.ScaleDegree";
          "abjad.tools.abctools.AbjadObject.AbjadObject" -> "abjad.tools.tonalanalysistools.TonalAnalysisAgent.TonalAnalysisAgent";
          "abjad.tools.datastructuretools.TypedFrozenset.TypedFrozenset" -> "abjad.tools.pitchtools.Set.Set";
          "abjad.tools.datastructuretools.TypedTuple.TypedTuple" -> "abjad.tools.pitchtools.Segment.Segment";
          "abjad.tools.pitchtools.IntervalSegment.IntervalSegment" -> "abjad.tools.tonalanalysistools.RootlessChordClass.RootlessChordClass";
          "abjad.tools.pitchtools.PitchClassSegment.PitchClassSegment" -> "abjad.tools.tonalanalysistools.Scale.Scale";
          "abjad.tools.pitchtools.PitchClassSet.PitchClassSet" -> "abjad.tools.tonalanalysistools.RootedChordClass.RootedChordClass";
          "builtins.object" -> "abjad.tools.abctools.AbjadObject.AbstractBase";
      }

--------

Classes
-------

.. toctree::
   :hidden:

   ChordExtent
   ChordInversion
   ChordOmission
   ChordQuality
   ChordSuspension
   Mode
   RomanNumeral
   RootedChordClass
   RootlessChordClass
   Scale
   ScaleDegree
   TonalAnalysisAgent

.. autosummary::
   :nosignatures:

   ChordExtent
   ChordInversion
   ChordOmission
   ChordQuality
   ChordSuspension
   Mode
   RomanNumeral
   RootedChordClass
   RootlessChordClass
   Scale
   ScaleDegree
   TonalAnalysisAgent

--------

Functions
---------

.. toctree::
   :hidden:

   select

.. autosummary::
   :nosignatures:

   select
