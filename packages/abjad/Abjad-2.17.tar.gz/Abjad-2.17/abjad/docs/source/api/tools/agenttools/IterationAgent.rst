.. currentmodule:: abjad.tools.agenttools

IterationAgent
==============

.. autoclass:: IterationAgent

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
          subgraph cluster_agenttools {
              graph [label=agenttools];
              "abjad.tools.agenttools.IterationAgent.IterationAgent" [color=black,
                  fontcolor=white,
                  group=1,
                  label=<<B>IterationAgent</B>>,
                  shape=box,
                  style="filled, rounded"];
          }
          subgraph cluster_builtins {
              graph [label=builtins];
              "builtins.object" [color=3,
                  group=2,
                  label=object,
                  shape=box];
          }
          "abjad.tools.abctools.AbjadObject.AbjadObject" -> "abjad.tools.agenttools.IterationAgent.IterationAgent";
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

      ~abjad.tools.agenttools.IterationAgent.IterationAgent.by_class
      ~abjad.tools.agenttools.IterationAgent.IterationAgent.by_components_and_grace_containers
      ~abjad.tools.agenttools.IterationAgent.IterationAgent.by_leaf
      ~abjad.tools.agenttools.IterationAgent.IterationAgent.by_leaf_pair
      ~abjad.tools.agenttools.IterationAgent.IterationAgent.by_logical_tie
      ~abjad.tools.agenttools.IterationAgent.IterationAgent.by_logical_voice
      ~abjad.tools.agenttools.IterationAgent.IterationAgent.by_logical_voice_from_component
      ~abjad.tools.agenttools.IterationAgent.IterationAgent.by_run
      ~abjad.tools.agenttools.IterationAgent.IterationAgent.by_semantic_voice
      ~abjad.tools.agenttools.IterationAgent.IterationAgent.by_spanner
      ~abjad.tools.agenttools.IterationAgent.IterationAgent.by_timeline
      ~abjad.tools.agenttools.IterationAgent.IterationAgent.by_timeline_and_logical_tie
      ~abjad.tools.agenttools.IterationAgent.IterationAgent.by_timeline_from_component
      ~abjad.tools.agenttools.IterationAgent.IterationAgent.by_topmost_logical_ties_and_components
      ~abjad.tools.agenttools.IterationAgent.IterationAgent.by_vertical_moment
      ~abjad.tools.agenttools.IterationAgent.IterationAgent.client
      ~abjad.tools.agenttools.IterationAgent.IterationAgent.depth_first
      ~abjad.tools.agenttools.IterationAgent.IterationAgent.__eq__
      ~abjad.tools.agenttools.IterationAgent.IterationAgent.__format__
      ~abjad.tools.agenttools.IterationAgent.IterationAgent.__hash__
      ~abjad.tools.agenttools.IterationAgent.IterationAgent.__ne__
      ~abjad.tools.agenttools.IterationAgent.IterationAgent.__repr__

Read-only properties
--------------------

.. autoattribute:: abjad.tools.agenttools.IterationAgent.IterationAgent.client

Methods
-------

.. automethod:: abjad.tools.agenttools.IterationAgent.IterationAgent.by_class

.. automethod:: abjad.tools.agenttools.IterationAgent.IterationAgent.by_components_and_grace_containers

.. automethod:: abjad.tools.agenttools.IterationAgent.IterationAgent.by_leaf

.. automethod:: abjad.tools.agenttools.IterationAgent.IterationAgent.by_leaf_pair

.. automethod:: abjad.tools.agenttools.IterationAgent.IterationAgent.by_logical_tie

.. automethod:: abjad.tools.agenttools.IterationAgent.IterationAgent.by_logical_voice

.. automethod:: abjad.tools.agenttools.IterationAgent.IterationAgent.by_logical_voice_from_component

.. automethod:: abjad.tools.agenttools.IterationAgent.IterationAgent.by_run

.. automethod:: abjad.tools.agenttools.IterationAgent.IterationAgent.by_semantic_voice

.. automethod:: abjad.tools.agenttools.IterationAgent.IterationAgent.by_spanner

.. automethod:: abjad.tools.agenttools.IterationAgent.IterationAgent.by_timeline

.. automethod:: abjad.tools.agenttools.IterationAgent.IterationAgent.by_timeline_and_logical_tie

.. automethod:: abjad.tools.agenttools.IterationAgent.IterationAgent.by_timeline_from_component

.. automethod:: abjad.tools.agenttools.IterationAgent.IterationAgent.by_topmost_logical_ties_and_components

.. automethod:: abjad.tools.agenttools.IterationAgent.IterationAgent.by_vertical_moment

.. automethod:: abjad.tools.agenttools.IterationAgent.IterationAgent.depth_first

Special methods
---------------

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.agenttools.IterationAgent.IterationAgent.__eq__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.agenttools.IterationAgent.IterationAgent.__format__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.agenttools.IterationAgent.IterationAgent.__hash__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.agenttools.IterationAgent.IterationAgent.__ne__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.agenttools.IterationAgent.IterationAgent.__repr__
