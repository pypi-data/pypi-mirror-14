mathtools
=========

.. automodule:: abjad.tools.mathtools

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
          subgraph cluster_durationtools {
              graph [label=durationtools];
              "abjad.tools.durationtools.Division.Division" [color=3,
                  group=2,
                  label=Division,
                  shape=box];
          }
          subgraph cluster_mathtools {
              graph [label=mathtools];
              "abjad.tools.mathtools.BoundedObject.BoundedObject" [color=black,
                  fontcolor=white,
                  group=4,
                  label=BoundedObject,
                  shape=box,
                  style="filled, rounded"];
              "abjad.tools.mathtools.Infinity.Infinity" [color=black,
                  fontcolor=white,
                  group=4,
                  label=Infinity,
                  shape=box,
                  style="filled, rounded"];
              "abjad.tools.mathtools.NegativeInfinity.NegativeInfinity" [color=black,
                  fontcolor=white,
                  group=4,
                  label=NegativeInfinity,
                  shape=box,
                  style="filled, rounded"];
              "abjad.tools.mathtools.NonreducedFraction.NonreducedFraction" [color=black,
                  fontcolor=white,
                  group=4,
                  label=NonreducedFraction,
                  shape=box,
                  style="filled, rounded"];
              "abjad.tools.mathtools.NonreducedRatio.NonreducedRatio" [color=black,
                  fontcolor=white,
                  group=4,
                  label=NonreducedRatio,
                  shape=box,
                  style="filled, rounded"];
              "abjad.tools.mathtools.Ratio.Ratio" [color=black,
                  fontcolor=white,
                  group=4,
                  label=Ratio,
                  shape=box,
                  style="filled, rounded"];
              "abjad.tools.mathtools.Infinity.Infinity" -> "abjad.tools.mathtools.NegativeInfinity.NegativeInfinity";
              "abjad.tools.mathtools.NonreducedRatio.NonreducedRatio" -> "abjad.tools.mathtools.Ratio.Ratio";
          }
          subgraph cluster_timespantools {
              graph [label=timespantools];
              "abjad.tools.timespantools.AnnotatedTimespan.AnnotatedTimespan" [color=7,
                  group=6,
                  label=AnnotatedTimespan,
                  shape=box];
              "abjad.tools.timespantools.Timespan.Timespan" [color=7,
                  group=6,
                  label=Timespan,
                  shape=box];
              "abjad.tools.timespantools.Timespan.Timespan" -> "abjad.tools.timespantools.AnnotatedTimespan.AnnotatedTimespan";
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
          "abjad.tools.abctools.AbjadObject.AbjadObject" -> "abjad.tools.mathtools.BoundedObject.BoundedObject";
          "abjad.tools.abctools.AbjadObject.AbjadObject" -> "abjad.tools.mathtools.Infinity.Infinity";
          "abjad.tools.abctools.AbjadObject.AbjadObject" -> "abjad.tools.mathtools.NonreducedFraction.NonreducedFraction";
          "abjad.tools.abctools.AbjadValueObject.AbjadValueObject" -> "abjad.tools.mathtools.NonreducedRatio.NonreducedRatio";
          "abjad.tools.mathtools.BoundedObject.BoundedObject" -> "abjad.tools.timespantools.Timespan.Timespan";
          "abjad.tools.mathtools.NonreducedFraction.NonreducedFraction" -> "abjad.tools.durationtools.Division.Division";
          "builtins.object" -> "abjad.tools.abctools.AbjadObject.AbstractBase";
          "builtins.object" -> "numbers.Number";
          "fractions.Fraction" -> "abjad.tools.mathtools.NonreducedFraction.NonreducedFraction";
          "numbers.Rational" -> "fractions.Fraction";
      }

--------

Classes
-------

.. toctree::
   :hidden:

   BoundedObject
   Infinity
   NegativeInfinity
   NonreducedFraction
   NonreducedRatio
   Ratio

.. autosummary::
   :nosignatures:

   BoundedObject
   Infinity
   NegativeInfinity
   NonreducedFraction
   NonreducedRatio
   Ratio

--------

Functions
---------

.. toctree::
   :hidden:

   all_are_equal
   all_are_integer_equivalent_exprs
   all_are_integer_equivalent_numbers
   all_are_nonnegative_integer_equivalent_numbers
   all_are_nonnegative_integer_powers_of_two
   all_are_nonnegative_integers
   all_are_numbers
   all_are_pairs
   all_are_pairs_of_types
   all_are_positive_integer_equivalent_numbers
   all_are_positive_integer_powers_of_two
   all_are_positive_integers
   all_are_unequal
   are_relatively_prime
   arithmetic_mean
   binomial_coefficient
   cumulative_products
   cumulative_signed_weights
   cumulative_sums
   cumulative_sums_pairwise
   difference_series
   divide_number_by_ratio
   divisors
   factors
   fraction_to_proper_fraction
   get_shared_numeric_sign
   greatest_common_divisor
   greatest_multiple_less_equal
   greatest_power_of_two_less_equal
   integer_equivalent_number_to_integer
   integer_to_base_k_tuple
   integer_to_binary_string
   is_assignable_integer
   is_dotted_integer
   is_fraction_equivalent_pair
   is_integer_equivalent_expr
   is_integer_equivalent_n_tuple
   is_integer_equivalent_number
   is_integer_equivalent_pair
   is_integer_equivalent_singleton
   is_integer_n_tuple
   is_integer_pair
   is_integer_singleton
   is_n_tuple
   is_negative_integer
   is_nonnegative_integer
   is_nonnegative_integer_equivalent_number
   is_nonnegative_integer_power_of_two
   is_null_tuple
   is_pair
   is_positive_integer
   is_positive_integer_equivalent_number
   is_positive_integer_power_of_two
   is_singleton
   least_common_multiple
   least_multiple_greater_equal
   least_power_of_two_greater_equal
   next_integer_partition
   partition_integer_by_ratio
   partition_integer_into_canonic_parts
   partition_integer_into_halves
   partition_integer_into_parts_less_than_double
   partition_integer_into_units
   remove_powers_of_two
   sign
   weight
   yield_all_compositions_of_integer
   yield_all_partitions_of_integer
   yield_nonreduced_fractions

.. autosummary::
   :nosignatures:

   all_are_equal
   all_are_integer_equivalent_exprs
   all_are_integer_equivalent_numbers
   all_are_nonnegative_integer_equivalent_numbers
   all_are_nonnegative_integer_powers_of_two
   all_are_nonnegative_integers
   all_are_numbers
   all_are_pairs
   all_are_pairs_of_types
   all_are_positive_integer_equivalent_numbers
   all_are_positive_integer_powers_of_two
   all_are_positive_integers
   all_are_unequal
   are_relatively_prime
   arithmetic_mean
   binomial_coefficient
   cumulative_products
   cumulative_signed_weights
   cumulative_sums
   cumulative_sums_pairwise
   difference_series
   divide_number_by_ratio
   divisors
   factors
   fraction_to_proper_fraction
   get_shared_numeric_sign
   greatest_common_divisor
   greatest_multiple_less_equal
   greatest_power_of_two_less_equal
   integer_equivalent_number_to_integer
   integer_to_base_k_tuple
   integer_to_binary_string
   is_assignable_integer
   is_dotted_integer
   is_fraction_equivalent_pair
   is_integer_equivalent_expr
   is_integer_equivalent_n_tuple
   is_integer_equivalent_number
   is_integer_equivalent_pair
   is_integer_equivalent_singleton
   is_integer_n_tuple
   is_integer_pair
   is_integer_singleton
   is_n_tuple
   is_negative_integer
   is_nonnegative_integer
   is_nonnegative_integer_equivalent_number
   is_nonnegative_integer_power_of_two
   is_null_tuple
   is_pair
   is_positive_integer
   is_positive_integer_equivalent_number
   is_positive_integer_power_of_two
   is_singleton
   least_common_multiple
   least_multiple_greater_equal
   least_power_of_two_greater_equal
   next_integer_partition
   partition_integer_by_ratio
   partition_integer_into_canonic_parts
   partition_integer_into_halves
   partition_integer_into_parts_less_than_double
   partition_integer_into_units
   remove_powers_of_two
   sign
   weight
   yield_all_compositions_of_integer
   yield_all_partitions_of_integer
   yield_nonreduced_fractions
