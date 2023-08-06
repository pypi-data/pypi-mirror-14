.. currentmodule:: abjad.tools.durationtools

Duration
========

.. autoclass:: Duration

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
              "abjad.tools.durationtools.Duration.Duration" [color=black,
                  fontcolor=white,
                  group=2,
                  label=<<B>Duration</B>>,
                  shape=box,
                  style="filled, rounded"];
              "abjad.tools.durationtools.Multiplier.Multiplier" [color=3,
                  group=2,
                  label=Multiplier,
                  shape=box];
              "abjad.tools.durationtools.Offset.Offset" [color=3,
                  group=2,
                  label=Offset,
                  shape=box];
              "abjad.tools.durationtools.Duration.Duration" -> "abjad.tools.durationtools.Multiplier.Multiplier";
              "abjad.tools.durationtools.Duration.Duration" -> "abjad.tools.durationtools.Offset.Offset";
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

      ~abjad.tools.durationtools.Duration.Duration.conjugate
      ~abjad.tools.durationtools.Duration.Duration.denominator
      ~abjad.tools.durationtools.Duration.Duration.dot_count
      ~abjad.tools.durationtools.Duration.Duration.durations_to_nonreduced_fractions
      ~abjad.tools.durationtools.Duration.Duration.equal_or_greater_assignable
      ~abjad.tools.durationtools.Duration.Duration.equal_or_greater_power_of_two
      ~abjad.tools.durationtools.Duration.Duration.equal_or_lesser_assignable
      ~abjad.tools.durationtools.Duration.Duration.equal_or_lesser_power_of_two
      ~abjad.tools.durationtools.Duration.Duration.flag_count
      ~abjad.tools.durationtools.Duration.Duration.from_decimal
      ~abjad.tools.durationtools.Duration.Duration.from_float
      ~abjad.tools.durationtools.Duration.Duration.from_lilypond_duration_string
      ~abjad.tools.durationtools.Duration.Duration.has_power_of_two_denominator
      ~abjad.tools.durationtools.Duration.Duration.imag
      ~abjad.tools.durationtools.Duration.Duration.implied_prolation
      ~abjad.tools.durationtools.Duration.Duration.is_assignable
      ~abjad.tools.durationtools.Duration.Duration.is_token
      ~abjad.tools.durationtools.Duration.Duration.lilypond_duration_string
      ~abjad.tools.durationtools.Duration.Duration.limit_denominator
      ~abjad.tools.durationtools.Duration.Duration.numerator
      ~abjad.tools.durationtools.Duration.Duration.pair
      ~abjad.tools.durationtools.Duration.Duration.prolation_string
      ~abjad.tools.durationtools.Duration.Duration.real
      ~abjad.tools.durationtools.Duration.Duration.reciprocal
      ~abjad.tools.durationtools.Duration.Duration.to_clock_string
      ~abjad.tools.durationtools.Duration.Duration.to_score_markup
      ~abjad.tools.durationtools.Duration.Duration.with_denominator
      ~abjad.tools.durationtools.Duration.Duration.yield_durations
      ~abjad.tools.durationtools.Duration.Duration.yield_equivalent_durations
      ~abjad.tools.durationtools.Duration.Duration.__abs__
      ~abjad.tools.durationtools.Duration.Duration.__add__
      ~abjad.tools.durationtools.Duration.Duration.__bool__
      ~abjad.tools.durationtools.Duration.Duration.__ceil__
      ~abjad.tools.durationtools.Duration.Duration.__complex__
      ~abjad.tools.durationtools.Duration.Duration.__copy__
      ~abjad.tools.durationtools.Duration.Duration.__deepcopy__
      ~abjad.tools.durationtools.Duration.Duration.__div__
      ~abjad.tools.durationtools.Duration.Duration.__divmod__
      ~abjad.tools.durationtools.Duration.Duration.__eq__
      ~abjad.tools.durationtools.Duration.Duration.__float__
      ~abjad.tools.durationtools.Duration.Duration.__floor__
      ~abjad.tools.durationtools.Duration.Duration.__floordiv__
      ~abjad.tools.durationtools.Duration.Duration.__format__
      ~abjad.tools.durationtools.Duration.Duration.__ge__
      ~abjad.tools.durationtools.Duration.Duration.__gt__
      ~abjad.tools.durationtools.Duration.Duration.__hash__
      ~abjad.tools.durationtools.Duration.Duration.__le__
      ~abjad.tools.durationtools.Duration.Duration.__lt__
      ~abjad.tools.durationtools.Duration.Duration.__mod__
      ~abjad.tools.durationtools.Duration.Duration.__mul__
      ~abjad.tools.durationtools.Duration.Duration.__ne__
      ~abjad.tools.durationtools.Duration.Duration.__neg__
      ~abjad.tools.durationtools.Duration.Duration.__new__
      ~abjad.tools.durationtools.Duration.Duration.__pos__
      ~abjad.tools.durationtools.Duration.Duration.__pow__
      ~abjad.tools.durationtools.Duration.Duration.__radd__
      ~abjad.tools.durationtools.Duration.Duration.__rdiv__
      ~abjad.tools.durationtools.Duration.Duration.__rdivmod__
      ~abjad.tools.durationtools.Duration.Duration.__repr__
      ~abjad.tools.durationtools.Duration.Duration.__rfloordiv__
      ~abjad.tools.durationtools.Duration.Duration.__rmod__
      ~abjad.tools.durationtools.Duration.Duration.__rmul__
      ~abjad.tools.durationtools.Duration.Duration.__round__
      ~abjad.tools.durationtools.Duration.Duration.__rpow__
      ~abjad.tools.durationtools.Duration.Duration.__rsub__
      ~abjad.tools.durationtools.Duration.Duration.__rtruediv__
      ~abjad.tools.durationtools.Duration.Duration.__str__
      ~abjad.tools.durationtools.Duration.Duration.__sub__
      ~abjad.tools.durationtools.Duration.Duration.__truediv__
      ~abjad.tools.durationtools.Duration.Duration.__trunc__

Read-only properties
--------------------

.. only:: html

   .. container:: inherited

      .. autoattribute:: abjad.tools.durationtools.Duration.Duration.denominator

.. autoattribute:: abjad.tools.durationtools.Duration.Duration.dot_count

.. autoattribute:: abjad.tools.durationtools.Duration.Duration.equal_or_greater_assignable

.. autoattribute:: abjad.tools.durationtools.Duration.Duration.equal_or_greater_power_of_two

.. autoattribute:: abjad.tools.durationtools.Duration.Duration.equal_or_lesser_assignable

.. autoattribute:: abjad.tools.durationtools.Duration.Duration.equal_or_lesser_power_of_two

.. autoattribute:: abjad.tools.durationtools.Duration.Duration.flag_count

.. autoattribute:: abjad.tools.durationtools.Duration.Duration.has_power_of_two_denominator

.. only:: html

   .. container:: inherited

      .. autoattribute:: abjad.tools.durationtools.Duration.Duration.imag

.. autoattribute:: abjad.tools.durationtools.Duration.Duration.implied_prolation

.. autoattribute:: abjad.tools.durationtools.Duration.Duration.is_assignable

.. autoattribute:: abjad.tools.durationtools.Duration.Duration.lilypond_duration_string

.. only:: html

   .. container:: inherited

      .. autoattribute:: abjad.tools.durationtools.Duration.Duration.numerator

.. autoattribute:: abjad.tools.durationtools.Duration.Duration.pair

.. autoattribute:: abjad.tools.durationtools.Duration.Duration.prolation_string

.. only:: html

   .. container:: inherited

      .. autoattribute:: abjad.tools.durationtools.Duration.Duration.real

.. autoattribute:: abjad.tools.durationtools.Duration.Duration.reciprocal

Methods
-------

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.durationtools.Duration.Duration.conjugate

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.durationtools.Duration.Duration.limit_denominator

.. automethod:: abjad.tools.durationtools.Duration.Duration.to_clock_string

.. automethod:: abjad.tools.durationtools.Duration.Duration.to_score_markup

.. automethod:: abjad.tools.durationtools.Duration.Duration.with_denominator

.. automethod:: abjad.tools.durationtools.Duration.Duration.yield_equivalent_durations

Class & static methods
----------------------

.. automethod:: abjad.tools.durationtools.Duration.Duration.durations_to_nonreduced_fractions

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.durationtools.Duration.Duration.from_decimal

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.durationtools.Duration.Duration.from_float

.. automethod:: abjad.tools.durationtools.Duration.Duration.from_lilypond_duration_string

.. automethod:: abjad.tools.durationtools.Duration.Duration.is_token

.. automethod:: abjad.tools.durationtools.Duration.Duration.yield_durations

Special methods
---------------

.. automethod:: abjad.tools.durationtools.Duration.Duration.__abs__

.. automethod:: abjad.tools.durationtools.Duration.Duration.__add__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.durationtools.Duration.Duration.__bool__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.durationtools.Duration.Duration.__ceil__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.durationtools.Duration.Duration.__complex__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.durationtools.Duration.Duration.__copy__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.durationtools.Duration.Duration.__deepcopy__

.. automethod:: abjad.tools.durationtools.Duration.Duration.__div__

.. automethod:: abjad.tools.durationtools.Duration.Duration.__divmod__

.. automethod:: abjad.tools.durationtools.Duration.Duration.__eq__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.durationtools.Duration.Duration.__float__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.durationtools.Duration.Duration.__floor__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.durationtools.Duration.Duration.__floordiv__

.. automethod:: abjad.tools.durationtools.Duration.Duration.__format__

.. automethod:: abjad.tools.durationtools.Duration.Duration.__ge__

.. automethod:: abjad.tools.durationtools.Duration.Duration.__gt__

.. automethod:: abjad.tools.durationtools.Duration.Duration.__hash__

.. automethod:: abjad.tools.durationtools.Duration.Duration.__le__

.. automethod:: abjad.tools.durationtools.Duration.Duration.__lt__

.. automethod:: abjad.tools.durationtools.Duration.Duration.__mod__

.. automethod:: abjad.tools.durationtools.Duration.Duration.__mul__

.. automethod:: abjad.tools.durationtools.Duration.Duration.__ne__

.. automethod:: abjad.tools.durationtools.Duration.Duration.__neg__

.. automethod:: abjad.tools.durationtools.Duration.Duration.__new__

.. automethod:: abjad.tools.durationtools.Duration.Duration.__pos__

.. automethod:: abjad.tools.durationtools.Duration.Duration.__pow__

.. automethod:: abjad.tools.durationtools.Duration.Duration.__radd__

.. automethod:: abjad.tools.durationtools.Duration.Duration.__rdiv__

.. automethod:: abjad.tools.durationtools.Duration.Duration.__rdivmod__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.durationtools.Duration.Duration.__repr__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.durationtools.Duration.Duration.__rfloordiv__

.. automethod:: abjad.tools.durationtools.Duration.Duration.__rmod__

.. automethod:: abjad.tools.durationtools.Duration.Duration.__rmul__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.durationtools.Duration.Duration.__round__

.. automethod:: abjad.tools.durationtools.Duration.Duration.__rpow__

.. automethod:: abjad.tools.durationtools.Duration.Duration.__rsub__

.. automethod:: abjad.tools.durationtools.Duration.Duration.__rtruediv__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.durationtools.Duration.Duration.__str__

.. automethod:: abjad.tools.durationtools.Duration.Duration.__sub__

.. automethod:: abjad.tools.durationtools.Duration.Duration.__truediv__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.durationtools.Duration.Duration.__trunc__
