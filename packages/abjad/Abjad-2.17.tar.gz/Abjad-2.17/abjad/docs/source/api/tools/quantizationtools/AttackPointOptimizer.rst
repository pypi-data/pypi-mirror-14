.. currentmodule:: abjad.tools.quantizationtools

AttackPointOptimizer
====================

.. autoclass:: AttackPointOptimizer

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
          subgraph cluster_quantizationtools {
              graph [label=quantizationtools];
              "abjad.tools.quantizationtools.AttackPointOptimizer.AttackPointOptimizer" [color=black,
                  fontcolor=white,
                  group=2,
                  label=<<B>AttackPointOptimizer</B>>,
                  shape=oval,
                  style="filled, rounded"];
              "abjad.tools.quantizationtools.MeasurewiseAttackPointOptimizer.MeasurewiseAttackPointOptimizer" [color=3,
                  group=2,
                  label=MeasurewiseAttackPointOptimizer,
                  shape=box];
              "abjad.tools.quantizationtools.NaiveAttackPointOptimizer.NaiveAttackPointOptimizer" [color=3,
                  group=2,
                  label=NaiveAttackPointOptimizer,
                  shape=box];
              "abjad.tools.quantizationtools.NullAttackPointOptimizer.NullAttackPointOptimizer" [color=3,
                  group=2,
                  label=NullAttackPointOptimizer,
                  shape=box];
              "abjad.tools.quantizationtools.AttackPointOptimizer.AttackPointOptimizer" -> "abjad.tools.quantizationtools.MeasurewiseAttackPointOptimizer.MeasurewiseAttackPointOptimizer";
              "abjad.tools.quantizationtools.AttackPointOptimizer.AttackPointOptimizer" -> "abjad.tools.quantizationtools.NaiveAttackPointOptimizer.NaiveAttackPointOptimizer";
              "abjad.tools.quantizationtools.AttackPointOptimizer.AttackPointOptimizer" -> "abjad.tools.quantizationtools.NullAttackPointOptimizer.NullAttackPointOptimizer";
          }
          subgraph cluster_builtins {
              graph [label=builtins];
              "builtins.object" [color=2,
                  group=1,
                  label=object,
                  shape=box];
          }
          "abjad.tools.abctools.AbjadObject.AbjadObject" -> "abjad.tools.quantizationtools.AttackPointOptimizer.AttackPointOptimizer";
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

      ~abjad.tools.quantizationtools.AttackPointOptimizer.AttackPointOptimizer.__call__
      ~abjad.tools.quantizationtools.AttackPointOptimizer.AttackPointOptimizer.__eq__
      ~abjad.tools.quantizationtools.AttackPointOptimizer.AttackPointOptimizer.__format__
      ~abjad.tools.quantizationtools.AttackPointOptimizer.AttackPointOptimizer.__hash__
      ~abjad.tools.quantizationtools.AttackPointOptimizer.AttackPointOptimizer.__ne__
      ~abjad.tools.quantizationtools.AttackPointOptimizer.AttackPointOptimizer.__repr__

Special methods
---------------

.. automethod:: abjad.tools.quantizationtools.AttackPointOptimizer.AttackPointOptimizer.__call__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.quantizationtools.AttackPointOptimizer.AttackPointOptimizer.__eq__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.quantizationtools.AttackPointOptimizer.AttackPointOptimizer.__format__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.quantizationtools.AttackPointOptimizer.AttackPointOptimizer.__hash__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.quantizationtools.AttackPointOptimizer.AttackPointOptimizer.__ne__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.quantizationtools.AttackPointOptimizer.AttackPointOptimizer.__repr__
