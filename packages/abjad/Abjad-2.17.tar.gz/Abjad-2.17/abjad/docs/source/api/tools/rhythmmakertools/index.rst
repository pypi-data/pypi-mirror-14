rhythmmakertools
================

.. automodule:: abjad.tools.rhythmmakertools

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
              "abjad.tools.datastructuretools.TypedCollection.TypedCollection" [color=3,
                  group=2,
                  label=TypedCollection,
                  shape=oval,
                  style=bold];
              "abjad.tools.datastructuretools.TypedCounter.TypedCounter" [color=3,
                  group=2,
                  label=TypedCounter,
                  shape=box];
              "abjad.tools.datastructuretools.TypedOrderedDict.TypedOrderedDict" [color=3,
                  group=2,
                  label=TypedOrderedDict,
                  shape=box];
              "abjad.tools.datastructuretools.TypedCollection.TypedCollection" -> "abjad.tools.datastructuretools.TypedCounter.TypedCounter";
              "abjad.tools.datastructuretools.TypedCollection.TypedCollection" -> "abjad.tools.datastructuretools.TypedOrderedDict.TypedOrderedDict";
          }
          subgraph cluster_rhythmmakertools {
              graph [label=rhythmmakertools];
              "abjad.tools.rhythmmakertools.AccelerandoRhythmMaker.AccelerandoRhythmMaker" [color=black,
                  fontcolor=white,
                  group=3,
                  label=AccelerandoRhythmMaker,
                  shape=box,
                  style="filled, rounded"];
              "abjad.tools.rhythmmakertools.BeamSpecifier.BeamSpecifier" [color=black,
                  fontcolor=white,
                  group=3,
                  label=BeamSpecifier,
                  shape=box,
                  style="filled, rounded"];
              "abjad.tools.rhythmmakertools.BurnishSpecifier.BurnishSpecifier" [color=black,
                  fontcolor=white,
                  group=3,
                  label=BurnishSpecifier,
                  shape=box,
                  style="filled, rounded"];
              "abjad.tools.rhythmmakertools.DurationSpellingSpecifier.DurationSpellingSpecifier" [color=black,
                  fontcolor=white,
                  group=3,
                  label=DurationSpellingSpecifier,
                  shape=box,
                  style="filled, rounded"];
              "abjad.tools.rhythmmakertools.EvenDivisionRhythmMaker.EvenDivisionRhythmMaker" [color=black,
                  fontcolor=white,
                  group=3,
                  label=EvenDivisionRhythmMaker,
                  shape=box,
                  style="filled, rounded"];
              "abjad.tools.rhythmmakertools.EvenRunRhythmMaker.EvenRunRhythmMaker" [color=black,
                  fontcolor=white,
                  group=3,
                  label=EvenRunRhythmMaker,
                  shape=box,
                  style="filled, rounded"];
              "abjad.tools.rhythmmakertools.ExampleWrapper.ExampleWrapper" [color=black,
                  fontcolor=white,
                  group=3,
                  label=ExampleWrapper,
                  shape=box,
                  style="filled, rounded"];
              "abjad.tools.rhythmmakertools.GalleryMaker.GalleryMaker" [color=black,
                  fontcolor=white,
                  group=3,
                  label=GalleryMaker,
                  shape=box,
                  style="filled, rounded"];
              "abjad.tools.rhythmmakertools.InciseSpecifier.InciseSpecifier" [color=black,
                  fontcolor=white,
                  group=3,
                  label=InciseSpecifier,
                  shape=box,
                  style="filled, rounded"];
              "abjad.tools.rhythmmakertools.IncisedRhythmMaker.IncisedRhythmMaker" [color=black,
                  fontcolor=white,
                  group=3,
                  label=IncisedRhythmMaker,
                  shape=box,
                  style="filled, rounded"];
              "abjad.tools.rhythmmakertools.InterpolationSpecifier.InterpolationSpecifier" [color=black,
                  fontcolor=white,
                  group=3,
                  label=InterpolationSpecifier,
                  shape=box,
                  style="filled, rounded"];
              "abjad.tools.rhythmmakertools.NoteRhythmMaker.NoteRhythmMaker" [color=black,
                  fontcolor=white,
                  group=3,
                  label=NoteRhythmMaker,
                  shape=box,
                  style="filled, rounded"];
              "abjad.tools.rhythmmakertools.PartitionTable.PartitionTable" [color=black,
                  fontcolor=white,
                  group=3,
                  label=PartitionTable,
                  shape=box,
                  style="filled, rounded"];
              "abjad.tools.rhythmmakertools.RhythmMaker.RhythmMaker" [color=black,
                  fontcolor=white,
                  group=3,
                  label=RhythmMaker,
                  shape=box,
                  style="filled, rounded"];
              "abjad.tools.rhythmmakertools.RotationCounter.RotationCounter" [color=black,
                  fontcolor=white,
                  group=3,
                  label=RotationCounter,
                  shape=box,
                  style="filled, rounded"];
              "abjad.tools.rhythmmakertools.SilenceMask.SilenceMask" [color=black,
                  fontcolor=white,
                  group=3,
                  label=SilenceMask,
                  shape=box,
                  style="filled, rounded"];
              "abjad.tools.rhythmmakertools.SkipRhythmMaker.SkipRhythmMaker" [color=black,
                  fontcolor=white,
                  group=3,
                  label=SkipRhythmMaker,
                  shape=box,
                  style="filled, rounded"];
              "abjad.tools.rhythmmakertools.SustainMask.SustainMask" [color=black,
                  fontcolor=white,
                  group=3,
                  label=SustainMask,
                  shape=box,
                  style="filled, rounded"];
              "abjad.tools.rhythmmakertools.Talea.Talea" [color=black,
                  fontcolor=white,
                  group=3,
                  label=Talea,
                  shape=box,
                  style="filled, rounded"];
              "abjad.tools.rhythmmakertools.TaleaRhythmMaker.TaleaRhythmMaker" [color=black,
                  fontcolor=white,
                  group=3,
                  label=TaleaRhythmMaker,
                  shape=box,
                  style="filled, rounded"];
              "abjad.tools.rhythmmakertools.TieSpecifier.TieSpecifier" [color=black,
                  fontcolor=white,
                  group=3,
                  label=TieSpecifier,
                  shape=box,
                  style="filled, rounded"];
              "abjad.tools.rhythmmakertools.TupletRhythmMaker.TupletRhythmMaker" [color=black,
                  fontcolor=white,
                  group=3,
                  label=TupletRhythmMaker,
                  shape=box,
                  style="filled, rounded"];
              "abjad.tools.rhythmmakertools.TupletSpellingSpecifier.TupletSpellingSpecifier" [color=black,
                  fontcolor=white,
                  group=3,
                  label=TupletSpellingSpecifier,
                  shape=box,
                  style="filled, rounded"];
              "abjad.tools.rhythmmakertools.RhythmMaker.RhythmMaker" -> "abjad.tools.rhythmmakertools.AccelerandoRhythmMaker.AccelerandoRhythmMaker";
              "abjad.tools.rhythmmakertools.RhythmMaker.RhythmMaker" -> "abjad.tools.rhythmmakertools.EvenDivisionRhythmMaker.EvenDivisionRhythmMaker";
              "abjad.tools.rhythmmakertools.RhythmMaker.RhythmMaker" -> "abjad.tools.rhythmmakertools.EvenRunRhythmMaker.EvenRunRhythmMaker";
              "abjad.tools.rhythmmakertools.RhythmMaker.RhythmMaker" -> "abjad.tools.rhythmmakertools.IncisedRhythmMaker.IncisedRhythmMaker";
              "abjad.tools.rhythmmakertools.RhythmMaker.RhythmMaker" -> "abjad.tools.rhythmmakertools.NoteRhythmMaker.NoteRhythmMaker";
              "abjad.tools.rhythmmakertools.RhythmMaker.RhythmMaker" -> "abjad.tools.rhythmmakertools.SkipRhythmMaker.SkipRhythmMaker";
              "abjad.tools.rhythmmakertools.RhythmMaker.RhythmMaker" -> "abjad.tools.rhythmmakertools.TaleaRhythmMaker.TaleaRhythmMaker";
              "abjad.tools.rhythmmakertools.RhythmMaker.RhythmMaker" -> "abjad.tools.rhythmmakertools.TupletRhythmMaker.TupletRhythmMaker";
          }
          subgraph cluster_builtins {
              graph [label=builtins];
              "builtins.object" [color=2,
                  group=1,
                  label=object,
                  shape=box];
          }
          "abjad.tools.abctools.AbjadObject.AbjadObject" -> "abjad.tools.datastructuretools.TypedCollection.TypedCollection";
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
          "abjad.tools.datastructuretools.TypedCounter.TypedCounter" -> "abjad.tools.rhythmmakertools.RotationCounter.RotationCounter";
          "abjad.tools.datastructuretools.TypedOrderedDict.TypedOrderedDict" -> "abjad.tools.rhythmmakertools.PartitionTable.PartitionTable";
          "builtins.object" -> "abjad.tools.abctools.AbjadObject.AbstractBase";
      }

--------

Illustration helpers
--------------------

.. toctree::
   :hidden:

   ExampleWrapper
   GalleryMaker

.. autosummary::
   :nosignatures:

   ExampleWrapper
   GalleryMaker

--------

Masks
-----

.. toctree::
   :hidden:

   SilenceMask
   SustainMask

.. autosummary::
   :nosignatures:

   SilenceMask
   SustainMask

--------

Rhythm-makers
-------------

.. toctree::
   :hidden:

   AccelerandoRhythmMaker
   EvenDivisionRhythmMaker
   EvenRunRhythmMaker
   IncisedRhythmMaker
   NoteRhythmMaker
   RhythmMaker
   SkipRhythmMaker
   TaleaRhythmMaker
   TupletRhythmMaker

.. autosummary::
   :nosignatures:

   AccelerandoRhythmMaker
   EvenDivisionRhythmMaker
   EvenRunRhythmMaker
   IncisedRhythmMaker
   NoteRhythmMaker
   RhythmMaker
   SkipRhythmMaker
   TaleaRhythmMaker
   TupletRhythmMaker

--------

Specifiers
----------

.. toctree::
   :hidden:

   BeamSpecifier
   BurnishSpecifier
   DurationSpellingSpecifier
   InciseSpecifier
   InterpolationSpecifier
   PartitionTable
   RotationCounter
   Talea
   TieSpecifier
   TupletSpellingSpecifier

.. autosummary::
   :nosignatures:

   BeamSpecifier
   BurnishSpecifier
   DurationSpellingSpecifier
   InciseSpecifier
   InterpolationSpecifier
   PartitionTable
   RotationCounter
   Talea
   TieSpecifier
   TupletSpellingSpecifier

--------

Functions
---------

.. toctree::
   :hidden:

   make_lilypond_file
   silence
   silence_all
   silence_every
   silence_except
   silence_first
   silence_last
   sustain
   sustain_all
   sustain_every
   sustain_first
   sustain_last

.. autosummary::
   :nosignatures:

   make_lilypond_file
   silence
   silence_all
   silence_every
   silence_except
   silence_first
   silence_last
   sustain
   sustain_all
   sustain_every
   sustain_first
   sustain_last
