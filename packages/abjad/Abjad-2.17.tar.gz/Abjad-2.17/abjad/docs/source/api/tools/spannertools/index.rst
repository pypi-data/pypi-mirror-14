spannertools
============

.. automodule:: abjad.tools.spannertools

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
          subgraph cluster_spannertools {
              graph [label=spannertools];
              "abjad.tools.spannertools.Beam.Beam" [color=black,
                  fontcolor=white,
                  group=2,
                  label=Beam,
                  shape=box,
                  style="filled, rounded"];
              "abjad.tools.spannertools.BowContactSpanner.BowContactSpanner" [color=black,
                  fontcolor=white,
                  group=2,
                  label=BowContactSpanner,
                  shape=box,
                  style="filled, rounded"];
              "abjad.tools.spannertools.ClefSpanner.ClefSpanner" [color=black,
                  fontcolor=white,
                  group=2,
                  label=ClefSpanner,
                  shape=box,
                  style="filled, rounded"];
              "abjad.tools.spannertools.ComplexBeam.ComplexBeam" [color=black,
                  fontcolor=white,
                  group=2,
                  label=ComplexBeam,
                  shape=box,
                  style="filled, rounded"];
              "abjad.tools.spannertools.ComplexTrillSpanner.ComplexTrillSpanner" [color=black,
                  fontcolor=white,
                  group=2,
                  label=ComplexTrillSpanner,
                  shape=box,
                  style="filled, rounded"];
              "abjad.tools.spannertools.Crescendo.Crescendo" [color=black,
                  fontcolor=white,
                  group=2,
                  label=Crescendo,
                  shape=box,
                  style="filled, rounded"];
              "abjad.tools.spannertools.Decrescendo.Decrescendo" [color=black,
                  fontcolor=white,
                  group=2,
                  label=Decrescendo,
                  shape=box,
                  style="filled, rounded"];
              "abjad.tools.spannertools.DuratedComplexBeam.DuratedComplexBeam" [color=black,
                  fontcolor=white,
                  group=2,
                  label=DuratedComplexBeam,
                  shape=box,
                  style="filled, rounded"];
              "abjad.tools.spannertools.GeneralizedBeam.GeneralizedBeam" [color=black,
                  fontcolor=white,
                  group=2,
                  label=GeneralizedBeam,
                  shape=box,
                  style="filled, rounded"];
              "abjad.tools.spannertools.Glissando.Glissando" [color=black,
                  fontcolor=white,
                  group=2,
                  label=Glissando,
                  shape=box,
                  style="filled, rounded"];
              "abjad.tools.spannertools.Hairpin.Hairpin" [color=black,
                  fontcolor=white,
                  group=2,
                  label=Hairpin,
                  shape=box,
                  style="filled, rounded"];
              "abjad.tools.spannertools.HiddenStaffSpanner.HiddenStaffSpanner" [color=black,
                  fontcolor=white,
                  group=2,
                  label=HiddenStaffSpanner,
                  shape=box,
                  style="filled, rounded"];
              "abjad.tools.spannertools.HorizontalBracketSpanner.HorizontalBracketSpanner" [color=black,
                  fontcolor=white,
                  group=2,
                  label=HorizontalBracketSpanner,
                  shape=box,
                  style="filled, rounded"];
              "abjad.tools.spannertools.MeasuredComplexBeam.MeasuredComplexBeam" [color=black,
                  fontcolor=white,
                  group=2,
                  label=MeasuredComplexBeam,
                  shape=box,
                  style="filled, rounded"];
              "abjad.tools.spannertools.MultipartBeam.MultipartBeam" [color=black,
                  fontcolor=white,
                  group=2,
                  label=MultipartBeam,
                  shape=box,
                  style="filled, rounded"];
              "abjad.tools.spannertools.OctavationSpanner.OctavationSpanner" [color=black,
                  fontcolor=white,
                  group=2,
                  label=OctavationSpanner,
                  shape=box,
                  style="filled, rounded"];
              "abjad.tools.spannertools.PhrasingSlur.PhrasingSlur" [color=black,
                  fontcolor=white,
                  group=2,
                  label=PhrasingSlur,
                  shape=box,
                  style="filled, rounded"];
              "abjad.tools.spannertools.PianoPedalSpanner.PianoPedalSpanner" [color=black,
                  fontcolor=white,
                  group=2,
                  label=PianoPedalSpanner,
                  shape=box,
                  style="filled, rounded"];
              "abjad.tools.spannertools.Slur.Slur" [color=black,
                  fontcolor=white,
                  group=2,
                  label=Slur,
                  shape=box,
                  style="filled, rounded"];
              "abjad.tools.spannertools.Spanner.Spanner" [color=black,
                  fontcolor=white,
                  group=2,
                  label=Spanner,
                  shape=box,
                  style="filled, rounded"];
              "abjad.tools.spannertools.StaffLinesSpanner.StaffLinesSpanner" [color=black,
                  fontcolor=white,
                  group=2,
                  label=StaffLinesSpanner,
                  shape=box,
                  style="filled, rounded"];
              "abjad.tools.spannertools.StemTremoloSpanner.StemTremoloSpanner" [color=black,
                  fontcolor=white,
                  group=2,
                  label=StemTremoloSpanner,
                  shape=box,
                  style="filled, rounded"];
              "abjad.tools.spannertools.TempoSpanner.TempoSpanner" [color=black,
                  fontcolor=white,
                  group=2,
                  label=TempoSpanner,
                  shape=box,
                  style="filled, rounded"];
              "abjad.tools.spannertools.TextSpanner.TextSpanner" [color=black,
                  fontcolor=white,
                  group=2,
                  label=TextSpanner,
                  shape=box,
                  style="filled, rounded"];
              "abjad.tools.spannertools.Tie.Tie" [color=black,
                  fontcolor=white,
                  group=2,
                  label=Tie,
                  shape=box,
                  style="filled, rounded"];
              "abjad.tools.spannertools.TrillSpanner.TrillSpanner" [color=black,
                  fontcolor=white,
                  group=2,
                  label=TrillSpanner,
                  shape=box,
                  style="filled, rounded"];
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
          subgraph cluster_builtins {
              graph [label=builtins];
              "builtins.object" [color=2,
                  group=1,
                  label=object,
                  shape=box];
          }
          "abjad.tools.abctools.AbjadObject.AbjadObject" -> "abjad.tools.spannertools.Spanner.Spanner";
          "builtins.object" -> "abjad.tools.abctools.AbjadObject.AbstractBase";
      }

--------

Classes
-------

.. toctree::
   :hidden:

   Beam
   BowContactSpanner
   ClefSpanner
   ComplexBeam
   ComplexTrillSpanner
   Crescendo
   Decrescendo
   DuratedComplexBeam
   GeneralizedBeam
   Glissando
   Hairpin
   HiddenStaffSpanner
   HorizontalBracketSpanner
   MeasuredComplexBeam
   MultipartBeam
   OctavationSpanner
   PhrasingSlur
   PianoPedalSpanner
   Slur
   Spanner
   StaffLinesSpanner
   StemTremoloSpanner
   TempoSpanner
   TextSpanner
   Tie
   TrillSpanner

.. autosummary::
   :nosignatures:

   Beam
   BowContactSpanner
   ClefSpanner
   ComplexBeam
   ComplexTrillSpanner
   Crescendo
   Decrescendo
   DuratedComplexBeam
   GeneralizedBeam
   Glissando
   Hairpin
   HiddenStaffSpanner
   HorizontalBracketSpanner
   MeasuredComplexBeam
   MultipartBeam
   OctavationSpanner
   PhrasingSlur
   PianoPedalSpanner
   Slur
   Spanner
   StaffLinesSpanner
   StemTremoloSpanner
   TempoSpanner
   TextSpanner
   Tie
   TrillSpanner

--------

Functions
---------

.. toctree::
   :hidden:

   make_colored_text_spanner_with_nibs
   make_dynamic_spanner_below_with_nib_at_right
   make_solid_text_spanner_with_nib

.. autosummary::
   :nosignatures:

   make_colored_text_spanner_with_nibs
   make_dynamic_spanner_below_with_nib_at_right
   make_solid_text_spanner_with_nib
