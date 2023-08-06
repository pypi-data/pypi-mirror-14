.. currentmodule:: abjad.tools.expressiontools

Expression
==========

.. autoclass:: Expression

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
          subgraph cluster_expressiontools {
              graph [label=expressiontools];
              "abjad.tools.expressiontools.Expression.Expression" [color=black,
                  fontcolor=white,
                  group=2,
                  label=<<B>Expression</B>>,
                  shape=box,
                  style="filled, rounded"];
              "abjad.tools.expressiontools.LabelExpression.LabelExpression" [color=3,
                  group=2,
                  label=LabelExpression,
                  shape=box];
              "abjad.tools.expressiontools.SequenceExpression.SequenceExpression" [color=3,
                  group=2,
                  label=SequenceExpression,
                  shape=box];
              "abjad.tools.expressiontools.Expression.Expression" -> "abjad.tools.expressiontools.LabelExpression.LabelExpression";
              "abjad.tools.expressiontools.Expression.Expression" -> "abjad.tools.expressiontools.SequenceExpression.SequenceExpression";
          }
          subgraph cluster_builtins {
              graph [label=builtins];
              "builtins.object" [color=2,
                  group=1,
                  label=object,
                  shape=box];
          }
          "abjad.tools.abctools.AbjadObject.AbjadObject" -> "abjad.tools.expressiontools.Expression.Expression";
          "builtins.object" -> "abjad.tools.abctools.AbjadObject.AbstractBase";
      }

Bases
-----

- :py:class:`abjad.tools.abctools.AbjadObject`

- :py:class:`abjad.tools.abctools.AbjadObject.AbstractBase`

- :py:class:`builtins.object`

.. only:: html

   Attribute summary
   -----------------

   .. autosummary::

      ~abjad.tools.expressiontools.Expression.Expression.callbacks
      ~abjad.tools.expressiontools.Expression.Expression.__eq__
      ~abjad.tools.expressiontools.Expression.Expression.__format__
      ~abjad.tools.expressiontools.Expression.Expression.__hash__
      ~abjad.tools.expressiontools.Expression.Expression.__ne__
      ~abjad.tools.expressiontools.Expression.Expression.__repr__

Read-only properties
--------------------

.. autoattribute:: abjad.tools.expressiontools.Expression.Expression.callbacks

Special methods
---------------

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.expressiontools.Expression.Expression.__eq__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.expressiontools.Expression.Expression.__format__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.expressiontools.Expression.Expression.__hash__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.expressiontools.Expression.Expression.__ne__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.expressiontools.Expression.Expression.__repr__
