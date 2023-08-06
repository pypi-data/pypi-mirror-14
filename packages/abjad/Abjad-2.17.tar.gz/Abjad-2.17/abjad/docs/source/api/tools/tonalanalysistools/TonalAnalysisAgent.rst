.. currentmodule:: abjad.tools.tonalanalysistools

TonalAnalysisAgent
==================

.. autoclass:: TonalAnalysisAgent

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
          subgraph cluster_tonalanalysistools {
              graph [label=tonalanalysistools];
              "abjad.tools.tonalanalysistools.TonalAnalysisAgent.TonalAnalysisAgent" [color=black,
                  fontcolor=white,
                  group=2,
                  label=<<B>TonalAnalysisAgent</B>>,
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
          "abjad.tools.abctools.AbjadObject.AbjadObject" -> "abjad.tools.tonalanalysistools.TonalAnalysisAgent.TonalAnalysisAgent";
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

      ~abjad.tools.tonalanalysistools.TonalAnalysisAgent.TonalAnalysisAgent.analyze_chords
      ~abjad.tools.tonalanalysistools.TonalAnalysisAgent.TonalAnalysisAgent.analyze_incomplete_chords
      ~abjad.tools.tonalanalysistools.TonalAnalysisAgent.TonalAnalysisAgent.analyze_incomplete_tonal_functions
      ~abjad.tools.tonalanalysistools.TonalAnalysisAgent.TonalAnalysisAgent.analyze_neighbor_notes
      ~abjad.tools.tonalanalysistools.TonalAnalysisAgent.TonalAnalysisAgent.analyze_passing_tones
      ~abjad.tools.tonalanalysistools.TonalAnalysisAgent.TonalAnalysisAgent.analyze_tonal_functions
      ~abjad.tools.tonalanalysistools.TonalAnalysisAgent.TonalAnalysisAgent.are_scalar_notes
      ~abjad.tools.tonalanalysistools.TonalAnalysisAgent.TonalAnalysisAgent.are_stepwise_ascending_notes
      ~abjad.tools.tonalanalysistools.TonalAnalysisAgent.TonalAnalysisAgent.are_stepwise_descending_notes
      ~abjad.tools.tonalanalysistools.TonalAnalysisAgent.TonalAnalysisAgent.are_stepwise_notes
      ~abjad.tools.tonalanalysistools.TonalAnalysisAgent.TonalAnalysisAgent.client
      ~abjad.tools.tonalanalysistools.TonalAnalysisAgent.TonalAnalysisAgent.__eq__
      ~abjad.tools.tonalanalysistools.TonalAnalysisAgent.TonalAnalysisAgent.__format__
      ~abjad.tools.tonalanalysistools.TonalAnalysisAgent.TonalAnalysisAgent.__hash__
      ~abjad.tools.tonalanalysistools.TonalAnalysisAgent.TonalAnalysisAgent.__ne__
      ~abjad.tools.tonalanalysistools.TonalAnalysisAgent.TonalAnalysisAgent.__repr__

Read-only properties
--------------------

.. autoattribute:: abjad.tools.tonalanalysistools.TonalAnalysisAgent.TonalAnalysisAgent.client

Methods
-------

.. automethod:: abjad.tools.tonalanalysistools.TonalAnalysisAgent.TonalAnalysisAgent.analyze_chords

.. automethod:: abjad.tools.tonalanalysistools.TonalAnalysisAgent.TonalAnalysisAgent.analyze_incomplete_chords

.. automethod:: abjad.tools.tonalanalysistools.TonalAnalysisAgent.TonalAnalysisAgent.analyze_incomplete_tonal_functions

.. automethod:: abjad.tools.tonalanalysistools.TonalAnalysisAgent.TonalAnalysisAgent.analyze_neighbor_notes

.. automethod:: abjad.tools.tonalanalysistools.TonalAnalysisAgent.TonalAnalysisAgent.analyze_passing_tones

.. automethod:: abjad.tools.tonalanalysistools.TonalAnalysisAgent.TonalAnalysisAgent.analyze_tonal_functions

.. automethod:: abjad.tools.tonalanalysistools.TonalAnalysisAgent.TonalAnalysisAgent.are_scalar_notes

.. automethod:: abjad.tools.tonalanalysistools.TonalAnalysisAgent.TonalAnalysisAgent.are_stepwise_ascending_notes

.. automethod:: abjad.tools.tonalanalysistools.TonalAnalysisAgent.TonalAnalysisAgent.are_stepwise_descending_notes

.. automethod:: abjad.tools.tonalanalysistools.TonalAnalysisAgent.TonalAnalysisAgent.are_stepwise_notes

Special methods
---------------

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.tonalanalysistools.TonalAnalysisAgent.TonalAnalysisAgent.__eq__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.tonalanalysistools.TonalAnalysisAgent.TonalAnalysisAgent.__format__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.tonalanalysistools.TonalAnalysisAgent.TonalAnalysisAgent.__hash__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.tonalanalysistools.TonalAnalysisAgent.TonalAnalysisAgent.__ne__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.tonalanalysistools.TonalAnalysisAgent.TonalAnalysisAgent.__repr__
