.. currentmodule:: abjad.tools.durationtools

Multiplier
==========

.. autoclass:: Multiplier

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
          subgraph cluster_durationtools {
              graph [label=durationtools];
              "abjad.tools.durationtools.Duration.Duration" [color=3,
                  group=2,
                  label=Duration,
                  shape=box];
              "abjad.tools.durationtools.Multiplier.Multiplier" [color=black,
                  fontcolor=white,
                  group=2,
                  label=<<B>Multiplier</B>>,
                  shape=box,
                  style="filled, rounded"];
              "abjad.tools.durationtools.Duration.Duration" -> "abjad.tools.durationtools.Multiplier.Multiplier";
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
              "numbers.Complex" [color=5,
                  group=4,
                  label=Complex,
                  shape=oval,
                  style=bold];
              "numbers.Number" [color=5,
                  group=4,
                  label=Number,
                  shape=box];
              "numbers.Rational" [color=5,
                  group=4,
                  label=Rational,
                  shape=oval,
                  style=bold];
              "numbers.Real" [color=5,
                  group=4,
                  label=Real,
                  shape=oval,
                  style=bold];
              "numbers.Complex" -> "numbers.Real";
              "numbers.Number" -> "numbers.Complex";
              "numbers.Real" -> "numbers.Rational";
          }
          "abjad.tools.abctools.AbjadObject.AbjadObject" -> "abjad.tools.durationtools.Duration.Duration";
          "builtins.object" -> "abjad.tools.abctools.AbjadObject.AbstractBase";
          "builtins.object" -> "numbers.Number";
          "fractions.Fraction" -> "abjad.tools.durationtools.Duration.Duration";
          "numbers.Rational" -> "fractions.Fraction";
      }

Bases
-----

- :py:class:`abjad.tools.durationtools.Duration`

- :py:class:`abjad.tools.abctools.AbjadObject`

- :py:class:`abjad.tools.abctools.AbjadObject.AbstractBase`

- :py:class:`fractions.Fraction`

- :py:class:`numbers.Rational`

- :py:class:`numbers.Real`

- :py:class:`numbers.Complex`

- :py:class:`numbers.Number`

- :py:class:`builtins.object`

.. only:: html

   Attribute summary
   -----------------

   .. autosummary::

      ~abjad.tools.durationtools.Multiplier.Multiplier.conjugate
      ~abjad.tools.durationtools.Multiplier.Multiplier.denominator
      ~abjad.tools.durationtools.Multiplier.Multiplier.dot_count
      ~abjad.tools.durationtools.Multiplier.Multiplier.durations_to_nonreduced_fractions
      ~abjad.tools.durationtools.Multiplier.Multiplier.equal_or_greater_assignable
      ~abjad.tools.durationtools.Multiplier.Multiplier.equal_or_greater_power_of_two
      ~abjad.tools.durationtools.Multiplier.Multiplier.equal_or_lesser_assignable
      ~abjad.tools.durationtools.Multiplier.Multiplier.equal_or_lesser_power_of_two
      ~abjad.tools.durationtools.Multiplier.Multiplier.flag_count
      ~abjad.tools.durationtools.Multiplier.Multiplier.from_decimal
      ~abjad.tools.durationtools.Multiplier.Multiplier.from_float
      ~abjad.tools.durationtools.Multiplier.Multiplier.from_lilypond_duration_string
      ~abjad.tools.durationtools.Multiplier.Multiplier.has_power_of_two_denominator
      ~abjad.tools.durationtools.Multiplier.Multiplier.imag
      ~abjad.tools.durationtools.Multiplier.Multiplier.implied_prolation
      ~abjad.tools.durationtools.Multiplier.Multiplier.is_assignable
      ~abjad.tools.durationtools.Multiplier.Multiplier.is_proper_tuplet_multiplier
      ~abjad.tools.durationtools.Multiplier.Multiplier.is_token
      ~abjad.tools.durationtools.Multiplier.Multiplier.lilypond_duration_string
      ~abjad.tools.durationtools.Multiplier.Multiplier.limit_denominator
      ~abjad.tools.durationtools.Multiplier.Multiplier.numerator
      ~abjad.tools.durationtools.Multiplier.Multiplier.pair
      ~abjad.tools.durationtools.Multiplier.Multiplier.prolation_string
      ~abjad.tools.durationtools.Multiplier.Multiplier.real
      ~abjad.tools.durationtools.Multiplier.Multiplier.reciprocal
      ~abjad.tools.durationtools.Multiplier.Multiplier.to_clock_string
      ~abjad.tools.durationtools.Multiplier.Multiplier.to_score_markup
      ~abjad.tools.durationtools.Multiplier.Multiplier.with_denominator
      ~abjad.tools.durationtools.Multiplier.Multiplier.yield_durations
      ~abjad.tools.durationtools.Multiplier.Multiplier.yield_equivalent_durations
      ~abjad.tools.durationtools.Multiplier.Multiplier.__abs__
      ~abjad.tools.durationtools.Multiplier.Multiplier.__add__
      ~abjad.tools.durationtools.Multiplier.Multiplier.__bool__
      ~abjad.tools.durationtools.Multiplier.Multiplier.__ceil__
      ~abjad.tools.durationtools.Multiplier.Multiplier.__complex__
      ~abjad.tools.durationtools.Multiplier.Multiplier.__copy__
      ~abjad.tools.durationtools.Multiplier.Multiplier.__deepcopy__
      ~abjad.tools.durationtools.Multiplier.Multiplier.__div__
      ~abjad.tools.durationtools.Multiplier.Multiplier.__divmod__
      ~abjad.tools.durationtools.Multiplier.Multiplier.__eq__
      ~abjad.tools.durationtools.Multiplier.Multiplier.__float__
      ~abjad.tools.durationtools.Multiplier.Multiplier.__floor__
      ~abjad.tools.durationtools.Multiplier.Multiplier.__floordiv__
      ~abjad.tools.durationtools.Multiplier.Multiplier.__format__
      ~abjad.tools.durationtools.Multiplier.Multiplier.__ge__
      ~abjad.tools.durationtools.Multiplier.Multiplier.__gt__
      ~abjad.tools.durationtools.Multiplier.Multiplier.__hash__
      ~abjad.tools.durationtools.Multiplier.Multiplier.__le__
      ~abjad.tools.durationtools.Multiplier.Multiplier.__lt__
      ~abjad.tools.durationtools.Multiplier.Multiplier.__mod__
      ~abjad.tools.durationtools.Multiplier.Multiplier.__mul__
      ~abjad.tools.durationtools.Multiplier.Multiplier.__ne__
      ~abjad.tools.durationtools.Multiplier.Multiplier.__neg__
      ~abjad.tools.durationtools.Multiplier.Multiplier.__new__
      ~abjad.tools.durationtools.Multiplier.Multiplier.__pos__
      ~abjad.tools.durationtools.Multiplier.Multiplier.__pow__
      ~abjad.tools.durationtools.Multiplier.Multiplier.__radd__
      ~abjad.tools.durationtools.Multiplier.Multiplier.__rdiv__
      ~abjad.tools.durationtools.Multiplier.Multiplier.__rdivmod__
      ~abjad.tools.durationtools.Multiplier.Multiplier.__repr__
      ~abjad.tools.durationtools.Multiplier.Multiplier.__rfloordiv__
      ~abjad.tools.durationtools.Multiplier.Multiplier.__rmod__
      ~abjad.tools.durationtools.Multiplier.Multiplier.__rmul__
      ~abjad.tools.durationtools.Multiplier.Multiplier.__round__
      ~abjad.tools.durationtools.Multiplier.Multiplier.__rpow__
      ~abjad.tools.durationtools.Multiplier.Multiplier.__rsub__
      ~abjad.tools.durationtools.Multiplier.Multiplier.__rtruediv__
      ~abjad.tools.durationtools.Multiplier.Multiplier.__str__
      ~abjad.tools.durationtools.Multiplier.Multiplier.__sub__
      ~abjad.tools.durationtools.Multiplier.Multiplier.__truediv__
      ~abjad.tools.durationtools.Multiplier.Multiplier.__trunc__

Read-only properties
--------------------

.. only:: html

   .. container:: inherited

      .. autoattribute:: abjad.tools.durationtools.Multiplier.Multiplier.denominator

.. only:: html

   .. container:: inherited

      .. autoattribute:: abjad.tools.durationtools.Multiplier.Multiplier.dot_count

.. only:: html

   .. container:: inherited

      .. autoattribute:: abjad.tools.durationtools.Multiplier.Multiplier.equal_or_greater_assignable

.. only:: html

   .. container:: inherited

      .. autoattribute:: abjad.tools.durationtools.Multiplier.Multiplier.equal_or_greater_power_of_two

.. only:: html

   .. container:: inherited

      .. autoattribute:: abjad.tools.durationtools.Multiplier.Multiplier.equal_or_lesser_assignable

.. only:: html

   .. container:: inherited

      .. autoattribute:: abjad.tools.durationtools.Multiplier.Multiplier.equal_or_lesser_power_of_two

.. only:: html

   .. container:: inherited

      .. autoattribute:: abjad.tools.durationtools.Multiplier.Multiplier.flag_count

.. only:: html

   .. container:: inherited

      .. autoattribute:: abjad.tools.durationtools.Multiplier.Multiplier.has_power_of_two_denominator

.. only:: html

   .. container:: inherited

      .. autoattribute:: abjad.tools.durationtools.Multiplier.Multiplier.imag

.. only:: html

   .. container:: inherited

      .. autoattribute:: abjad.tools.durationtools.Multiplier.Multiplier.implied_prolation

.. only:: html

   .. container:: inherited

      .. autoattribute:: abjad.tools.durationtools.Multiplier.Multiplier.is_assignable

.. autoattribute:: abjad.tools.durationtools.Multiplier.Multiplier.is_proper_tuplet_multiplier

.. only:: html

   .. container:: inherited

      .. autoattribute:: abjad.tools.durationtools.Multiplier.Multiplier.lilypond_duration_string

.. only:: html

   .. container:: inherited

      .. autoattribute:: abjad.tools.durationtools.Multiplier.Multiplier.numerator

.. only:: html

   .. container:: inherited

      .. autoattribute:: abjad.tools.durationtools.Multiplier.Multiplier.pair

.. only:: html

   .. container:: inherited

      .. autoattribute:: abjad.tools.durationtools.Multiplier.Multiplier.prolation_string

.. only:: html

   .. container:: inherited

      .. autoattribute:: abjad.tools.durationtools.Multiplier.Multiplier.real

.. only:: html

   .. container:: inherited

      .. autoattribute:: abjad.tools.durationtools.Multiplier.Multiplier.reciprocal

Methods
-------

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.durationtools.Multiplier.Multiplier.conjugate

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.durationtools.Multiplier.Multiplier.limit_denominator

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.durationtools.Multiplier.Multiplier.to_clock_string

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.durationtools.Multiplier.Multiplier.to_score_markup

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.durationtools.Multiplier.Multiplier.with_denominator

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.durationtools.Multiplier.Multiplier.yield_equivalent_durations

Class & static methods
----------------------

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.durationtools.Multiplier.Multiplier.durations_to_nonreduced_fractions

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.durationtools.Multiplier.Multiplier.from_decimal

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.durationtools.Multiplier.Multiplier.from_float

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.durationtools.Multiplier.Multiplier.from_lilypond_duration_string

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.durationtools.Multiplier.Multiplier.is_token

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.durationtools.Multiplier.Multiplier.yield_durations

Special methods
---------------

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.durationtools.Multiplier.Multiplier.__abs__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.durationtools.Multiplier.Multiplier.__add__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.durationtools.Multiplier.Multiplier.__bool__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.durationtools.Multiplier.Multiplier.__ceil__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.durationtools.Multiplier.Multiplier.__complex__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.durationtools.Multiplier.Multiplier.__copy__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.durationtools.Multiplier.Multiplier.__deepcopy__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.durationtools.Multiplier.Multiplier.__div__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.durationtools.Multiplier.Multiplier.__divmod__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.durationtools.Multiplier.Multiplier.__eq__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.durationtools.Multiplier.Multiplier.__float__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.durationtools.Multiplier.Multiplier.__floor__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.durationtools.Multiplier.Multiplier.__floordiv__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.durationtools.Multiplier.Multiplier.__format__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.durationtools.Multiplier.Multiplier.__ge__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.durationtools.Multiplier.Multiplier.__gt__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.durationtools.Multiplier.Multiplier.__hash__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.durationtools.Multiplier.Multiplier.__le__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.durationtools.Multiplier.Multiplier.__lt__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.durationtools.Multiplier.Multiplier.__mod__

.. automethod:: abjad.tools.durationtools.Multiplier.Multiplier.__mul__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.durationtools.Multiplier.Multiplier.__ne__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.durationtools.Multiplier.Multiplier.__neg__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.durationtools.Multiplier.Multiplier.__new__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.durationtools.Multiplier.Multiplier.__pos__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.durationtools.Multiplier.Multiplier.__pow__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.durationtools.Multiplier.Multiplier.__radd__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.durationtools.Multiplier.Multiplier.__rdiv__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.durationtools.Multiplier.Multiplier.__rdivmod__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.durationtools.Multiplier.Multiplier.__repr__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.durationtools.Multiplier.Multiplier.__rfloordiv__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.durationtools.Multiplier.Multiplier.__rmod__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.durationtools.Multiplier.Multiplier.__rmul__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.durationtools.Multiplier.Multiplier.__round__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.durationtools.Multiplier.Multiplier.__rpow__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.durationtools.Multiplier.Multiplier.__rsub__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.durationtools.Multiplier.Multiplier.__rtruediv__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.durationtools.Multiplier.Multiplier.__str__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.durationtools.Multiplier.Multiplier.__sub__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.durationtools.Multiplier.Multiplier.__truediv__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.durationtools.Multiplier.Multiplier.__trunc__
