sequencetools
=============

.. automodule:: abjad.tools.sequencetools

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
          subgraph cluster_sequencetools {
              graph [label=sequencetools];
              "abjad.tools.sequencetools.Duplication.Duplication" [color=black,
                  fontcolor=white,
                  group=2,
                  label=Duplication,
                  shape=box,
                  style="filled, rounded"];
              "abjad.tools.sequencetools.Sequence.Sequence" [color=black,
                  fontcolor=white,
                  group=2,
                  label=Sequence,
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
          "abjad.tools.abctools.AbjadObject.AbjadObject" -> "abjad.tools.sequencetools.Sequence.Sequence";
          "abjad.tools.abctools.AbjadValueObject.AbjadValueObject" -> "abjad.tools.sequencetools.Duplication.Duplication";
          "builtins.object" -> "abjad.tools.abctools.AbjadObject.AbstractBase";
      }

--------

Classes
-------

.. toctree::
   :hidden:

   Duplication
   Sequence

.. autosummary::
   :nosignatures:

   Duplication
   Sequence

--------

Functions
---------

.. toctree::
   :hidden:

   flatten_sequence
   increase_elements
   interlace_sequences
   iterate_sequence_boustrophedon
   iterate_sequence_nwise
   join_subsequences
   join_subsequences_by_sign_of_elements
   negate_elements
   overwrite_elements
   partition_sequence_by_counts
   partition_sequence_by_ratio_of_lengths
   partition_sequence_by_ratio_of_weights
   partition_sequence_by_restricted_growth_function
   partition_sequence_by_sign_of_elements
   partition_sequence_by_value_of_elements
   partition_sequence_by_weights
   permute_sequence
   remove_elements
   remove_repeated_elements
   remove_subsequence_of_weight_at_index
   repeat_elements
   repeat_sequence
   repeat_sequence_to_length
   repeat_sequence_to_weight
   replace_elements
   retain_elements
   reverse_sequence
   rotate_sequence
   splice_between_elements
   split_sequence
   sum_consecutive_elements_by_sign
   sum_elements
   truncate_sequence
   yield_all_combinations_of_elements
   yield_all_k_ary_sequences_of_length
   yield_all_pairs_between_sequences
   yield_all_partitions_of_sequence
   yield_all_permutations_of_sequence
   yield_all_permutations_of_sequence_in_orbit
   yield_all_restricted_growth_functions_of_length
   yield_all_rotations_of_sequence
   yield_all_set_partitions_of_sequence
   yield_all_subsequences_of_sequence
   yield_all_unordered_pairs_of_sequence
   yield_outer_product_of_sequences
   zip_sequences

.. autosummary::
   :nosignatures:

   flatten_sequence
   increase_elements
   interlace_sequences
   iterate_sequence_boustrophedon
   iterate_sequence_nwise
   join_subsequences
   join_subsequences_by_sign_of_elements
   negate_elements
   overwrite_elements
   partition_sequence_by_counts
   partition_sequence_by_ratio_of_lengths
   partition_sequence_by_ratio_of_weights
   partition_sequence_by_restricted_growth_function
   partition_sequence_by_sign_of_elements
   partition_sequence_by_value_of_elements
   partition_sequence_by_weights
   permute_sequence
   remove_elements
   remove_repeated_elements
   remove_subsequence_of_weight_at_index
   repeat_elements
   repeat_sequence
   repeat_sequence_to_length
   repeat_sequence_to_weight
   replace_elements
   retain_elements
   reverse_sequence
   rotate_sequence
   splice_between_elements
   split_sequence
   sum_consecutive_elements_by_sign
   sum_elements
   truncate_sequence
   yield_all_combinations_of_elements
   yield_all_k_ary_sequences_of_length
   yield_all_pairs_between_sequences
   yield_all_partitions_of_sequence
   yield_all_permutations_of_sequence
   yield_all_permutations_of_sequence_in_orbit
   yield_all_restricted_growth_functions_of_length
   yield_all_rotations_of_sequence
   yield_all_set_partitions_of_sequence
   yield_all_subsequences_of_sequence
   yield_all_unordered_pairs_of_sequence
   yield_outer_product_of_sequences
   zip_sequences
