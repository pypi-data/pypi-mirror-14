expressiontools
===============

.. automodule:: abjad.tools.expressiontools

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
              "abjad.tools.abctools.AbjadObject.AbstractBase" -> "abjad.tools.abctools.AbjadObject.AbjadObject";
          }
          subgraph cluster_expressiontools {
              graph [label=expressiontools];
              "abjad.tools.expressiontools.Callback.Callback" [color=black,
                  fontcolor=white,
                  group=2,
                  label=Callback,
                  shape=box,
                  style="filled, rounded"];
              "abjad.tools.expressiontools.Expression.Expression" [color=black,
                  fontcolor=white,
                  group=2,
                  label=Expression,
                  shape=box,
                  style="filled, rounded"];
              "abjad.tools.expressiontools.LabelExpression.LabelExpression" [color=black,
                  fontcolor=white,
                  group=2,
                  label=LabelExpression,
                  shape=box,
                  style="filled, rounded"];
              "abjad.tools.expressiontools.SequenceExpression.SequenceExpression" [color=black,
                  fontcolor=white,
                  group=2,
                  label=SequenceExpression,
                  shape=box,
                  style="filled, rounded"];
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
          "abjad.tools.abctools.AbjadObject.AbjadObject" -> "abjad.tools.expressiontools.Callback.Callback";
          "abjad.tools.abctools.AbjadObject.AbjadObject" -> "abjad.tools.expressiontools.Expression.Expression";
          "builtins.object" -> "abjad.tools.abctools.AbjadObject.AbstractBase";
      }

--------

Expressions
-----------

.. toctree::
   :hidden:

   Callback
   Expression
   LabelExpression
   SequenceExpression

.. autosummary::
   :nosignatures:

   Callback
   Expression
   LabelExpression
   SequenceExpression
