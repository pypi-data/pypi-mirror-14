.. currentmodule:: abjad.tools.indicatortools

TimeSignature
=============

.. autoclass:: TimeSignature

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
              "abjad.tools.abctools.AbjadValueObject.AbjadValueObject" [color=1,
                  group=0,
                  label=AbjadValueObject,
                  shape=box];
              "abjad.tools.abctools.AbjadObject.AbjadObject" -> "abjad.tools.abctools.AbjadValueObject.AbjadValueObject";
              "abjad.tools.abctools.AbjadObject.AbstractBase" -> "abjad.tools.abctools.AbjadObject.AbjadObject";
          }
          subgraph cluster_indicatortools {
              graph [label=indicatortools];
              "abjad.tools.indicatortools.TimeSignature.TimeSignature" [color=black,
                  fontcolor=white,
                  group=2,
                  label=<<B>TimeSignature</B>>,
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
          "abjad.tools.abctools.AbjadValueObject.AbjadValueObject" -> "abjad.tools.indicatortools.TimeSignature.TimeSignature";
          "builtins.object" -> "abjad.tools.abctools.AbjadObject.AbstractBase";
      }

Bases
-----

- :py:class:`abjad.tools.abctools.AbjadValueObject`

- :py:class:`abjad.tools.abctools.AbjadObject`

- :py:class:`abjad.tools.abctools.AbjadObject.AbstractBase`

- :py:class:`builtins.object`

.. only:: html

   Attribute summary
   -----------------

   .. autosummary::

      ~abjad.tools.indicatortools.TimeSignature.TimeSignature.default_scope
      ~abjad.tools.indicatortools.TimeSignature.TimeSignature.denominator
      ~abjad.tools.indicatortools.TimeSignature.TimeSignature.duration
      ~abjad.tools.indicatortools.TimeSignature.TimeSignature.has_non_power_of_two_denominator
      ~abjad.tools.indicatortools.TimeSignature.TimeSignature.implied_prolation
      ~abjad.tools.indicatortools.TimeSignature.TimeSignature.numerator
      ~abjad.tools.indicatortools.TimeSignature.TimeSignature.pair
      ~abjad.tools.indicatortools.TimeSignature.TimeSignature.partial
      ~abjad.tools.indicatortools.TimeSignature.TimeSignature.suppress
      ~abjad.tools.indicatortools.TimeSignature.TimeSignature.with_power_of_two_denominator
      ~abjad.tools.indicatortools.TimeSignature.TimeSignature.__add__
      ~abjad.tools.indicatortools.TimeSignature.TimeSignature.__copy__
      ~abjad.tools.indicatortools.TimeSignature.TimeSignature.__eq__
      ~abjad.tools.indicatortools.TimeSignature.TimeSignature.__format__
      ~abjad.tools.indicatortools.TimeSignature.TimeSignature.__ge__
      ~abjad.tools.indicatortools.TimeSignature.TimeSignature.__gt__
      ~abjad.tools.indicatortools.TimeSignature.TimeSignature.__hash__
      ~abjad.tools.indicatortools.TimeSignature.TimeSignature.__le__
      ~abjad.tools.indicatortools.TimeSignature.TimeSignature.__lt__
      ~abjad.tools.indicatortools.TimeSignature.TimeSignature.__ne__
      ~abjad.tools.indicatortools.TimeSignature.TimeSignature.__radd__
      ~abjad.tools.indicatortools.TimeSignature.TimeSignature.__repr__
      ~abjad.tools.indicatortools.TimeSignature.TimeSignature.__str__

Read-only properties
--------------------

.. autoattribute:: abjad.tools.indicatortools.TimeSignature.TimeSignature.default_scope

.. autoattribute:: abjad.tools.indicatortools.TimeSignature.TimeSignature.denominator

.. autoattribute:: abjad.tools.indicatortools.TimeSignature.TimeSignature.duration

.. autoattribute:: abjad.tools.indicatortools.TimeSignature.TimeSignature.has_non_power_of_two_denominator

.. autoattribute:: abjad.tools.indicatortools.TimeSignature.TimeSignature.implied_prolation

.. autoattribute:: abjad.tools.indicatortools.TimeSignature.TimeSignature.numerator

.. autoattribute:: abjad.tools.indicatortools.TimeSignature.TimeSignature.pair

.. autoattribute:: abjad.tools.indicatortools.TimeSignature.TimeSignature.partial

Read/write properties
---------------------

.. autoattribute:: abjad.tools.indicatortools.TimeSignature.TimeSignature.suppress

Methods
-------

.. automethod:: abjad.tools.indicatortools.TimeSignature.TimeSignature.with_power_of_two_denominator

Special methods
---------------

.. automethod:: abjad.tools.indicatortools.TimeSignature.TimeSignature.__add__

.. automethod:: abjad.tools.indicatortools.TimeSignature.TimeSignature.__copy__

.. automethod:: abjad.tools.indicatortools.TimeSignature.TimeSignature.__eq__

.. automethod:: abjad.tools.indicatortools.TimeSignature.TimeSignature.__format__

.. automethod:: abjad.tools.indicatortools.TimeSignature.TimeSignature.__ge__

.. automethod:: abjad.tools.indicatortools.TimeSignature.TimeSignature.__gt__

.. automethod:: abjad.tools.indicatortools.TimeSignature.TimeSignature.__hash__

.. automethod:: abjad.tools.indicatortools.TimeSignature.TimeSignature.__le__

.. automethod:: abjad.tools.indicatortools.TimeSignature.TimeSignature.__lt__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.indicatortools.TimeSignature.TimeSignature.__ne__

.. automethod:: abjad.tools.indicatortools.TimeSignature.TimeSignature.__radd__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.indicatortools.TimeSignature.TimeSignature.__repr__

.. automethod:: abjad.tools.indicatortools.TimeSignature.TimeSignature.__str__
