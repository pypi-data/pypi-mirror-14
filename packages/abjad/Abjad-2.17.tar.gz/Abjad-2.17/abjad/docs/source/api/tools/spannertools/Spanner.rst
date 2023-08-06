.. currentmodule:: abjad.tools.spannertools

Spanner
=======

.. autoclass:: Spanner

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
          subgraph cluster_spannertools {
              graph [label=spannertools];
              "abjad.tools.spannertools.Beam.Beam" [color=3,
                  group=2,
                  label=Beam,
                  shape=box];
              "abjad.tools.spannertools.BowContactSpanner.BowContactSpanner" [color=3,
                  group=2,
                  label=BowContactSpanner,
                  shape=box];
              "abjad.tools.spannertools.ClefSpanner.ClefSpanner" [color=3,
                  group=2,
                  label=ClefSpanner,
                  shape=box];
              "abjad.tools.spannertools.ComplexBeam.ComplexBeam" [color=3,
                  group=2,
                  label=ComplexBeam,
                  shape=box];
              "abjad.tools.spannertools.ComplexTrillSpanner.ComplexTrillSpanner" [color=3,
                  group=2,
                  label=ComplexTrillSpanner,
                  shape=box];
              "abjad.tools.spannertools.Crescendo.Crescendo" [color=3,
                  group=2,
                  label=Crescendo,
                  shape=box];
              "abjad.tools.spannertools.Decrescendo.Decrescendo" [color=3,
                  group=2,
                  label=Decrescendo,
                  shape=box];
              "abjad.tools.spannertools.DuratedComplexBeam.DuratedComplexBeam" [color=3,
                  group=2,
                  label=DuratedComplexBeam,
                  shape=box];
              "abjad.tools.spannertools.GeneralizedBeam.GeneralizedBeam" [color=3,
                  group=2,
                  label=GeneralizedBeam,
                  shape=box];
              "abjad.tools.spannertools.Glissando.Glissando" [color=3,
                  group=2,
                  label=Glissando,
                  shape=box];
              "abjad.tools.spannertools.Hairpin.Hairpin" [color=3,
                  group=2,
                  label=Hairpin,
                  shape=box];
              "abjad.tools.spannertools.HiddenStaffSpanner.HiddenStaffSpanner" [color=3,
                  group=2,
                  label=HiddenStaffSpanner,
                  shape=box];
              "abjad.tools.spannertools.HorizontalBracketSpanner.HorizontalBracketSpanner" [color=3,
                  group=2,
                  label=HorizontalBracketSpanner,
                  shape=box];
              "abjad.tools.spannertools.MeasuredComplexBeam.MeasuredComplexBeam" [color=3,
                  group=2,
                  label=MeasuredComplexBeam,
                  shape=box];
              "abjad.tools.spannertools.MultipartBeam.MultipartBeam" [color=3,
                  group=2,
                  label=MultipartBeam,
                  shape=box];
              "abjad.tools.spannertools.OctavationSpanner.OctavationSpanner" [color=3,
                  group=2,
                  label=OctavationSpanner,
                  shape=box];
              "abjad.tools.spannertools.PhrasingSlur.PhrasingSlur" [color=3,
                  group=2,
                  label=PhrasingSlur,
                  shape=box];
              "abjad.tools.spannertools.PianoPedalSpanner.PianoPedalSpanner" [color=3,
                  group=2,
                  label=PianoPedalSpanner,
                  shape=box];
              "abjad.tools.spannertools.Slur.Slur" [color=3,
                  group=2,
                  label=Slur,
                  shape=box];
              "abjad.tools.spannertools.Spanner.Spanner" [color=black,
                  fontcolor=white,
                  group=2,
                  label=<<B>Spanner</B>>,
                  shape=box,
                  style="filled, rounded"];
              "abjad.tools.spannertools.StaffLinesSpanner.StaffLinesSpanner" [color=3,
                  group=2,
                  label=StaffLinesSpanner,
                  shape=box];
              "abjad.tools.spannertools.StemTremoloSpanner.StemTremoloSpanner" [color=3,
                  group=2,
                  label=StemTremoloSpanner,
                  shape=box];
              "abjad.tools.spannertools.TempoSpanner.TempoSpanner" [color=3,
                  group=2,
                  label=TempoSpanner,
                  shape=box];
              "abjad.tools.spannertools.TextSpanner.TextSpanner" [color=3,
                  group=2,
                  label=TextSpanner,
                  shape=box];
              "abjad.tools.spannertools.Tie.Tie" [color=3,
                  group=2,
                  label=Tie,
                  shape=box];
              "abjad.tools.spannertools.TrillSpanner.TrillSpanner" [color=3,
                  group=2,
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

Bases
-----

- :py:class:`abjad.tools.abctools.AbjadObject`

- :py:class:`abjad.tools.abctools.AbjadObject.AbstractBase`

- :py:class:`builtins.object`

.. only:: html

   Attribute summary
   -----------------

   .. autosummary::

      ~abjad.tools.spannertools.Spanner.Spanner.components
      ~abjad.tools.spannertools.Spanner.Spanner.name
      ~abjad.tools.spannertools.Spanner.Spanner.overrides
      ~abjad.tools.spannertools.Spanner.Spanner.__contains__
      ~abjad.tools.spannertools.Spanner.Spanner.__copy__
      ~abjad.tools.spannertools.Spanner.Spanner.__eq__
      ~abjad.tools.spannertools.Spanner.Spanner.__format__
      ~abjad.tools.spannertools.Spanner.Spanner.__getitem__
      ~abjad.tools.spannertools.Spanner.Spanner.__hash__
      ~abjad.tools.spannertools.Spanner.Spanner.__len__
      ~abjad.tools.spannertools.Spanner.Spanner.__lt__
      ~abjad.tools.spannertools.Spanner.Spanner.__ne__
      ~abjad.tools.spannertools.Spanner.Spanner.__repr__

Read-only properties
--------------------

.. autoattribute:: abjad.tools.spannertools.Spanner.Spanner.components

.. autoattribute:: abjad.tools.spannertools.Spanner.Spanner.name

.. autoattribute:: abjad.tools.spannertools.Spanner.Spanner.overrides

Special methods
---------------

.. automethod:: abjad.tools.spannertools.Spanner.Spanner.__contains__

.. automethod:: abjad.tools.spannertools.Spanner.Spanner.__copy__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.spannertools.Spanner.Spanner.__eq__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.spannertools.Spanner.Spanner.__format__

.. automethod:: abjad.tools.spannertools.Spanner.Spanner.__getitem__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.spannertools.Spanner.Spanner.__hash__

.. automethod:: abjad.tools.spannertools.Spanner.Spanner.__len__

.. automethod:: abjad.tools.spannertools.Spanner.Spanner.__lt__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.spannertools.Spanner.Spanner.__ne__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.spannertools.Spanner.Spanner.__repr__
