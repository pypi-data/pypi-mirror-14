.. currentmodule:: abjad.tools.agenttools

InspectionAgent
===============

.. autoclass:: InspectionAgent

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
              "abjad.tools.agenttools.InspectionAgent.InspectionAgent" [color=black,
                  fontcolor=white,
                  group=1,
                  label=<<B>InspectionAgent</B>>,
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

      ~abjad.tools.agenttools.InspectionAgent.InspectionAgent.client
      ~abjad.tools.agenttools.InspectionAgent.InspectionAgent.get_annotation
      ~abjad.tools.agenttools.InspectionAgent.InspectionAgent.get_badly_formed_components
      ~abjad.tools.agenttools.InspectionAgent.InspectionAgent.get_components
      ~abjad.tools.agenttools.InspectionAgent.InspectionAgent.get_contents
      ~abjad.tools.agenttools.InspectionAgent.InspectionAgent.get_descendants
      ~abjad.tools.agenttools.InspectionAgent.InspectionAgent.get_duration
      ~abjad.tools.agenttools.InspectionAgent.InspectionAgent.get_effective
      ~abjad.tools.agenttools.InspectionAgent.InspectionAgent.get_effective_staff
      ~abjad.tools.agenttools.InspectionAgent.InspectionAgent.get_grace_container
      ~abjad.tools.agenttools.InspectionAgent.InspectionAgent.get_grace_containers
      ~abjad.tools.agenttools.InspectionAgent.InspectionAgent.get_indicator
      ~abjad.tools.agenttools.InspectionAgent.InspectionAgent.get_indicators
      ~abjad.tools.agenttools.InspectionAgent.InspectionAgent.get_leaf
      ~abjad.tools.agenttools.InspectionAgent.InspectionAgent.get_lineage
      ~abjad.tools.agenttools.InspectionAgent.InspectionAgent.get_logical_tie
      ~abjad.tools.agenttools.InspectionAgent.InspectionAgent.get_markup
      ~abjad.tools.agenttools.InspectionAgent.InspectionAgent.get_parentage
      ~abjad.tools.agenttools.InspectionAgent.InspectionAgent.get_sounding_pitch
      ~abjad.tools.agenttools.InspectionAgent.InspectionAgent.get_sounding_pitches
      ~abjad.tools.agenttools.InspectionAgent.InspectionAgent.get_spanner
      ~abjad.tools.agenttools.InspectionAgent.InspectionAgent.get_spanners
      ~abjad.tools.agenttools.InspectionAgent.InspectionAgent.get_timespan
      ~abjad.tools.agenttools.InspectionAgent.InspectionAgent.get_vertical_moment
      ~abjad.tools.agenttools.InspectionAgent.InspectionAgent.get_vertical_moment_at
      ~abjad.tools.agenttools.InspectionAgent.InspectionAgent.has_effective_indicator
      ~abjad.tools.agenttools.InspectionAgent.InspectionAgent.has_indicator
      ~abjad.tools.agenttools.InspectionAgent.InspectionAgent.has_spanner
      ~abjad.tools.agenttools.InspectionAgent.InspectionAgent.is_bar_line_crossing
      ~abjad.tools.agenttools.InspectionAgent.InspectionAgent.is_well_formed
      ~abjad.tools.agenttools.InspectionAgent.InspectionAgent.report_modifications
      ~abjad.tools.agenttools.InspectionAgent.InspectionAgent.tabulate_well_formedness_violations
      ~abjad.tools.agenttools.InspectionAgent.InspectionAgent.__eq__
      ~abjad.tools.agenttools.InspectionAgent.InspectionAgent.__format__
      ~abjad.tools.agenttools.InspectionAgent.InspectionAgent.__hash__
      ~abjad.tools.agenttools.InspectionAgent.InspectionAgent.__ne__
      ~abjad.tools.agenttools.InspectionAgent.InspectionAgent.__repr__

Read-only properties
--------------------

.. autoattribute:: abjad.tools.agenttools.InspectionAgent.InspectionAgent.client

Methods
-------

.. automethod:: abjad.tools.agenttools.InspectionAgent.InspectionAgent.get_annotation

.. automethod:: abjad.tools.agenttools.InspectionAgent.InspectionAgent.get_badly_formed_components

.. automethod:: abjad.tools.agenttools.InspectionAgent.InspectionAgent.get_components

.. automethod:: abjad.tools.agenttools.InspectionAgent.InspectionAgent.get_contents

.. automethod:: abjad.tools.agenttools.InspectionAgent.InspectionAgent.get_descendants

.. automethod:: abjad.tools.agenttools.InspectionAgent.InspectionAgent.get_duration

.. automethod:: abjad.tools.agenttools.InspectionAgent.InspectionAgent.get_effective

.. automethod:: abjad.tools.agenttools.InspectionAgent.InspectionAgent.get_effective_staff

.. automethod:: abjad.tools.agenttools.InspectionAgent.InspectionAgent.get_grace_container

.. automethod:: abjad.tools.agenttools.InspectionAgent.InspectionAgent.get_grace_containers

.. automethod:: abjad.tools.agenttools.InspectionAgent.InspectionAgent.get_indicator

.. automethod:: abjad.tools.agenttools.InspectionAgent.InspectionAgent.get_indicators

.. automethod:: abjad.tools.agenttools.InspectionAgent.InspectionAgent.get_leaf

.. automethod:: abjad.tools.agenttools.InspectionAgent.InspectionAgent.get_lineage

.. automethod:: abjad.tools.agenttools.InspectionAgent.InspectionAgent.get_logical_tie

.. automethod:: abjad.tools.agenttools.InspectionAgent.InspectionAgent.get_markup

.. automethod:: abjad.tools.agenttools.InspectionAgent.InspectionAgent.get_parentage

.. automethod:: abjad.tools.agenttools.InspectionAgent.InspectionAgent.get_sounding_pitch

.. automethod:: abjad.tools.agenttools.InspectionAgent.InspectionAgent.get_sounding_pitches

.. automethod:: abjad.tools.agenttools.InspectionAgent.InspectionAgent.get_spanner

.. automethod:: abjad.tools.agenttools.InspectionAgent.InspectionAgent.get_spanners

.. automethod:: abjad.tools.agenttools.InspectionAgent.InspectionAgent.get_timespan

.. automethod:: abjad.tools.agenttools.InspectionAgent.InspectionAgent.get_vertical_moment

.. automethod:: abjad.tools.agenttools.InspectionAgent.InspectionAgent.get_vertical_moment_at

.. automethod:: abjad.tools.agenttools.InspectionAgent.InspectionAgent.has_effective_indicator

.. automethod:: abjad.tools.agenttools.InspectionAgent.InspectionAgent.has_indicator

.. automethod:: abjad.tools.agenttools.InspectionAgent.InspectionAgent.has_spanner

.. automethod:: abjad.tools.agenttools.InspectionAgent.InspectionAgent.is_bar_line_crossing

.. automethod:: abjad.tools.agenttools.InspectionAgent.InspectionAgent.is_well_formed

.. automethod:: abjad.tools.agenttools.InspectionAgent.InspectionAgent.report_modifications

.. automethod:: abjad.tools.agenttools.InspectionAgent.InspectionAgent.tabulate_well_formedness_violations

Special methods
---------------

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.agenttools.InspectionAgent.InspectionAgent.__eq__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.agenttools.InspectionAgent.InspectionAgent.__format__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.agenttools.InspectionAgent.InspectionAgent.__hash__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.agenttools.InspectionAgent.InspectionAgent.__ne__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.agenttools.InspectionAgent.InspectionAgent.__repr__
