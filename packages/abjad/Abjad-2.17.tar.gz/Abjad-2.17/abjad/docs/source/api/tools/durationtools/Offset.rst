.. currentmodule:: abjad.tools.durationtools

Offset
======

.. autoclass:: Offset

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
              "abjad.tools.durationtools.Offset.Offset" [color=black,
                  fontcolor=white,
                  group=2,
                  label=<<B>Offset</B>>,
                  shape=box,
                  style="filled, rounded"];
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

      ~abjad.tools.durationtools.Offset.Offset.conjugate
      ~abjad.tools.durationtools.Offset.Offset.denominator
      ~abjad.tools.durationtools.Offset.Offset.dot_count
      ~abjad.tools.durationtools.Offset.Offset.durations_to_nonreduced_fractions
      ~abjad.tools.durationtools.Offset.Offset.equal_or_greater_assignable
      ~abjad.tools.durationtools.Offset.Offset.equal_or_greater_power_of_two
      ~abjad.tools.durationtools.Offset.Offset.equal_or_lesser_assignable
      ~abjad.tools.durationtools.Offset.Offset.equal_or_lesser_power_of_two
      ~abjad.tools.durationtools.Offset.Offset.flag_count
      ~abjad.tools.durationtools.Offset.Offset.from_decimal
      ~abjad.tools.durationtools.Offset.Offset.from_float
      ~abjad.tools.durationtools.Offset.Offset.from_lilypond_duration_string
      ~abjad.tools.durationtools.Offset.Offset.has_power_of_two_denominator
      ~abjad.tools.durationtools.Offset.Offset.imag
      ~abjad.tools.durationtools.Offset.Offset.implied_prolation
      ~abjad.tools.durationtools.Offset.Offset.is_assignable
      ~abjad.tools.durationtools.Offset.Offset.is_token
      ~abjad.tools.durationtools.Offset.Offset.lilypond_duration_string
      ~abjad.tools.durationtools.Offset.Offset.limit_denominator
      ~abjad.tools.durationtools.Offset.Offset.numerator
      ~abjad.tools.durationtools.Offset.Offset.pair
      ~abjad.tools.durationtools.Offset.Offset.prolation_string
      ~abjad.tools.durationtools.Offset.Offset.real
      ~abjad.tools.durationtools.Offset.Offset.reciprocal
      ~abjad.tools.durationtools.Offset.Offset.to_clock_string
      ~abjad.tools.durationtools.Offset.Offset.to_score_markup
      ~abjad.tools.durationtools.Offset.Offset.with_denominator
      ~abjad.tools.durationtools.Offset.Offset.yield_durations
      ~abjad.tools.durationtools.Offset.Offset.yield_equivalent_durations
      ~abjad.tools.durationtools.Offset.Offset.__abs__
      ~abjad.tools.durationtools.Offset.Offset.__add__
      ~abjad.tools.durationtools.Offset.Offset.__bool__
      ~abjad.tools.durationtools.Offset.Offset.__ceil__
      ~abjad.tools.durationtools.Offset.Offset.__complex__
      ~abjad.tools.durationtools.Offset.Offset.__copy__
      ~abjad.tools.durationtools.Offset.Offset.__deepcopy__
      ~abjad.tools.durationtools.Offset.Offset.__div__
      ~abjad.tools.durationtools.Offset.Offset.__divmod__
      ~abjad.tools.durationtools.Offset.Offset.__eq__
      ~abjad.tools.durationtools.Offset.Offset.__float__
      ~abjad.tools.durationtools.Offset.Offset.__floor__
      ~abjad.tools.durationtools.Offset.Offset.__floordiv__
      ~abjad.tools.durationtools.Offset.Offset.__format__
      ~abjad.tools.durationtools.Offset.Offset.__ge__
      ~abjad.tools.durationtools.Offset.Offset.__gt__
      ~abjad.tools.durationtools.Offset.Offset.__hash__
      ~abjad.tools.durationtools.Offset.Offset.__le__
      ~abjad.tools.durationtools.Offset.Offset.__lt__
      ~abjad.tools.durationtools.Offset.Offset.__mod__
      ~abjad.tools.durationtools.Offset.Offset.__mul__
      ~abjad.tools.durationtools.Offset.Offset.__ne__
      ~abjad.tools.durationtools.Offset.Offset.__neg__
      ~abjad.tools.durationtools.Offset.Offset.__new__
      ~abjad.tools.durationtools.Offset.Offset.__pos__
      ~abjad.tools.durationtools.Offset.Offset.__pow__
      ~abjad.tools.durationtools.Offset.Offset.__radd__
      ~abjad.tools.durationtools.Offset.Offset.__rdiv__
      ~abjad.tools.durationtools.Offset.Offset.__rdivmod__
      ~abjad.tools.durationtools.Offset.Offset.__repr__
      ~abjad.tools.durationtools.Offset.Offset.__rfloordiv__
      ~abjad.tools.durationtools.Offset.Offset.__rmod__
      ~abjad.tools.durationtools.Offset.Offset.__rmul__
      ~abjad.tools.durationtools.Offset.Offset.__round__
      ~abjad.tools.durationtools.Offset.Offset.__rpow__
      ~abjad.tools.durationtools.Offset.Offset.__rsub__
      ~abjad.tools.durationtools.Offset.Offset.__rtruediv__
      ~abjad.tools.durationtools.Offset.Offset.__str__
      ~abjad.tools.durationtools.Offset.Offset.__sub__
      ~abjad.tools.durationtools.Offset.Offset.__truediv__
      ~abjad.tools.durationtools.Offset.Offset.__trunc__

Read-only properties
--------------------

.. only:: html

   .. container:: inherited

      .. autoattribute:: abjad.tools.durationtools.Offset.Offset.denominator

.. only:: html

   .. container:: inherited

      .. autoattribute:: abjad.tools.durationtools.Offset.Offset.dot_count

.. only:: html

   .. container:: inherited

      .. autoattribute:: abjad.tools.durationtools.Offset.Offset.equal_or_greater_assignable

.. only:: html

   .. container:: inherited

      .. autoattribute:: abjad.tools.durationtools.Offset.Offset.equal_or_greater_power_of_two

.. only:: html

   .. container:: inherited

      .. autoattribute:: abjad.tools.durationtools.Offset.Offset.equal_or_lesser_assignable

.. only:: html

   .. container:: inherited

      .. autoattribute:: abjad.tools.durationtools.Offset.Offset.equal_or_lesser_power_of_two

.. only:: html

   .. container:: inherited

      .. autoattribute:: abjad.tools.durationtools.Offset.Offset.flag_count

.. only:: html

   .. container:: inherited

      .. autoattribute:: abjad.tools.durationtools.Offset.Offset.has_power_of_two_denominator

.. only:: html

   .. container:: inherited

      .. autoattribute:: abjad.tools.durationtools.Offset.Offset.imag

.. only:: html

   .. container:: inherited

      .. autoattribute:: abjad.tools.durationtools.Offset.Offset.implied_prolation

.. only:: html

   .. container:: inherited

      .. autoattribute:: abjad.tools.durationtools.Offset.Offset.is_assignable

.. only:: html

   .. container:: inherited

      .. autoattribute:: abjad.tools.durationtools.Offset.Offset.lilypond_duration_string

.. only:: html

   .. container:: inherited

      .. autoattribute:: abjad.tools.durationtools.Offset.Offset.numerator

.. only:: html

   .. container:: inherited

      .. autoattribute:: abjad.tools.durationtools.Offset.Offset.pair

.. only:: html

   .. container:: inherited

      .. autoattribute:: abjad.tools.durationtools.Offset.Offset.prolation_string

.. only:: html

   .. container:: inherited

      .. autoattribute:: abjad.tools.durationtools.Offset.Offset.real

.. only:: html

   .. container:: inherited

      .. autoattribute:: abjad.tools.durationtools.Offset.Offset.reciprocal

Methods
-------

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.durationtools.Offset.Offset.conjugate

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.durationtools.Offset.Offset.limit_denominator

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.durationtools.Offset.Offset.to_clock_string

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.durationtools.Offset.Offset.to_score_markup

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.durationtools.Offset.Offset.with_denominator

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.durationtools.Offset.Offset.yield_equivalent_durations

Class & static methods
----------------------

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.durationtools.Offset.Offset.durations_to_nonreduced_fractions

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.durationtools.Offset.Offset.from_decimal

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.durationtools.Offset.Offset.from_float

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.durationtools.Offset.Offset.from_lilypond_duration_string

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.durationtools.Offset.Offset.is_token

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.durationtools.Offset.Offset.yield_durations

Special methods
---------------

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.durationtools.Offset.Offset.__abs__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.durationtools.Offset.Offset.__add__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.durationtools.Offset.Offset.__bool__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.durationtools.Offset.Offset.__ceil__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.durationtools.Offset.Offset.__complex__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.durationtools.Offset.Offset.__copy__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.durationtools.Offset.Offset.__deepcopy__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.durationtools.Offset.Offset.__div__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.durationtools.Offset.Offset.__divmod__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.durationtools.Offset.Offset.__eq__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.durationtools.Offset.Offset.__float__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.durationtools.Offset.Offset.__floor__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.durationtools.Offset.Offset.__floordiv__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.durationtools.Offset.Offset.__format__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.durationtools.Offset.Offset.__ge__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.durationtools.Offset.Offset.__gt__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.durationtools.Offset.Offset.__hash__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.durationtools.Offset.Offset.__le__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.durationtools.Offset.Offset.__lt__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.durationtools.Offset.Offset.__mod__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.durationtools.Offset.Offset.__mul__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.durationtools.Offset.Offset.__ne__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.durationtools.Offset.Offset.__neg__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.durationtools.Offset.Offset.__new__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.durationtools.Offset.Offset.__pos__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.durationtools.Offset.Offset.__pow__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.durationtools.Offset.Offset.__radd__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.durationtools.Offset.Offset.__rdiv__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.durationtools.Offset.Offset.__rdivmod__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.durationtools.Offset.Offset.__repr__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.durationtools.Offset.Offset.__rfloordiv__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.durationtools.Offset.Offset.__rmod__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.durationtools.Offset.Offset.__rmul__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.durationtools.Offset.Offset.__round__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.durationtools.Offset.Offset.__rpow__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.durationtools.Offset.Offset.__rsub__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.durationtools.Offset.Offset.__rtruediv__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.durationtools.Offset.Offset.__str__

.. automethod:: abjad.tools.durationtools.Offset.Offset.__sub__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.durationtools.Offset.Offset.__truediv__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.durationtools.Offset.Offset.__trunc__
