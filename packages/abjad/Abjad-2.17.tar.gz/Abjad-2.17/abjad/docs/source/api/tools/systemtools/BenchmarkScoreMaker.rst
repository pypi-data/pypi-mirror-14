.. currentmodule:: abjad.tools.systemtools

BenchmarkScoreMaker
===================

.. autoclass:: BenchmarkScoreMaker

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
          subgraph cluster_systemtools {
              graph [label=systemtools];
              "abjad.tools.systemtools.BenchmarkScoreMaker.BenchmarkScoreMaker" [color=black,
                  fontcolor=white,
                  group=2,
                  label=<<B>BenchmarkScoreMaker</B>>,
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
          "abjad.tools.abctools.AbjadObject.AbjadObject" -> "abjad.tools.systemtools.BenchmarkScoreMaker.BenchmarkScoreMaker";
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

      ~abjad.tools.systemtools.BenchmarkScoreMaker.BenchmarkScoreMaker.make_bound_hairpin_score_01
      ~abjad.tools.systemtools.BenchmarkScoreMaker.BenchmarkScoreMaker.make_bound_hairpin_score_02
      ~abjad.tools.systemtools.BenchmarkScoreMaker.BenchmarkScoreMaker.make_bound_hairpin_score_03
      ~abjad.tools.systemtools.BenchmarkScoreMaker.BenchmarkScoreMaker.make_hairpin_score_01
      ~abjad.tools.systemtools.BenchmarkScoreMaker.BenchmarkScoreMaker.make_hairpin_score_02
      ~abjad.tools.systemtools.BenchmarkScoreMaker.BenchmarkScoreMaker.make_hairpin_score_03
      ~abjad.tools.systemtools.BenchmarkScoreMaker.BenchmarkScoreMaker.make_score_00
      ~abjad.tools.systemtools.BenchmarkScoreMaker.BenchmarkScoreMaker.make_score_with_indicators_01
      ~abjad.tools.systemtools.BenchmarkScoreMaker.BenchmarkScoreMaker.make_score_with_indicators_02
      ~abjad.tools.systemtools.BenchmarkScoreMaker.BenchmarkScoreMaker.make_score_with_indicators_03
      ~abjad.tools.systemtools.BenchmarkScoreMaker.BenchmarkScoreMaker.make_spanner_score_01
      ~abjad.tools.systemtools.BenchmarkScoreMaker.BenchmarkScoreMaker.make_spanner_score_02
      ~abjad.tools.systemtools.BenchmarkScoreMaker.BenchmarkScoreMaker.make_spanner_score_03
      ~abjad.tools.systemtools.BenchmarkScoreMaker.BenchmarkScoreMaker.make_spanner_score_04
      ~abjad.tools.systemtools.BenchmarkScoreMaker.BenchmarkScoreMaker.make_spanner_score_05
      ~abjad.tools.systemtools.BenchmarkScoreMaker.BenchmarkScoreMaker.make_spanner_score_06
      ~abjad.tools.systemtools.BenchmarkScoreMaker.BenchmarkScoreMaker.make_spanner_score_07
      ~abjad.tools.systemtools.BenchmarkScoreMaker.BenchmarkScoreMaker.make_spanner_score_08
      ~abjad.tools.systemtools.BenchmarkScoreMaker.BenchmarkScoreMaker.make_spanner_score_09
      ~abjad.tools.systemtools.BenchmarkScoreMaker.BenchmarkScoreMaker.__eq__
      ~abjad.tools.systemtools.BenchmarkScoreMaker.BenchmarkScoreMaker.__format__
      ~abjad.tools.systemtools.BenchmarkScoreMaker.BenchmarkScoreMaker.__hash__
      ~abjad.tools.systemtools.BenchmarkScoreMaker.BenchmarkScoreMaker.__ne__
      ~abjad.tools.systemtools.BenchmarkScoreMaker.BenchmarkScoreMaker.__repr__

Methods
-------

.. automethod:: abjad.tools.systemtools.BenchmarkScoreMaker.BenchmarkScoreMaker.make_bound_hairpin_score_01

.. automethod:: abjad.tools.systemtools.BenchmarkScoreMaker.BenchmarkScoreMaker.make_bound_hairpin_score_02

.. automethod:: abjad.tools.systemtools.BenchmarkScoreMaker.BenchmarkScoreMaker.make_bound_hairpin_score_03

.. automethod:: abjad.tools.systemtools.BenchmarkScoreMaker.BenchmarkScoreMaker.make_hairpin_score_01

.. automethod:: abjad.tools.systemtools.BenchmarkScoreMaker.BenchmarkScoreMaker.make_hairpin_score_02

.. automethod:: abjad.tools.systemtools.BenchmarkScoreMaker.BenchmarkScoreMaker.make_hairpin_score_03

.. automethod:: abjad.tools.systemtools.BenchmarkScoreMaker.BenchmarkScoreMaker.make_score_00

.. automethod:: abjad.tools.systemtools.BenchmarkScoreMaker.BenchmarkScoreMaker.make_score_with_indicators_01

.. automethod:: abjad.tools.systemtools.BenchmarkScoreMaker.BenchmarkScoreMaker.make_score_with_indicators_02

.. automethod:: abjad.tools.systemtools.BenchmarkScoreMaker.BenchmarkScoreMaker.make_score_with_indicators_03

.. automethod:: abjad.tools.systemtools.BenchmarkScoreMaker.BenchmarkScoreMaker.make_spanner_score_01

.. automethod:: abjad.tools.systemtools.BenchmarkScoreMaker.BenchmarkScoreMaker.make_spanner_score_02

.. automethod:: abjad.tools.systemtools.BenchmarkScoreMaker.BenchmarkScoreMaker.make_spanner_score_03

.. automethod:: abjad.tools.systemtools.BenchmarkScoreMaker.BenchmarkScoreMaker.make_spanner_score_04

.. automethod:: abjad.tools.systemtools.BenchmarkScoreMaker.BenchmarkScoreMaker.make_spanner_score_05

.. automethod:: abjad.tools.systemtools.BenchmarkScoreMaker.BenchmarkScoreMaker.make_spanner_score_06

.. automethod:: abjad.tools.systemtools.BenchmarkScoreMaker.BenchmarkScoreMaker.make_spanner_score_07

.. automethod:: abjad.tools.systemtools.BenchmarkScoreMaker.BenchmarkScoreMaker.make_spanner_score_08

.. automethod:: abjad.tools.systemtools.BenchmarkScoreMaker.BenchmarkScoreMaker.make_spanner_score_09

Special methods
---------------

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.systemtools.BenchmarkScoreMaker.BenchmarkScoreMaker.__eq__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.systemtools.BenchmarkScoreMaker.BenchmarkScoreMaker.__format__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.systemtools.BenchmarkScoreMaker.BenchmarkScoreMaker.__hash__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.systemtools.BenchmarkScoreMaker.BenchmarkScoreMaker.__ne__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.systemtools.BenchmarkScoreMaker.BenchmarkScoreMaker.__repr__
