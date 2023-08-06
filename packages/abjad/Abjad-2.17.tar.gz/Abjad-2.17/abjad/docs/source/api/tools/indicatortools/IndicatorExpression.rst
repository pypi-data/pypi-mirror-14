.. currentmodule:: abjad.tools.indicatortools

IndicatorExpression
===================

.. autoclass:: IndicatorExpression

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
              "abjad.tools.indicatortools.IndicatorExpression.IndicatorExpression" [color=black,
                  fontcolor=white,
                  group=2,
                  label=<<B>IndicatorExpression</B>>,
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
          "abjad.tools.abctools.AbjadValueObject.AbjadValueObject" -> "abjad.tools.indicatortools.IndicatorExpression.IndicatorExpression";
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

      ~abjad.tools.indicatortools.IndicatorExpression.IndicatorExpression.component
      ~abjad.tools.indicatortools.IndicatorExpression.IndicatorExpression.indicator
      ~abjad.tools.indicatortools.IndicatorExpression.IndicatorExpression.is_annotation
      ~abjad.tools.indicatortools.IndicatorExpression.IndicatorExpression.name
      ~abjad.tools.indicatortools.IndicatorExpression.IndicatorExpression.scope
      ~abjad.tools.indicatortools.IndicatorExpression.IndicatorExpression.__copy__
      ~abjad.tools.indicatortools.IndicatorExpression.IndicatorExpression.__eq__
      ~abjad.tools.indicatortools.IndicatorExpression.IndicatorExpression.__format__
      ~abjad.tools.indicatortools.IndicatorExpression.IndicatorExpression.__hash__
      ~abjad.tools.indicatortools.IndicatorExpression.IndicatorExpression.__ne__
      ~abjad.tools.indicatortools.IndicatorExpression.IndicatorExpression.__repr__

Read-only properties
--------------------

.. autoattribute:: abjad.tools.indicatortools.IndicatorExpression.IndicatorExpression.component

.. autoattribute:: abjad.tools.indicatortools.IndicatorExpression.IndicatorExpression.indicator

.. autoattribute:: abjad.tools.indicatortools.IndicatorExpression.IndicatorExpression.is_annotation

.. autoattribute:: abjad.tools.indicatortools.IndicatorExpression.IndicatorExpression.name

.. autoattribute:: abjad.tools.indicatortools.IndicatorExpression.IndicatorExpression.scope

Special methods
---------------

.. automethod:: abjad.tools.indicatortools.IndicatorExpression.IndicatorExpression.__copy__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.indicatortools.IndicatorExpression.IndicatorExpression.__eq__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.indicatortools.IndicatorExpression.IndicatorExpression.__format__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.indicatortools.IndicatorExpression.IndicatorExpression.__hash__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.indicatortools.IndicatorExpression.IndicatorExpression.__ne__

.. automethod:: abjad.tools.indicatortools.IndicatorExpression.IndicatorExpression.__repr__
