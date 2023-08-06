templatetools
=============

.. automodule:: abjad.tools.templatetools

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
          subgraph cluster_templatetools {
              graph [label=templatetools];
              "abjad.tools.templatetools.GroupedRhythmicStavesScoreTemplate.GroupedRhythmicStavesScoreTemplate" [color=black,
                  fontcolor=white,
                  group=2,
                  label=GroupedRhythmicStavesScoreTemplate,
                  shape=box,
                  style="filled, rounded"];
              "abjad.tools.templatetools.GroupedStavesScoreTemplate.GroupedStavesScoreTemplate" [color=black,
                  fontcolor=white,
                  group=2,
                  label=GroupedStavesScoreTemplate,
                  shape=box,
                  style="filled, rounded"];
              "abjad.tools.templatetools.StringOrchestraScoreTemplate.StringOrchestraScoreTemplate" [color=black,
                  fontcolor=white,
                  group=2,
                  label=StringOrchestraScoreTemplate,
                  shape=box,
                  style="filled, rounded"];
              "abjad.tools.templatetools.StringQuartetScoreTemplate.StringQuartetScoreTemplate" [color=black,
                  fontcolor=white,
                  group=2,
                  label=StringQuartetScoreTemplate,
                  shape=box,
                  style="filled, rounded"];
              "abjad.tools.templatetools.TwoStaffPianoScoreTemplate.TwoStaffPianoScoreTemplate" [color=black,
                  fontcolor=white,
                  group=2,
                  label=TwoStaffPianoScoreTemplate,
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
          "abjad.tools.abctools.AbjadObject.AbjadObject" -> "abjad.tools.templatetools.GroupedRhythmicStavesScoreTemplate.GroupedRhythmicStavesScoreTemplate";
          "abjad.tools.abctools.AbjadObject.AbjadObject" -> "abjad.tools.templatetools.GroupedStavesScoreTemplate.GroupedStavesScoreTemplate";
          "abjad.tools.abctools.AbjadObject.AbjadObject" -> "abjad.tools.templatetools.StringQuartetScoreTemplate.StringQuartetScoreTemplate";
          "abjad.tools.abctools.AbjadObject.AbjadObject" -> "abjad.tools.templatetools.TwoStaffPianoScoreTemplate.TwoStaffPianoScoreTemplate";
          "abjad.tools.abctools.AbjadValueObject.AbjadValueObject" -> "abjad.tools.templatetools.StringOrchestraScoreTemplate.StringOrchestraScoreTemplate";
          "builtins.object" -> "abjad.tools.abctools.AbjadObject.AbstractBase";
      }

--------

Classes
-------

.. toctree::
   :hidden:

   GroupedRhythmicStavesScoreTemplate
   GroupedStavesScoreTemplate
   StringOrchestraScoreTemplate
   StringQuartetScoreTemplate
   TwoStaffPianoScoreTemplate

.. autosummary::
   :nosignatures:

   GroupedRhythmicStavesScoreTemplate
   GroupedStavesScoreTemplate
   StringOrchestraScoreTemplate
   StringQuartetScoreTemplate
   TwoStaffPianoScoreTemplate
