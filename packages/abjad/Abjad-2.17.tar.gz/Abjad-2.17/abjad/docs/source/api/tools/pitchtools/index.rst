pitchtools
==========

.. automodule:: abjad.tools.pitchtools

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
              "abjad.tools.abctools.AbjadValueObject.AbjadValueObject" [color=1,
                  group=0,
                  label=AbjadValueObject,
                  shape=box];
              "abjad.tools.abctools.AbjadObject.AbjadObject" -> "abjad.tools.abctools.AbjadValueObject.AbjadValueObject";
              "abjad.tools.abctools.AbjadObject.AbstractBase" -> "abjad.tools.abctools.AbjadObject.AbjadObject";
          }
          subgraph cluster_datastructuretools {
              graph [label=datastructuretools];
              "abjad.tools.datastructuretools.PayloadTree.PayloadTree" [color=3,
                  group=2,
                  label=PayloadTree,
                  shape=box];
              "abjad.tools.datastructuretools.TypedCollection.TypedCollection" [color=3,
                  group=2,
                  label=TypedCollection,
                  shape=oval,
                  style=bold];
              "abjad.tools.datastructuretools.TypedCounter.TypedCounter" [color=3,
                  group=2,
                  label=TypedCounter,
                  shape=box];
              "abjad.tools.datastructuretools.TypedFrozenset.TypedFrozenset" [color=3,
                  group=2,
                  label=TypedFrozenset,
                  shape=box];
              "abjad.tools.datastructuretools.TypedList.TypedList" [color=3,
                  group=2,
                  label=TypedList,
                  shape=box];
              "abjad.tools.datastructuretools.TypedTuple.TypedTuple" [color=3,
                  group=2,
                  label=TypedTuple,
                  shape=box];
              "abjad.tools.datastructuretools.TypedCollection.TypedCollection" -> "abjad.tools.datastructuretools.TypedCounter.TypedCounter";
              "abjad.tools.datastructuretools.TypedCollection.TypedCollection" -> "abjad.tools.datastructuretools.TypedFrozenset.TypedFrozenset";
              "abjad.tools.datastructuretools.TypedCollection.TypedCollection" -> "abjad.tools.datastructuretools.TypedList.TypedList";
              "abjad.tools.datastructuretools.TypedCollection.TypedCollection" -> "abjad.tools.datastructuretools.TypedTuple.TypedTuple";
          }
          subgraph cluster_pitchtools {
              graph [label=pitchtools];
              "abjad.tools.pitchtools.Accidental.Accidental" [color=black,
                  fontcolor=white,
                  group=3,
                  label=Accidental,
                  shape=box,
                  style="filled, rounded"];
              "abjad.tools.pitchtools.Interval.Interval" [color=black,
                  fontcolor=white,
                  group=3,
                  label=Interval,
                  shape=oval,
                  style="filled, rounded"];
              "abjad.tools.pitchtools.IntervalClass.IntervalClass" [color=black,
                  fontcolor=white,
                  group=3,
                  label=IntervalClass,
                  shape=oval,
                  style="filled, rounded"];
              "abjad.tools.pitchtools.IntervalClassSegment.IntervalClassSegment" [color=black,
                  fontcolor=white,
                  group=3,
                  label=IntervalClassSegment,
                  shape=box,
                  style="filled, rounded"];
              "abjad.tools.pitchtools.IntervalClassSet.IntervalClassSet" [color=black,
                  fontcolor=white,
                  group=3,
                  label=IntervalClassSet,
                  shape=box,
                  style="filled, rounded"];
              "abjad.tools.pitchtools.IntervalClassVector.IntervalClassVector" [color=black,
                  fontcolor=white,
                  group=3,
                  label=IntervalClassVector,
                  shape=box,
                  style="filled, rounded"];
              "abjad.tools.pitchtools.IntervalSegment.IntervalSegment" [color=black,
                  fontcolor=white,
                  group=3,
                  label=IntervalSegment,
                  shape=box,
                  style="filled, rounded"];
              "abjad.tools.pitchtools.IntervalSet.IntervalSet" [color=black,
                  fontcolor=white,
                  group=3,
                  label=IntervalSet,
                  shape=box,
                  style="filled, rounded"];
              "abjad.tools.pitchtools.IntervalVector.IntervalVector" [color=black,
                  fontcolor=white,
                  group=3,
                  label=IntervalVector,
                  shape=box,
                  style="filled, rounded"];
              "abjad.tools.pitchtools.Inversion.Inversion" [color=black,
                  fontcolor=white,
                  group=3,
                  label=Inversion,
                  shape=box,
                  style="filled, rounded"];
              "abjad.tools.pitchtools.Multiplication.Multiplication" [color=black,
                  fontcolor=white,
                  group=3,
                  label=Multiplication,
                  shape=box,
                  style="filled, rounded"];
              "abjad.tools.pitchtools.NamedInterval.NamedInterval" [color=black,
                  fontcolor=white,
                  group=3,
                  label=NamedInterval,
                  shape=box,
                  style="filled, rounded"];
              "abjad.tools.pitchtools.NamedIntervalClass.NamedIntervalClass" [color=black,
                  fontcolor=white,
                  group=3,
                  label=NamedIntervalClass,
                  shape=box,
                  style="filled, rounded"];
              "abjad.tools.pitchtools.NamedInversionEquivalentIntervalClass.NamedInversionEquivalentIntervalClass" [color=black,
                  fontcolor=white,
                  group=3,
                  label=NamedInversionEquivalentIntervalClass,
                  shape=box,
                  style="filled, rounded"];
              "abjad.tools.pitchtools.NamedPitch.NamedPitch" [color=black,
                  fontcolor=white,
                  group=3,
                  label=NamedPitch,
                  shape=box,
                  style="filled, rounded"];
              "abjad.tools.pitchtools.NamedPitchClass.NamedPitchClass" [color=black,
                  fontcolor=white,
                  group=3,
                  label=NamedPitchClass,
                  shape=box,
                  style="filled, rounded"];
              "abjad.tools.pitchtools.NumberedInterval.NumberedInterval" [color=black,
                  fontcolor=white,
                  group=3,
                  label=NumberedInterval,
                  shape=box,
                  style="filled, rounded"];
              "abjad.tools.pitchtools.NumberedIntervalClass.NumberedIntervalClass" [color=black,
                  fontcolor=white,
                  group=3,
                  label=NumberedIntervalClass,
                  shape=box,
                  style="filled, rounded"];
              "abjad.tools.pitchtools.NumberedInversionEquivalentIntervalClass.NumberedInversionEquivalentIntervalClass" [color=black,
                  fontcolor=white,
                  group=3,
                  label=NumberedInversionEquivalentIntervalClass,
                  shape=box,
                  style="filled, rounded"];
              "abjad.tools.pitchtools.NumberedPitch.NumberedPitch" [color=black,
                  fontcolor=white,
                  group=3,
                  label=NumberedPitch,
                  shape=box,
                  style="filled, rounded"];
              "abjad.tools.pitchtools.NumberedPitchClass.NumberedPitchClass" [color=black,
                  fontcolor=white,
                  group=3,
                  label=NumberedPitchClass,
                  shape=box,
                  style="filled, rounded"];
              "abjad.tools.pitchtools.NumberedPitchClassColorMap.NumberedPitchClassColorMap" [color=black,
                  fontcolor=white,
                  group=3,
                  label=NumberedPitchClassColorMap,
                  shape=box,
                  style="filled, rounded"];
              "abjad.tools.pitchtools.Octave.Octave" [color=black,
                  fontcolor=white,
                  group=3,
                  label=Octave,
                  shape=box,
                  style="filled, rounded"];
              "abjad.tools.pitchtools.Pitch.Pitch" [color=black,
                  fontcolor=white,
                  group=3,
                  label=Pitch,
                  shape=oval,
                  style="filled, rounded"];
              "abjad.tools.pitchtools.PitchArray.PitchArray" [color=black,
                  fontcolor=white,
                  group=3,
                  label=PitchArray,
                  shape=box,
                  style="filled, rounded"];
              "abjad.tools.pitchtools.PitchArrayCell.PitchArrayCell" [color=black,
                  fontcolor=white,
                  group=3,
                  label=PitchArrayCell,
                  shape=box,
                  style="filled, rounded"];
              "abjad.tools.pitchtools.PitchArrayColumn.PitchArrayColumn" [color=black,
                  fontcolor=white,
                  group=3,
                  label=PitchArrayColumn,
                  shape=box,
                  style="filled, rounded"];
              "abjad.tools.pitchtools.PitchArrayInventory.PitchArrayInventory" [color=black,
                  fontcolor=white,
                  group=3,
                  label=PitchArrayInventory,
                  shape=box,
                  style="filled, rounded"];
              "abjad.tools.pitchtools.PitchArrayRow.PitchArrayRow" [color=black,
                  fontcolor=white,
                  group=3,
                  label=PitchArrayRow,
                  shape=box,
                  style="filled, rounded"];
              "abjad.tools.pitchtools.PitchClass.PitchClass" [color=black,
                  fontcolor=white,
                  group=3,
                  label=PitchClass,
                  shape=oval,
                  style="filled, rounded"];
              "abjad.tools.pitchtools.PitchClassSegment.PitchClassSegment" [color=black,
                  fontcolor=white,
                  group=3,
                  label=PitchClassSegment,
                  shape=box,
                  style="filled, rounded"];
              "abjad.tools.pitchtools.PitchClassSet.PitchClassSet" [color=black,
                  fontcolor=white,
                  group=3,
                  label=PitchClassSet,
                  shape=box,
                  style="filled, rounded"];
              "abjad.tools.pitchtools.PitchClassTree.PitchClassTree" [color=black,
                  fontcolor=white,
                  group=3,
                  label=PitchClassTree,
                  shape=box,
                  style="filled, rounded"];
              "abjad.tools.pitchtools.PitchClassVector.PitchClassVector" [color=black,
                  fontcolor=white,
                  group=3,
                  label=PitchClassVector,
                  shape=box,
                  style="filled, rounded"];
              "abjad.tools.pitchtools.PitchOperation.PitchOperation" [color=black,
                  fontcolor=white,
                  group=3,
                  label=PitchOperation,
                  shape=box,
                  style="filled, rounded"];
              "abjad.tools.pitchtools.PitchRange.PitchRange" [color=black,
                  fontcolor=white,
                  group=3,
                  label=PitchRange,
                  shape=box,
                  style="filled, rounded"];
              "abjad.tools.pitchtools.PitchRangeInventory.PitchRangeInventory" [color=black,
                  fontcolor=white,
                  group=3,
                  label=PitchRangeInventory,
                  shape=box,
                  style="filled, rounded"];
              "abjad.tools.pitchtools.PitchSegment.PitchSegment" [color=black,
                  fontcolor=white,
                  group=3,
                  label=PitchSegment,
                  shape=box,
                  style="filled, rounded"];
              "abjad.tools.pitchtools.PitchSet.PitchSet" [color=black,
                  fontcolor=white,
                  group=3,
                  label=PitchSet,
                  shape=box,
                  style="filled, rounded"];
              "abjad.tools.pitchtools.PitchVector.PitchVector" [color=black,
                  fontcolor=white,
                  group=3,
                  label=PitchVector,
                  shape=box,
                  style="filled, rounded"];
              "abjad.tools.pitchtools.Registration.Registration" [color=black,
                  fontcolor=white,
                  group=3,
                  label=Registration,
                  shape=box,
                  style="filled, rounded"];
              "abjad.tools.pitchtools.RegistrationComponent.RegistrationComponent" [color=black,
                  fontcolor=white,
                  group=3,
                  label=RegistrationComponent,
                  shape=box,
                  style="filled, rounded"];
              "abjad.tools.pitchtools.RegistrationInventory.RegistrationInventory" [color=black,
                  fontcolor=white,
                  group=3,
                  label=RegistrationInventory,
                  shape=box,
                  style="filled, rounded"];
              "abjad.tools.pitchtools.Retrogression.Retrogression" [color=black,
                  fontcolor=white,
                  group=3,
                  label=Retrogression,
                  shape=box,
                  style="filled, rounded"];
              "abjad.tools.pitchtools.Rotation.Rotation" [color=black,
                  fontcolor=white,
                  group=3,
                  label=Rotation,
                  shape=box,
                  style="filled, rounded"];
              "abjad.tools.pitchtools.Segment.Segment" [color=black,
                  fontcolor=white,
                  group=3,
                  label=Segment,
                  shape=oval,
                  style="filled, rounded"];
              "abjad.tools.pitchtools.Set.Set" [color=black,
                  fontcolor=white,
                  group=3,
                  label=Set,
                  shape=oval,
                  style="filled, rounded"];
              "abjad.tools.pitchtools.StaffPosition.StaffPosition" [color=black,
                  fontcolor=white,
                  group=3,
                  label=StaffPosition,
                  shape=box,
                  style="filled, rounded"];
              "abjad.tools.pitchtools.Transposition.Transposition" [color=black,
                  fontcolor=white,
                  group=3,
                  label=Transposition,
                  shape=box,
                  style="filled, rounded"];
              "abjad.tools.pitchtools.TwelveToneRow.TwelveToneRow" [color=black,
                  fontcolor=white,
                  group=3,
                  label=TwelveToneRow,
                  shape=box,
                  style="filled, rounded"];
              "abjad.tools.pitchtools.Vector.Vector" [color=black,
                  fontcolor=white,
                  group=3,
                  label=Vector,
                  shape=oval,
                  style="filled, rounded"];
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
          subgraph cluster_tonalanalysistools {
              graph [label=tonalanalysistools];
              "abjad.tools.tonalanalysistools.RootedChordClass.RootedChordClass" [color=5,
                  group=4,
                  label=RootedChordClass,
                  shape=box];
              "abjad.tools.tonalanalysistools.RootlessChordClass.RootlessChordClass" [color=5,
                  group=4,
                  label=RootlessChordClass,
                  shape=box];
              "abjad.tools.tonalanalysistools.Scale.Scale" [color=5,
                  group=4,
                  label=Scale,
                  shape=box];
          }
          subgraph cluster_builtins {
              graph [label=builtins];
              "builtins.object" [color=2,
                  group=1,
                  label=object,
                  shape=box];
          }
          "abjad.tools.abctools.AbjadObject.AbjadObject" -> "abjad.tools.datastructuretools.PayloadTree.PayloadTree";
          "abjad.tools.abctools.AbjadObject.AbjadObject" -> "abjad.tools.datastructuretools.TypedCollection.TypedCollection";
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
          "abjad.tools.abctools.AbjadValueObject.AbjadValueObject" -> "abjad.tools.pitchtools.Inversion.Inversion";
          "abjad.tools.abctools.AbjadValueObject.AbjadValueObject" -> "abjad.tools.pitchtools.Multiplication.Multiplication";
          "abjad.tools.abctools.AbjadValueObject.AbjadValueObject" -> "abjad.tools.pitchtools.PitchOperation.PitchOperation";
          "abjad.tools.abctools.AbjadValueObject.AbjadValueObject" -> "abjad.tools.pitchtools.Retrogression.Retrogression";
          "abjad.tools.abctools.AbjadValueObject.AbjadValueObject" -> "abjad.tools.pitchtools.Rotation.Rotation";
          "abjad.tools.abctools.AbjadValueObject.AbjadValueObject" -> "abjad.tools.pitchtools.Transposition.Transposition";
          "abjad.tools.datastructuretools.PayloadTree.PayloadTree" -> "abjad.tools.pitchtools.PitchClassTree.PitchClassTree";
          "abjad.tools.datastructuretools.TypedCounter.TypedCounter" -> "abjad.tools.pitchtools.Vector.Vector";
          "abjad.tools.datastructuretools.TypedFrozenset.TypedFrozenset" -> "abjad.tools.pitchtools.Set.Set";
          "abjad.tools.datastructuretools.TypedList.TypedList" -> "abjad.tools.pitchtools.PitchArrayInventory.PitchArrayInventory";
          "abjad.tools.datastructuretools.TypedList.TypedList" -> "abjad.tools.pitchtools.PitchRangeInventory.PitchRangeInventory";
          "abjad.tools.datastructuretools.TypedList.TypedList" -> "abjad.tools.pitchtools.Registration.Registration";
          "abjad.tools.datastructuretools.TypedList.TypedList" -> "abjad.tools.pitchtools.RegistrationInventory.RegistrationInventory";
          "abjad.tools.datastructuretools.TypedTuple.TypedTuple" -> "abjad.tools.pitchtools.Segment.Segment";
          "abjad.tools.pitchtools.IntervalSegment.IntervalSegment" -> "abjad.tools.tonalanalysistools.RootlessChordClass.RootlessChordClass";
          "abjad.tools.pitchtools.PitchClassSegment.PitchClassSegment" -> "abjad.tools.tonalanalysistools.Scale.Scale";
          "abjad.tools.pitchtools.PitchClassSet.PitchClassSet" -> "abjad.tools.tonalanalysistools.RootedChordClass.RootedChordClass";
          "builtins.object" -> "abjad.tools.abctools.AbjadObject.AbstractBase";
      }

--------

Abstract Classes
----------------

.. toctree::
   :hidden:

   Interval
   IntervalClass
   Pitch
   PitchClass
   Segment
   Set
   Vector

.. autosummary::
   :nosignatures:

   Interval
   IntervalClass
   Pitch
   PitchClass
   Segment
   Set
   Vector

--------

Classes
-------

.. toctree::
   :hidden:

   Accidental
   IntervalClassSegment
   IntervalClassSet
   IntervalClassVector
   IntervalSegment
   IntervalSet
   IntervalVector
   Inversion
   Multiplication
   NamedInterval
   NamedIntervalClass
   NamedInversionEquivalentIntervalClass
   NamedPitch
   NamedPitchClass
   NumberedInterval
   NumberedIntervalClass
   NumberedInversionEquivalentIntervalClass
   NumberedPitch
   NumberedPitchClass
   NumberedPitchClassColorMap
   Octave
   PitchArray
   PitchArrayCell
   PitchArrayColumn
   PitchArrayInventory
   PitchArrayRow
   PitchClassSegment
   PitchClassSet
   PitchClassTree
   PitchClassVector
   PitchOperation
   PitchRange
   PitchRangeInventory
   PitchSegment
   PitchSet
   PitchVector
   Registration
   RegistrationComponent
   RegistrationInventory
   Retrogression
   Rotation
   StaffPosition
   Transposition
   TwelveToneRow

.. autosummary::
   :nosignatures:

   Accidental
   IntervalClassSegment
   IntervalClassSet
   IntervalClassVector
   IntervalSegment
   IntervalSet
   IntervalVector
   Inversion
   Multiplication
   NamedInterval
   NamedIntervalClass
   NamedInversionEquivalentIntervalClass
   NamedPitch
   NamedPitchClass
   NumberedInterval
   NumberedIntervalClass
   NumberedInversionEquivalentIntervalClass
   NumberedPitch
   NumberedPitchClass
   NumberedPitchClassColorMap
   Octave
   PitchArray
   PitchArrayCell
   PitchArrayColumn
   PitchArrayInventory
   PitchArrayRow
   PitchClassSegment
   PitchClassSet
   PitchClassTree
   PitchClassVector
   PitchOperation
   PitchRange
   PitchRangeInventory
   PitchSegment
   PitchSet
   PitchVector
   Registration
   RegistrationComponent
   RegistrationInventory
   Retrogression
   Rotation
   StaffPosition
   Transposition
   TwelveToneRow

--------

Functions
---------

.. toctree::
   :hidden:

   instantiate_pitch_and_interval_test_collection
   inventory_named_inversion_equivalent_interval_classes
   iterate_named_pitch_pairs_in_expr
   list_named_pitches_in_expr
   list_numbered_interval_numbers_pairwise
   list_numbered_inversion_equivalent_interval_classes_pairwise
   list_ordered_named_pitch_pairs_from_expr_1_to_expr_2
   list_pitch_numbers_in_expr
   list_unordered_named_pitch_pairs_in_expr
   set_written_pitch_of_pitched_components_in_expr
   sort_named_pitch_carriers_in_expr
   transpose_named_pitch_by_numbered_interval_and_respell
   transpose_pitch_carrier_by_interval
   transpose_pitch_class_number_to_pitch_number_neighbor
   transpose_pitch_expr_into_pitch_range
   transpose_pitch_number_by_octave_transposition_mapping
   yield_all_pitch_class_sets

.. autosummary::
   :nosignatures:

   instantiate_pitch_and_interval_test_collection
   inventory_named_inversion_equivalent_interval_classes
   iterate_named_pitch_pairs_in_expr
   list_named_pitches_in_expr
   list_numbered_interval_numbers_pairwise
   list_numbered_inversion_equivalent_interval_classes_pairwise
   list_ordered_named_pitch_pairs_from_expr_1_to_expr_2
   list_pitch_numbers_in_expr
   list_unordered_named_pitch_pairs_in_expr
   set_written_pitch_of_pitched_components_in_expr
   sort_named_pitch_carriers_in_expr
   transpose_named_pitch_by_numbered_interval_and_respell
   transpose_pitch_carrier_by_interval
   transpose_pitch_class_number_to_pitch_number_neighbor
   transpose_pitch_expr_into_pitch_range
   transpose_pitch_number_by_octave_transposition_mapping
   yield_all_pitch_class_sets
