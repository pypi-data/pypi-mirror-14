.. currentmodule:: abjad.tools.mathtools

NonreducedFraction
==================

.. autoclass:: NonreducedFraction

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
              "abjad.tools.durationtools.Division.Division" [color=3,
                  group=2,
                  label=Division,
                  shape=box];
          }
          subgraph cluster_mathtools {
              graph [label=mathtools];
              "abjad.tools.mathtools.NonreducedFraction.NonreducedFraction" [color=black,
                  fontcolor=white,
                  group=4,
                  label=<<B>NonreducedFraction</B>>,
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
          "abjad.tools.abctools.AbjadObject.AbjadObject" -> "abjad.tools.mathtools.NonreducedFraction.NonreducedFraction";
          "abjad.tools.mathtools.NonreducedFraction.NonreducedFraction" -> "abjad.tools.durationtools.Division.Division";
          "builtins.object" -> "abjad.tools.abctools.AbjadObject.AbstractBase";
          "builtins.object" -> "numbers.Number";
          "fractions.Fraction" -> "abjad.tools.mathtools.NonreducedFraction.NonreducedFraction";
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

      ~abjad.tools.mathtools.NonreducedFraction.NonreducedFraction.conjugate
      ~abjad.tools.mathtools.NonreducedFraction.NonreducedFraction.denominator
      ~abjad.tools.mathtools.NonreducedFraction.NonreducedFraction.from_decimal
      ~abjad.tools.mathtools.NonreducedFraction.NonreducedFraction.from_float
      ~abjad.tools.mathtools.NonreducedFraction.NonreducedFraction.imag
      ~abjad.tools.mathtools.NonreducedFraction.NonreducedFraction.limit_denominator
      ~abjad.tools.mathtools.NonreducedFraction.NonreducedFraction.multiply_with_cross_cancelation
      ~abjad.tools.mathtools.NonreducedFraction.NonreducedFraction.multiply_with_numerator_preservation
      ~abjad.tools.mathtools.NonreducedFraction.NonreducedFraction.multiply_without_reducing
      ~abjad.tools.mathtools.NonreducedFraction.NonreducedFraction.numerator
      ~abjad.tools.mathtools.NonreducedFraction.NonreducedFraction.pair
      ~abjad.tools.mathtools.NonreducedFraction.NonreducedFraction.real
      ~abjad.tools.mathtools.NonreducedFraction.NonreducedFraction.reduce
      ~abjad.tools.mathtools.NonreducedFraction.NonreducedFraction.with_denominator
      ~abjad.tools.mathtools.NonreducedFraction.NonreducedFraction.with_multiple_of_denominator
      ~abjad.tools.mathtools.NonreducedFraction.NonreducedFraction.__abs__
      ~abjad.tools.mathtools.NonreducedFraction.NonreducedFraction.__add__
      ~abjad.tools.mathtools.NonreducedFraction.NonreducedFraction.__bool__
      ~abjad.tools.mathtools.NonreducedFraction.NonreducedFraction.__ceil__
      ~abjad.tools.mathtools.NonreducedFraction.NonreducedFraction.__complex__
      ~abjad.tools.mathtools.NonreducedFraction.NonreducedFraction.__copy__
      ~abjad.tools.mathtools.NonreducedFraction.NonreducedFraction.__deepcopy__
      ~abjad.tools.mathtools.NonreducedFraction.NonreducedFraction.__div__
      ~abjad.tools.mathtools.NonreducedFraction.NonreducedFraction.__divmod__
      ~abjad.tools.mathtools.NonreducedFraction.NonreducedFraction.__eq__
      ~abjad.tools.mathtools.NonreducedFraction.NonreducedFraction.__float__
      ~abjad.tools.mathtools.NonreducedFraction.NonreducedFraction.__floor__
      ~abjad.tools.mathtools.NonreducedFraction.NonreducedFraction.__floordiv__
      ~abjad.tools.mathtools.NonreducedFraction.NonreducedFraction.__format__
      ~abjad.tools.mathtools.NonreducedFraction.NonreducedFraction.__ge__
      ~abjad.tools.mathtools.NonreducedFraction.NonreducedFraction.__gt__
      ~abjad.tools.mathtools.NonreducedFraction.NonreducedFraction.__hash__
      ~abjad.tools.mathtools.NonreducedFraction.NonreducedFraction.__le__
      ~abjad.tools.mathtools.NonreducedFraction.NonreducedFraction.__lt__
      ~abjad.tools.mathtools.NonreducedFraction.NonreducedFraction.__mod__
      ~abjad.tools.mathtools.NonreducedFraction.NonreducedFraction.__mul__
      ~abjad.tools.mathtools.NonreducedFraction.NonreducedFraction.__ne__
      ~abjad.tools.mathtools.NonreducedFraction.NonreducedFraction.__neg__
      ~abjad.tools.mathtools.NonreducedFraction.NonreducedFraction.__new__
      ~abjad.tools.mathtools.NonreducedFraction.NonreducedFraction.__pos__
      ~abjad.tools.mathtools.NonreducedFraction.NonreducedFraction.__pow__
      ~abjad.tools.mathtools.NonreducedFraction.NonreducedFraction.__radd__
      ~abjad.tools.mathtools.NonreducedFraction.NonreducedFraction.__rdiv__
      ~abjad.tools.mathtools.NonreducedFraction.NonreducedFraction.__rdivmod__
      ~abjad.tools.mathtools.NonreducedFraction.NonreducedFraction.__repr__
      ~abjad.tools.mathtools.NonreducedFraction.NonreducedFraction.__rfloordiv__
      ~abjad.tools.mathtools.NonreducedFraction.NonreducedFraction.__rmod__
      ~abjad.tools.mathtools.NonreducedFraction.NonreducedFraction.__rmul__
      ~abjad.tools.mathtools.NonreducedFraction.NonreducedFraction.__round__
      ~abjad.tools.mathtools.NonreducedFraction.NonreducedFraction.__rpow__
      ~abjad.tools.mathtools.NonreducedFraction.NonreducedFraction.__rsub__
      ~abjad.tools.mathtools.NonreducedFraction.NonreducedFraction.__rtruediv__
      ~abjad.tools.mathtools.NonreducedFraction.NonreducedFraction.__str__
      ~abjad.tools.mathtools.NonreducedFraction.NonreducedFraction.__sub__
      ~abjad.tools.mathtools.NonreducedFraction.NonreducedFraction.__truediv__
      ~abjad.tools.mathtools.NonreducedFraction.NonreducedFraction.__trunc__

Read-only properties
--------------------

.. autoattribute:: abjad.tools.mathtools.NonreducedFraction.NonreducedFraction.denominator

.. autoattribute:: abjad.tools.mathtools.NonreducedFraction.NonreducedFraction.imag

.. autoattribute:: abjad.tools.mathtools.NonreducedFraction.NonreducedFraction.numerator

.. autoattribute:: abjad.tools.mathtools.NonreducedFraction.NonreducedFraction.pair

.. autoattribute:: abjad.tools.mathtools.NonreducedFraction.NonreducedFraction.real

Methods
-------

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.mathtools.NonreducedFraction.NonreducedFraction.conjugate

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.mathtools.NonreducedFraction.NonreducedFraction.limit_denominator

.. automethod:: abjad.tools.mathtools.NonreducedFraction.NonreducedFraction.multiply_with_cross_cancelation

.. automethod:: abjad.tools.mathtools.NonreducedFraction.NonreducedFraction.multiply_with_numerator_preservation

.. automethod:: abjad.tools.mathtools.NonreducedFraction.NonreducedFraction.multiply_without_reducing

.. automethod:: abjad.tools.mathtools.NonreducedFraction.NonreducedFraction.reduce

.. automethod:: abjad.tools.mathtools.NonreducedFraction.NonreducedFraction.with_denominator

.. automethod:: abjad.tools.mathtools.NonreducedFraction.NonreducedFraction.with_multiple_of_denominator

Class & static methods
----------------------

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.mathtools.NonreducedFraction.NonreducedFraction.from_decimal

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.mathtools.NonreducedFraction.NonreducedFraction.from_float

Special methods
---------------

.. automethod:: abjad.tools.mathtools.NonreducedFraction.NonreducedFraction.__abs__

.. automethod:: abjad.tools.mathtools.NonreducedFraction.NonreducedFraction.__add__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.mathtools.NonreducedFraction.NonreducedFraction.__bool__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.mathtools.NonreducedFraction.NonreducedFraction.__ceil__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.mathtools.NonreducedFraction.NonreducedFraction.__complex__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.mathtools.NonreducedFraction.NonreducedFraction.__copy__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.mathtools.NonreducedFraction.NonreducedFraction.__deepcopy__

.. automethod:: abjad.tools.mathtools.NonreducedFraction.NonreducedFraction.__div__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.mathtools.NonreducedFraction.NonreducedFraction.__divmod__

.. automethod:: abjad.tools.mathtools.NonreducedFraction.NonreducedFraction.__eq__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.mathtools.NonreducedFraction.NonreducedFraction.__float__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.mathtools.NonreducedFraction.NonreducedFraction.__floor__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.mathtools.NonreducedFraction.NonreducedFraction.__floordiv__

.. automethod:: abjad.tools.mathtools.NonreducedFraction.NonreducedFraction.__format__

.. automethod:: abjad.tools.mathtools.NonreducedFraction.NonreducedFraction.__ge__

.. automethod:: abjad.tools.mathtools.NonreducedFraction.NonreducedFraction.__gt__

.. automethod:: abjad.tools.mathtools.NonreducedFraction.NonreducedFraction.__hash__

.. automethod:: abjad.tools.mathtools.NonreducedFraction.NonreducedFraction.__le__

.. automethod:: abjad.tools.mathtools.NonreducedFraction.NonreducedFraction.__lt__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.mathtools.NonreducedFraction.NonreducedFraction.__mod__

.. automethod:: abjad.tools.mathtools.NonreducedFraction.NonreducedFraction.__mul__

.. automethod:: abjad.tools.mathtools.NonreducedFraction.NonreducedFraction.__ne__

.. automethod:: abjad.tools.mathtools.NonreducedFraction.NonreducedFraction.__neg__

.. automethod:: abjad.tools.mathtools.NonreducedFraction.NonreducedFraction.__new__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.mathtools.NonreducedFraction.NonreducedFraction.__pos__

.. automethod:: abjad.tools.mathtools.NonreducedFraction.NonreducedFraction.__pow__

.. automethod:: abjad.tools.mathtools.NonreducedFraction.NonreducedFraction.__radd__

.. automethod:: abjad.tools.mathtools.NonreducedFraction.NonreducedFraction.__rdiv__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.mathtools.NonreducedFraction.NonreducedFraction.__rdivmod__

.. automethod:: abjad.tools.mathtools.NonreducedFraction.NonreducedFraction.__repr__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.mathtools.NonreducedFraction.NonreducedFraction.__rfloordiv__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.mathtools.NonreducedFraction.NonreducedFraction.__rmod__

.. automethod:: abjad.tools.mathtools.NonreducedFraction.NonreducedFraction.__rmul__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.mathtools.NonreducedFraction.NonreducedFraction.__round__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.mathtools.NonreducedFraction.NonreducedFraction.__rpow__

.. automethod:: abjad.tools.mathtools.NonreducedFraction.NonreducedFraction.__rsub__

.. automethod:: abjad.tools.mathtools.NonreducedFraction.NonreducedFraction.__rtruediv__

.. automethod:: abjad.tools.mathtools.NonreducedFraction.NonreducedFraction.__str__

.. automethod:: abjad.tools.mathtools.NonreducedFraction.NonreducedFraction.__sub__

.. automethod:: abjad.tools.mathtools.NonreducedFraction.NonreducedFraction.__truediv__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.mathtools.NonreducedFraction.NonreducedFraction.__trunc__
