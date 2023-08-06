.. currentmodule:: abjad.tools.expressiontools

SequenceExpression
==================

.. autoclass:: SequenceExpression

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
              "abjad.tools.expressiontools.SequenceExpression.SequenceExpression" [color=black,
                  fontcolor=white,
                  group=2,
                  label=<<B>SequenceExpression</B>>,
                  shape=box,
                  style="filled, rounded"];
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

- :py:class:`abjad.tools.expressiontools.Expression`

- :py:class:`abjad.tools.abctools.AbjadObject`

- :py:class:`abjad.tools.abctools.AbjadObject.AbstractBase`

- :py:class:`builtins.object`

.. only:: html

   Attribute summary
   -----------------

   .. autosummary::

      ~abjad.tools.expressiontools.SequenceExpression.SequenceExpression.callbacks
      ~abjad.tools.expressiontools.SequenceExpression.SequenceExpression.flatten
      ~abjad.tools.expressiontools.SequenceExpression.SequenceExpression.map
      ~abjad.tools.expressiontools.SequenceExpression.SequenceExpression.partition_by_counts
      ~abjad.tools.expressiontools.SequenceExpression.SequenceExpression.partition_by_ratio_of_lengths
      ~abjad.tools.expressiontools.SequenceExpression.SequenceExpression.reverse
      ~abjad.tools.expressiontools.SequenceExpression.SequenceExpression.rotate
      ~abjad.tools.expressiontools.SequenceExpression.SequenceExpression.sequence
      ~abjad.tools.expressiontools.SequenceExpression.SequenceExpression.split
      ~abjad.tools.expressiontools.SequenceExpression.SequenceExpression.sum
      ~abjad.tools.expressiontools.SequenceExpression.SequenceExpression.__add__
      ~abjad.tools.expressiontools.SequenceExpression.SequenceExpression.__call__
      ~abjad.tools.expressiontools.SequenceExpression.SequenceExpression.__eq__
      ~abjad.tools.expressiontools.SequenceExpression.SequenceExpression.__format__
      ~abjad.tools.expressiontools.SequenceExpression.SequenceExpression.__getitem__
      ~abjad.tools.expressiontools.SequenceExpression.SequenceExpression.__hash__
      ~abjad.tools.expressiontools.SequenceExpression.SequenceExpression.__ne__
      ~abjad.tools.expressiontools.SequenceExpression.SequenceExpression.__radd__
      ~abjad.tools.expressiontools.SequenceExpression.SequenceExpression.__repr__

Read-only properties
--------------------

.. only:: html

   .. container:: inherited

      .. autoattribute:: abjad.tools.expressiontools.SequenceExpression.SequenceExpression.callbacks

Methods
-------

.. automethod:: abjad.tools.expressiontools.SequenceExpression.SequenceExpression.flatten

.. automethod:: abjad.tools.expressiontools.SequenceExpression.SequenceExpression.map

.. automethod:: abjad.tools.expressiontools.SequenceExpression.SequenceExpression.partition_by_counts

.. automethod:: abjad.tools.expressiontools.SequenceExpression.SequenceExpression.partition_by_ratio_of_lengths

.. automethod:: abjad.tools.expressiontools.SequenceExpression.SequenceExpression.reverse

.. automethod:: abjad.tools.expressiontools.SequenceExpression.SequenceExpression.rotate

.. automethod:: abjad.tools.expressiontools.SequenceExpression.SequenceExpression.sequence

.. automethod:: abjad.tools.expressiontools.SequenceExpression.SequenceExpression.split

.. automethod:: abjad.tools.expressiontools.SequenceExpression.SequenceExpression.sum

Special methods
---------------

.. automethod:: abjad.tools.expressiontools.SequenceExpression.SequenceExpression.__add__

.. automethod:: abjad.tools.expressiontools.SequenceExpression.SequenceExpression.__call__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.expressiontools.SequenceExpression.SequenceExpression.__eq__

.. automethod:: abjad.tools.expressiontools.SequenceExpression.SequenceExpression.__format__

.. automethod:: abjad.tools.expressiontools.SequenceExpression.SequenceExpression.__getitem__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.expressiontools.SequenceExpression.SequenceExpression.__hash__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.expressiontools.SequenceExpression.SequenceExpression.__ne__

.. automethod:: abjad.tools.expressiontools.SequenceExpression.SequenceExpression.__radd__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.expressiontools.SequenceExpression.SequenceExpression.__repr__
