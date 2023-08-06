.. currentmodule:: abjad.tools.expressiontools

LabelExpression
===============

.. autoclass:: LabelExpression

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
              "abjad.tools.expressiontools.Expression.Expression" [color=3,
                  group=2,
                  label=Expression,
                  shape=box];
              "abjad.tools.expressiontools.LabelExpression.LabelExpression" [color=black,
                  fontcolor=white,
                  group=2,
                  label=<<B>LabelExpression</B>>,
                  shape=box,
                  style="filled, rounded"];
              "abjad.tools.expressiontools.Expression.Expression" -> "abjad.tools.expressiontools.LabelExpression.LabelExpression";
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

- :py:class:`abjad.tools.expressiontools.Expression`

- :py:class:`abjad.tools.abctools.AbjadObject`

- :py:class:`abjad.tools.abctools.AbjadObject.AbstractBase`

- :py:class:`builtins.object`

.. only:: html

   Attribute summary
   -----------------

   .. autosummary::

      ~abjad.tools.expressiontools.LabelExpression.LabelExpression.callbacks
      ~abjad.tools.expressiontools.LabelExpression.LabelExpression.color_container
      ~abjad.tools.expressiontools.LabelExpression.LabelExpression.color_leaves
      ~abjad.tools.expressiontools.LabelExpression.LabelExpression.color_note_heads
      ~abjad.tools.expressiontools.LabelExpression.LabelExpression.remove_markup
      ~abjad.tools.expressiontools.LabelExpression.LabelExpression.vertical_moments
      ~abjad.tools.expressiontools.LabelExpression.LabelExpression.with_durations
      ~abjad.tools.expressiontools.LabelExpression.LabelExpression.with_indices
      ~abjad.tools.expressiontools.LabelExpression.LabelExpression.with_intervals
      ~abjad.tools.expressiontools.LabelExpression.LabelExpression.with_pitches
      ~abjad.tools.expressiontools.LabelExpression.LabelExpression.with_start_offsets
      ~abjad.tools.expressiontools.LabelExpression.LabelExpression.__call__
      ~abjad.tools.expressiontools.LabelExpression.LabelExpression.__eq__
      ~abjad.tools.expressiontools.LabelExpression.LabelExpression.__format__
      ~abjad.tools.expressiontools.LabelExpression.LabelExpression.__hash__
      ~abjad.tools.expressiontools.LabelExpression.LabelExpression.__ne__
      ~abjad.tools.expressiontools.LabelExpression.LabelExpression.__repr__

Read-only properties
--------------------

.. only:: html

   .. container:: inherited

      .. autoattribute:: abjad.tools.expressiontools.LabelExpression.LabelExpression.callbacks

Methods
-------

.. automethod:: abjad.tools.expressiontools.LabelExpression.LabelExpression.color_container

.. automethod:: abjad.tools.expressiontools.LabelExpression.LabelExpression.color_leaves

.. automethod:: abjad.tools.expressiontools.LabelExpression.LabelExpression.color_note_heads

.. automethod:: abjad.tools.expressiontools.LabelExpression.LabelExpression.remove_markup

.. automethod:: abjad.tools.expressiontools.LabelExpression.LabelExpression.vertical_moments

.. automethod:: abjad.tools.expressiontools.LabelExpression.LabelExpression.with_durations

.. automethod:: abjad.tools.expressiontools.LabelExpression.LabelExpression.with_indices

.. automethod:: abjad.tools.expressiontools.LabelExpression.LabelExpression.with_intervals

.. automethod:: abjad.tools.expressiontools.LabelExpression.LabelExpression.with_pitches

.. automethod:: abjad.tools.expressiontools.LabelExpression.LabelExpression.with_start_offsets

Special methods
---------------

.. automethod:: abjad.tools.expressiontools.LabelExpression.LabelExpression.__call__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.expressiontools.LabelExpression.LabelExpression.__eq__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.expressiontools.LabelExpression.LabelExpression.__format__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.expressiontools.LabelExpression.LabelExpression.__hash__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.expressiontools.LabelExpression.LabelExpression.__ne__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.expressiontools.LabelExpression.LabelExpression.__repr__
