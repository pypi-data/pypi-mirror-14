.. currentmodule:: abjad.tools.quantizationtools

Heuristic
=========

.. autoclass:: Heuristic

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
              "abjad.tools.quantizationtools.DistanceHeuristic.DistanceHeuristic" [color=3,
                  group=2,
                  label=DistanceHeuristic,
                  shape=box];
              "abjad.tools.quantizationtools.Heuristic.Heuristic" [color=black,
                  fontcolor=white,
                  group=2,
                  label=<<B>Heuristic</B>>,
                  shape=oval,
                  style="filled, rounded"];
              "abjad.tools.quantizationtools.Heuristic.Heuristic" -> "abjad.tools.quantizationtools.DistanceHeuristic.DistanceHeuristic";
          }
          subgraph cluster_builtins {
              graph [label=builtins];
              "builtins.object" [color=2,
                  group=1,
                  label=object,
                  shape=box];
          }
          "abjad.tools.abctools.AbjadObject.AbjadObject" -> "abjad.tools.quantizationtools.Heuristic.Heuristic";
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

      ~abjad.tools.quantizationtools.Heuristic.Heuristic.__call__
      ~abjad.tools.quantizationtools.Heuristic.Heuristic.__eq__
      ~abjad.tools.quantizationtools.Heuristic.Heuristic.__format__
      ~abjad.tools.quantizationtools.Heuristic.Heuristic.__hash__
      ~abjad.tools.quantizationtools.Heuristic.Heuristic.__ne__
      ~abjad.tools.quantizationtools.Heuristic.Heuristic.__repr__

Special methods
---------------

.. automethod:: abjad.tools.quantizationtools.Heuristic.Heuristic.__call__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.quantizationtools.Heuristic.Heuristic.__eq__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.quantizationtools.Heuristic.Heuristic.__format__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.quantizationtools.Heuristic.Heuristic.__hash__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.quantizationtools.Heuristic.Heuristic.__ne__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.quantizationtools.Heuristic.Heuristic.__repr__
