.. currentmodule:: abjad.tools.durationtools

Division
========

.. autoclass:: Division

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
              "abjad.tools.durationtools.Division.Division" [color=black,
                  fontcolor=white,
                  group=2,
                  label=<<B>Division</B>>,
                  shape=box,
                  style="filled, rounded"];
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
          "abjad.tools.abctools.AbjadObject.AbjadObject" -> "abjad.tools.mathtools.NonreducedFraction.NonreducedFraction";
          "abjad.tools.mathtools.NonreducedFraction.NonreducedFraction" -> "abjad.tools.durationtools.Division.Division";
          "builtins.object" -> "abjad.tools.abctools.AbjadObject.AbstractBase";
          "builtins.object" -> "numbers.Number";
          "fractions.Fraction" -> "abjad.tools.mathtools.NonreducedFraction.NonreducedFraction";
          "numbers.Rational" -> "fractions.Fraction";
      }

Bases
-----

- :py:class:`abjad.tools.mathtools.NonreducedFraction`

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

      ~abjad.tools.durationtools.Division.Division.conjugate
      ~abjad.tools.durationtools.Division.Division.denominator
      ~abjad.tools.durationtools.Division.Division.duration
      ~abjad.tools.durationtools.Division.Division.from_decimal
      ~abjad.tools.durationtools.Division.Division.from_float
      ~abjad.tools.durationtools.Division.Division.imag
      ~abjad.tools.durationtools.Division.Division.limit_denominator
      ~abjad.tools.durationtools.Division.Division.multiply_with_cross_cancelation
      ~abjad.tools.durationtools.Division.Division.multiply_with_numerator_preservation
      ~abjad.tools.durationtools.Division.Division.multiply_without_reducing
      ~abjad.tools.durationtools.Division.Division.numerator
      ~abjad.tools.durationtools.Division.Division.pair
      ~abjad.tools.durationtools.Division.Division.payload
      ~abjad.tools.durationtools.Division.Division.real
      ~abjad.tools.durationtools.Division.Division.reduce
      ~abjad.tools.durationtools.Division.Division.start_offset
      ~abjad.tools.durationtools.Division.Division.stop_offset
      ~abjad.tools.durationtools.Division.Division.with_denominator
      ~abjad.tools.durationtools.Division.Division.with_multiple_of_denominator
      ~abjad.tools.durationtools.Division.Division.__abs__
      ~abjad.tools.durationtools.Division.Division.__add__
      ~abjad.tools.durationtools.Division.Division.__bool__
      ~abjad.tools.durationtools.Division.Division.__ceil__
      ~abjad.tools.durationtools.Division.Division.__complex__
      ~abjad.tools.durationtools.Division.Division.__copy__
      ~abjad.tools.durationtools.Division.Division.__deepcopy__
      ~abjad.tools.durationtools.Division.Division.__div__
      ~abjad.tools.durationtools.Division.Division.__divmod__
      ~abjad.tools.durationtools.Division.Division.__eq__
      ~abjad.tools.durationtools.Division.Division.__float__
      ~abjad.tools.durationtools.Division.Division.__floor__
      ~abjad.tools.durationtools.Division.Division.__floordiv__
      ~abjad.tools.durationtools.Division.Division.__format__
      ~abjad.tools.durationtools.Division.Division.__ge__
      ~abjad.tools.durationtools.Division.Division.__gt__
      ~abjad.tools.durationtools.Division.Division.__hash__
      ~abjad.tools.durationtools.Division.Division.__le__
      ~abjad.tools.durationtools.Division.Division.__lt__
      ~abjad.tools.durationtools.Division.Division.__mod__
      ~abjad.tools.durationtools.Division.Division.__mul__
      ~abjad.tools.durationtools.Division.Division.__ne__
      ~abjad.tools.durationtools.Division.Division.__neg__
      ~abjad.tools.durationtools.Division.Division.__new__
      ~abjad.tools.durationtools.Division.Division.__pos__
      ~abjad.tools.durationtools.Division.Division.__pow__
      ~abjad.tools.durationtools.Division.Division.__radd__
      ~abjad.tools.durationtools.Division.Division.__rdiv__
      ~abjad.tools.durationtools.Division.Division.__rdivmod__
      ~abjad.tools.durationtools.Division.Division.__repr__
      ~abjad.tools.durationtools.Division.Division.__rfloordiv__
      ~abjad.tools.durationtools.Division.Division.__rmod__
      ~abjad.tools.durationtools.Division.Division.__rmul__
      ~abjad.tools.durationtools.Division.Division.__round__
      ~abjad.tools.durationtools.Division.Division.__rpow__
      ~abjad.tools.durationtools.Division.Division.__rsub__
      ~abjad.tools.durationtools.Division.Division.__rtruediv__
      ~abjad.tools.durationtools.Division.Division.__str__
      ~abjad.tools.durationtools.Division.Division.__sub__
      ~abjad.tools.durationtools.Division.Division.__truediv__
      ~abjad.tools.durationtools.Division.Division.__trunc__

Read-only properties
--------------------

.. only:: html

   .. container:: inherited

      .. autoattribute:: abjad.tools.durationtools.Division.Division.denominator

.. autoattribute:: abjad.tools.durationtools.Division.Division.duration

.. only:: html

   .. container:: inherited

      .. autoattribute:: abjad.tools.durationtools.Division.Division.imag

.. only:: html

   .. container:: inherited

      .. autoattribute:: abjad.tools.durationtools.Division.Division.numerator

.. only:: html

   .. container:: inherited

      .. autoattribute:: abjad.tools.durationtools.Division.Division.pair

.. autoattribute:: abjad.tools.durationtools.Division.Division.payload

.. only:: html

   .. container:: inherited

      .. autoattribute:: abjad.tools.durationtools.Division.Division.real

.. autoattribute:: abjad.tools.durationtools.Division.Division.start_offset

.. autoattribute:: abjad.tools.durationtools.Division.Division.stop_offset

Methods
-------

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.durationtools.Division.Division.conjugate

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.durationtools.Division.Division.limit_denominator

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.durationtools.Division.Division.multiply_with_cross_cancelation

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.durationtools.Division.Division.multiply_with_numerator_preservation

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.durationtools.Division.Division.multiply_without_reducing

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.durationtools.Division.Division.reduce

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.durationtools.Division.Division.with_denominator

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.durationtools.Division.Division.with_multiple_of_denominator

Class & static methods
----------------------

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.durationtools.Division.Division.from_decimal

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.durationtools.Division.Division.from_float

Special methods
---------------

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.durationtools.Division.Division.__abs__

.. automethod:: abjad.tools.durationtools.Division.Division.__add__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.durationtools.Division.Division.__bool__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.durationtools.Division.Division.__ceil__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.durationtools.Division.Division.__complex__

.. automethod:: abjad.tools.durationtools.Division.Division.__copy__

.. automethod:: abjad.tools.durationtools.Division.Division.__deepcopy__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.durationtools.Division.Division.__div__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.durationtools.Division.Division.__divmod__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.durationtools.Division.Division.__eq__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.durationtools.Division.Division.__float__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.durationtools.Division.Division.__floor__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.durationtools.Division.Division.__floordiv__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.durationtools.Division.Division.__format__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.durationtools.Division.Division.__ge__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.durationtools.Division.Division.__gt__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.durationtools.Division.Division.__hash__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.durationtools.Division.Division.__le__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.durationtools.Division.Division.__lt__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.durationtools.Division.Division.__mod__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.durationtools.Division.Division.__mul__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.durationtools.Division.Division.__ne__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.durationtools.Division.Division.__neg__

.. automethod:: abjad.tools.durationtools.Division.Division.__new__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.durationtools.Division.Division.__pos__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.durationtools.Division.Division.__pow__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.durationtools.Division.Division.__radd__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.durationtools.Division.Division.__rdiv__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.durationtools.Division.Division.__rdivmod__

.. automethod:: abjad.tools.durationtools.Division.Division.__repr__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.durationtools.Division.Division.__rfloordiv__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.durationtools.Division.Division.__rmod__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.durationtools.Division.Division.__rmul__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.durationtools.Division.Division.__round__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.durationtools.Division.Division.__rpow__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.durationtools.Division.Division.__rsub__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.durationtools.Division.Division.__rtruediv__

.. automethod:: abjad.tools.durationtools.Division.Division.__str__

.. automethod:: abjad.tools.durationtools.Division.Division.__sub__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.durationtools.Division.Division.__truediv__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.durationtools.Division.Division.__trunc__
