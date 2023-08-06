scoretools
==========

.. automodule:: abjad.tools.scoretools

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
              "abjad.tools.datastructuretools.TypedList.TypedList" [color=3,
                  group=2,
                  label=TypedList,
                  shape=box];
              "abjad.tools.datastructuretools.TypedCollection.TypedCollection" -> "abjad.tools.datastructuretools.TypedList.TypedList";
          }
          subgraph cluster_scoretools {
              graph [label=scoretools];
              "abjad.tools.scoretools.Chord.Chord" [color=black,
                  fontcolor=white,
                  group=3,
                  label=Chord,
                  shape=box,
                  style="filled, rounded"];
              "abjad.tools.scoretools.Cluster.Cluster" [color=black,
                  fontcolor=white,
                  group=3,
                  label=Cluster,
                  shape=box,
                  style="filled, rounded"];
              "abjad.tools.scoretools.Component.Component" [color=black,
                  fontcolor=white,
                  group=3,
                  label=Component,
                  shape=oval,
                  style="filled, rounded"];
              "abjad.tools.scoretools.Container.Container" [color=black,
                  fontcolor=white,
                  group=3,
                  label=Container,
                  shape=box,
                  style="filled, rounded"];
              "abjad.tools.scoretools.Context.Context" [color=black,
                  fontcolor=white,
                  group=3,
                  label=Context,
                  shape=box,
                  style="filled, rounded"];
              "abjad.tools.scoretools.DrumNoteHead.DrumNoteHead" [color=black,
                  fontcolor=white,
                  group=3,
                  label=DrumNoteHead,
                  shape=box,
                  style="filled, rounded"];
              "abjad.tools.scoretools.FixedDurationContainer.FixedDurationContainer" [color=black,
                  fontcolor=white,
                  group=3,
                  label=FixedDurationContainer,
                  shape=box,
                  style="filled, rounded"];
              "abjad.tools.scoretools.FixedDurationTuplet.FixedDurationTuplet" [color=black,
                  fontcolor=white,
                  group=3,
                  label=FixedDurationTuplet,
                  shape=box,
                  style="filled, rounded"];
              "abjad.tools.scoretools.GraceContainer.GraceContainer" [color=black,
                  fontcolor=white,
                  group=3,
                  label=GraceContainer,
                  shape=box,
                  style="filled, rounded"];
              "abjad.tools.scoretools.Leaf.Leaf" [color=black,
                  fontcolor=white,
                  group=3,
                  label=Leaf,
                  shape=oval,
                  style="filled, rounded"];
              "abjad.tools.scoretools.Measure.Measure" [color=black,
                  fontcolor=white,
                  group=3,
                  label=Measure,
                  shape=box,
                  style="filled, rounded"];
              "abjad.tools.scoretools.MultimeasureRest.MultimeasureRest" [color=black,
                  fontcolor=white,
                  group=3,
                  label=MultimeasureRest,
                  shape=box,
                  style="filled, rounded"];
              "abjad.tools.scoretools.Note.Note" [color=black,
                  fontcolor=white,
                  group=3,
                  label=Note,
                  shape=box,
                  style="filled, rounded"];
              "abjad.tools.scoretools.NoteHead.NoteHead" [color=black,
                  fontcolor=white,
                  group=3,
                  label=NoteHead,
                  shape=box,
                  style="filled, rounded"];
              "abjad.tools.scoretools.NoteHeadInventory.NoteHeadInventory" [color=black,
                  fontcolor=white,
                  group=3,
                  label=NoteHeadInventory,
                  shape=box,
                  style="filled, rounded"];
              "abjad.tools.scoretools.Rest.Rest" [color=black,
                  fontcolor=white,
                  group=3,
                  label=Rest,
                  shape=box,
                  style="filled, rounded"];
              "abjad.tools.scoretools.Score.Score" [color=black,
                  fontcolor=white,
                  group=3,
                  label=Score,
                  shape=box,
                  style="filled, rounded"];
              "abjad.tools.scoretools.Skip.Skip" [color=black,
                  fontcolor=white,
                  group=3,
                  label=Skip,
                  shape=box,
                  style="filled, rounded"];
              "abjad.tools.scoretools.Staff.Staff" [color=black,
                  fontcolor=white,
                  group=3,
                  label=Staff,
                  shape=box,
                  style="filled, rounded"];
              "abjad.tools.scoretools.StaffGroup.StaffGroup" [color=black,
                  fontcolor=white,
                  group=3,
                  label=StaffGroup,
                  shape=box,
                  style="filled, rounded"];
              "abjad.tools.scoretools.Tuplet.Tuplet" [color=black,
                  fontcolor=white,
                  group=3,
                  label=Tuplet,
                  shape=box,
                  style="filled, rounded"];
              "abjad.tools.scoretools.Voice.Voice" [color=black,
                  fontcolor=white,
                  group=3,
                  label=Voice,
                  shape=box,
                  style="filled, rounded"];
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
          subgraph cluster_builtins {
              graph [label=builtins];
              "builtins.object" [color=2,
                  group=1,
                  label=object,
                  shape=box];
          }
          "abjad.tools.abctools.AbjadObject.AbjadObject" -> "abjad.tools.datastructuretools.TypedCollection.TypedCollection";
          "abjad.tools.abctools.AbjadObject.AbjadObject" -> "abjad.tools.scoretools.Component.Component";
          "abjad.tools.abctools.AbjadObject.AbjadObject" -> "abjad.tools.scoretools.NoteHead.NoteHead";
          "abjad.tools.datastructuretools.TypedList.TypedList" -> "abjad.tools.scoretools.NoteHeadInventory.NoteHeadInventory";
          "builtins.object" -> "abjad.tools.abctools.AbjadObject.AbstractBase";
      }

--------

Abstract Classes
----------------

.. toctree::
   :hidden:

   Component
   Leaf

.. autosummary::
   :nosignatures:

   Component
   Leaf

--------

Containers
----------

.. toctree::
   :hidden:

   Cluster
   Container
   FixedDurationContainer
   FixedDurationTuplet
   GraceContainer
   Measure
   Tuplet

.. autosummary::
   :nosignatures:

   Cluster
   Container
   FixedDurationContainer
   FixedDurationTuplet
   GraceContainer
   Measure
   Tuplet

--------

Contexts
--------

.. toctree::
   :hidden:

   Context
   Score
   Staff
   StaffGroup
   Voice

.. autosummary::
   :nosignatures:

   Context
   Score
   Staff
   StaffGroup
   Voice

--------

Leaves
------

.. toctree::
   :hidden:

   Chord
   MultimeasureRest
   Note
   Rest
   Skip

.. autosummary::
   :nosignatures:

   Chord
   MultimeasureRest
   Note
   Rest
   Skip

--------

Note heads
----------

.. toctree::
   :hidden:

   DrumNoteHead
   NoteHead
   NoteHeadInventory

.. autosummary::
   :nosignatures:

   DrumNoteHead
   NoteHead
   NoteHeadInventory

--------

Functions
---------

.. toctree::
   :hidden:

   append_spacer_skip_to_underfull_measure
   append_spacer_skips_to_underfull_measures_in_expr
   apply_full_measure_tuplets_to_contents_of_measures_in_expr
   extend_measures_in_expr_and_apply_full_measure_tuplets
   fill_measures_in_expr_with_full_measure_spacer_skips
   fill_measures_in_expr_with_minimal_number_of_notes
   fill_measures_in_expr_with_repeated_notes
   fill_measures_in_expr_with_time_signature_denominator_notes
   get_measure
   get_measure_that_starts_with_container
   get_measure_that_stops_with_container
   get_next_measure_from_component
   get_previous_measure_from_component
   make_empty_piano_score
   make_leaves
   make_leaves_from_talea
   make_multimeasure_rests
   make_multiplied_quarter_notes
   make_notes
   make_notes_with_multiplied_durations
   make_percussion_note
   make_piano_score_from_leaves
   make_piano_sketch_score_from_leaves
   make_repeated_notes
   make_repeated_notes_from_time_signature
   make_repeated_notes_from_time_signatures
   make_repeated_notes_with_shorter_notes_at_end
   make_repeated_rests_from_time_signatures
   make_repeated_skips_from_time_signatures
   make_rests
   make_skips
   make_spacer_skip_measures
   make_tied_leaf
   move_full_measure_tuplet_prolation_to_measure_time_signature
   move_measure_prolation_to_full_measure_tuplet
   scale_measure_denominator_and_adjust_measure_contents
   set_measure_denominator_and_adjust_numerator

.. autosummary::
   :nosignatures:

   append_spacer_skip_to_underfull_measure
   append_spacer_skips_to_underfull_measures_in_expr
   apply_full_measure_tuplets_to_contents_of_measures_in_expr
   extend_measures_in_expr_and_apply_full_measure_tuplets
   fill_measures_in_expr_with_full_measure_spacer_skips
   fill_measures_in_expr_with_minimal_number_of_notes
   fill_measures_in_expr_with_repeated_notes
   fill_measures_in_expr_with_time_signature_denominator_notes
   get_measure
   get_measure_that_starts_with_container
   get_measure_that_stops_with_container
   get_next_measure_from_component
   get_previous_measure_from_component
   make_empty_piano_score
   make_leaves
   make_leaves_from_talea
   make_multimeasure_rests
   make_multiplied_quarter_notes
   make_notes
   make_notes_with_multiplied_durations
   make_percussion_note
   make_piano_score_from_leaves
   make_piano_sketch_score_from_leaves
   make_repeated_notes
   make_repeated_notes_from_time_signature
   make_repeated_notes_from_time_signatures
   make_repeated_notes_with_shorter_notes_at_end
   make_repeated_rests_from_time_signatures
   make_repeated_skips_from_time_signatures
   make_rests
   make_skips
   make_spacer_skip_measures
   make_tied_leaf
   move_full_measure_tuplet_prolation_to_measure_time_signature
   move_measure_prolation_to_full_measure_tuplet
   scale_measure_denominator_and_adjust_measure_contents
   set_measure_denominator_and_adjust_numerator
