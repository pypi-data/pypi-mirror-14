agenttools
==========

.. automodule:: abjad.tools.agenttools

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
          subgraph cluster_agenttools {
              graph [label=agenttools];
              "abjad.tools.agenttools.InspectionAgent.InspectionAgent" [color=black,
                  fontcolor=white,
                  group=1,
                  label=InspectionAgent,
                  shape=box,
                  style="filled, rounded"];
              "abjad.tools.agenttools.IterationAgent.IterationAgent" [color=black,
                  fontcolor=white,
                  group=1,
                  label=IterationAgent,
                  shape=box,
                  style="filled, rounded"];
              "abjad.tools.agenttools.LabelAgent.LabelAgent" [color=black,
                  fontcolor=white,
                  group=1,
                  label=LabelAgent,
                  shape=box,
                  style="filled, rounded"];
              "abjad.tools.agenttools.MutationAgent.MutationAgent" [color=black,
                  fontcolor=white,
                  group=1,
                  label=MutationAgent,
                  shape=box,
                  style="filled, rounded"];
              "abjad.tools.agenttools.PersistenceAgent.PersistenceAgent" [color=black,
                  fontcolor=white,
                  group=1,
                  label=PersistenceAgent,
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
          "abjad.tools.abctools.AbjadObject.AbjadObject" -> "abjad.tools.agenttools.InspectionAgent.InspectionAgent";
          "abjad.tools.abctools.AbjadObject.AbjadObject" -> "abjad.tools.agenttools.IterationAgent.IterationAgent";
          "abjad.tools.abctools.AbjadObject.AbjadObject" -> "abjad.tools.agenttools.LabelAgent.LabelAgent";
          "abjad.tools.abctools.AbjadObject.AbjadObject" -> "abjad.tools.agenttools.MutationAgent.MutationAgent";
          "abjad.tools.abctools.AbjadObject.AbjadObject" -> "abjad.tools.agenttools.PersistenceAgent.PersistenceAgent";
          "builtins.object" -> "abjad.tools.abctools.AbjadObject.AbstractBase";
      }

--------

Classes
-------

.. toctree::
   :hidden:

   InspectionAgent
   IterationAgent
   LabelAgent
   MutationAgent
   PersistenceAgent

.. autosummary::
   :nosignatures:

   InspectionAgent
   IterationAgent
   LabelAgent
   MutationAgent
   PersistenceAgent
