durationtools
=============

.. automodule:: abjad.tools.durationtools

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
          subgraph cluster_durationtools {
              graph [label=durationtools];
              "abjad.tools.durationtools.Division.Division" [color=black,
                  fontcolor=white,
                  group=2,
                  label=Division,
                  shape=box,
                  style="filled, rounded"];
              "abjad.tools.durationtools.Duration.Duration" [color=black,
                  fontcolor=white,
                  group=2,
                  label=Duration,
                  shape=box,
                  style="filled, rounded"];
              "abjad.tools.durationtools.Multiplier.Multiplier" [color=black,
                  fontcolor=white,
                  group=2,
                  label=Multiplier,
                  shape=box,
                  style="filled, rounded"];
              "abjad.tools.durationtools.Offset.Offset" [color=black,
                  fontcolor=white,
                  group=2,
                  label=Offset,
                  shape=box,
                  style="filled, rounded"];
              "abjad.tools.durationtools.Duration.Duration" -> "abjad.tools.durationtools.Multiplier.Multiplier";
              "abjad.tools.durationtools.Duration.Duration" -> "abjad.tools.durationtools.Offset.Offset";
          }
          subgraph cluster_mathtools {
              graph [label=mathtools];
              "abjad.tools.mathtools.NonreducedFraction.NonreducedFraction" [color=5,
                  group=4,
                  label=NonreducedFraction,
                  shape=box];
          }
          subgraph cluster_builtins {
              graph [label=builtins];
              "builtins.object" [color=2,
                  group=1,
                  label=object,
                  shape=box];
          }
          subgraph cluster_fractions {
              graph [label=fractions];
              "fractions.Fraction" [color=4,
                  group=3,
                  label=Fraction,
                  shape=box];
          }
          subgraph cluster_numbers {
              graph [label=numbers];
              "numbers.Complex" [color=6,
                  group=5,
                  label=Complex,
                  shape=oval,
                  style=bold];
              "numbers.Number" [color=6,
                  group=5,
                  label=Number,
                  shape=box];
              "numbers.Rational" [color=6,
                  group=5,
                  label=Rational,
                  shape=oval,
                  style=bold];
              "numbers.Real" [color=6,
                  group=5,
                  label=Real,
                  shape=oval,
                  style=bold];
              "numbers.Complex" -> "numbers.Real";
              "numbers.Number" -> "numbers.Complex";
              "numbers.Real" -> "numbers.Rational";
          }
          "abjad.tools.abctools.AbjadObject.AbjadObject" -> "abjad.tools.durationtools.Duration.Duration";
          "abjad.tools.abctools.AbjadObject.AbjadObject" -> "abjad.tools.mathtools.NonreducedFraction.NonreducedFraction";
          "abjad.tools.mathtools.NonreducedFraction.NonreducedFraction" -> "abjad.tools.durationtools.Division.Division";
          "builtins.object" -> "abjad.tools.abctools.AbjadObject.AbstractBase";
          "builtins.object" -> "numbers.Number";
          "fractions.Fraction" -> "abjad.tools.durationtools.Duration.Duration";
          "fractions.Fraction" -> "abjad.tools.mathtools.NonreducedFraction.NonreducedFraction";
          "numbers.Rational" -> "fractions.Fraction";
      }

--------

Classes
-------

.. toctree::
   :hidden:

   Division
   Duration
   Multiplier
   Offset

.. autosummary::
   :nosignatures:

   Division
   Duration
   Multiplier
   Offset
